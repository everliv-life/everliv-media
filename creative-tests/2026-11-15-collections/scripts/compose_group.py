"""EverLiv group compositor (collection / banner images).

Authenticity rules (same as compose_authentic.py):
  * product pixels = supplier cut-out, uniformly resized, x ONE exposure scalar shared by every product in the image,
    + luminance-only grain. No tint, no relight, no mirroring, no warping.
  * the SCENE may be white-balanced toward neutral (scene_wb) - never the product.
  * shadows are drawn on the scene only (under/behind products), from each product's own silhouette.

Usage: compose_group.py layout.json
layout.json = {
  "plate": "...jpg", "out": "name", "scene_wb": 0.5, "expo": "auto" | 0.97,
  "expo_region": [x0,y0,x1,y1],              # plate region used for auto exposure (empty surface near products)
  "mode": "topdown" | "upright",
  "shadow": {...},                            # topdown: dx,dy,sigma,strength ; upright: contact,glen,gdx,gsigma,gstrength
  "items": [ {"cutout": "...png", "x": cx, "y": cy_or_baseline, "w": target_width_px, "choke": 0} ]   # back-to-front order
  "exports": [[W,H,"tag"], ...]               # plain downscales of the master (same aspect only)
}
For topdown items (x,y) is the centre; for upright items y is the base line (bottom of the product)."""
import sys, json, numpy as np, cv2
from PIL import Image

L = json.load(open(sys.argv[1]))
P = np.asarray(Image.open(L['plate']).convert('RGB')).astype(np.float32)
H, W = P.shape[:2]
report = {'plate': L['plate'], 'items': []}

wbf = float(L.get('scene_wb', 0))
if wbf > 0:
    lum = P.mean(-1); sel = (lum > np.percentile(lum, 85)) & ((P.max(-1) - P.min(-1)) < 70)
    wp = P[sel].mean(0); gain = (wp.mean() / wp) ** wbf
    P = np.clip(P * gain, 0, 255); report['scene_wb_gain'] = gain.round(4).tolist()

# --- load + scale items
items = []
for it in L['items']:
    c = np.asarray(Image.open(it['cutout']).convert('RGBA')).astype(np.float32)
    s = it['w'] / c.shape[1]
    if s > 1.0: raise SystemExit('refusing to upscale a cut-out above 1.0x: ' + it['cutout'])
    nw, nh = int(round(c.shape[1] * s)), int(round(c.shape[0] * s))
    r = cv2.resize(c, (nw, nh), interpolation=cv2.INTER_AREA)
    rgb, al = r[..., :3], r[..., 3] / 255.0
    if it.get('choke', 0):
        k = int(it['choke']); al = np.minimum(al, cv2.erode(al, np.ones((2 * k + 1, 2 * k + 1), np.uint8)))
    al = np.where(al > 0.995, 1.0, al)
    if L['mode'] == 'topdown': x0, y0 = int(round(it['x'] - nw / 2)), int(round(it['y'] - nh / 2))
    else: x0, y0 = int(round(it['x'] - nw / 2)), int(round(it['y'] - nh))
    items.append(dict(rgb=rgb, al=al, x0=x0, y0=y0, w=nw, h=nh, src=it['cutout'], scale=s))

def place(arr2d, x0, y0):
    full = np.zeros((H, W), np.float32); h, w = arr2d.shape
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    full[ya:yb, xa:xb] = arr2d[ya - y0:yb - y0, xa - x0:xb - x0]; return full

# --- exposure: one scalar for all products
if L.get('expo', 'auto') == 'auto':
    x0r, y0r, x1r, y1r = L['expo_region']
    ref = np.percentile(P[y0r:y1r, x0r:x1r].mean(-1), 75)
    lab = np.concatenate([it['rgb'][it['al'] > 0.99].mean(-1) for it in items])
    paper = np.percentile(lab, 90)
    expo = float(np.clip(ref / paper * float(L.get('expo_bias', 1.0)), 0.85, 1.05))
else:
    expo = float(L['expo'])
report['exposure_scalar'] = round(expo, 4)

