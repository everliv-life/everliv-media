"""Round 2 motion: membership pieces use the gold-leaf moments, each with a different treatment and pacing;
product motion stays free of the member emblem/shimmer."""
import sys, asyncio
import fx
from fx import A, u, glint, logo_draw, emblem_live, heartbeat_line, GOLD, CHAMP, LIME, IVORY, LEAF, B
from build_assets import logo, foot, header, FINE_M, FINE_S, MUTED
fx.SIZES['story'] = B.SIZES['story']
P = {}
fx.XCSS += '@keyframes slot{0%{opacity:0;transform:translateX(90px)}14%{opacity:1;transform:none}82%{opacity:1;transform:none}100%{opacity:0;transform:translateX(-60px)}}'
P['PRICE-hydrate'] = fx.price_piece('tin-hydrate--cutout.png', 'Hydrate<br>Oral Strips', '$34.99', '$27.99', '20%')
# Variant B: emblem-led, slow ring orbit (Jan 21)
P['J16-ten-days-left'] = ('feed', 'green', 9.0, f"""<div style='{A('fade', .6, 0)}'>{header(True, member=False)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:36px'>
  <div style='{A('grow', 1.4, .2)}'>{emblem_live(250, 1.2, 3.4, 4.2, ring_dur=3.6)}</div>
  <div class='eb' style='color:{GOLD};{A('fade', .7, 1.6)}'>The final ten days</div>
  <div class='hd' style='font-size:104px'><div style='{A('up', .9, 2.0)}'>10 days left</div><div style='{A('up', .9, 2.3)}'>to join at <i>$49.99.</i></div></div>
  <div class='p' style='font-size:36px;color:{CHAMP};{A('fade', .8, 3.2)}'>Your membership lasts a full 12 months.</div>
  <div class='p' style='font-size:30px;{A('fade', .8, 3.8)}'>Up to 20% off eligible products. Shop as often as you like.</div>
</div><div style='{A('fade', .8, 4.4)}'>{foot(FINE_M, 'center')}</div>""")
# Variant A: message first, logo draws in last with the gold leaf (Jan 31)
def last(fmt, w):
    return (fmt, 'green', 9.5, f"""<div></div>
<div class='mid' style='align-items:center;text-align:center;gap:38px'>
  <div class='eb' style='color:{GOLD};{A('fade', .6, .2)}'>Today · January 31</div>
  <div class='hd' style='font-size:{118 if fmt == 'story' else 104}px'><div style='{A('up', .9, .5)}'>Last chance</div><div style='{A('up', .9, .8)}'>to join at <i>$49.99.</i></div></div>
  <div class='p' style='font-size:38px;color:{CHAMP};{A('fade', .8, 1.6)}'>Your membership lasts a full 12 months.</div>
  <div class='p' style='font-size:32px;{A('fade', .8, 2.2)}'>Up to 20% off eligible products, as often as you shop.<br>From February 1, it costs $69.99 to join.</div>
  <div style='margin-top:30px'>{logo_draw(True, w, 3.0)}</div>
</div><div style='{A('fade', .8, 3.0)}'>{foot(FINE_S, 'center')}</div>""")
P['J24-last-chance--feed'] = last('feed', 560)
P['J24-last-chance--reel'] = last('story', 640)
# Product reel: no member emblem, plain logo
NAMES = [('energy', 'Energy', 'Green-tea caffeine, L-theanine and B12.'), ('hydrate', 'Hydrate', 'Seven botanicals, for your water routine.'),
         ('iron', 'Iron', 'Iron in a dissolvable strip.'), ('d3k2', 'D3 + K2', 'Vitamin D3 and K2 together.')]
seq = ''
for k, (t, n, l) in enumerate(NAMES):
    t0 = .6 + k * 1.7
    seq += (f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;"
            f"animation:slot 1.9s {t0}s both'>"
            f"<img src='{u(f'tin-{t}--cutout.png')}' style='width:620px'><div class='hd' style='font-size:110px;color:{LEAF}'>{n}</div>"
            f"<div class='p' style='font-size:38px'>{l}</div></div>")
P['J11-strips-family--reel'] = ('story', 'ivory', 10.5, f"""<div style='display:flex;justify-content:center'>{logo(False, 50)}</div>
<div style='position:relative'>{seq}
  <div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:50px;{A('fade', .8, 7.6)}'>
    <img src='{u('strips-available-4--2x2--transparent.png')}' style='width:820px'>
    <div class='hd' style='font-size:96px;color:{LEAF}'>Four strips.<br><i>No water needed.</i></div>
    <div class='p' style='font-size:36px'>30 strips per tin · $34.99 · Any 3 for $79.99</div></div></div>
{foot('Energy Strips contain caffeine; Iron: keep out of reach of children. Build Your Own Bundle has its own pricing (no member price).', 'center')}""")
if __name__ == '__main__':
    fx.P.clear(); fx.P.update(P)
    asyncio.run(fx.render(sys.argv[1:] or None))
