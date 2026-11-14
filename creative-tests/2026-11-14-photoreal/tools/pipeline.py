"""EverLiv v4 product-integration pipeline (one pass, no manual tuning).

usage: python3 pipeline.py <scene.png> <cutout.png> <out_prefix> [--grey] [--topdown]
  1. detect the blank stand-in automatically (low-saturation blob of plausible size/aspect)
  2. scale the scene to the output size FIRST (2160x2700 master; 1080x1350 feed made by downscaling)
  3. fit the authentic cutout ONCE to cover the stand-in (aspect preserved), base-aligned
  4. light transferred from the stand-in (cylinder/plane falloff), stand-in remnants inpainted
  5. fidelity report: label sharpness vs source at same width, aspect check, 100%/feed/thumb sheet
"""
import sys, json
sys.path.insert(0, '/home/claude/serum')
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import transfer
from measure import sharp, label_region

OW, OH = 2160, 2700


def detect_by_edges(img_rgb):
    """Fallback when the stand-in shares its colour with the background (e.g. white bottle on a pale sky):
    closed, smooth, untextured object found from edges, then refined with GrabCut."""
    g = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    H, W = g.shape
    e = cv2.Canny(cv2.GaussianBlur(g, (5, 5), 1.2), 20, 60)
    e = cv2.dilate(e, np.ones((3, 3), np.uint8))
    cnts, _ = cv2.findContours(e, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tex = cv2.Laplacian(g, cv2.CV_32F); tex = cv2.blur(np.abs(tex), (15, 15))
    best, score = None, -1
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w * h < 0.02 * H * W or w > 0.6 * W or h > 0.8 * H or y + h > 0.97 * H or x <= 2 or x + w >= W - 2 or y <= 2:
            continue
        hull = cv2.convexHull(c); solidity = cv2.contourArea(c) / max(1, cv2.contourArea(hull))
        inner = tex[y + h // 5:y + 4 * h // 5, x + w // 5:x + 4 * w // 5].mean()
        s = cv2.contourArea(hull) * (1 / (1 + inner)) * (0.5 + solidity)
        if s > score:
            best, score = (x, y, w, h), s
    if best is None:
        raise SystemExit('stand-in not found')
    x, y, w, h = best
    mask = np.full((H, W), cv2.GC_BGD, np.uint8)
    mask[max(0, y - 10):y + h + 10, max(0, x - 10):x + w + 10] = cv2.GC_PR_BGD
    mask[y + h // 6:y + 5 * h // 6, x + w // 5:x + 4 * w // 5] = cv2.GC_FGD
    mask[y:y + h, x:x + w][mask[y:y + h, x:x + w] == cv2.GC_PR_BGD] = cv2.GC_PR_FGD
    bg_, fg_ = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR), mask, None, bg_, fg_, 6, cv2.GC_INIT_WITH_MASK)
    m = ((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)).astype(np.uint8)
    # a blank stand-in is neutral: drop saturated pixels (skin, wood, props) that GrabCut absorbed
    a_ = img_rgb.astype(np.int32); neutral = ((a_.max(-1) - a_.min(-1)) < 32).astype(np.uint8)
    m = cv2.morphologyEx(m & neutral, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m); k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); m = (lab == k).astype(np.uint8)
    ys, xs = np.where(m)
    return m, (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)


