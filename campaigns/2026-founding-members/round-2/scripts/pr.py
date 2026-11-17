"""Photoreal holiday + January motion pieces (round 2). Scenes: Gemini (scene art only). Products: authentic cut-outs.
Motion kept subtle: slow push-in, twinkles on the scene's own lights, candle/fire flicker, steam, snowfall.
The gold-leaf logo/emblem shimmer is reserved for membership pieces."""
import json, sys, asyncio
import fx
from fx import P as FXP, A, u, snow, steam, glint, logo_draw, emblem_live, flame, GOLD, CHAMP, LIME, IVORY, LEAF, B, FINE_S
from build_assets import logo, foot, FINE_M
R = json.load(open(fx.B.ROOT/'src'/'scenes'/'comp'/'report.json'))
AI = "Product shown as supplied; scene digitally created."
AI0 = "Scene digitally created."
P = {}

def tw(name, n=14, size=54):
    return ''.join(f"<i style='position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;margin:-{size//2}px;border-radius:50%;"
                   f"background:radial-gradient(rgba(255,226,160,.85),rgba(255,210,130,0) 70%);mix-blend-mode:screen;"
                   f"animation:twk {1.8 + (i % 5)*.35:.2f}s {-(i*.37) % 2:.2f}s infinite ease-in-out'></i>" for i, (x, y) in enumerate(R[name]['twinkles'][:n]))

def scene(name, inner='', top='', bottom='', snowy=False, twinkle=True, origin='50% 60%', bh=340):
    return f"""<div style='position:absolute;inset:0;overflow:hidden'>
  <div style='position:absolute;inset:0;transform-origin:{origin};{A('push', 8.5, 0, 'linear')}'>
    <img src='{u(f'scenes/comp/{name}.png')}' style='width:100%;height:100%;display:block'>{tw(name) if twinkle else ''}{inner}</div>
  {snow(1080, 1350, 60) if snowy else ''}
  <div style='position:absolute;left:0;right:0;top:0;height:560px;background:linear-gradient(rgba(16,24,16,.72),rgba(16,24,16,0))'></div>
  <div style='position:absolute;left:0;right:0;bottom:0;height:{bh}px;background:linear-gradient(rgba(16,24,16,0),rgba(16,24,16,.9))'></div></div>
<div style='position:relative'>{logo(True, 44)}</div>
<div style='position:relative;align-self:start;margin-top:40px'>{top}</div>
<div style='position:relative;color:{IVORY}'>{bottom}</div>"""

def head(eb, hd, sub='', t=.5, size=96):
    return (f"<div class='eb' style='color:{CHAMP};{A('fade', .7, t)}'>{eb}</div>"
            f"<div class='hd' style='font-size:{size}px;margin-top:16px;color:{IVORY};text-shadow:0 2px 24px rgba(0,0,0,.35);{A('up', 1.0, t + .3)}'>{hd}</div>"
            + (f"<div class='p' style='font-size:32px;margin-top:20px;color:{IVORY};{A('fade', .8, t + 1.1)}'>{sub}</div>" if sub else ''))

def fine(t, delay=2.2): return f"<div style='{A('fade', .8, delay)}'>{foot(t)}</div>"

P['PR01-thanksgiving-table'] = ('feed', 'green', 8.5, scene('thanksgiving-table',
    top=head('Happy Thanksgiving', 'Thank <i>you.</i>', 'To everyone who tried a strip, brewed a cup or built a routine with us this year.'),
    bottom=fine(AI), origin='60% 40%'))
P['PR02-fireplace-stocking-stuffers'] = ('feed', 'green', 8.5, scene('fireplace-living-room',
    inner=fx.flame(216, 741, 230, 0) + fx.flame(160, 780, 150, .5) + fx.flame(240, 700, 160, .9),
    top=head('Stocking stuffers', 'Small enough<br>for <i>every stocking.</i>', 'Energy, Hydrate, Iron and D3+K2 oral strips · 30 strips per tin, $34.99', size=88),
    bottom=fine(AI + ' Energy Strips contain caffeine; see product pages for warnings.'), origin='50% 85%', bh=150))
P['PR03-snowman-gifts'] = ('feed', 'green', 8.5, scene('snowman-garden', snowy=True,
    top=head('For the winter routine', 'Gifts that<br><i>won\'t melt.</i>', 'Hydrate and D3+K2 oral strips · no water needed', size=92),
    bottom=fine(AI), origin='60% 80%', bh=150))
P['PR04-santa-christmas-eve'] = ('feed', 'green', 9.0, scene('santa-sleigh-village', snowy=True,
    top=f"<div style='text-align:center'>{head('Christmas Eve', 'Merry <i>&amp; bright.</i>', 'From all of us at EverLiv.', size=110)}</div>",
    bottom=fine(AI0), origin='40% 70%'))
