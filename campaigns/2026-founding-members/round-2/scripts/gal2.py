"""Refresh the review gallery from the round-2 calendar (same artifact, same Approve/Edit/Reject keys)."""
import json, glob, shutil, subprocess, pathlib
from PIL import Image
import plan2
R = pathlib.Path(__file__).parent; G = R/'gallery'; AS = R/'assets'
(G/'img').mkdir(exist_ok=True); (G/'video').mkdir(exist_ok=True)
old = json.load(open(G/'data.json'))
def jpg(png):
    rel = 'img/' + png.relative_to(AS).as_posix().replace('/', '__').replace('.png', '.jpg')
    Image.open(png).convert('RGB').save(G/rel, quality=84); return rel
def vid(stem):
    for d in (AS/'anim', AS/'video'):
        f = d/f'{stem}.mp4'
        if f.exists():
            shutil.copy(f, G/'video'/f.name)
            post = G/'img'/f'poster-{stem}.jpg'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '5', '-i', str(f), '-frames:v', '1', '-vf', 'scale=540:-2', '-q:v', '4', str(post)])
            return f'video/{f.name}', f'img/poster-{stem}.jpg'
    return None, None
pieces = []
for p in plan2.P:
    if p['rev'] == 'REMOVED':
        continue
    stem = p['asset']
    pngs = sorted(x for x in AS.glob(f'{stem}*.png') if not x.name.startswith('_'))
    if p['fmt'] == 'email' and not pngs:
        pngs = sorted(AS.glob(f'{stem}*.png'))
    imgs = [jpg(x) for x in pngs][:6]
    vids, posters = [], []
    for m in p['motion']:
        v, po = vid(m)
        if v: vids.append(v); posters.append(po)
    if p['fmt'] == 'reel' and not vids:
        v, po = vid(stem)
        if v: vids.append(v); posters.append(po)
    pieces.append(dict(id=p['id'], date=p['date'], phase=p['phase'], title=p['title'], hook=p['hook'], caption=p['caption'], fmt=p['fmt'],
                       platforms=list(p['platforms']), status=p['status'], rev=p['rev'], kind=p['kind'], music=p.get('music', ''),
                       note=p.get('note', ''), deps=p['deps'], alt=[], imgs=imgs, vids=vids, posters=posters, cta=p['cta'], url=''))
d = dict(old); d['pieces'] = pieces
d['stories'] = [jpg(x) for x in sorted((AS/'stories-r2').glob('*.png'))]
AN = [('MV-R2-01', 'Membership: logo draw + gold leaf (reels end)', 'A02 · A04R · B01R · C19', 'A04R-reveal-reel--with-logo-outro', 'Reserved for membership reels; product reels keep plain endings.'),
 ('MV-R2-02', 'Membership: emblem ring orbit + heartbeat (slow)', 'J16 · Jan 21', 'J16-ten-days-left', 'Emblem-led variant with a slower ring orbit.'),
 ('MV-R2-03', 'Membership: last chance, logo draws in last', 'J24 · Jan 31', 'J24-last-chance--reel', 'Message first; the logo and gold leaf close it.'),
 ('MV-R2-04', 'Membership: heartbeat line to member price (Hydrate)', 'J06 · Jan 7', 'PRICE-hydrate', 'Exact product price: $34.99 everyday, $27.99 member (20%).'),
 ('MV-R2-05', 'Membership: wreath door, Founding Member', 'C17 · Dec 18', 'PR08-door-wreath-founding-member', 'Photoreal scene + emblem moment + approved Founding Member statement.'),
 ('MV-R2-06', 'Thanksgiving table (photoreal)', 'A07 · Nov 26', 'PR01-thanksgiving-table', 'Candle flicker, twinkles, slow push-in.'),
 ('MV-R2-07', 'Fireplace stocking stuffers (photoreal)', 'C05 · Dec 6', 'PR02-fireplace-stocking-stuffers', 'Fire glow, tree lights; four tins on the table.'),
 ('MV-R2-08', 'Snowman: gifts that won\'t melt (photoreal)', 'C11 slot · Dec 12', 'PR03-snowman-gifts', 'Snowfall, garden lights; Hydrate and D3+K2.'),
 ('MV-R2-09', 'Santa over the village (photoreal)', 'D04 · Dec 24', 'PR04-santa-christmas-eve', 'Christmas Eve; no products.'),
 ('MV-R2-10', 'Christmas morning (photoreal)', 'X25 · Dec 25', 'PR05-christmas-morning', 'Steam from the mugs, candle; sincere greeting, no sell.'),
 ('MV-R2-11', 'Tree and model train (photoreal)', 'C13 · Dec 14', 'PR06-tree-train-gifts', 'Tree lights; processing-time note, no delivery promise.'),
 ('MV-R2-12', 'Gift-wrapping workshop, soaps (photoreal)', 'C07 · Dec 8', 'PR07-workshop-soaps', 'Lamp-light twinkle; elf hat as a subtle nod.'),
 ('MV-R2-13', 'Cozy coffee: Cocoa (smaller bag)', 'P19 · Nov 19 / C03', 'COFFEE2-cocoa-steam', 'Bag ~15% smaller; calmer lights; steam.'),
 ('MV-R2-14', 'Cozy coffee: Caramel (smaller bag)', 'P1219 · Dec 19', 'COFFEE2-caramel-steam', 'Same treatment.'),
 ('MV-R2-15', 'New year kitchen (photoreal)', 'J01a · Jan 1', 'PR09-new-year-kitchen', 'Morning light sweep; Hydrate, Iron, D3+K2.'),
 ('MV-R2-16', 'Packed for the new year (photoreal)', 'J04 · J17', 'PR10-entryway-gym-bag', 'Bright entryway; Hydrate and Energy.'),
 ('MV-R2-17', 'Strips spotlight reel', 'J11 · Jan 14', 'J11-strips-family--reel', 'Four tins, one at a time; product reel, plain logo.')]
d['anims'] = []
for i, t, w, stem, n in AN:
    v, po = vid(stem)
    if v: d['anims'].append(dict(id=i, title=t, where=w, file=v, poster=po, note=n))
d['decisions'] = []
json.dump(d, open(G/'data.json', 'w'))
cal = json.load(open(R/'package-r2'/'calendar-r2.json')); json.dump(cal, open(G/'calendar.json', 'w'))
print(len(pieces), 'pieces', sum(len(p['vids']) for p in pieces), 'videos')