def trim_to_object(m):
    """Keep only the columns where the mask is (nearly) full height: separates an upright product
    from a hand/arm or prop that merged with it in the mask."""
    cols = m.sum(0); keep = cols >= 0.75 * cols.max()
    xs = np.where(keep)[0]
    # longest contiguous run
    runs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1); xs = max(runs, key=len)
    m2 = np.zeros_like(m); m2[:, xs.min():xs.max() + 1] = m[:, xs.min():xs.max() + 1]
    ys = np.where(m2.any(1))[0]
    return m2, (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def detect_from_brief(img_rgb, hint):
    """Brief-guided detection: the scene prompt fixes where the stand-in should be
    (centre x/y as frame fractions, height fraction, height/width aspect). GrabCut inside that region."""
    cxf, cyf, hf, asp = hint
    H, W = img_rgb.shape[:2]
    h = hf * H * 1.35; w = h / asp * 1.35
    x0, y0 = int(max(1, cxf * W - w / 2)), int(max(1, cyf * H - h / 2))
    x1, y1 = int(min(W - 2, cxf * W + w / 2)), int(min(H - 2, cyf * H + h / 2))
    mask = np.zeros((H, W), np.uint8)
    bg_, fg_ = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR), mask, (x0, y0, x1 - x0, y1 - y0), bg_, fg_, 6, cv2.GC_INIT_WITH_RECT)
    m = ((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m); k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); m = (lab == k).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    # GrabCut height is reliable; width is constrained by the known product aspect from the brief
    ys, xs = np.where(m)
    top, bot = int(np.percentile(ys, 0.5)), int(np.percentile(ys, 99.5)) + 1
    core = m[top + (bot - top) // 4: bot - (bot - top) // 4]
    cx = float(np.median(np.where(core)[1]))
    hw = (bot - top) / asp / 2
    bx0, bx1 = int(cx - hw), int(cx + hw)
    m2 = np.zeros_like(m); m2[top:bot, bx0:bx1] = m[top:bot, bx0:bx1]
    return m2, (bx0, top, bx1, bot)


def detect_standin(img_rgb, grey=True, hint=None):
    try:
        m, bb = _detect_standin(img_rgb, grey)
    except SystemExit:
        m, bb = None, None
    if hint is not None:
        H, W = img_rgb.shape[:2]
        ok = bb is not None and (bb[3] - bb[1]) > 0.5 * hint[2] * H and \
            abs(((bb[3] - bb[1]) / max(1, bb[2] - bb[0])) / hint[3] - 1) < 0.5
        if not ok:
            return detect_from_brief(img_rgb, hint)
    if m is None:
        raise SystemExit('stand-in not found')
    return m, bb


def _detect_standin(img_rgb, grey=True):
    a = img_rgb.astype(np.int32)
    sat = a.max(-1) - a.min(-1)
    lum = a.mean(-1)
    cand = (sat < (26 if grey else 34)) & (lum > 60) & (lum < 250)
    cand = cv2.morphologyEx(cand.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    cand = cv2.morphologyEx(cand, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(cand)
    H, W = cand.shape
    best, score = None, -1
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < 0.01 * H * W or w > 0.7 * W or h > 0.85 * H or y <= 2 or area > 0.35 * H * W or x <= 2 or x + w >= W - 2 or y + h >= H - 2:
            continue
        fill = area / (w * h)                      # solid objects fill their bbox
        cx = (x + w / 2) / W
        s = area * fill * (1.0 - 0.5 * abs(cx - 0.45))
        if fill > 0.55 and s > score:
            best, score = i, s
    if best is None:
        return detect_by_edges(img_rgb)
    m = (lab == best).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    x, y, w, h, _ = st[best]
    return m, (x, y, x + w, y + h)


def run(scene_path, cut_path, prefix, grey=True, topdown=False, shape='flat', hint=None):
    src = np.asarray(Image.open(scene_path).convert('RGB'))
    m, (x0, y0, x1, y1) = detect_standin(src, grey, hint)
    H, W = src.shape[:2]
    s = max(OW / W, OH / H)
    RW, RH = int(round(W * s)), int(round(H * s))
    sc = Image.fromarray(src).resize((RW, RH), Image.LANCZOS)
    cy = (y0 + y1) / 2 * s
    top = int(min(max(0, cy - OH / 2), RH - OH)); left = (RW - OW) // 2
    sc = sc.crop((left, top, left + OW, top + OH))
    T = lambda v: int(round(v * s))
    box = (T(x0) - left, T(y0) - top, T(x1) - left, T(y1) - top)
    mS = cv2.resize(m, (RW, RH), interpolation=cv2.INTER_NEAREST)[top:top + OH, left:left + OW]
    cut = Image.open(cut_path).convert('RGBA')
    cut = cut.crop(cut.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
    bw, bh = box[2] - box[0], box[3] - box[1]
    k = max(bw / cut.width, bh / cut.height)       # cover the stand-in, aspect preserved
    out_h = int(round(cut.height * k))
    # light is sampled only from columns that are solidly stand-in (no background/shadow fringe)
    colfrac = (mS[box[1]:box[3], box[0]:box[2]] > 0).mean(0)
    solid = np.where(colfrac > 0.9 * colfrac.max())[0]
    light_box = (box[0] + int(solid.min()), box[1], box[0] + int(solid.max()) + 1, box[3])
    st_vals = np.asarray(sc).astype(float)[box[1]:box[3], box[0]:box[2]][mS[box[1]:box[3], box[0]:box[2]] > 0]
    white_ref = float(np.percentile(st_vals.max(-1), 97))
    res, bb = transfer.composite(sc, cut_path, box, out_h, white_ref=white_ref, relative=True, delight=('col' if shape == 'cyl' else 'none'), light_box=light_box, contact=0.55 if not topdown else 0.0,
                                 grain=1.0, soften=0)
    pm = transfer.LAST_MASK
    # remnants of the stand-in not covered by the product -> inpaint from surroundings
    rem = ((cv2.dilate(mS, np.ones((9, 9), np.uint8)) > 0) & (pm < 0.5)).astype(np.uint8)
    rem = cv2.dilate(rem, np.ones((5, 5), np.uint8)); rem[pm > 0.9] = 0
    arr = np.asarray(res)[..., ::-1].copy()
    if rem.sum():
        arr = cv2.inpaint(arr, rem, 7, cv2.INPAINT_TELEA)
    final = Image.fromarray(arr[..., ::-1])
    final.save(prefix + '-2160x2700.png')
    feed = final.resize((1080, 1350), Image.LANCZOS); feed.save(prefix + '-1080x1350.png')
    # fidelity metrics on the feed file
    fb = tuple(int(round(v / 2)) for v in bb)
    w = fb[2] - fb[0]
    c = Image.open(cut_path).convert('RGBA'); c = c.crop(c.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
    r = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS); bg = Image.new('RGB', r.size, (255, 255, 255)); bg.paste(r, (0, 0), r)
    sv = sharp(label_region(bg, (0, 0) + bg.size)); fv = sharp(label_region(feed, fb))
    ys, xs = np.where(pm > 0.5)
    asp_out = (xs.max() - xs.min() + 1) / (ys.max() - ys.min() + 1); asp_src = c.width / c.height
    rep = {'standin_bbox_native': [int(x0), int(y0), int(x1), int(y1)], 'product_bbox_feed': fb,
           'label_sharpness_pct': round(100 * fv / sv), 'aspect_error_pct': round(100 * abs(asp_out / asp_src - 1), 2),
           'remnant_px_inpainted_2160': int(rem.sum()), 'product_width_pct_of_frame': round(100 * w / 1080)}
    json.dump(rep, open(prefix + '-report.json', 'w'), indent=1)
    # review sheet: 100% crop | feed | thumbnail
    F = '/home/claude/fonts/'
    Tf = ImageFont.truetype(F + 'figtree-latin-800-normal.ttf', 22)
    crop = final.crop((bb[0] - 40, bb[1] - 40, bb[2] + 40, min(OH, bb[1] + 760)))
    crop.thumbnail((700, 820))
    sheet = Image.new('RGB', (40 + 540 + 40 + crop.width + 40 + 150 + 40, 900), (241, 239, 234))
    d = ImageDraw.Draw(sheet)
    sheet.paste(feed.resize((540, 675), Image.LANCZOS), (40, 70)); d.text((40, 30), 'FEED', font=Tf, fill=(26, 28, 23))
    sheet.paste(crop, (620, 70)); d.text((620, 30), '100% (2160 master)', font=Tf, fill=(26, 28, 23))
    sheet.paste(feed.resize((150, 188), Image.LANCZOS), (660 + crop.width, 70)); d.text((660 + crop.width, 30), 'THUMB', font=Tf, fill=(26, 28, 23))
    sheet.save(prefix + '-qa-sheet.jpg', quality=90)
    print(json.dumps(rep))


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3], grey='--white' not in sys.argv, topdown='--topdown' in sys.argv, shape=('cyl' if '--cyl' in sys.argv else 'flat'),
        hint=[tuple(float(v) for v in a.split('=')[1].split(',')) for a in sys.argv if a.startswith('--hint=')][0] if any(a.startswith('--hint=') for a in sys.argv) else None)
