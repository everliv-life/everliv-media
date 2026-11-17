"""EverLiv campaign walkthrough: one chronological 1920x1080 MP4 (Nov 17, 2026 -> Jan 31, 2027).
Real assets only; proposed motion versions, concepts, specs and January plans are labelled as such."""
import asyncio, json, subprocess, shutil, pathlib, datetime as dt, collections, re
from playwright.async_api import async_playwright
import build_assets as B
import plan, plan2
from build_assets import u, GOLD, CHAMP, LEAF, IVORY, INK, LIME

R = B.ROOT; AS = R/'assets'; AN = AS/'anim'; VD = AS/'video'
W = R/'walkthrough-r2'; FR = W/'frames'; SG = W/'segs'
for d in (FR, SG): shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
G = json.load(open(R/'gallery'/'data.json'))
PK = {p['id']: p for p in plan2.P}
START, END = dt.date(2026, 11, 18), dt.date(2027, 1, 31)

def dur(p): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)]))
def png(rel): return AS/(pathlib.Path(rel).stem + '.png')

CSS = B.CSS.replace('body{{width:var(--w);height:var(--h)', 'body{{width:1920px;height:1080px') + f"""
body{{width:1920px;height:1080px;background:radial-gradient(120% 100% at 75% 0%,#33503a 0%,{LEAF} 50%,#1d301d 100%);color:{IVORY}}}
.top{{position:absolute;left:70px;right:70px;top:46px;display:flex;justify-content:space-between;align-items:center}}
.tl{{position:absolute;left:70px;right:70px;bottom:44px;height:26px}}
.tl .bar{{position:absolute;left:0;right:0;top:12px;height:2px;background:rgba(201,178,124,.25)}}
.tl .fill{{position:absolute;left:0;top:12px;height:2px;background:{GOLD}}}
.tl .dot{{position:absolute;top:5px;width:16px;height:16px;margin-left:-8px;border-radius:50%;background:{GOLD};box-shadow:0 0 0 6px rgba(201,178,124,.18)}}
.tl .m{{position:absolute;top:-22px;font:600 14px Figtree;letter-spacing:.14em;text-transform:uppercase;color:rgba(234,223,195,.55);transform:translateX(-50%)}}
.left{{position:absolute;left:110px;top:170px;width:760px}}
.slot{{position:absolute;left:1000px;top:105px;width:840px;height:870px;display:flex;align-items:center;justify-content:center}}
.slot img{{max-width:840px;max-height:870px;border-radius:18px;box-shadow:0 40px 80px -30px rgba(0,0,0,.6)}}
.pill{{display:inline-block;padding:9px 16px;border-radius:999px;font:700 15px Figtree;letter-spacing:.14em;text-transform:uppercase}}
.chips span{{display:inline-block;margin:0 8px 8px 0;padding:6px 12px;border:1px solid rgba(233,228,223,.3);border-radius:999px;font:600 16px Figtree}}
"""
PILL = {'ready': (CHAMP, LEAF, 'Ready for review'), 'new': ('#DCE8D0', LEAF, 'New in round 2'), 'replaced': ('#EADFC3', LEAF, 'Replaced in round 2'), 'hold': ('#F3DFA8', '#5b4510', 'Template · on hold'), 'motion': (GOLD, LEAF, 'Motion version · proposed'),
        'concept': ('#E7C9A9', '#5a3418', 'Concept · illustration test'), 'spec': ('#F3DFA8', '#5b4510', 'Not yet produced · script only'),
        'todo': ('#F2C4C4', '#6b1d1d', 'Not yet produced'), 'plan': ('rgba(233,228,223,.16)', IVORY, 'Planned · not yet produced'),
        'email': ('#DCE8D0', LEAF, 'Email · to opted-in subscribers')}
def pill(k, extra=''):
    bg, fg, t = PILL[k]; return f"<span class='pill' style='background:{bg};color:{fg}'>{t}{extra}</span>"

