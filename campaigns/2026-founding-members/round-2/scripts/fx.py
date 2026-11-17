"""EverLiv animation pack v1. Brand art is never redrawn: the logo 'draw' traces the original paths and settles on
the exact original fill; shimmer, ring light and pulse are masked light passes over the original artwork.
Holiday line art (wreath, stocking, train, leaves, snow, steam) is original, drawn here in brand gold."""
import asyncio, math, random, shutil, subprocess, sys, re
from playwright.async_api import async_playwright
import build_assets as B
from build_assets import u, S as SRC, GOLD, CHAMP, LEAF, IVORY, PAGE, INK, LIME, header, logo, emblem, leaf, foot, FINE_S, AI, SIZES
from anim import ACSS, A, glint

OUT = B.ROOT/'assets'/'anim'; OUT.mkdir(parents=True, exist_ok=True)
FPS = 30
random.seed(7)

XCSS = """
@keyframes dr{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes fi{from{fill-opacity:0}to{fill-opacity:1}}
@keyframes so{from{stroke-opacity:1}to{stroke-opacity:0}}
@keyframes rot{from{transform:rotate(0)}to{transform:rotate(360deg)}}
@keyframes sweepR{0%{background-position:-20% 0}100%{background-position:120% 0}}
@keyframes fall{from{transform:translate3d(0,-60px,0)}to{transform:translate3d(var(--dx),calc(var(--h) + 60px),0)}}
@keyframes leaffall{0%{transform:translate(0,-120px) rotate(0)}100%{transform:translate(var(--dx),calc(var(--h) + 120px)) rotate(var(--r))}}
@keyframes steam{0%{opacity:0;transform:translateY(0) scaleX(1)}25%{opacity:var(--o)}70%{opacity:calc(var(--o) * .6)}100%{opacity:0;transform:translateY(-300px) scaleX(1.5)}}
@keyframes twk{0%,100%{opacity:.15}50%{opacity:.85}}
@keyframes push{from{transform:scale(1)}to{transform:scale(1.06)}}
@keyframes pop{0%{transform:scale(0)}70%{transform:scale(1.25)}100%{transform:scale(1)}}
@keyframes drop{0%{opacity:0;transform:translateY(-140px)}60%{opacity:1;transform:translateY(16px)}80%{transform:translateY(-6px)}100%{opacity:1;transform:none}}
@keyframes roll{from{transform:translateX(-1350px)}to{transform:translateX(0)}}
@keyframes puff{0%{opacity:0;transform:translate(0,0) scale(.4)}20%{opacity:.8}100%{opacity:0;transform:translate(-90px,-150px) scale(1.8)}}
@keyframes slidein{from{opacity:0;transform:translateX(80px)}to{opacity:1;transform:none}}
.ld path{stroke-dasharray:1 1;stroke-dashoffset:1;fill-opacity:0}
.la{fill:none;stroke-linecap:round;stroke-linejoin:round}
"""

def masked(maskfile, anim, extra='', grad=None):
    m = u(maskfile)
    g = grad or "linear-gradient(105deg,transparent 41%,rgba(255,246,214,var(--a,.85)) 50%,transparent 59%)"
    return (f"<div style='position:absolute;inset:0;pointer-events:none;mix-blend-mode:screen;background:{g};background-size:300% 100%;"
            f"background-repeat:no-repeat;-webkit-mask:url({m}) center/contain no-repeat;mask:url({m}) center/contain no-repeat;{anim};{extra}'></div>")

LOGO_VB = (1416.0, 488.7)
def logo_draw(white, w, t0, stroke=GOLD, shimmer=True, dur=1.5):
    """Trace the original logo paths, settle on the original fill, then a gold light passes through the leaf."""
    svg = (SRC/('everliv-logo-white.svg' if white else 'everliv-logo.svg')).read_text()
    svg = re.sub(r'<\?xml[^>]*>', '', svg)
    i = [0]
    def addp(m):
        k = i[0]; i[0] += 1; d = t0 + k*0.09
        return (f"<path pathLength='1' style='stroke:{stroke};stroke-width:3.2;"
                f"animation:dr {dur}s {d:.2f}s both cubic-bezier(.5,.1,.3,1),fi .8s {d+dur*.75:.2f}s both,so .7s {d+dur:.2f}s both' ")
    svg = re.sub(r'<path ', addp, svg)
    svg = svg.replace('<svg ', f"<svg class='ld' style='width:{w}px;height:{w*LOGO_VB[1]/LOGO_VB[0]:.1f}px;display:block;overflow:visible' ", 1)
    h = w*LOGO_VB[1]/LOGO_VB[0]
    sh = ''
    if shimmer:
        ts = t0 + 0.09*10 + dur + .6
        if white:  # white artwork: a gold light passes through it (multiply = gold on white)
            gg = "linear-gradient(105deg,transparent 36%,rgba(201,170,105,.95) 50%,transparent 64%)"
            sh = (masked('_mask-logo-leaf.svg', A('sweep', 1.6, ts, 'ease-in-out'), 'mix-blend-mode:multiply', gg) +
                  masked('_mask-logo-beat.svg', A('sweepR', 1.3, ts + .25, 'ease-in-out'), 'mix-blend-mode:multiply', gg))
        else:
            sh = (masked('_mask-logo-leaf.svg', A('sweep', 1.4, ts, 'ease-in-out'), "--a:.95") +
                  masked('_mask-logo-beat.svg', A('sweepR', 1.1, ts + .2, 'ease-in-out'), "--a:.7"))
        sh += (
              glint(int(w*0.665), int(h*0.13), ts + .7, 1.0))
    return f"<div style='position:relative;width:{w}px;height:{h:.0f}px'>{svg}{sh}</div>"

