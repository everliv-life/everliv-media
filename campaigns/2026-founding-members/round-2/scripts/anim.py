"""Animated samples: HTML/CSS keyframes -> frame-accurate capture -> MP4.
Logo, emblems and product art are never altered: effects are light passes (masked overlays), opacity and
whole-element motion only. Frames are captured by pausing every animation and seeking currentTime."""
import asyncio, pathlib, subprocess, shutil, sys
from playwright.async_api import async_playwright
import build_assets as B
from build_assets import u, GOLD, CHAMP, LEAF, IVORY, header, logo, emblem, leaf, foot, FINE_M, SIZES

OUT = B.ROOT/'assets'/'anim'; OUT.mkdir(parents=True, exist_ok=True)
FPS = 30

ACSS = f"""
.a{{animation-fill-mode:both;animation-timing-function:cubic-bezier(.22,.7,.2,1)}}
@keyframes up{{from{{opacity:0;transform:translateY(28px)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes grow{{from{{opacity:0;transform:scale(.86)}}to{{opacity:1;transform:none}}}}
@keyframes rule{{from{{width:0}}to{{width:84px}}}}
/* foil light pass, masked to the gold artwork so only existing gold catches light */
.sheen{{position:absolute;inset:0;pointer-events:none;mix-blend-mode:screen;
  background:linear-gradient(105deg,transparent 0%,transparent 40%,rgba(255,246,214,0) 41%,rgba(255,246,214,var(--a,.55)) 50%,rgba(255,246,214,0) 59%,transparent 60%,transparent 100%);
  background-size:300% 100%;background-repeat:no-repeat}}
@keyframes sweep{{0%{{background-position:120% 0}}100%{{background-position:-20% 0}}}}
.glint{{position:absolute;width:76px;height:76px;margin:-38px 0 0 -38px;pointer-events:none;opacity:0}}
.glint:before,.glint:after{{content:'';position:absolute;left:50%;top:50%;background:radial-gradient(closest-side,#FFF8E2,rgba(255,248,226,0));transform:translate(-50%,-50%)}}
.glint:before{{width:76px;height:4px}} .glint:after{{width:4px;height:76px}}
.glint i{{position:absolute;left:50%;top:50%;width:18px;height:18px;margin:-9px;border-radius:50%;background:radial-gradient(#FFFBEF,rgba(255,240,200,0))}}
@keyframes tw{{0%{{opacity:0;transform:scale(.3) rotate(0)}}40%{{opacity:1;transform:scale(1) rotate(20deg)}}100%{{opacity:0;transform:scale(.4) rotate(45deg)}}}}
@keyframes tilt{{0%{{transform:perspective(1600px) rotateY(-16deg) rotateX(6deg) rotate(-4deg)}}50%{{transform:perspective(1600px) rotateY(10deg) rotateX(-3deg) rotate(-4deg)}}100%{{transform:perspective(1600px) rotateY(-16deg) rotateX(6deg) rotate(-4deg)}}}}
@keyframes drift{{from{{transform:scale(1)}}to{{transform:scale(1.035)}}}}
@keyframes dim{{from{{opacity:1}}to{{opacity:.45}}}}
@keyframes lineIn{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
"""
def A(name, dur, delay, extra=''):  # animation shorthand
    return f"animation:{name} {dur}s {delay}s both{(' ' + extra) if extra else ''}"

def glint(x, y, delay, dur=1.1):
    return f"<div class='glint' style='left:{x}px;top:{y}px;{A('tw', dur, delay, 'ease-in-out')}'><i></i></div>"

def masked_sheen(svg, delay, dur=1.6):
    m = u(svg)
    return (f"<div class='sheen' style='-webkit-mask:url({m}) center/contain no-repeat;mask:url({m}) center/contain no-repeat;"
            f"{A('sweep', dur, delay, 'ease-in-out')}'></div>")

def emblem_fx(size, sheen_at, cls_anim=''):
    return (f"<div style='position:relative;width:{size}px;height:{size}px;{cls_anim}'>{emblem(size)}"
            f"{masked_sheen('everliv-member-mark-gold-circle-leaf.svg', sheen_at)}</div>")

S = {}
# 1 — Teaser with foil shimmer (A01 feed, 7 s)
S['ANIM-1-teaser-foil-shimmer'] = ('feed', 'green', 7.0, f"""
<div style='{A('fade', .8, 0)}'>{header(True, member=False)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:56px;position:relative'>
  {emblem_fx(150, 2.2, A('grow', 1.2, .3))}
  <div class='hd' style='font-size:92px'>
    <div style='{A('up', .9, 1.0)}'>Something new is</div>
    <div style='{A('up', .9, 1.35)}'><i>taking shape</i> at EverLiv.</div></div>
  <div style='height:2px;display:flex;justify-content:center'><div class='rule' style='{A('rule', .8, 2.0)}'></div></div>
  <div class='p' style='font-size:32px;opacity:.85;{A('fade', .9, 2.6)}'>A little gold. A lot more to discover.</div>
  {glint(812, 92, 3.7)}{glint(380, 655, 4.5, 1.0)}
</div>
<div class='eb' style='text-align:center;color:{GOLD};font-size:22px;{A('fade', .8, 3.2)}'>More on Monday</div>""")