def timeline(day, phase):
    tot = (END - START).days; x = lambda d: 100 * (d - START).days / tot
    marks = [(dt.date(2026, 11, 27), 'Black Friday'), (dt.date(2026, 12, 1), 'Dec'), (dt.date(2026, 12, 25), 'Christmas'), (dt.date(2027, 1, 1), 'Jan'), (END, 'Jan 31')]
    m = ''.join(f"<div class='m' style='left:{x(d):.2f}%'>{t}</div>" for d, t in marks)
    return (f"<div class='top'>{B.logo(True, 40)}<div class='eb' style='color:{GOLD};font-size:18px'>{phase}</div></div>"
            f"<div class='tl'><div class='bar'></div><div class='fill' style='width:{x(day):.2f}%'></div>{m}<div class='dot' style='left:{x(day):.2f}%'></div></div>")

def page(body): return f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{--w:1920px;--h:1080px;--pad:0}}{CSS}</style></head><body>{body}</body></html>"


PH = [(dt.date(2026, 11, 18), dt.date(2026, 11, 26), '1 · Introduce the Founding Member', 'Nov 18–26', 'Strips and coffee open the feed, then the Member Price Club reveal on Mon Nov 23, how it works, the math, Iron, and a photoreal Thanksgiving.'),
      (dt.date(2026, 11, 27), dt.date(2026, 11, 30), '2 · Black Friday to Cyber Monday', 'Nov 27–30', 'A short sale vs 12 months of up to 20% off, with D3 + K2 and Energy between the offer posts.'),
      (dt.date(2026, 12, 1), dt.date(2026, 12, 20), '3 · Holiday gifting', 'Dec 1–20', 'Photoreal holiday scenes with real products: fireplace, snowman, train, workshop, a wreath door for members, and cozy coffee.'),
      (dt.date(2026, 12, 21), dt.date(2026, 12, 31), '4 · Christmas to New Year', 'Dec 21–31', 'Santa on Christmas Eve, a sincere Christmas Day, a product-led 2027 routine and a brand-only New Year\'s Eve.'),
      (dt.date(2027, 1, 1), END, '5 · New Year and the final window', 'Jan 1–31', 'Routines, product discovery and member value; the final ten days build to "Last chance to join at $49.99."')]
def phase_of(d): return next(p for p in PH if p[0] <= d <= p[1])
KIND = {'member': 'Membership', 'product': 'Product & gifting', 'brand': 'Brand & lifestyle'}
SEGS = []
def still(html, s): SEGS.append(('still', html, s, None))
def video(html, path, s=None): SEGS.append(('video', html, s or dur(path), path))
def left(day, p, label_html, sub=''):
    d = dt.date.fromisoformat(day)
    chips = ''.join(f"<span>{x.replace('*', '')}</span>" for x in p.get('platforms', []))
    kind = KIND.get(p.get('kind', ''), '')
    mus = f"<div class='p' style='font-size:22px;margin-top:16px;color:{CHAMP}'>♪ {' · '.join(p['music'].split(' · ')[:2])}</div>" if p.get('music') else ''
    return f"""<div class='left'>
  <div class='eb' style='color:{LIME};font-size:20px'>{d.strftime('%a')} · {d.strftime('%b')} {d.day} · {kind}</div>
  <div class='hd' style='font-size:62px;margin-top:22px'>{p['title']}</div>
  <div class='hd' style='font-size:36px;margin-top:20px;color:{CHAMP}'><i>“{p['hook']}”</i></div>
  <div style='margin-top:30px'>{label_html}</div>{mus}
  {f"<div class='p' style='font-size:22px;margin-top:18px;opacity:.85'>{sub}</div>" if sub else ''}
  <div class='chips' style='margin-top:26px'>{chips}</div></div>"""
def slide(day, phase, p, label, img=None, sub=''):
    return page(timeline(dt.date.fromisoformat(day), phase) + left(day, p, label, sub) + (f"<div class='slot'><img src='{img.as_uri()}'></div>" if img else "<div class='slot'></div>"))