def emblem_live(size, t_ring=1.0, t_beat=1.6, t_leaf=2.3, ring_dur=2.6, loop_ring=False):
    """Original emblem + light orbiting the gold ring + pulse along the heartbeat + light through the leaf."""
    ring_anim = f"animation:rot {ring_dur}s {t_ring}s {'infinite' if loop_ring else '1'} linear both"
    ring = (f"<div style='position:absolute;inset:0;-webkit-mask:url({u('_mask-emblem-ring.svg')}) center/contain no-repeat;"
            f"mask:url({u('_mask-emblem-ring.svg')}) center/contain no-repeat;mix-blend-mode:screen'>"
            f"<div style='position:absolute;inset:-2px;border-radius:50%;background:conic-gradient(from 0deg,transparent 0 290deg,rgba(255,246,214,.15) 310deg,rgba(255,250,232,1) 352deg,transparent 360deg);{ring_anim}'></div></div>")
    return (f"<div style='position:relative;width:{size}px;height:{size}px'>{emblem(size)}{ring}"
            f"{masked('_mask-emblem-beat.svg', A('sweepR', 1.2, t_beat, 'ease-in-out'), '--a:.9')}"
            f"{masked('_mask-emblem-leaf.svg', A('sweep', 1.3, t_leaf, 'ease-in-out'), '--a:.9')}</div>")

def snow(w, h, n=70, color='255,255,255', op=.85):
    out = []
    for _ in range(n):
        x = random.uniform(0, w); s = random.uniform(4, 13); d = random.uniform(6, 13)
        out.append(f"<i style='position:absolute;left:{x:.0f}px;top:0;width:{s:.1f}px;height:{s:.1f}px;border-radius:50%;"
                   f"background:radial-gradient(rgba({color},{op}),rgba({color},0) 70%);--dx:{random.uniform(-80,80):.0f}px;--h:{h}px;"
                   f"animation:fall {d:.1f}s {-random.uniform(0,d):.1f}s infinite linear'></i>")
    return f"<div style='position:absolute;inset:0;pointer-events:none;overflow:hidden'>{''.join(out)}</div>"

LEAF_ART = "M0,-46 C26,-30 30,10 0,46 C-30,10 -26,-30 0,-46 Z M0,-40 L0,52 M0,-12 L14,-24 M0,6 L-15,-6 M0,22 L13,10"
def falling_leaves(w, h, n=16, color=GOLD):
    out = []
    for _ in range(n):
        x = random.uniform(-40, w); sc = random.uniform(.6, 1.3); d = random.uniform(7, 12)
        out.append(f"<svg viewBox='-40 -60 80 120' style='position:absolute;left:{x:.0f}px;top:0;width:{56*sc:.0f}px;overflow:visible;"
                   f"--dx:{random.uniform(-160,160):.0f}px;--h:{h}px;--r:{random.choice([-1,1])*random.uniform(180,420):.0f}deg;"
                   f"animation:leaffall {d:.1f}s {-random.uniform(0,d):.1f}s infinite linear'>"
                   f"<path class='la' d='{LEAF_ART}' stroke='{color}' stroke-width='3' opacity='.75'/></svg>")
    return f"<div style='position:absolute;inset:0;pointer-events:none;overflow:hidden'>{''.join(out)}</div>"

def steam(x, y, n=4, o=.42):
    paths = ["M0,0 C-30,-60 30,-110 0,-170 C-28,-225 22,-260 0,-320", "M0,0 C25,-50 -25,-115 5,-175 C30,-230 -15,-270 6,-330",
             "M0,0 C-18,-70 28,-120 -4,-180 C-30,-240 14,-280 -6,-320"]
    out = []
    for k in range(n):
        d = 4.2; p = paths[k % 3]
        out.append(f"<svg viewBox='-60 -340 120 350' style='position:absolute;left:{x - 60 + (k-1.5)*26:.0f}px;top:{y-340}px;width:120px;height:350px;overflow:visible;"
                   f"filter:blur(7px);--o:{o};animation:steam {d}s {-k*d/n:.2f}s infinite ease-out'>"
                   f"<path d='{p}' fill='none' stroke='rgba(255,252,245,1)' stroke-width='16' stroke-linecap='round'/></svg>")
    return ''.join(out)