# 2 — Founding Member card tilt + light pass (A05 s1, 8 s)
CARD = f"""<div class='card' style='transform-origin:center;{A('tilt', 8, 0, 'ease-in-out')}'>
      <div class='row'>{logo(True,38)}<div class='club'>{leaf(24)}Member Price Club</div></div>
      <div class='fm'>Founding Member</div><div class='ln'></div><div class='meta'><span>12 months</span><span>Paid once</span></div>
      <div class='sheen' style='--a:.28;border-radius:30px;{A('sweep', 1.8, 1.6, 'ease-in-out')}'></div>
      <div class='sheen' style='--a:.28;border-radius:30px;{A('sweep', 1.8, 5.4, 'ease-in-out')}'></div></div>"""
S['ANIM-2-card-tilt'] = ('feed', 'ivory', 8.0, f"""{header(False)}
<div class='mid' style='gap:36px;position:relative'>
  <div class='eb' style='color:#9C7A3A;{A('fade', .7, .1)}'>How it works</div>
  <div class='hd' style='font-size:98px;color:{LEAF}'>
    <div style='{A('up', .9, .3)}'>One payment.</div>
    <div style='{A('up', .9, .6)}'><i>Twelve months</i> of</div>
    <div style='{A('up', .9, .9)}'>member pricing.</div></div>
  <div style='margin-top:30px;display:flex;justify-content:center;{A('grow', 1.1, 1.0)}'><div style='transform:scale(.92)'>{CARD}</div></div>
  {glint(250, 735, 2.6)}{glint(860, 1010, 6.2, 1.0)}
</div><div class='eb' style='font-size:20px;color:#3E5B41;{A('fade', .8, 2)}'>Swipe →</div>""")

# 3 — Price moment: price to join vs membership length kept visibly separate (no strike-through, no timeline)
S['ANIM-3-price-to-join'] = ('feed', 'green', 8.0, f"""
<div style='{A('fade', .6, 0)}'>{header(True)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:30px;position:relative'>
  <div class='eb' style='color:{GOLD};{A('fade', .7, .3)}'>Founding price to join</div>
  <div style='position:relative;{A('grow', 1.1, .7)}'>
    <div class='hd' style='font-size:230px;line-height:1;color:{IVORY}'>$49.99</div>
    <div class='hd sheen' style='position:absolute;inset:0;font-size:230px;line-height:1;--a:.9;-webkit-background-clip:text;background-clip:text;color:transparent;{A('sweep', 1.7, 2.0, 'ease-in-out')}'>$49.99</div>
    {glint(540, 26, 2.9)}</div>
  <div class='p' style='font-size:40px;line-height:1.35;{A('up', .8, 1.5)}'>Paid once. Member pricing on <b>every eligible order</b><br>for <b>12 full months</b>, as often as you shop.</div>
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:22px;width:880px;margin-top:22px'>
   <div style='border:1.5px solid {GOLD};border-radius:24px;padding:26px;{A('up', .7, 3.4)}'><div class='eb' style='font-size:19px;color:{GOLD}'>Join by Jan 31, 2027</div><div class='hd' style='font-size:64px;color:{CHAMP};margin-top:8px'>$49.99</div></div>
   <div style='border:1.5px solid rgba(233,228,223,.3);border-radius:24px;padding:26px;{A('up', .7, 3.8)};opacity:.7'><div class='eb' style='font-size:19px'>Join from Feb 1, 2027</div><div class='hd' style='font-size:64px;margin-top:8px'>$69.99</div></div></div>
  <div class='p' style='font-size:34px;color:{CHAMP};{A('fade', .8, 4.6)}'>Either way, your membership lasts a full 12 months.</div>
</div>
<div style='{A('fade', .8, 5.4)}'>{foot(FINE_M, 'center')}</div>""")

async def capture(only=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page()
        for name, (fmt, cls, dur, body) in S.items():
            if only and not any(name.startswith(o) for o in only): continue
            w, h, _ = SIZES[fmt]; fr = OUT/f'_{name}'; shutil.rmtree(fr, ignore_errors=True); fr.mkdir()
            html = B.page(fmt, cls, body).replace('</style>', ACSS + '</style>')
            hp = OUT/f'{name}.html'; hp.write_text(html)
            await pg.set_viewport_size({'width': w, 'height': h}); await pg.goto(hp.as_uri())
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            n = int(dur*FPS)
            for i in range(n):
                t = i*1000/FPS
                await pg.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={t}}})")
                await pg.screenshot(path=str(fr/f'{i:04d}.png'))
            mp4 = OUT/f'{name}.mp4'
            subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',str(fr/'%04d.png'),
                            '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)], check=True)
            # poster = final frame
            shutil.copy(fr/f'{n-1:04d}.png', OUT/f'{name}--last.png'); shutil.copy(fr/f'{int(n*.4):04d}.png', OUT/f'{name}--mid.png')
            print(name, mp4.stat().st_size//1024, 'KB')
        await b.close()
if __name__ == '__main__':
    asyncio.run(capture(sys.argv[1:] or None))
