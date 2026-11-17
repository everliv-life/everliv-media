"""Composite authentic product cut-outs into Gemini photoreal scenes (scene art only; packaging never generated).
Product pixels = cut-out x ONE uniform exposure scalar (no tint, no warp, never upscaled past 1.0x). Soft contact shadow only."""
import numpy as np, json
from PIL import Image, ImageFilter
from pathlib import Path
SRC = Path(__file__).parent/'src'; SC = SRC/'scenes'; OUT = SRC/'scenes'/'comp'; OUT.mkdir(exist_ok=True)
W, H = 1080, 1350

def base(name):
    im = Image.open(SC/f'{name}.jpeg').convert('RGB'); s = max(W/im.width, H/im.height)
    im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS); l = (im.width-W)//2; t = (im.height-H)//2
    return im.crop((l, t, l+W, t+H))

def place(bg, cut, bx, by, h, expo=1.0, shadow=.55):
    c = Image.open(SRC/cut).convert('RGBA'); c = c.crop(c.getbbox())
    k = min(h / c.height, 1.0); c = c.resize((round(c.width*k), round(c.height*k)), Image.LANCZOS)
    a = np.asarray(c).astype(np.float32); a[..., :3] = np.clip(a[..., :3]*expo, 0, 255); c = Image.fromarray(a.astype(np.uint8), 'RGBA')
    x = round(bx*W - c.width/2); y = round(by*H - c.height)
    sh = Image.new('L', (W, H), 0); sw = c.width*1.15; shh = max(10, c.height*.07)
    from PIL import ImageDraw
    ImageDraw.Draw(sh).ellipse([x + c.width/2 - sw/2, y + c.height - shh*.55, x + c.width/2 + sw/2, y + c.height + shh*.45], fill=int(255*shadow))
    sh = sh.filter(ImageFilter.GaussianBlur(max(6, c.height*.03)))
    bg = Image.composite(Image.new('RGB', (W, H), (12, 10, 8)), bg, sh)
    bg.paste(c, (x, y), c)
    return bg, dict(cut=cut, scale=round(k, 3), exposure=expo, box=[x, y, c.width, c.height])

TIN = lambda t: f'tin-{t}--cutout.png'
SPEC = {
 'thanksgiving-table': [('everliv-hazelnut-coffee-medium-roast--front-cutout-v2.png', .80, .83, 360, .93)],
 'fireplace-living-room': [(TIN('energy'), .27, .925, 150, .9), (TIN('hydrate'), .43, .925, 150, .9), (TIN('iron'), .59, .925, 150, .9), (TIN('d3k2'), .75, .925, 150, .9)],
 'snowman-garden': [(TIN('hydrate'), .52, .845, 135, .82), (TIN('d3k2'), .70, .845, 135, .82)],
 'new-year-kitchen': [(TIN('hydrate'), .36, .83, 165, 1.0), (TIN('iron'), .53, .83, 165, 1.0), (TIN('d3k2'), .70, .83, 165, 1.0)],
 'winter-entryway-gym-bag': [(TIN('hydrate'), .70, .64, 112, .97), (TIN('energy'), .845, .64, 112, .97)],
 'tree-model-train': [('everliv-cocoa-coffee-medium-roast--front-cutout-v2.png', .82, .9, 320, .9), (TIN('hydrate'), .63, .9, 125, .9)],
 'gift-wrapping-workshop': [('everliv-milk-honey-soap--front-cutout-v2.png', .34, .87, 190, .92), ('everliv-sandalwood-soap--front-cutout-v2.png', .53, .87, 190, .92)],
 'christmas-morning': [], 'santa-sleigh-village': [], 'front-door-wreath-mistletoe': [],
}
def bright_points(img, n=26, thr=225, mind=60):
    L = np.asarray(img.convert('L').filter(ImageFilter.GaussianBlur(3))).astype(np.float32); pts = []
    idx = np.dstack(np.unravel_index(np.argsort(-L.ravel()), L.shape))[0]
    for y, x in idx[:60000]:
        if L[y, x] < thr: break
        if all((x-px)**2 + (y-py)**2 > mind**2 for px, py in pts): pts.append((int(x), int(y)))
        if len(pts) >= n: break
    return pts

if __name__ == '__main__':
    rep = {}
    for name, items in SPEC.items():
        bg = base(name); r = []
        pts = bright_points(bg)
        for cut, bx, by, h, e in items:
            bg, info = place(bg, cut, bx, by, h, e); r.append(info)
        bg.save(OUT/f'{name}.png'); rep[name] = dict(products=r, twinkles=pts)
    json.dump(rep, open(OUT/'report.json', 'w'), indent=1)
    s = Image.new('RGB', (5*270, 2*338))
    for k, name in enumerate(SPEC): s.paste(Image.open(OUT/f'{name}.png').resize((270, 338)), ((k % 5)*270, (k//5)*338))
    s.save('/tmp/comp.png'); print('ok')