P['PR05-christmas-morning'] = ('feed', 'green', 8.5, scene('christmas-morning', twinkle=False,
    inner=steam(443, 618, 3, .38) + steam(637, 680, 3, .38) + fx.flame(788, 600, 70, .3),
    top=head('Christmas Day', 'Merry <i>Christmas.</i>', 'Wishing you a slow, warm morning. From all of us at EverLiv.', size=100),
    bottom=fine(AI0), origin='50% 50%'))
P['PR06-tree-train-gifts'] = ('feed', 'green', 8.5, scene('tree-model-train',
    top=head('All aboard', 'Gifts that <i>travel well.</i>', 'Free U.S. shipping · orders processed in 1–3 business days', size=88),
    bottom=fine(AI + ' Delivery times are estimates and not guaranteed.'), origin='70% 85%', bh=150))
P['PR07-workshop-soaps'] = ('feed', 'green', 8.5, scene('gift-wrapping-workshop',
    top=head('Wrapped with care', 'Handmade soaps,<br><i>ready to give.</i>', 'Six scents · from $20.99', size=88),
    bottom=fine(AI), origin='45% 85%', bh=150))
# Membership: gold-leaf emblem moment + the approved Founding Member statement
P['PR08-door-wreath-founding-member'] = ('feed', 'green', 9.0, scene('front-door-wreath-mistletoe', snowy=True,
    top=f"""<div style='display:flex;gap:28px;align-items:center'><div style='{A('grow', 1.0, .3)}'>{emblem_live(130, 1.4, 2.2, 2.9)}</div>
      <div>{head('Founding Member', 'This one\'s <i>yours.</i>', t=.6, size=92)}</div></div>
      <div class='p' style='font-size:34px;margin-top:26px;color:{IVORY};{A('fade', .8, 2.0)}'>Join by January 31 for $49.99.<br>Enjoy <b>up to 20% off</b> eligible products for a full 12 months.</div>""",
    bottom=fine(FINE_S + ' ' + AI0, 3.0), origin='50% 40%'))
P['PR09-new-year-kitchen'] = ('feed', 'ivory', 8.5, scene('new-year-kitchen', twinkle=False,
    inner=f"<div class='sheen' style='--a:.35;mix-blend-mode:screen;{A('sweep', 3.0, .8, 'ease-in-out')}'></div>",
    top=head('New year', 'Simple routines,<br><i>every day.</i>', 'Hydrate, Iron and D3+K2 oral strips · 30 strips per tin', size=92),
    bottom=fine(AI), origin='50% 80%', bh=150))
P['PR10-entryway-gym-bag'] = ('feed', 'ivory', 8.5, scene('winter-entryway-gym-bag', twinkle=False,
    top=head('January', 'Packed for <i>the new year.</i>', 'Hydrate and Energy oral strips · fit in any bag', size=88),
    bottom=fine(AI + ' Energy Strips contain caffeine; see product pages for warnings.'), origin='80% 60%', bh=150))

# Coffee (smaller bag, calmer): replace the round-1 coffee pieces
def coffee2(img, eb, hd):
    return ('feed', 'green', 8.0, f"""<div style='position:absolute;inset:0;overflow:hidden'>
  <div style='position:absolute;inset:0;transform-origin:22% 70%;{A('push', 8, 0, 'linear')}'>
    <img src='{u(img)}' style='width:100%;height:100%;object-fit:cover'>
    {fx.twinkles([(150,130),(420,120),(700,150),(980,120),(560,210)], 40)}{steam(232, 905, 3, .36)}</div>
  <div style='position:absolute;left:0;right:0;top:0;height:520px;background:linear-gradient(rgba(20,30,20,.6),rgba(20,30,20,0))'></div>
  <div style='position:absolute;left:0;right:0;bottom:0;height:200px;background:linear-gradient(rgba(20,30,20,0),rgba(20,30,20,.75))'></div></div>
<div style='position:relative'>{logo(True, 46)}</div>
<div style='position:relative;margin-top:40px'><div class='eb' style='color:{CHAMP};{A('fade', .7, .6)}'>{eb}</div>
  <div class='hd' style='font-size:92px;margin-top:16px;color:{IVORY};{A('up', 1.0, 1.0)}'>{hd}</div></div>
<div style='position:relative;color:{IVORY};{A('fade', .8, 2.4)}'>{foot(AI + ' Free U.S. shipping on every order.')}</div>""")
P['COFFEE2-cocoa-steam'] = coffee2('coffee-v2/cocoa-coffee-medium-roast-1080x1350.png', 'Cocoa · medium roast', 'Cozy season,<br><i>brewed.</i>')
P['COFFEE2-caramel-steam'] = coffee2('coffee-v2/caramel-coffee-dark-roast-1080x1350.png', 'Caramel · dark roast', 'Pour. Sip.<br><i>Slow down.</i>')

if __name__ == '__main__':
    fx.P.clear(); fx.P.update(P)
    asyncio.run(fx.render(sys.argv[1:] or None))