def twinkles(pts, size=46):
    return ''.join(f"<i style='position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;margin:-{size//2}px;border-radius:50%;"
                   f"background:radial-gradient(rgba(255,226,160,.9),rgba(255,210,130,0) 70%);mix-blend-mode:screen;"
                   f"animation:twk {random.uniform(1.6,2.8):.1f}s {-random.uniform(0,2):.1f}s infinite ease-in-out'></i>" for x, y in pts)

def wreath(size, t0, color=GOLD):
    c = size/2; R = size*0.40; n = 30; parts = []
    for k in range(n):
        a = 2*math.pi*k/n; x = c + R*math.cos(a); y = c + R*math.sin(a); rot = math.degrees(a) + (55 if k % 2 else -55)
        parts.append(f"<path class='la' pathLength='1' d='M0,-26 C14,-14 14,10 0,26 C-14,10 -14,-14 0,-26 Z M0,-20 L0,22' transform='translate({x:.1f},{y:.1f}) rotate({rot:.0f})' "
                     f"stroke='{color}' stroke-width='2.6' style='stroke-dasharray:1 1;animation:dr .9s {t0 + k*0.05:.2f}s both'/>")
    berries = ''.join(f"<circle cx='{c + (R+4)*math.cos(2*math.pi*k/10 + .3):.1f}' cy='{c + (R+4)*math.sin(2*math.pi*k/10 + .3):.1f}' r='7' fill='{CHAMP}' "
                      f"style='transform-box:fill-box;transform-origin:center;animation:pop .5s {t0 + 1.7 + k*.07:.2f}s both'/>" for k in range(10))
    bow = (f"<path class='la' pathLength='1' d='M{c},{c+R} c-40,-34 -84,-8 -60,24 c14,18 44,4 60,-24 c40,-34 84,-8 60,24 c-14,18 -44,4 -60,-24 l-34,70 m34,-70 l34,70' "
           f"stroke='{color}' stroke-width='3' style='stroke-dasharray:1 1;animation:dr 1.2s {t0 + 1.4:.2f}s both'/>")
    return f"<svg viewBox='0 0 {size} {size}' style='position:absolute;inset:0;width:{size}px;height:{size}px;overflow:visible'>{''.join(parts)}{berries}{bow}</svg>"

def stocking(w, t0, color=GOLD):
    d = ("M60,20 L200,20 L200,60 L196,300 C196,330 210,350 250,372 C300,398 330,430 314,476 C296,526 230,530 190,500 "
         "L80,420 C52,398 50,380 52,350 L60,60 Z M60,20 L200,20 L200,60 L60,60 Z")
    cuff = "M54,16 L206,16 L206,66 L54,66 Z"
    return (f"<svg viewBox='0 0 380 560' style='width:{w}px;overflow:visible'>"
            f"<path class='la' pathLength='1' d='{d}' stroke='{color}' stroke-width='4' style='stroke-dasharray:1 1;animation:dr 2.2s {t0}s both ease-in-out'/>"
            f"<path class='la' pathLength='1' d='{cuff}' stroke='{color}' stroke-width='4' style='stroke-dasharray:1 1;animation:dr 1s {t0+1.6}s both'/>"
            + ''.join(f"<circle cx='{70 + k*22}' cy='41' r='4' fill='{CHAMP}' style='transform-box:fill-box;transform-origin:center;animation:pop .4s {t0+2.2+k*.05:.2f}s both'/>" for k in range(7))
            + "</svg>")

def train(t0, tins):
    """Gold line-art train; each car carries an unaltered tin cut from the approved four-tin image."""
    wheel = lambda x: (f"<g transform='translate({x},250)'><g style='transform-box:fill-box;transform-origin:center;animation:rot 1.1s {t0}s 4 linear both'>"
                       f"<circle r='26' class='la' stroke='{GOLD}' stroke-width='4'/><path d='M-26,0 L26,0 M0,-26 L0,26' stroke='{GOLD}' stroke-width='3'/></g></g>")
    eng = (f"<path class='la' stroke='{GOLD}' stroke-width='4' d='M20,230 L20,120 L120,120 L120,60 L200,60 L200,120 L250,120 L250,230 Z M140,60 L140,20 L180,20 L180,60 M250,200 L290,230 M20,230 L290,230'/>"
           + wheel(70) + wheel(200))
    cars = ''
    for k, t in enumerate(tins):
        x0 = 320 + k*230
        cars += (f"<path class='la' stroke='{GOLD}' stroke-width='4' d='M{x0},230 L{x0},150 L{x0+200},150 L{x0+200},230 Z M{x0-30},215 L{x0},215'/>"
                 + wheel(x0+50) + wheel(x0+150) +
                 f"<image href='{u(f'tin-{t}--cutout.png')}' x='{x0+12}' y='18' width='176' height='194'/>")
    puffs = ''.join(f"<circle cx='160' cy='10' r='26' fill='rgba(233,228,223,.55)' style='transform-box:fill-box;transform-origin:center;animation:puff 1.6s {t0 + k*.4:.1f}s infinite ease-out'/>" for k in range(4))
    return (f"<svg viewBox='0 -160 1260 440' style='width:1000px;overflow:visible'><g style='animation:roll 3.6s {t0}s both cubic-bezier(.2,.7,.2,1)'>{puffs}{eng}{cars}</g>"
            f"<path d='M-40,282 L1300,282' stroke='{GOLD}' stroke-width='3' opacity='.6'/></svg>")

