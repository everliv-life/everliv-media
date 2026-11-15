"""EverLiv straight-on authentic compositor (v1, Nov 14 2026).
Rules enforced in code:
  * Product pixels come from the verified cut-out unchanged, except ONE uniform exposure scalar
    (same factor on R,G,B -> no hue/tint change; clamped 0.85..1.08). No relighting maps, no colour tint.
  * Scale once from cut-out to final pixels (LANCZOS), never upscaled beyond 1.0x of the cut-out.
  * Background, light and shadows come from the generated scene/clean plate. The stand-in's shadow
    (scene/plate ratio) is re-mapped from the stand-in footprint onto the product footprint.
  * Built at the final output resolution (2160x2700 master; 1080x1350 feed).
Usage: compose_authentic.py <scene> <plate> <standin_mask.npy> <cutout.png> <out_prefix> [--topdown] [--fill=0.92] [--expo=auto|1.0]
"""
import sys, json, numpy as np, cv2
from PIL import Image

OW, OH = 2160, 2700
def arg(k, d=None):
    for a in sys.argv:
        if a.startswith(k + '='): return a.split('=', 1)[1]
    return d

scene_p, plate_p, mask_p, cut_p, out = sys.argv[1:6]
topdown = '--topdown' in sys.argv
fill = float(arg('--fill', '1.0'))          # product size relative to stand-in (height for upright, fit for topdown)
expo_mode = arg('--expo', 'auto')

S = np.asarray(Image.open(scene_p).convert('RGB')).astype(np.float32)
P = np.asarray(Image.open(plate_p).convert('RGB').resize((S.shape[1], S.shape[0]), Image.LANCZOS)).astype(np.float32)
M = np.load(mask_p).astype(np.uint8)
H, W = S.shape[:2]
ys, xs = np.where(M > 0); bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1

# ---- shadow matte from the stand-in (luminance ratio scene/plate), stand-in interior excluded
eps = 6.0
ratio = np.clip((S.mean(-1) + eps) / (P.mean(-1) + eps), 0.2, 1.0)
inside = cv2.dilate(M, np.ones((31, 31), np.uint8))
r8 = (ratio * 255).astype(np.uint8)
rfill = cv2.inpaint(r8, inside, 15, cv2.INPAINT_TELEA).astype(np.float32) / 255
rfill = cv2.GaussianBlur(rfill, (0, 0), 3)
near = cv2.dilate(M, np.ones((int(0.5 * (by1 - by0)) | 1, int(0.9 * (bx1 - bx0)) | 1), np.uint8)).astype(np.float32)
near = cv2.GaussianBlur(near, (0, 0), 30)
shadow = 1 - (1 - rfill) * near                    # 1 = no shadow

# ---- final canvas (scale to height, centre-crop width)
s = OH / H; RW = int(round(W * s)); left = (RW - OW) // 2
up = lambda a, it=cv2.INTER_LANCZOS4: cv2.resize(a, (RW, OH), interpolation=it)[:, left:left + OW]
PL = up(P); SH = up(shadow.astype(np.float32), cv2.INTER_LINEAR)
X0, Y0, X1, Y1 = bx0 * s - left, by0 * s, bx1 * s - left, by1 * s

# ---- product placement (one uniform scale from the cut-out)
cut = Image.open(cut_p).convert('RGBA')
cw, ch = cut.size
if topdown:
    k = min((X1 - X0) / cw, (Y1 - Y0) / ch) * fill
else:
    k = (Y1 - Y0) / ch * fill
k = min(k, 1.0)                                      # never upscale the authentic asset
pw, ph = int(round(cw * k)), int(round(ch * k))
prod = np.asarray(cut.resize((pw, ph), Image.LANCZOS)).astype(np.float32)
rgb, al = prod[..., :3], prod[..., 3] / 255.0
cx = (X0 + X1) / 2
px = int(round(cx - pw / 2))
py = int(round((Y0 + Y1) / 2 - ph / 2)) if topdown else int(round(Y1 - ph))

# ---- remap the stand-in shadow onto the product footprint (affine bbox -> bbox), keep scene shadow elsewhere
sx, sy = pw / (X1 - X0), ph / (Y1 - Y0)
A = np.float32([[sx, 0, px - X0 * sx], [0, sy, (py + ph if not topdown else py) - (Y1 if not topdown else Y0) * sy]])
if topdown:
    A = np.float32([[sx, 0, px - X0 * sx], [0, sy, py - Y0 * sy]])
SHm = cv2.warpAffine(SH, A, (OW, OH), flags=cv2.INTER_LINEAR, borderValue=1.0)
synth = arg('--synth-shadow')        # dx,dy,sigma,strength in output px: cast from the product's own silhouette
if synth:
    dx, dy, sg, stg = [float(v) for v in synth.split(',')]
    sil = np.zeros((OH, OW), np.float32)
    al0 = np.asarray(cut.resize((pw, ph), Image.LANCZOS)).astype(np.float32)[..., 3] / 255.0
    ya_, yb_, xa_, xb_ = max(0, py), min(OH, py + ph), max(0, px), min(OW, px + pw)
    sil[ya_:yb_, xa_:xb_] = al0[ya_ - py:yb_ - py, xa_ - px:xb_ - px]
    Mt = np.float32([[1, 0, dx], [0, 1, dy]])
    cast = cv2.GaussianBlur(cv2.warpAffine(sil, Mt, (OW, OH)), (0, 0), sg)
    SHm = np.ones((OH, OW), np.float32) - stg * cast
    SH = np.ones((OH, OW), np.float32)       # plate already has the stand-in shadow removed
