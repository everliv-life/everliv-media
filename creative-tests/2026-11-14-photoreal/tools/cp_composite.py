"""Clean-plate compositor (EverLiv v5).

inputs: scene with blank stand-in, clean plate of the same scene (stand-in removed by the generator),
        authentic supplier cutout.
1. register plate to scene (ECC, affine) on pixels away from the stand-in
2. stand-in mask: GrabCut seeded by detection, refined by scene/plate difference
3. shadow matte = scene / plate outside the stand-in (the scene's own contact + cast shadow and
   occlusion), smoothed, ratio <= 1
4. authentic cutout scaled ONCE to final pixels, fitted to the stand-in's base and height
   (aspect preserved), light taken from the stand-in (colour ratio, terminator, vertical falloff)
5. composite: plate * shadow matte, product on top, fine grain matched, all at 2160x2700
6. fidelity + QA outputs (label sharpness vs source, 100% / feed / thumb sheet)
"""
import sys, json
sys.path.insert(0, '/home/claude/serum')
import numpy as np, cv2
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from pipeline import detect_standin
from measure import sharp, label_region

OW, OH = 2160, 2700


def load(p):
    return np.asarray(Image.open(p).convert('RGB'))


def register(plate, scene, keep):
    a = cv2.cvtColor(scene, cv2.COLOR_RGB2GRAY).astype(np.float32)
    b = cv2.cvtColor(plate, cv2.COLOR_RGB2GRAY).astype(np.float32)
    warp = np.eye(2, 3, dtype=np.float32)
    try:
        _, warp = cv2.findTransformECC(a, b, warp, cv2.MOTION_AFFINE,
                                       (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6),
                                       keep.astype(np.uint8), 5)
    except cv2.error:
        pass
    out = cv2.warpAffine(plate, warp, (scene.shape[1], scene.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                         borderMode=cv2.BORDER_REFLECT)
    return out, warp


def run(scene_p, plate_p, cut_p, prefix, shape='cyl', topdown=False, hint=None, product_shrink=1.0):
    sc = load(scene_p)
    pl = load(plate_p)
    if pl.shape != sc.shape:
        pl = cv2.resize(pl, (sc.shape[1], sc.shape[0]), interpolation=cv2.INTER_LANCZOS4)
    H, W = sc.shape[:2]
    m0, (x0, y0, x1, y1) = detect_standin(sc, grey=(shape != 'cyl'), hint=hint)
    keep = 1 - cv2.dilate(m0, np.ones((61, 61), np.uint8))
    pl, warp = register(pl, sc, keep)
    # refine the stand-in mask with the scene/plate difference (object = strong, non-shadow change)
    d = np.abs(sc.astype(np.int16) - pl.astype(np.int16)).max(-1)
    box = np.zeros((H, W), np.uint8); box[max(0, y0 - 8):y1 + 8, max(0, x0 - 8):x1 + 8] = 1
    fg = np.where(box > 0, np.where(m0 > 0, cv2.GC_PR_FGD, cv2.GC_PR_BGD), cv2.GC_BGD).astype(np.uint8)
    fg[cv2.erode(m0, np.ones((15, 15), np.uint8)) > 0] = cv2.GC_FGD
    fg[(box > 0) & (d < 6)] = cv2.GC_BGD
    bg_, fgm = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(cv2.cvtColor(sc, cv2.COLOR_RGB2BGR), fg, None, bg_, fgm, 4, cv2.GC_INIT_WITH_MASK)
    sm = ((fg == cv2.GC_FGD) | (fg == cv2.GC_PR_FGD)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(sm); k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); sm = (lab == k).astype(np.uint8)
    sm = cv2.morphologyEx(sm, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    ys, xs = np.where(sm); x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    # shadow matte: ratio outside the stand-in, smoothed; inside the footprint use the nearest outside values
    eps = 4.0
    ratio = (sc.astype(np.float32) + eps) / (pl.astype(np.float32) + eps)
    ratio = np.clip(ratio, 0.15, 1.0)
    inside = cv2.dilate(sm, np.ones((5, 5) if '--ring' not in sys.argv else (41, 41), np.uint8))
    rl = ratio.mean(-1)
    r8 = np.clip(rl * 255, 0, 255).astype(np.uint8)
    rl_out = cv2.inpaint(r8, inside, 9, cv2.INPAINT_TELEA).astype(np.float32) / 255
    rl_out = cv2.GaussianBlur(rl_out, (0, 0), 2.0)
    # keep only the shadow attached to the object (local region), elsewhere 1 (generator drift)
    region = cv2.dilate(sm, np.ones((int(0.9 * (y1 - y0)) | 1, int(1.4 * (x1 - x0)) | 1), np.uint8))
    region = cv2.GaussianBlur(region.astype(np.float32), (0, 0), 25)
    matte = 1 - (1 - rl_out) * region
    # ---- up to final resolution
    s = max(OW / W, OH / H); RW, RH = round(W * s), round(H * s)
    left, top = (RW - OW) // 2, int(min(max(0, (y0 + y1) / 2 * s - OH / 2), RH - OH))
    up = lambda a, interp=cv2.INTER_LANCZOS4: cv2.resize(a, (RW, RH), interpolation=interp)[top:top + OH, left:left + OW]
    PL = up(pl).astype(np.float32); SC = up(sc).astype(np.float32)
    MT = up(matte.astype(np.float32), cv2.INTER_LINEAR)
    SM = up(sm, cv2.INTER_NEAREST)
    T = lambda v: v * s
    bx0, by0, bx1, by1 = T(x0) - left, T(y0) - top, T(x1) - left, T(y1) - top
    # ---- authentic product: one scale, height-fitted to the stand-in, base-aligned, centred
    cut = Image.open(cut_p).convert('RGBA')
    cut = cut.crop(cut.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
    ph = (by1 - by0) * product_shrink
    if topdown:
        k = min((bx1 - bx0) / cut.width, (by1 - by0) / cut.height)
    else:
        k = ph / cut.height
    pw, phh = round(cut.width * k), round(cut.height * k)
    prod = cut.resize((pw, phh), Image.LANCZOS)
    a = np.asarray(prod).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3] / 255
    # edge: erode the render's dark matte fringe 1.5px, feather 0.6px (no blur of the label itself)
    al = cv2.erode((al * 255).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32) / 255
    al = cv2.GaussianBlur(al, (0, 0), 0.6 if '--wrap' not in sys.argv else 1.0)
    px = int(round((bx0 + bx1) / 2 - pw / 2)); py = int(round(by1 - phh)) if not topdown else int(round((by0 + by1) / 2 - phh / 2))
    # ---- light from the stand-in (ratio to its brightest lit column), applied to the product
    st_pix = SC[int(by0):int(by1), int(bx0):int(bx1)]
    stm = SM[int(by0):int(by1), int(bx0):int(bx1)] > 0
    cols = []
    for x in range(st_pix.shape[1]):
        c = st_pix[:, x][stm[:, x]]
        cols.append(np.median(c, 0) if len(c) > 10 else np.array([np.nan] * 3))
    cols = np.array(cols)
    good = ~np.isnan(cols[:, 0])
    ref = np.percentile(cols[good].mean(1), 97)
    cols = np.array([np.interp(np.arange(len(cols)), np.where(good)[0], cols[good, c]) for c in range(3)]).T / ref
    if shape != 'cyl':
        cols[:] = np.median(cols[good], 0)       # flat face: one uniform light colour/exposure
    rows = []
    for y in range(st_pix.shape[0]):
        c = st_pix[y][stm[y]]
        rows.append(np.median(c.mean(-1)) if len(c) > 5 else np.nan)
    rows = np.array(rows); g2 = ~np.isnan(rows)
    rows = np.interp(np.arange(len(rows)), np.where(g2)[0], rows[g2])
    rows = cv2.GaussianBlur(rows.reshape(-1, 1).astype(np.float32), (0, 0), 25).ravel()
    rows = rows / np.median(rows)
    hx = np.linspace(0, len(cols) - 1, pw); L = np.stack([np.interp(hx, np.arange(len(cols)), cols[:, c]) for c in range(3)], -1)
    vy = np.linspace(0, len(rows) - 1, phh); V = np.interp(vy, np.arange(len(rows)), rows)
    light = np.clip(L[None] * (V[:, None, None] if shape == 'cyl' else 1.0), 0.2, 1.0)
    # the supplier render carries studio shading: remove its horizontal shape only (cylinders)
    if shape == 'cyl':
        lum = rgb.mean(-1); solid = al > 0.98
        r0, r1 = int(phh * .45), int(phh * .95)
        cp = np.array([np.median(lum[r0:r1, x][solid[r0:r1, x]]) if solid[r0:r1, x].sum() > 10 else np.nan for x in range(pw)])
        gg = ~np.isnan(cp); cp = np.interp(np.arange(pw), np.where(gg)[0], cp[gg])
        cp = cv2.GaussianBlur(cp.reshape(1, -1).astype(np.float32), (0, 0), max(2, pw / 30)).ravel()
        rgb = rgb / (cp / np.percentile(cp, 90))[None, :, None]
    # photographic fill: a bounce card on the shadow side (as a product photographer would use),
    # raising the label face to >= 0.88 of the key while keeping the light direction and falloff
    band = light[int(phh * .45):int(phh * .95)].mean()
    if shape == 'cyl' and band < 0.85:
        f = (0.85 - band) / (1 - band)
        light = f + (1 - f) * light
    # ambient colour: environment bounce measured from the plate around the product (partial, 30%)
    env = PL[int(max(0, py)):int(min(OH, py + phh)), int(max(0, px - pw)):int(min(OW, px + 2 * pw))].reshape(-1, 3)
    envc = np.median(env, 0); envc = envc / envc.mean()
    light = light * (envc ** (0.3 if shape == "cyl" else (0.06 if '--plane' in sys.argv else 0.12)))[None, None, :]
    if shape != 'cyl' and '--plane' in sys.argv:
        # flat face: fit a smooth light plane to the stand-in face (the scene's real key direction),
        # cancel the supplier render's own plane, no environment tint (keeps packaging colour true)
        def plane(img2d, msk):
            yy, xx = np.mgrid[0:img2d.shape[0], 0:img2d.shape[1]]
            Aq = np.c_[xx[msk] / img2d.shape[1], yy[msk] / img2d.shape[0], np.ones(msk.sum())]
            c, *_ = np.linalg.lstsq(Aq, img2d[msk], rcond=None); return c
        sh_, sw_ = st_pix.shape[:2]
        inner = np.zeros_like(stm); inner[int(sh_*.15):int(sh_*.88), int(sw_*.12):int(sw_*.88)] = True
        cs = plane(st_pix.mean(-1), stm & inner)
        cr = plane(rgb.mean(-1), al > 0.98)
        yy, xx = np.mgrid[0:phh, 0:pw]
        P_scene = (cs[0]*xx/pw + cs[1]*yy/phh + cs[2]); P_scene = P_scene / P_scene.max()
        P_src = (cr[0]*xx/pw + cr[1]*yy/phh + cr[2]); P_src = P_src / P_src.mean()
        lvl = float(np.median(cols[good].mean(1)))
        lvl = max(lvl, 0.9)   # photographic fill: keep the face at >=0.9 of key at its brightest corner
        light = (P_scene * lvl / P_src)[..., None] * np.ones(3)[None, None]
        # subtle specular on the dark rim facing the key (upper-left edge): lighting, not packaging change
        dark = (rgb.mean(-1) < 70) & (al > 0.9)
        edge_ul = np.exp(-((xx / pw) + (yy / phh)) * 3.0)
        light = light + (dark * edge_ul * 0.0)[..., None]
        rgb = rgb + (dark * edge_ul)[..., None] * 38.0
        light = light * (envc ** 0.06)[None, None, :]
    if shape == 'cyl' and '--grad' in sys.argv:
        # scene key from back-right (cast shadow falls front-left): cylinder falloff left->right + right rim
        u = np.linspace(0, 1, pw)
        ramp = 0.86 + 0.14 * u ** 0.8
        rim = 0.08 * np.exp(-((1 - u) / 0.06) ** 2)
        light = light * (ramp + rim)[None, :, None]
        # remove the cap-top glow (stand-in's lit top surface leaked into the row profile)
        top = int(phh * 0.10)
        light[:top] = np.minimum(light[:top], light[top:top + 1])
        bm = light[int(phh * .45):int(phh * .95)].mean()
        if bm < 0.88: light = np.clip(light * (0.88 / bm), 0, 1.04)
    lit = np.clip(rgb * light, 0, 255)
    print('light range', float(light.min()), float(light.max()), 'label-band mean', float(light[int(phh*.45):int(phh*.95)].mean()))
    # ---- compose: clean plate x shadow matte, product over
    out = PL * MT[..., None]
    # contact occlusion: a tight dark line where the product's base meets the surface (light-scaled)
    if not topdown or True:
        base_mask = np.zeros((OH, OW), np.float32)
        ab = (al > 0.5).astype(np.uint8)
        bottom = np.zeros_like(ab); 
        for x in range(ab.shape[1]):
            ys_ = np.where(ab[:, x])[0]
            if len(ys_): bottom[ys_.max(), x] = 1
        yy_, xx_ = np.where(bottom)
        for yv, xv in zip(yy_, xx_):
            Y, X = py + yv, px + xv
            if 0 <= Y < OH and 0 <= X < OW: base_mask[Y, X] = 1
        occ = cv2.GaussianBlur(cv2.dilate(base_mask, np.ones((3, 9), np.uint8)), (0, 0), 3.0)
        occ = np.clip(occ / max(occ.max(), 1e-6), 0, 1) * 0.55
        if '--grad' in sys.argv:
            wide = cv2.GaussianBlur(cv2.dilate(base_mask, np.ones((5, 21), np.uint8)), (0, 0), 9.0)
            occ = np.maximum(occ, np.clip(wide / max(wide.max(), 1e-6), 0, 1) * 0.35)
        out *= (1 - occ[..., None] * np.array([0.82, 0.86, 0.9], np.float32))
    y_a, y_b = max(0, py), min(OH, py + phh); x_a, x_b = max(0, px), min(OW, px + pw)
    A = al[y_a - py:y_b - py, x_a - px:x_b - px][..., None]
    bg = out.copy()
    out[y_a:y_b, x_a:x_b] = out[y_a:y_b, x_a:x_b] * (1 - A) + lit[y_a - py:y_b - py, x_a - px:x_b - px] * A
    if '--wrap' in sys.argv:
        # light wrap: blurred background bleeds 2-3 px into the product edge (lens behaviour)
        full = np.zeros((OH, OW), np.float32); full[y_a:y_b, x_a:x_b] = A[..., 0]
        inner = cv2.GaussianBlur(1 - full, (0, 0), 2.5) * full
        bgb = cv2.GaussianBlur(bg, (0, 0), 6)
        w = np.clip(inner * 1.6, 0, 0.45)[..., None]
        out = out * (1 - w) + np.maximum(out, bgb) * w
    # matched grain over the whole frame (product included) so noise is uniform
    g = SC[100:400, 100:400].mean(-1); hp = g - cv2.GaussianBlur(g, (0, 0), 2)
    gsd = max(0.6, min(2.5, hp.std() * 0.6))
    noise = np.random.default_rng(3).normal(0, gsd, (OH, OW, 1)).astype(np.float32)
    # luminance-only grain at the scene's measured level; product gets the same grain at 60% so the
    # label keeps its edge contrast (grain is added after compositing, never blur)
    pa = np.zeros((OH, OW), np.float32); pa[y_a:y_b, x_a:x_b] = A[..., 0]
    out += noise * (1 - (0.1 if '--wrap' in sys.argv else 0.4) * pa)[..., None]
    final = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    final.save(prefix + '-2160x2700.png')
    feed = final.resize((1080, 1350), Image.LANCZOS); feed.save(prefix + '-1080x1350.png')
    # fidelity
    fb = (px // 2, py // 2, (px + pw) // 2, (py + phh) // 2); w = fb[2] - fb[0]
    c2 = cut.resize((w, round(cut.height * w / cut.width)), Image.LANCZOS); bg = Image.new('RGB', c2.size, (255, 255, 255)); bg.paste(c2, (0, 0), c2)
    rep = {'label_sharpness_pct': round(100 * sharp(label_region(feed, fb)) / sharp(label_region(bg, (0, 0) + bg.size))),
           'aspect_error_pct': round(100 * abs((pw / phh) / (cut.width / cut.height) - 1), 2),
           'registration_affine': np.round(warp, 4).tolist(), 'product_height_pct_of_frame': round(100 * phh / OH)}
    json.dump(rep, open(prefix + '-report.json', 'w'), indent=1)
    sheet_w = 40 + 540 + 40 + 700 + 40 + 150 + 40
    sheet = Image.new('RGB', (sheet_w, 900), (241, 239, 234)); dr = ImageDraw.Draw(sheet)
    Fn = ImageFont.truetype('/home/claude/fonts/figtree-latin-800-normal.ttf', 22)
    sheet.paste(feed.resize((540, 675), Image.LANCZOS), (40, 70)); dr.text((40, 30), 'FEED', font=Fn, fill=(26, 28, 23))
    cx0 = max(0, px - 120); cy0 = max(0, py - 60)
    crop = final.crop((cx0, cy0, min(OW, cx0 + 700), min(OH, cy0 + 800))); sheet.paste(crop, (620, 70))
    dr.text((620, 30), '100% (2160 master)', font=Fn, fill=(26, 28, 23))
    sheet.paste(feed.resize((150, 188), Image.LANCZOS), (1360, 70)); dr.text((1360, 30), 'THUMB', font=Fn, fill=(26, 28, 23))
    sheet.save(prefix + '-qa-sheet.jpg', quality=90)
    print(json.dumps(rep))


if __name__ == '__main__':
    a = sys.argv
    run(a[1], a[2], a[3], a[4], shape='cyl' if '--cyl' in a else 'flat', topdown='--topdown' in a,
        hint=None, product_shrink=float([x.split('=')[1] for x in a if x.startswith('--shrink=')][0]) if any(x.startswith('--shrink=') for x in a) else 1.0)