def mistletoe(w, t0):
    leaves = [("M200,30 C150,40 120,80 110,130", 1), ("M200,30 C250,40 280,80 290,130", 1)]
    lv = lambda x, y, r: (f"<path class='la' pathLength='1' d='M0,0 C18,-14 46,-12 62,0 C46,12 18,14 0,0 Z' transform='translate({x},{y}) rotate({r})' stroke='{GOLD}' stroke-width='3' "
                          f"style='stroke-dasharray:1 1;animation:dr .8s {t0+.6:.1f}s both'/>")
    body = ''.join(f"<path class='la' pathLength='1' d='{d}' stroke='{GOLD}' stroke-width='3.5' style='stroke-dasharray:1 1;animation:dr 1.2s {t0}s both'/>" for d, _ in leaves)
    body += lv(110, 130, 120) + lv(110, 130, 200) + lv(290, 130, 60) + lv(290, 130, -20) + lv(200, 30, 90)
    body += ''.join(f"<circle cx='{x}' cy='{y}' r='9' fill='{IVORY}' style='transform-box:fill-box;transform-origin:center;animation:pop .45s {t0+1.4+k*.12:.2f}s both'/>"
                    for k, (x, y) in enumerate([(104, 142), (122, 150), (296, 142), (278, 150)]))
    body += f"<path d='M200,-60 L200,30' stroke='{GOLD}' stroke-width='2' opacity='.7' pathLength='1' style='stroke-dasharray:1 1;animation:dr .6s {t0-.4:.1f}s both'/>"
    return f"<svg viewBox='60 -60 280 240' style='width:{w}px;overflow:visible'>{body}</svg>"

def heartbeat_line(w, t0, color=GOLD):
    d = "M0,40 L260,40 L290,40 L310,4 L336,78 L360,22 L378,40 L640,40"
    return (f"<svg viewBox='0 0 640 80' style='width:{w}px;overflow:visible'><path class='la' pathLength='1' d='{d}' stroke='{color}' stroke-width='4' "
            f"style='stroke-dasharray:1 1;animation:dr 1.4s {t0}s both ease-in-out'/>"
            f"<circle cx='640' cy='40' r='9' fill='{color}' style='transform-box:fill-box;transform-origin:center;animation:pop .5s {t0+1.35:.2f}s both'/></svg>")

def sign_off(white, t0, w=420):
    return f"<div style='display:flex;justify-content:center'>{logo_draw(white, w, t0)}</div>"

PRICE_NOTE = "Live everliv.life prices Nov 16, 2026; may change. Member price requires an active membership. "

# ------------------------------------------------------------------ pieces
P = {}
# 0 · Reusable sign-off (append to reels / end of posts)
for fmt, cls, white in [('story', 'green', True), ('feed', 'green', True), ('feed', 'ivory', False)]:
    P[f'OUTRO-logo-draw--{cls}-{fmt}'] = (fmt, cls, 4.6, f"""<div></div>
<div class='mid' style='align-items:center;gap:40px'>{logo_draw(white, 760, .3)}
<div class='eb' style='color:{GOLD if white else '#9C7A3A'};{A('fade', .8, 3.3)}'>everliv.life</div></div><div></div>""")

# A04 · Reveal: ring light orbits, heartbeat pulses, leaf lights up
P['A04-reveal--animated'] = ('feed', 'green', 8.0, f"""<div style='{A('fade', .6, 0)}'>{header(True, member=False)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:38px'>
  <div style='{A('grow', 1.0, .2)}'>{emblem_live(190, 1.0, 2.0, 2.8)}</div>
  <div class='eb' style='color:{GOLD};{A('fade', .7, 1.2)}'>Introducing the Member Price Club</div>
  <div class='hd' style='font-size:104px'><div style='{A('up', .9, 1.6)}'>Become a</div><div style='{A('up', .9, 1.9)}'><i>Founding Member.</i></div></div>
  <div class='p' style='font-size:34px;{A('fade', .8, 3.0)}'>One $49.99 payment. Member pricing on every eligible<br>order for 12 months, as often as you shop.</div>
</div><div style='{A('fade', .8, 3.8)}'>{foot(B.FINE_M, 'center')}</div>""")