def card(title, kicker, body, foot='', big=False):
    return page(f"""<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 200px'>
  <div style='margin-bottom:46px'>{B.emblem(120) if big else B.logo(True, 56)}</div>
  <div class='eb' style='color:{GOLD};font-size:22px'>{kicker}</div>
  <div class='hd' style='font-size:{92 if big else 80}px;margin-top:26px'>{title}</div>
  <div class='p' style='font-size:30px;margin-top:34px;opacity:.9;max-width:1400px'>{body}</div>
  {f"<div class='p' style='font-size:22px;margin-top:38px;color:{CHAMP};opacity:.85;max-width:1400px'>{foot}</div>" if foot else ''}</div>""")
def bullets(kicker, title, pts, s=11):
    li = ''.join(f"<li style='margin-bottom:22px'>{x}</li>" for x in pts)
    still(page(f"""<div class='top'>{B.logo(True, 40)}<div class='eb' style='color:{GOLD};font-size:18px'>Round 2 review</div></div>
<div style='position:absolute;left:150px;right:150px;top:170px'><div class='eb' style='color:{LIME};font-size:22px'>{kicker}</div>
<div class='hd' style='font-size:80px;margin-top:18px'>{title}</div><ul class='p' style='font-size:31px;line-height:1.38;margin-top:34px;padding-left:34px'>{li}</ul></div>"""), s)

SEGS.append(('full', None, dur(AN/'OUTRO-logo-draw--wide.mp4'), AN/'OUTRO-logo-draw--wide.mp4'))
still(card('The Founding Member campaign · round 2', 'Campaign walkthrough · Nov 18, 2026 – Jan 31, 2027',
           'Every post in calendar order. Motion versions play in place of stills where they are the proposed primary.',
           'Draft for Jeff &amp; Esther. Nothing published or scheduled. Music shown is proposed (3 attached to unpublished Metricool drafts).'), 6)
bullets('What changed', 'Round 2 in one minute', ['“Up to 20% off” on every membership post; exact 15% / 20% kept on product prices.',
        'Mix now 41% membership · 40% product · 19% brand (was 56 / 24 / 20). Hydrate, Iron, D3+K2 and Energy each get a post.',
        'Photoreal holiday scenes with real products; line-art kept only as backups. Coffee bag ~15% smaller.',
        'Gold-leaf logo and emblem moments reserved for membership. January fully built: 22 feed posts, 5 emails, countdown Stories.'], 12)
pieces = [p for p in plan2.P if p['rev'] != 'REMOVED']
def phase_card(ph):
    a, b, name, rng, msg = ph
    n, c = plan2.mix(a.isoformat(), b.isoformat())
    mix = ' · '.join(f"{c[k]} {KIND[k].lower()}" for k in ('member', 'product', 'brand') if c[k])
    still(card(name.split(' · ')[1], f"Phase {name.split(' · ')[0]} · {rng}", msg, f"{n} feed pieces · {mix}"), 5)
cur = None
for p in pieces:
    d = dt.date.fromisoformat(p['date']); ph = phase_of(d)
    if ph is not cur: cur = ph; phase_card(ph)
    phn = ph[2]; pid = p['id']
    lab = {'NEW': 'new', 'REPLACED': 'replaced'}.get(p['rev'], 'ready')
    if p['status'] == 'TEMPLATE' or p['rev'] == 'HOLD':
        still(slide(p['date'], phn, p, pill('hold'), None, p.get('note') or 'Held until approval.'), 3.2); continue
    if p['fmt'] == 'email':
        pngs = sorted(AS.glob(f"{p['asset']}*.png"))
        subj = re.search(r'Subject: "([^"]+)"', p['caption']); sub = f"Subject: “{subj.group(1)}”" if subj else ''
        still(slide(p['date'], phn, p, pill('email'), pngs[0] if pngs else None, sub), 3.0); continue
    vids = [m for m in p['motion'] if (AN/f'{m}.mp4').exists()]
    if p['fmt'] == 'reel':
        path = AN/f"{vids[0]}.mp4" if vids else (AN/f"{p['asset']}.mp4" if (AN/f"{p['asset']}.mp4").exists() else VD/f"{p['asset']}.mp4")
        sub = 'Membership reel: ends on the gold-leaf logo.' if 'outro' in path.name or p['id'].startswith('J24') else ''
        video(slide(p['date'], phn, p, pill(lab), None, sub), path); continue
    if p['status'] == 'MOTION' and vids:
        video(slide(p['date'], phn, p, pill(lab, ' · motion'), None, p.get('note', '')), AN/f'{vids[0]}.mp4'); continue
    pngs = [x for x in sorted(AS.glob(f"{p['asset']}*.png")) if not x.name.startswith('_')]
    if p['fmt'] == 'carousel':
        n = min(len(pngs), 4)
        for i, im in enumerate(pngs[:4]): still(slide(p['date'], phn, p, pill(lab, f' · slide {i+1}/{len(pngs)}'), im), 1.9)
    else:
        for i, im in enumerate(pngs[:1]): still(slide(p['date'], phn, p, pill(lab), im), 3.2)
    for m in vids[:1]:
        video(slide(p['date'], phn, p, pill('motion'), None, 'Same post with motion (proposed).'), AN/f'{m}.mp4')
