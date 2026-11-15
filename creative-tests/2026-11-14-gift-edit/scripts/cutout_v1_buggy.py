"""Verified product cut-outs from authentic supplier renders (EverLiv, Nov 14 2026).
Product pixels are never edited: interior RGB is copied 1:1 from the source; only the alpha matte is computed,
and RGB is decontaminated ONLY in the semi-transparent edge band (removes background fringe).
Usage: python3 cutout.py <source> <out.png> [--from-alpha]   (--from-alpha: source already has alpha; fix + decontaminate)"""
import sys, json, numpy as np, cv2
from PIL import Image

def decontaminate(rgb, a):
    """edge-band RGB <- nearest fully-opaque interior colour (inpaint), interior untouched"""
    solid = a >= 0.98
    band = (a > 0.0) & ~solid
    src = rgb.copy().astype(np.uint8)
    hole = (~solid).astype(np.uint8)
    fill = cv2.inpaint(src[..., ::-1], hole, 3, cv2.INPAINT_TELEA)[..., ::-1]
    out = rgb.copy(); out[band] = fill[band]; return out, int(band.sum())

def from_render(path):
    im = np.asarray(Image.open(path).convert('RGB')).astype(np.int16)
    H, W = im.shape[:2]
    border = np.concatenate([im[:12].reshape(-1, 3), im[-12:].reshape(-1, 3), im[:, :12].reshape(-1, 3), im[:, -12:].reshape(-1, 3)])
    bg = np.median(border, 0)
    d = np.abs(im - bg).max(-1)
    # product = clearly different from bg OR textured; shadow = smooth, low-chroma darkening below product
    chroma = im.max(-1) - im.min(-1)
    gm = cv2.GaussianBlur(cv2.Laplacian(im.mean(-1).astype(np.float32), cv2.CV_32F) ** 2, (0, 0), 3)
    mask = np.full((H, W), cv2.GC_PR_BGD, np.uint8)
    mask[d < 5] = cv2.GC_BGD
    sure = (d > 45) | ((d > 20) & ((chroma > 18) | (gm > 30)))
    sure = cv2.erode(sure.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    mask[sure] = cv2.GC_FGD
    mask[(d >= 5) & ~sure & (d > 14)] = cv2.GC_PR_FGD
    bgm, fgm = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(im.astype(np.uint8)[..., ::-1].copy(), mask, None, bgm, fgm, 5, cv2.GC_INIT_WITH_MASK)
    m = ((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    m = (lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m = np.zeros_like(m); cv2.drawContours(m, [max(cs, key=cv2.contourArea)], -1, 1, -1)   # fill holes
    if '--trim-floor' in sys.argv:
        # remove supplier floor/soft shadow captured under the object: per column, cut below the last
        # object-like pixel (object-like = not light low-chroma smooth background), then smooth the cut line
        lum = im.mean(-1); bgl = (chroma < 12) & (lum > 110)   # neutral grey floor/shadow (soaps: coloured or near-black)
        objlike = (m > 0) & ~bgl
        ys, xs = np.where(m > 0); x0, x1 = xs.min(), xs.max()
        bottom = np.full(W, -1)
        for x in range(x0, x1 + 1):
            r = np.where(objlike[:, x])[0]
            if len(r): bottom[x] = r.max()
        valid = bottom >= 0
        bsm = bottom.astype(np.float32).copy()
        k = 31
        pad = np.pad(bsm[x0:x1 + 1], k // 2, mode='edge')
        bsm[x0:x1 + 1] = np.array([np.median(pad[i:i + k]) for i in range(x1 - x0 + 1)])
        yy = np.arange(H)[:, None]
        cut = yy > (np.minimum(bottom, bsm) + 1)[None, :]
        m[cut & valid[None, :]] = 0
        inrange = np.zeros(W, bool); inrange[x0:x1 + 1] = True
        m[:, inrange & ~valid] = 0          # columns with no object-like pixel are pure floor leak
        n, lab, st, _ = cv2.connectedComponentsWithStats(m)
        m = (lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
    if '--trim-floor' in sys.argv:
        # restore label-band ends that wrap around the bar sides (light shading close to bg): grow the mask
        # horizontally by up to 14 px into pixels that differ from bg (d > 8), away from the top/bottom floor
        ys, xs = np.where(m > 0); ty, by = ys.min() + 25, ys.max() - 25
        for _ in range(14):
            grow = cv2.dilate(m, np.ones((1, 3), np.uint8)) & (d > 8).astype(np.uint8)
            grow[:ty] = m[:ty]; grow[by:] = m[by:]
            m = np.maximum(m, grow)
    a = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8)
    a = np.where(m > 0, np.maximum(a, 0.5), a)       # keep the true edge at >=50%
    return im.astype(np.uint8), a

def main():
    src, out = sys.argv[1], sys.argv[2]
    if '--from-alpha' in sys.argv:
        x = np.asarray(Image.open(src).convert('RGBA')).astype(np.float32)
        rgb, a = x[..., :3].astype(np.uint8), x[..., 3] / 255.0
        a = np.where(a >= 250 / 255, 1.0, a)          # fix near-opaque interior (e.g. 254) to fully opaque
    else:
        rgb, a = from_render(src)
    rgb2, nb = decontaminate(rgb.astype(np.float32), a)
    ys, xs = np.where(a > 0.01); x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    pad = 4; x0, y0 = max(0, x0 - pad), max(0, y0 - pad); x1, y1 = min(a.shape[1], x1 + pad), min(a.shape[0], y1 + pad)
    A = (np.clip(a, 0, 1) * 255).round().astype(np.uint8)
    Image.fromarray(np.dstack([np.clip(rgb2, 0, 255).astype(np.uint8), A])[y0:y1, x0:x1], 'RGBA').save(out)
    solid = (a >= 0.98)
    # verification: interior pixels identical to source?
    same = bool((rgb2[solid].astype(np.uint8) == rgb[solid].astype(np.uint8)).all())
    rep = {'source': src, 'out': out, 'crop_box': [int(x0), int(y0), int(x1), int(y1)], 'size': [int(x1 - x0), int(y1 - y0)],
           'opaque_px': int(solid.sum()), 'edge_band_px': nb, 'interior_pixels_identical_to_source': same}
    json.dump(rep, open(out.replace('.png', '.json'), 'w'), indent=1); print(json.dumps(rep))

if __name__ == '__main__':
    main()