# Member price highlights
def price_piece(img, name, every, member, rate, extra_fine=''):
    return ('feed', 'ivory', 8.0, f"""<div style='{A('fade', .5, 0)}'>{header(False)}</div>
<div class='mid' style='gap:30px'>
  <div class='row' style='align-items:center;gap:40px'>
    <div class='tile' style='width:470px;height:470px;{A('grow', 1.0, .2)}'><img src='{u(img)}'></div>
    <div style='flex:1'>
      <div class='eb' style='color:#9C7A3A;{A('fade', .6, .6)}'>Member price</div>
      <div class='hd' style='font-size:64px;color:{LEAF};margin-top:14px;{A('up', .8, .8)}'>{name}</div>
      <div style='margin-top:30px;{A('fade', .7, 1.4)}'><div class='eb' style='font-size:19px;color:{MUTED}'>Everyday</div><div class='hd' style='font-size:58px;color:{MUTED}'>{every}</div></div>
    </div></div>
  <div style='display:flex;align-items:center;gap:26px'>{heartbeat_line(560, 2.0)}
    <div style='position:relative;{A('grow', .8, 3.2)}'>
      <div style='display:flex;align-items:center;gap:18px;background:{LEAF};border:1.5px solid {GOLD};border-radius:26px;padding:22px 30px'>
        {emblem_live(84, 3.6, 4.1, 4.6)}<div><div class='eb' style='font-size:17px;color:{CHAMP};white-space:nowrap'>Member · {rate} off</div>
        <div class='hd' style='font-size:76px;color:{IVORY}'>{member}</div></div></div>
      {glint(330, 22, 5.0)}</div></div>
  <div class='p' style='font-size:30px;{A('fade', .7, 4.4)}'>Every eligible order, for 12 months. Shop as often as you like.</div>
</div><div style='{A('fade', .7, 4.8)}'>{foot(PRICE_NOTE + FINE_S + extra_fine)}</div>""")
MUTED = B.MUTED
P['PRICE-nad'] = price_piece('everliv-nad.jpg', 'NAD+', '$59.99', '$47.99', '20%')
P['PRICE-creatine'] = price_piece('everliv-pure-creatine-monohydrate.jpg', 'Pure Creatine<br>Monohydrate', '$34.99', '$29.74', '15%')
P['PRICE-energy'] = price_piece('energy-strips--front.jpg', 'Energy<br>Oral Strips', '$34.99', '$27.99', '20%', ' Contains caffeine; see product page for warnings.')

# Coffee: steam, twinkling lights, slow push-in
def coffee(img, eb, hd):
    return ('feed', 'green', 8.0, f"""<div style='position:absolute;inset:0;overflow:hidden'>
  <div style='position:absolute;inset:0;transform-origin:22% 70%;{A('push', 8, 0, 'linear')}'>
    <img src='{u(img)}' style='width:100%;height:100%;object-fit:cover'>
    {twinkles([(150,130),(260,190),(420,120),(560,210),(700,150),(860,200),(980,120),(330,90),(780,95)])}
    {steam(232, 905)}</div>
  <div style='position:absolute;left:0;right:0;top:0;height:520px;background:linear-gradient(rgba(20,30,20,.62),rgba(20,30,20,0))'></div><div style='position:absolute;left:0;right:0;bottom:0;height:200px;background:linear-gradient(rgba(20,30,20,0),rgba(20,30,20,.75))'></div></div>
<div style='position:relative'>{logo(True, 46)}</div>
<div style='position:relative;margin-top:40px'>
  <div class='eb' style='color:{CHAMP};{A('fade', .7, .6)}'>{eb}</div>
  <div class='hd' style='font-size:92px;margin-top:16px;{A('up', 1.0, 1.0)}'>{hd}</div></div>
<div style='position:relative;color:{IVORY};{A('fade', .8, 2.4)}'>{foot(AI + ' Free U.S. shipping on every order.')}</div>""")
P['COFFEE-cocoa-steam'] = coffee('everliv-cocoa-coffee--holiday-kitchen--social-1080x1350.png', 'Cocoa · medium roast', 'Cozy season,<br><i>brewed.</i>')
P['COFFEE-caramel-steam'] = coffee('everliv-caramel-coffee--holiday-kitchen--social-1080x1350.png', 'Caramel · dark roast', 'Pour. Sip.<br><i>Slow down.</i>')

# Thanksgiving
P['A07-thanksgiving--animated'] = ('feed', 'ivory', 8.0, f"""{falling_leaves(1080, 1350)}
<div style='position:relative;{A('fade', .6, 0)}'>{header(False, member=False)}</div>
<div class='mid' style='position:relative;align-items:center;text-align:center;gap:40px'>
  <div class='hd' style='font-size:150px;color:{LEAF};{A('up', 1.0, .5)}'>Thank <i>you.</i></div>
  <div style='height:2px;display:flex;justify-content:center'><div class='rule' style='{A('rule', .8, 1.4)}'></div></div>
  <div class='p' style='font-size:36px;{A('fade', .9, 1.9)}'>To everyone who tried a strip, brewed a cup or<br>built a routine with us this year.</div></div>
<div style='position:relative'><div class='eb' style='text-align:center;color:#9C7A3A;font-size:20px;margin-bottom:22px;{A('fade', .6, 3.0)}'>Happy Thanksgiving from</div>{sign_off(False, 3.2, 360)}</div>""")