# blend: inside the stand-in's neighbourhood use the remapped shadow, outside keep the original scene shadow
reg = np.zeros((OH, OW), np.float32); reg[int(max(0, Y0 - 300)):int(min(OH, Y1 + 300)), int(max(0, X0 - 400)):int(min(OW, X1 + 400))] = 1
reg = cv2.GaussianBlur(reg, (0, 0), 60)
SHf = SH * (1 - reg) + SHm * reg
out_img = PL * SHf[..., None]

# ---- contact occlusion (upright: along the base; topdown: thin all-round occlusion)
pa = np.zeros((OH, OW), np.float32)
ya, yb, xa, xb = max(0, py), min(OH, py + ph), max(0, px), min(OW, px + pw)
pa[ya:yb, xa:xb] = al[ya - py:yb - py, xa - px:xb - px]
if topdown:
    occ = cv2.GaussianBlur(cv2.dilate((pa > 0.5).astype(np.float32), np.ones((5, 5), np.uint8)), (0, 0), 4) * (1 - pa)
    out_img *= (1 - 0.35 * occ)[..., None]
else:
    base = np.zeros((OH, OW), np.float32)
    for x in range(xa, xb):
        col = np.where(pa[:, x] > 0.5)[0]
        if len(col): base[col.max(), x] = 1
    occ = cv2.GaussianBlur(cv2.dilate(base, np.ones((3, 15), np.uint8)), (0, 0), 3.5)
    occ = occ / max(occ.max(), 1e-6) * 0.6
    out_img *= (1 - occ[..., None] * np.array([0.85, 0.87, 0.9], np.float32))

# ---- one uniform exposure scalar for the product (luminance of the stand-in's lit face vs the cut-out)
if expo_mode == 'auto':
    st_l = np.median(S[M > 0].mean(-1)); pr_l = np.median(rgb[al > 0.98].mean(-1))
    ref_l = np.median(P[max(0, by0):by1, max(0, bx0 - 200):bx0].mean(-1)) if bx0 > 200 else st_l
    expo = float(np.clip(st_l / max(pr_l, 1), 0.85, 1.08))
else:
    expo = float(expo_mode)
prod_rgb = np.clip(rgb * expo, 0, 255)
A3 = al[ya - py:yb - py, xa - px:xb - px][..., None]
out_img[ya:yb, xa:xb] = out_img[ya:yb, xa:xb] * (1 - A3) + prod_rgb[ya - py:yb - py, xa - px:xb - px] * A3

# ---- grain matched to the plate, at 50% on the product (luminance only, no colour)
g = PL[200:600, 200:600].mean(-1); gsd = float(np.clip((g - cv2.GaussianBlur(g, (0, 0), 2)).std(), 0.5, 3.0))
noise = np.random.default_rng(7).normal(0, gsd, (OH, OW, 1)).astype(np.float32)
out_img += noise * (1 - 0.5 * pa)[..., None]
final = Image.fromarray(np.clip(out_img, 0, 255).astype(np.uint8))
final.save(out + '-2160x2700.png'); final.resize((1080, 1350), Image.LANCZOS).save(out + '-1080x1350.png')

# ---- fidelity metrics vs the cut-out at the same width
def p99(a):
    g = cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
    return float(np.percentile(np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1)), 99))
crop = np.asarray(final)[ya:yb, xa:xb].astype(np.float32)
ref = np.asarray(cut.convert('RGB').resize((pw, ph), Image.LANCZOS)).astype(np.float32)[ya - py:yb - py, xa - px:xb - px]
solid = al[ya - py:yb - py, xa - px:xb - px] > 0.98
hue_shift = (crop[solid] / np.maximum(crop[solid].mean(-1, keepdims=True), 1)) - (ref[solid] / np.maximum(ref[solid].mean(-1, keepdims=True), 1))
rep = {'scale_from_cutout': round(k, 4), 'product_px': [pw, ph], 'product_height_pct_of_frame': round(100 * ph / OH, 1),
       'product_width_pct_of_frame': round(100 * pw / OW, 1), 'exposure_scalar': round(expo, 3),
       'label_sharpness_pct_of_source_same_width': round(100 * p99(crop) / p99(ref)),
       'mean_abs_chroma_ratio_shift': round(float(np.abs(hue_shift).mean()), 4),
       'note': 'product pixels = cut-out x exposure scalar + luminance grain; no tint'}
json.dump(rep, open(out + '-report.json', 'w'), indent=1); print(json.dumps(rep))
