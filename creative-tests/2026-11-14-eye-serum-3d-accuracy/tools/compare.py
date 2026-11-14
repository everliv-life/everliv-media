"""Compare the neutral 3D render against the supplier front render (same 2048 framing).
Outputs: side-by-side, difference overlay, detail crops, colour + geometry metrics (json)."""
import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

R_P, S_P, LAB_P, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
bg = (247, 247, 247)
r = Image.open(R_P).convert('RGBA'); base = Image.new('RGBA', r.size, bg + (255,)); base.alpha_composite(r)
R = base.convert('RGB'); S = Image.open(S_P).convert('RGB'); L = Image.open(LAB_P).convert('RGB')
Ra, Sa = np.asarray(R).astype(int), np.asarray(S).astype(int)

def silhouette(a):
    d = np.abs(a - np.array(bg)).max(-1) > 6
    return d
def prof(a):
    d = silhouette(a)
    out = {}
    for y in (300, 500, 700, 740, 1000, 1400, 1700):
        xs = np.where(d[y, 600:1450])[0]
        out[y] = int(xs.max() - xs.min()) if len(xs) else 0
    col = np.where(d[:, 1000:1046].any(1))[0]
    out['top'] = int(col.min()); out['bottom_incl_shadow'] = int(col.max())
    return out

def green_box(a):
    m = (a[..., 1] - a[..., 0] > 40) & (a[..., 1] - a[..., 2] > 40)
    ys, xs = np.where(m); return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

metrics = {'supplier_profile': prof(Sa), 'render_profile': prof(Ra),
           'leaf_bbox_supplier': green_box(Sa), 'leaf_bbox_render': green_box(Ra)}

# colour: sample ink colours via masks inside the same label windows
def ink(a, box, kind):
    x0, y0, x1, y1 = box; p = a[y0:y1, x0:x1].reshape(-1, 3)
    if kind == 'green': m = (p[:, 1] - p[:, 0] > 40) & (p[:, 1] - p[:, 2] > 40)
    elif kind == 'gold': m = (p[:, 0] - p[:, 2] > 40) & (p[:, 0] > 120)
    elif kind == 'dark': m = p.mean(1) < 110
    else: m = p.mean(1) > np.percentile(p.mean(1), 70)
    return p[m].mean(0).round(1).tolist() if m.sum() > 5 else None
def chroma_ratio(c, paper):   # ink relative to the paper white in the same image (removes shading level)
    return [round(c[i] / paper[i], 3) for i in range(3)] if c and paper else None

wins = {'logo_leaf': ((960, 850, 1140, 950), 'green'), 'logo_type': ((800, 840, 1000, 950), 'dark'),
        'gold_rules_and_series': ((850, 1520, 1200, 1570), 'gold'), 'vertical_title': ((930, 960, 1000, 1500), 'dark'),
        'paper_near_title': ((820, 1100, 900, 1300), 'paper')}
col = {}
for k, (box, kind) in wins.items():
    col[k] = {'supplier': ink(Sa, box, kind), 'render': ink(Ra, box, kind)}
for who in ('supplier', 'render'):
    paper = col['paper_near_title'][who]
    for k in wins:
        if k != 'paper_near_title':
            col[k][who + '_rel_paper'] = chroma_ratio(col[k][who], paper)
La = np.asarray(L).astype(int)
art = {'leaf': ink(La, (640, 120, 860, 240), 'green'), 'type_dark': ink(La, (400, 80, 650, 240), 'dark'),
       'gold': ink(La, (330, 1200, 1100, 1260), 'gold'), 'paper': La[1100, 350].tolist()}
art_rel = {k: chroma_ratio(v, art['paper']) for k, v in art.items() if k != 'paper'}
metrics['colour'] = col; metrics['artwork_flat'] = art; metrics['artwork_rel_paper'] = art_rel

# visuals
W = Image.new('RGB', (2 * 900 + 60, 1700), 'white'); d = ImageDraw.Draw(W)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
except Exception: f = None
W.paste(S.crop((570, 180, 1470, 1860)).resize((900, 1680)), (0, 20)); W.paste(R.crop((570, 180, 1470, 1860)).resize((900, 1680)), (960, 20))
d.text((10, 0), 'SUPPLIER FRONT RENDER', fill='black', font=f); d.text((970, 0), '3D MODEL — NEUTRAL (provisional)', fill='black', font=f)
W.save(OUT + '-side-by-side.jpg', quality=92)
diff = ImageChops.difference(S, R).convert('L').point(lambda v: min(255, v * 3))
ov = Image.blend(S, R, 0.5)
W2 = Image.new('RGB', (1800, 1680), 'white'); W2.paste(ov.crop((570, 180, 1470, 1860)), (0, 0)); W2.paste(Image.merge('RGB', [diff] * 3).crop((570, 180, 1470, 1860)), (900, 0))
W2.save(OUT + '-overlay-and-diff.jpg', quality=92)
crops = {'logo': (780, 820, 1150, 960), 'title_top': (840, 950, 1060, 1250), 'series_netwt': (820, 1500, 1230, 1620),
         'qr_edge': (1120, 1100, 1250, 1350), 'left_edge_text': (800, 780, 880, 1050), 'cap_collar': (780, 230, 1260, 820), 'base': (780, 1580, 1260, 1830)}
for k, b in crops.items():
    a, c = S.crop(b), R.crop(b); w, h = a.size; sc = max(1, int(600 / max(w, h)))
    a, c = a.resize((w * sc, h * sc), Image.LANCZOS), c.resize((w * sc, h * sc), Image.LANCZOS)
    P = Image.new('RGB', (2 * a.width + 20, a.height), 'white'); P.paste(a, (0, 0)); P.paste(c, (a.width + 20, 0)); P.save(f'{OUT}-crop-{k}.jpg', quality=92)
json.dump(metrics, open(OUT + '-metrics.json', 'w'), indent=1)
print(json.dumps(metrics, indent=1))