bullets('Approve before publishing', 'Decisions for Jeff &amp; Esther', ['Approve the round-2 mix and the photoreal holiday direction (line-art = backups only).',
        'Music workflow: Metricool Instagram audio, Claude selects and attaches; confirm tracks in Meta Sound Collection once.',
        'January: approve the team-note voice (J15) and the countdown cadence (Jan 21, 24, 27, 29, 31).',
        'Drop B03R (checkout recording); C18 stays on hold until label panels are verified.',
        'New products: templates only until Restructuring confirms each launch.'], 12)
still(card('Your feedback next', 'End of walkthrough', 'Approve, edit or reject in the gallery; then Claude finalizes captions, prices and Metricool drafts.',
           'Gallery: claude.ai/artifact/6v7zNVF6vBnM4UhyUqMTo3', big=True), 6)
SEGS.append(('full', None, dur(AN/'OUTRO-logo-draw--wide.mp4'), AN/'OUTRO-logo-draw--wide.mp4'))

# ------------------------------------------------------------- render
async def frames():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1920, 'height': 1080})
        for i, (k, html, s, v) in enumerate(SEGS):
            if html is None: continue
            f = FR/f'{i:04d}.html'; f.write_text(html); await pg.goto(f.as_uri())
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(120)
            await pg.screenshot(path=str(FR/f'{i:04d}.png'))
        await b.close()
asyncio.run(frames())

ENC = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-r', '30']
lst = []
for i, (k, html, s, v) in enumerate(SEGS):
    out = SG/f'{i:04d}.mp4'; fo = max(s - .3, 0)
    fade = f"fade=t=in:st=0:d=0.3,fade=t=out:st={fo:.2f}:d=0.3"
    if k == 'still':
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', f'{s:.2f}', '-i', str(FR/f'{i:04d}.png'), '-vf', f'{fade},format=yuv420p', *ENC, str(out)]
    elif k == 'full':  # 4:5 animation centred full-frame on brand green
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', str(v), '-vf', f'{fade},format=yuv420p', *ENC, str(out)]
    else:  # video in the right-hand slot
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', str(FR/f'{i:04d}.png'), '-i', str(v), '-filter_complex',
               f'[1:v]scale=-2:870,setsar=1[a];[0:v][a]overlay=1000+(840-w)/2:105:shortest=1,{fade},format=yuv420p', '-t', f'{s:.2f}', *ENC, str(out)]
    subprocess.run(cmd, check=True); lst.append(f"file '{out}'")
(W/'list.txt').write_text('\n'.join(lst))
final = W/'EverLiv-Campaign-Walkthrough-R2-Nov18-Jan31.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(W/'list.txt'), '-c', 'copy', '-movflags', '+faststart', str(final)], check=True)
print('segments', len(SEGS), 'duration', round(dur(final), 1), 's', final.stat().st_size // 1024 // 1024, 'MB')
