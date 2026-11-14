"""Lighting-transfer composite of authentic packaging onto a generated stand-in.

The authentic cutout is only uniformly scaled (aspect preserved, never warped or redrawn).
Its pixels are multiplied by the stand-in's photographed light (a smooth separable model of
the blank bottle's shading: left-right cylinder falloff x top-bottom gradient), so the real
label receives the scene's actual light colour, falloff and exposure.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw


def light_model(scene, box, seam_rows=(), body=(0.35, 0.92)):
    x0, y0, x1, y1 = box
    s = np.asarray(scene.convert('RGB')).astype(np.float32)[y0:y1, x0:x1]
    h, w = s.shape[:2]
    rows = np.arange(h)
    ok = np.ones(h, bool)
    for a, b in seam_rows:
        ok[a - y0:b - y0] = False
    by0, by1 = int(h * body[0]), int(h * body[1])
    band = s[by0:by1][ok[by0:by1]]
    hprof = np.median(band, axis=0)                    # (w,3) colour across the cylinder
    lum = s.mean(-1)
    inner = lum[:, int(w * 0.25):int(w * 0.75)]
    vprof = np.median(inner, axis=1)                   # (h,) brightness top->bottom
    vprof = np.interp(rows, rows[ok], vprof[ok])
    k = 25
    vprof = np.convolve(np.pad(vprof, k, mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')
    vnorm = vprof / np.median(vprof[by0:by1])
    return hprof, vnorm


def composite(scene, cut_path, box, out_h, seam_rows=(), white_ref=246.0, soften=0.6,
              contact=0.55, extra_shadow=None, grain=2.0, xshift=0, arc=0, cap_from=None, flat=False, relative=False, delight='full', light_box=None):
    sc = scene.convert('RGB')
    x0, y0, x1, y1 = box
    hprof, vnorm = light_model(sc, light_box or box, seam_rows)
    cut = Image.open(cut_path).convert('RGBA')
    cut = cut.crop(cut.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
    k = out_h / cut.height
    cut = cut.resize((round(cut.width * k), out_h), Image.LANCZOS)
    # remove the render's dark matte fringe: erode alpha 2 px and feather it
    al_img = cut.getchannel('A').filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.8))
    if soften:
        cut = cut.filter(ImageFilter.GaussianBlur(soften))
    cut.putalpha(al_img)
    w, h = cut.size
    a = np.asarray(cut).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3:] / 255
    # de-light the supplier render: remove its baked studio shading (smooth per-column and
    # per-row illumination estimated with medians, so sparse label print does not affect it)
    lum = rgb.mean(-1)
    solid = al[..., 0] > 0.98
    r0, r1 = int(h * 0.40), int(h * 0.97)
    colp = np.array([np.median(lum[r0:r1, x][solid[r0:r1, x]]) if solid[r0:r1, x].sum() > 10 else np.nan for x in range(w)])
    good = ~np.isnan(colp)
    colp = np.interp(np.arange(w), np.arange(w)[good], colp[good])
    kk = max(3, w // 25)
    colp = np.convolve(np.pad(colp, kk, mode='edge'), np.ones(2 * kk + 1) / (2 * kk + 1), 'valid')
    c0, c1 = int(w * 0.3), int(w * 0.7)
    rowp = np.array([np.median(lum[y, c0:c1][solid[y, c0:c1]]) if solid[y, c0:c1].sum() > 5 else np.nan for y in range(h)])
    good = ~np.isnan(rowp)
    rowp = np.interp(np.arange(h), np.arange(h)[good], rowp[good])
    kk = max(5, h // 40)
    rowp = np.convolve(np.pad(rowp, kk, mode='edge'), np.ones(2 * kk + 1) / (2 * kk + 1), 'valid')
    rowp = rowp / np.median(rowp[r0:r1])
    if delight == 'col':
        rowp = np.ones_like(rowp)
    illum = colp[None, :] * rowp[:, None]
    if delight == 'none':
        pass
    elif relative:
        # keep the package's own colour/brightness: remove only the render's shading SHAPE
        rgb = np.clip(rgb / (illum / np.median(colp))[..., None], 0, 255)
    else:
        rgb = np.clip(rgb / illum[..., None] * 252.0, 0, 255)
    # resample the light model to the real bottle's footprint
    hx = np.linspace(0, len(hprof) - 1, w)
    H = np.stack([np.interp(hx, np.arange(len(hprof)), hprof[:, c]) for c in range(3)], -1)  # (w,3)
    vy = np.linspace(0, len(vnorm) - 1, h)
    V = np.interp(vy, np.arange(len(vnorm)), vnorm)                                           # (h,)
    light = H[None, :, :] * V[:, None, None] / white_ref                                      # stand-in albedo ~ white
    if flat:
        light = np.ones_like(light) * 0.97
    elif relative:
        # scene light as a ratio: brightest (lit) side of the stand-in = the package as printed
        Hl = H.mean(-1)
        light = (H / np.percentile(Hl, 97))[None, :, :] * V[:, None, None]
        light = np.clip(light, 0.25, 1.08)
    lit = np.clip(rgb * light, 0, 255)
    lit += np.random.default_rng(5).normal(0, grain, lit.shape[:2])[..., None]
    if arc:
        # camera slightly above: the base reads as the front half of an ellipse
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        cyb = h - 1 - arc
        inside = ((xx - (w - 1) / 2) / (w / 2)) ** 2 + ((yy - cyb) / arc) ** 2 <= 1.0
        m = np.where(yy > cyb, inside, True).astype(np.float32)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255
        al = al * m[..., None]
    prod = Image.fromarray(np.dstack([np.clip(lit, 0, 255), al * 255]).astype(np.uint8), 'RGBA')
    cx = (x0 + x1) / 2 + xshift
    px, py = round(cx - w / 2), y1 - h
    out = sc.convert('RGBA')
    # widen the existing contact shadow to the real (wider) footprint
    if contact:
        c = Image.new('L', out.size, 0)
        ImageDraw.Draw(c).ellipse((px - 2, y1 - 9, px + w + 2, y1 + 6), fill=255)
        c = np.asarray(c.filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255 * contact
        o = np.asarray(out).astype(np.float32)
        o[..., :3] *= (1 - c[..., None] * np.array([0.55, 0.62, 0.72]))
        out = Image.fromarray(o.astype(np.uint8), 'RGBA')
    if extra_shadow is not None:
        out = extra_shadow(out, (px, py, px + w, py + h))
    out.alpha_composite(prod, (px, py))
    global LAST_MASK
    LAST_MASK = np.zeros((sc.height, sc.width), np.float32)
    LAST_MASK[py:py + h, px:px + w] = np.asarray(prod.getchannel('A')).astype(np.float32) / 255
    if cap_from is not None:
        # cap top seen from slightly above: the stand-in's own blank top surface, widened to the
        # real cap's width (the real cap top is plain white; no packaging pixels are involved)
        cx0, cy0, cx1, cy1 = cap_from
        disc = sc.crop((cx0, cy0, cx1, cy1)).convert('RGBA')
        dw = w
        disc = disc.resize((dw, cy1 - cy0), Image.LANCZOS)
        dm = Image.new('L', disc.size, 0)
        ImageDraw.Draw(dm).ellipse((0, 0, dw - 1, (cy1 - cy0) - 1), fill=255)
        disc.putalpha(dm.filter(ImageFilter.GaussianBlur(0.8)))
        out.alpha_composite(disc, (px, py - (cy1 - cy0) // 2))
    return out.convert('RGB'), (px, py, px + w, py + h)