# Christmas: wreath greeting
P['D04-holiday-greeting--animated'] = ('feed', 'green', 9.0, f"""{snow(1080, 1350)}
<div style='position:relative'></div>
<div class='mid' style='position:relative;align-items:center;text-align:center;gap:44px'>
  <div style='position:relative;width:420px;height:420px;display:flex;align-items:center;justify-content:center'>{wreath(420, .3)}
    <div style='{A('grow', 1.0, 1.6)}'>{emblem_live(170, 2.6, 3.4, 4.0)}</div></div>
  <div class='hd' style='font-size:110px'><div style='{A('up', .9, 2.4)}'>Happy <i>holidays.</i></div></div>
  <div class='p' style='font-size:34px;opacity:.9;{A('fade', .9, 3.2)}'>Wishing you a calm, warm and well-rested season.</div></div>
<div style='position:relative'>{sign_off(True, 4.6, 360)}</div>""")

# Stocking stuffers
TINS = ['energy', 'hydrate', 'iron', 'd3k2']
P['C05-stocking-stuffer--animated'] = ('feed', 'green', 8.5, f"""{snow(1080, 1350, 45)}
<div style='position:relative'>{header(True, member=False)}</div>
<div style='position:relative;display:grid;grid-template-columns:1fr 250px;gap:10px;align-items:center'>
  <div><div class='eb' style='color:{LIME};{A('fade', .6, .2)}'>Stocking stuffers</div>
    <div class='hd' style='font-size:70px;white-space:nowrap;margin-top:20px;{A('up', .9, .5)}'>The stocking stuffer<br>that fits <i>in a pocket.</i></div>
    <div style='display:grid;grid-template-columns:repeat(2,190px);gap:18px;margin-top:40px'>
      {''.join(f"<img src='{u(f'tin-{t}--cutout.png')}' style='width:190px;{A('drop', .9, 2.6 + k*.3)}'>" for k, t in enumerate(TINS))}</div></div>
  <div style='position:relative'>{stocking(250, .6)}{glint(84, 22, 3.4)}</div></div>
<div style='position:relative;{A('fade', .7, 4.2)}'><div class='p' style='font-size:30px;margin-bottom:14px'>30 strips per tin, $34.99 · Any 3 for $79.99</div>
{foot('Energy Strips contain caffeine; see product pages for warnings. Build Your Own Bundle has its own pricing (no member price).')}</div>""")

# Train
P['C13-gift-train--animated'] = ('feed', 'green', 8.5, f"""{snow(1080, 1350, 40)}
<div style='position:relative'>{header(True, member=False)}</div>
<div class='mid' style='position:relative;gap:60px'>
  <div><div class='eb' style='color:{LIME};{A('fade', .6, .2)}'>All aboard</div>
  <div class='hd' style='font-size:96px;margin-top:18px;{A('up', .9, .4)}'>Gifts that <i>travel well.</i></div></div>
  <div style='margin-left:-20px'>{train(1.0, TINS)}</div>
  <div class='p' style='font-size:32px;{A('fade', .8, 4.4)}'>Free U.S. shipping · orders processed in 1–3 business days.<br>Order early for the holidays.</div></div>
<div style='position:relative;{A('fade', .7, 4.8)}'>{foot('Delivery times are estimates and not guaranteed. Energy Strips contain caffeine; see product pages for warnings.')}</div>""")

# Mistletoe over the card (gift yourself)
CARD = B.card(-4, .9).replace("<div class='card'", "<div class='card' style='overflow:hidden'", 1)
P['C17-mistletoe-card--animated'] = ('feed', 'green', 8.0, f"""{snow(1080, 1350, 35)}
<div style='position:relative'>{header(True)}</div>
<div class='mid' style='position:relative;gap:30px'>
  <div style='display:flex;justify-content:center;margin-top:-40px'>{mistletoe(300, .4)}</div>
  <div class='eb' style='color:{GOLD};{A('fade', .6, 1.4)}'>For you, this time</div>
  <div class='hd' style='font-size:86px'><div style='{A('up', .9, 1.7)}'>Done shopping for</div><div style='{A('up', .9, 2.0)}'>everyone else?</div><div style='{A('up', .9, 2.4)}'><i>This one's yours.</i></div></div>
  <div style='position:relative;{A('grow', 1.0, 3.0)}'><div style='{A('tilt', 6, 3.0, 'ease-in-out')}'>{B.card(0, .9)}</div>
    <div class='sheen' style='--a:.3;{A('sweep', 1.8, 4.4, 'ease-in-out')}'></div></div></div>
<div style='position:relative;{A('fade', .7, 4.2)}'>{foot(B.FINE_M)}</div>""")