# --- shadows on the scene
S = np.ones((H, W), np.float32)
sh = L['shadow']
for it in items:
    A = place(it['al'], it['x0'], it['y0'])
    if L['mode'] == 'topdown':
        cast = cv2.GaussianBlur(np.roll(np.roll(A, int(sh['dx']), 1), int(sh['dy']), 0), (0, 0), sh['sigma'])
        contact = cv2.GaussianBlur(cv2.dilate(A, np.ones((5, 5), np.uint8)), (0, 0), 3)
        S *= (1 - sh['strength'] * cast) * (1 - sh.get('contact', 0.22) * contact)
    else:
        # contact: bottom-most opaque pixel per column, kept only near the true base
        base = np.zeros((H, W), np.float32); hb = it['h']
        for x in range(it['w']):
            col = np.where(it['al'][:, x] > 0.5)[0]
            if len(col) and col.max() > hb * 0.85:
                X, Y = it['x0'] + x, it['y0'] + col.max()
                if 0 <= X < W and 0 <= Y < H: base[Y, X] = 1
        bys = np.where(base.any(1))[0]; yb0 = bys.max()
        occ = cv2.GaussianBlur(cv2.dilate(base, np.ones((5, 15), np.uint8)), (0, 0), 6)
        occ = occ / max(occ.max(), 1e-6)
        # ground shadow: silhouette laid on the surface behind the product, skewed away from the key light
        hgt = max(2, int(hb * sh['glen']))
        sil = (A > 0.5).astype(np.float32)[max(0, it['y0']):yb0 + 1]
        sq = cv2.resize(sil, (W, hgt), interpolation=cv2.INTER_AREA)
        g = np.zeros((H, W), np.float32); y0g = max(0, yb0 - hgt + 1); g[y0g:yb0 + 1] = sq[-(yb0 + 1 - y0g):]
        M2 = np.float32([[1, sh['gdx'] / hgt, -sh['gdx'] * (yb0 - hgt) / hgt], [0, 1, 0]])
        g = cv2.warpAffine(g, M2, (W, H))
        g = np.maximum(g, occ)
        g = cv2.GaussianBlur(np.clip(g, 0, 1), (0, 0), sh['gsigma'])
        fade = np.ones(H, np.float32); n = int(sh.get('front_fade', 40))
        fade[yb0:yb0 + n] = np.linspace(1, 0, len(fade[yb0:yb0 + n])); fade[yb0 + n:] = 0
        g *= fade[:, None]
        S *= (1 - sh['gstrength'] * g) * (1 - sh.get('contact', 0.25) * occ * fade[:, None])
out = P * S[..., None]

# --- products, back to front
PA = np.zeros((H, W), np.float32)
for it in items:
    A = place(it['al'], it['x0'], it['y0'])
    R = np.zeros((H, W, 3), np.float32)
    for ch in range(3): R[..., ch] = place(it['rgb'][..., ch], it['x0'], it['y0'])
    out = out * (1 - A[..., None]) + np.clip(R * expo, 0, 255) * A[..., None]
    PA = np.maximum(PA, A)
    report['items'].append({'cutout': it['src'], 'scale': round(it['scale'], 4), 'px': [it['w'], it['h']], 'xy': [it['x0'], it['y0']]})

# --- grain matched to the plate (luminance only)
g = P.mean(-1); gsd = float(np.clip((g - cv2.GaussianBlur(g, (0, 0), 2)).std(), 0.5, 4.0))
gsd = float(L.get('grain_sd', gsd))
rng = np.random.default_rng(7); noise = rng.normal(0, gsd, (H, W)).astype(np.float32)
noise = cv2.GaussianBlur(noise, (0, 0), 0.6) * 1.6
out = out + (noise * PA)[..., None]
report['grain_sd'] = round(gsd, 2)
out = np.clip(out, 0, 255).astype(np.uint8)
name = L['out']
Image.fromarray(out).save(name + '-master.png')
for (ew, eh, tag) in L.get('exports', []):
    im = Image.fromarray(out); ar = ew / eh
    if abs(W / H - ar) > 1e-3:
        if W / H > ar: cw = int(round(H * ar)); im = im.crop(((W - cw) // 2, 0, (W - cw) // 2 + cw, H))
        else: ch = int(round(W / ar)); im = im.crop((0, (H - ch) // 2, W, (H - ch) // 2 + ch))
    im.resize((ew, eh), Image.LANCZOS).save(f'{name}-{tag}-{ew}x{eh}.png')
report['disclosure'] = 'Product shown as supplied; scene digitally created.'
report['note'] = 'product pixels = cut-out x one exposure scalar + luminance grain; no tint, relight, warp or mirroring'
json.dump(report, open(name + '-report.json', 'w'), indent=1)
print(json.dumps({k: report[k] for k in ('exposure_scalar', 'grain_sd')}))
