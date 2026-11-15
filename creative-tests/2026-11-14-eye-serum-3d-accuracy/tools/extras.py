import sys, json, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
RP, SP, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
r = Image.open(RP).convert('RGBA'); b = Image.new('RGBA', r.size, (247,247,247,255)); b.alpha_composite(r)
R = np.asarray(b.convert('RGB')).astype(np.uint8); S = np.asarray(Image.open(SP).convert('RGB')).astype(np.uint8)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
# silhouette masks (object vs background; floor shadow excluded by restricting to x 780..1270 & y<1800)
def sil(a):
    m = (np.abs(a.astype(int) - 247).max(-1) > 7).astype(np.uint8)
    m[:, :780] = 0; m[:, 1270:] = 0; m[1801:] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m); k = 1 + np.argmax(st[1:, 4]); m = (lab == k).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); c = max(cs, key=cv2.contourArea)
    f = np.zeros_like(m); cv2.drawContours(f, [c], -1, 1, -1); return f
mS, mR = sil(S), sil(R)
iou = (mS & mR).sum() / (mS | mR).sum()
# edge overlay on the render: supplier contour red, model contour cyan
ov = R.copy()
for m, col in ((mS, (230, 0, 0)), (mR, (0, 170, 230))):
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); cv2.drawContours(ov, cs, -1, col, 2)
o = Image.fromarray(ov).crop((700, 200, 1350, 1850)); o.save(OUT + '-silhouette-overlay.jpg', quality=93)
# zoomed top & base of silhouette overlay
for nm, box in (('top', (760, 220, 1290, 360)), ('base', (760, 1700, 1290, 1830))):
    z = Image.fromarray(ov).crop(box); z = z.resize((z.width * 2, z.height * 2), Image.LANCZOS); z.save(f'{OUT}-silhouette-{nm}-200pct.jpg', quality=93)
# row-wise silhouette width difference
rows = {}
for y in range(260, 1790, 10):
    a, c = np.where(mS[y])[0], np.where(mR[y])[0]
    if len(a) and len(c): rows[y] = (int(a.min()) - int(c.min()), int(a.max()) - int(c.max()))
worst = max(max(abs(v[0]), abs(v[1])) for v in rows.values())
# cap & collar close-up side by side at 200%
box = (780, 230, 1270, 830)
A = Image.fromarray(S).crop(box); B = Image.fromarray(R).crop(box)
A = A.resize((A.width * 2 // 1, A.height * 2 // 1), Image.LANCZOS); B = B.resize(A.size, Image.LANCZOS)
P = Image.new('RGB', (A.width * 2 + 30, A.height + 50), 'white'); d = ImageDraw.Draw(P)
P.paste(A, (0, 50)); P.paste(B, (A.width + 30, 50))
d.text((10, 10), 'SUPPLIER (cap & upper body, 200%)', fill='black', font=f); d.text((A.width + 40, 10), 'MODEL v5 (same crop, 200%)', fill='black', font=f)
P.save(OUT + '-cap-collar-closeup.jpg', quality=93)
# label sharpness: Laplacian variance in text windows (same coords)
def lapv(a, bx):
    x0, y0, x1, y1 = bx; g = cv2.cvtColor(a[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY).astype(np.float32)
    return float(cv2.Laplacian(g, cv2.CV_32F).var())
wins = {'logo': (880, 840, 1060, 950), 'title': (960, 1000, 1040, 1600), 'netwt_series': (900, 1595, 1110, 1690), 'qr': (1180, 1180, 1240, 1380), 'ingredients_edge': (1180, 830, 1240, 1000)}
sharp = {k: {'supplier': round(lapv(S, v)), 'model': round(lapv(R, v)), 'ratio': round(lapv(R, v) / max(lapv(S, v), 1e-6), 2)} for k, v in wins.items()}
# QR position: dark-module bbox in window
def qr(a):
    p = a[1150:1420, 1160:1245].mean(-1) < 80; ys, xs = np.where(p); return [int(xs.min() + 1160), int(ys.min() + 1150), int(xs.max() + 1160), int(ys.max() + 1150)]
res = {'silhouette_IoU': round(float(iou), 4), 'silhouette_worst_row_edge_offset_px': worst, 'label_sharpness_laplacian': sharp, 'qr_bbox': {'supplier': qr(S), 'model': qr(R)}}
json.dump(res, open(OUT + '-extras.json', 'w'), indent=1); print(json.dumps(res, indent=1))