# ---------------- Holiday illustration set (Gemini line art, scene only; real products placed unaltered)
HX = """
@keyframes wipeL{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes wipeU{from{clip-path:inset(100% 0 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes wipeD{from{clip-path:inset(0 0 100% 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes fly{0%{transform:translate(-1150px,420px) rotate(-6deg)}70%{transform:translate(40px,-20px) rotate(-3deg)}100%{transform:translate(0,0) rotate(0)}}
@keyframes flick{0%,100%{opacity:.55;transform:scale(1)}30%{opacity:.95;transform:scale(1.12)}60%{opacity:.7;transform:scale(.94)}}
"""
XCSS += HX
def hol(name): return u(f'holiday/{name}--lines.png')
def flame(x, y, s=60, d=0):
    return (f"<i style='position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;margin:-{s//2}px;border-radius:50%;"
            f"background:radial-gradient(rgba(255,214,140,.95),rgba(255,170,80,.0) 70%);mix-blend-mode:screen;animation:flick {1.1+d*.3:.1f}s {-d:.1f}s infinite ease-in-out'></i>")
AIL = "Holiday illustration digitally created; products shown as supplied."

P['HOL-santa-flyover'] = ('feed', 'green', 9.0, f"""{snow(1080, 1350, 60)}
<div style='position:relative'>{header(True, member=False)}</div>
<div class='mid' style='position:relative;gap:46px'>
  <div style='position:relative;height:430px'><img src='{hol('santa-sleigh')}' style='position:absolute;left:0;top:0;width:900px;{A('fly', 3.4, .3, 'cubic-bezier(.3,.6,.25,1)')}'>
    {glint(860, 40, 3.4)}{glint(120, 330, 3.8, 1.0)}</div>
  <div style='text-align:center'><div class='hd' style='font-size:112px'><div style='{A('up', .9, 3.0)}'>Merry <i>&amp; bright.</i></div></div>
  <div class='p' style='font-size:34px;opacity:.9;margin-top:22px;{A('fade', .9, 3.6)}'>From all of us at EverLiv.</div></div></div>
<div style='position:relative'>{sign_off(True, 4.6, 340)}</div>""")

P['HOL-snowman-stocking-stuffers'] = ('feed', 'green', 8.5, f"""{snow(1080, 1350, 70)}
<div style='position:relative'>{header(True, member=False)}</div>
<div style='position:relative;display:grid;grid-template-columns:470px 1fr;gap:30px;align-items:center'>
  <img src='{hol('snowman')}' style='width:470px;{A('wipeD', 2.2, .2, 'ease-in-out')}'>
  <div><div class='eb' style='color:{LIME};{A('fade', .6, 1.4)}'>Stocking stuffers</div>
    <div class='hd' style='font-size:80px;margin-top:18px;{A('up', .9, 1.6)}'>Gifts that <i>won't melt.</i></div>
    <div style='display:grid;grid-template-columns:repeat(2,170px);gap:16px;margin-top:34px'>
      {''.join(f"<img src='{u(f'tin-{t}--cutout.png')}' style='width:170px;{A('drop', .9, 2.8 + k*.25)}'>" for k, t in enumerate(TINS))}</div></div></div>
<div style='position:relative;{A('fade', .7, 4.2)}'><div class='p' style='font-size:30px;margin-bottom:14px'>30 strips per tin, $34.99 · Any 3 for $79.99</div>
{foot(AIL + ' Energy Strips contain caffeine; see product pages for warnings. Build Your Own Bundle has its own pricing (no member price).')}</div>""")

P['HOL-thanksgiving-table'] = ('feed', 'green', 9.0, f"""{falling_leaves(1080, 1350, 12)}
<div style='position:relative'>{header(True, member=False)}</div>
<div class='mid' style='position:relative;gap:40px'>
  <div style='text-align:center'><div class='eb' style='color:{GOLD};{A('fade', .6, .2)}'>Happy Thanksgiving</div>
  <div class='hd' style='font-size:92px;margin-top:18px'><div style='{A('up', .9, .4)}'>Grateful for every</div><div style='{A('up', .9, .7)}'><i>table we're part of.</i></div></div></div>
  <div style='position:relative;width:912px;height:369px'>
    <img src='{hol('thanksgiving-table')}' style='position:absolute;inset:0;width:912px;{A('wipeL', 2.4, 1.2, 'ease-in-out')}'>
    <div style='{A('fade', .8, 2.6)}'>{flame(264, 22, 50, 0)}{flame(301, 16, 50, .4)}{flame(584, 16, 50, .8)}</div>
    <img src='{u('everliv-hazelnut-coffee-medium-roast--front-cutout-v2.png')}' style='position:absolute;left:700px;top:20px;height:205px;{A('drop', .9, 3.4)}'>
    <img src='{u('tin-hydrate--cutout.png')}' style='position:absolute;left:810px;top:132px;width:86px;{A('drop', .9, 3.7)}'></div>
  <div class='p' style='font-size:32px;text-align:center;{A('fade', .8, 4.2)}'>Thank you for making room for us this year.</div></div>
<div style='position:relative'><div style='{A('fade', .6, 4.6)}'>{foot(AIL, 'center')}</div></div>""")

P['HOL-fireplace-mantel'] = ('feed', 'green', 9.0, f"""{snow(1080, 1350, 30)}
<div style='position:relative'>{header(True, member=False)}</div>
<div class='mid' style='position:relative;gap:34px'>
  <div><div class='eb' style='color:{LIME};{A('fade', .6, .2)}'>Home for the holidays</div>
  <div class='hd' style='font-size:86px;margin-top:16px;{A('up', .9, .4)}'>Something small<br>for <i>every stocking.</i></div></div>
  <div style='position:relative;width:900px;height:745px;margin:0 auto'>
    <img src='{hol('fireplace')}' style='position:absolute;inset:0;width:900px;{A('wipeU', 2.4, 1.0, 'ease-in-out')}'>
    <div style='{A('fade', .8, 2.8)}'>{flame(324, 560, 170, 0)}{flame(300, 590, 110, .5)}{flame(350, 585, 120, .9)}</div>
    {''.join(f"<img src='{u(f'tin-{t}--cutout.png')}' style='position:absolute;left:{70 + k*125}px;top:110px;width:110px;{A('drop', .8, 3.4 + k*.22)}'>" for k, t in enumerate(TINS))}
    {glint(860, 30, 4.8)}</div></div>
<div style='position:relative;{A('fade', .7, 4.6)}'><div class='p' style='font-size:28px;margin-bottom:12px'>30 strips per tin, $34.99 · Any 3 for $79.99</div>
{foot(AIL + ' Energy Strips contain caffeine; see product pages for warnings.')}</div>""")


HX2 = "@keyframes walk{0%{transform:translateX(-700px)}100%{transform:translateX(0)}} @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}"
XCSS += HX2
P['HOL-elf-last-minute'] = ('feed', 'green', 8.5, f"""{snow(1080, 1350, 55)}
<div style='position:relative'>{header(True, member=False)}</div>
<div style='position:relative;display:grid;grid-template-columns:440px 1fr;gap:34px;align-items:center'>
  <div style='{A('walk', 2.4, .2, 'cubic-bezier(.3,.6,.3,1)')}'><img src='{hol('elf')}' style='width:440px;animation:bob .6s .2s 4 ease-in-out both'></div>
  <div><div class='eb' style='color:{LIME};{A('fade', .6, 1.6)}'>Last-minute gifts</div>
    <div class='hd' style='font-size:84px;margin-top:18px'><div style='{A('up', .9, 1.8)}'>Gifts,</div><div style='{A('up', .9, 2.1)}'><i>sorted.</i></div></div>
    <div class='p' style='font-size:32px;margin-top:26px;{A('fade', .8, 2.8)}'>Coffee, handmade soaps and oral strips. Free U.S. shipping; orders processed in 1–3 business days.</div>
    <div style='display:flex;gap:14px;margin-top:30px'>{''.join(f"<img src='{u(f'tin-{t}--cutout.png')}' style='width:110px;{A('drop', .8, 3.4 + k*.2)}'>" for k, t in enumerate(TINS))}</div></div></div>
<div style='position:relative;{A('fade', .7, 4.2)}'>{foot(AIL + ' Delivery times are estimates and not guaranteed. Energy Strips contain caffeine; see product pages for warnings.')}</div>""")

SIZES['wide'] = (1920, 1080, '0')
P['OUTRO-logo-draw--wide'] = ('wide', 'green', 4.6, f"""<div></div>
<div class='mid' style='align-items:center;gap:44px'>{logo_draw(True, 900, .3)}
<div class='eb' style='color:{GOLD};{A('fade', .8, 3.3)}'>everliv.life</div></div><div></div>""")
async def render(only=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page()
        for name, (fmt, cls, dur, body) in P.items():
            if only and not any(name.startswith(o) for o in only): continue
            w, h, _ = SIZES[fmt]; fr = OUT/f'_{name}'; shutil.rmtree(fr, ignore_errors=True); fr.mkdir()
            html = B.page(fmt, cls, body).replace('</style>', ACSS + XCSS + '</style>')
            hp = OUT/f'{name}.html'; hp.write_text(html)
            await pg.set_viewport_size({'width': w, 'height': h}); await pg.goto(hp.as_uri())
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            n = int(dur*FPS)
            for i in range(n):
                await pg.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={i*1000/FPS}}})")
                await pg.screenshot(path=str(fr/f'{i:04d}.png'))
            mp4 = OUT/f'{name}.mp4'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr/'%04d.png'), '-c:v', 'libx264',
                            '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(mp4)], check=True)
            print(name, n, 'frames', mp4.stat().st_size//1024, 'KB', flush=True)
        await b.close()
if __name__ == '__main__':
    asyncio.run(render(sys.argv[1:] or None))
