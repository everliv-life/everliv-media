"""Round 2 static designs (Nov 17): product spotlights, January creative, rebalanced year-end posts, Story frame set.
Wording standard: 'Up to 20% off' as the primary membership message; product-specific member prices shown exactly
(live everliv.life, Nov 16 2026); Jan 31 = last day to join at $49.99, always paired with 'your membership lasts a full 12 months'."""
import sys, asyncio
import build_assets as B
from build_assets import add, u, header, logo, emblem, leaf, foot, card, FINE_M, FINE_S, AI, LEAF, IVORY, PAGE, INK, CHAMP, GOLD, LIME, MUTED
B.A.clear()
TIN = lambda t: u(f'tin-{t}--cutout.png')
PRICE = "Live everliv.life prices, Nov 16, 2026; may change. "
PROMO = "Up to 20% off eligible products for 12 months. Shop as often as you like."
STRIP_FMT = "Dissolves on your tongue. No water, no pills. 30 strips per tin."

def spotlight(pid, tin, name, line, member, rate, warn=''):
    add(pid, 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:#3E5B41'>Meet the strips</div>
  <div style='display:grid;grid-template-columns:470px 1fr;gap:44px;align-items:center'>
    <div style='background:linear-gradient(160deg,#fff,#ECEAE4);border-radius:30px;padding:40px;box-shadow:0 30px 60px -36px rgba(30,43,30,.5)'><img src='{TIN(tin)}' style='width:100%;display:block'></div>
    <div><div class='hd' style='font-size:92px;color:{LEAF}'>{name}</div>
      <div class='p' style='font-size:32px;margin-top:22px'>{line}</div>
      <div class='p' style='font-size:26px;margin-top:18px;color:{MUTED}'>{STRIP_FMT}</div></div></div>
  <div style='display:flex;gap:22px'>
    <div style='flex:1;border:1.5px solid rgba(42,66,42,.2);border-radius:24px;padding:24px 28px'><div class='eb' style='font-size:18px;color:{MUTED}'>Everyday</div><div class='hd' style='font-size:58px;color:{LEAF}'>$34.99</div></div>
    <div style='flex:1;background:{LEAF};border-radius:24px;padding:24px 28px;color:{IVORY}'><div class='tag' style='color:{CHAMP};font-size:18px'>{leaf(20)}Member · {rate} off</div><div class='hd' style='font-size:58px'>{member}</div></div></div>
</div>{foot(PRICE + (warn + ' ' if warn else '') + 'Member price requires an active Member Price Club membership. ' + FINE_S)}""")

spotlight('N03-hydrate-spotlight', 'hydrate', 'Hydrate<br><i>Oral Strips</i>', 'Seven botanicals, including turmeric and chicory, in a dissolvable strip for your daily water routine.', '$27.99', '20%')
spotlight('N01-iron-spotlight', 'iron', 'Iron<br><i>Oral Strips</i>', 'Iron in a dissolvable oral strip.', '$27.99', '20%', 'Keep out of reach of children.')
spotlight('N04-energy-spotlight', 'energy', 'Energy<br><i>Oral Strips</i>', '50 mg green-tea caffeine, 30 mg L-theanine and B12 in a cranberry strip.', '$27.99', '20%', 'Contains caffeine; see product page for warnings.')
spotlight('N02-d3k2-spotlight', 'd3k2', 'D3 + K2<br><i>Oral Strips</i>', 'Vitamin D3 and K2 together in a dissolvable strip.', '$27.99', '20%')

# --- D07 (product routine carousel) and D10 (brand New Year's Eve), rebalanced
def routine(pid, n, eb, hd, body, imgs, cls='ivory', fine=''):
    tiles = ''.join(f"<div style='flex:1;background:linear-gradient(160deg,#fff,#ECEAE4);border-radius:26px;padding:26px;display:flex;align-items:center;justify-content:center;height:420px'><img src='{u(i)}' style='max-width:100%;max-height:370px'></div>" for i in imgs)
    add(pid, 'feed', cls, f"""{header(False, member=False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:#3E5B41'>{eb}</div>
  <div class='hd' style='font-size:92px;color:{LEAF}'>{hd}</div>
  <div style='display:flex;gap:24px'>{tiles}</div>
  <div class='p' style='font-size:32px'>{body}</div>
</div><div style='display:flex;justify-content:space-between;align-items:flex-end'>{foot(fine) if fine else '<div></div>'}<div class='eb' style='font-size:20px;color:#3E5B41'>{n}</div></div>""")
COF = 'everliv-hazelnut-coffee-medium-roast--front-cutout-v2.png'
routine('D07v2-routine-2027_s1', '1 / 3', 'Build your 2027 routine', 'Morning:<br><i>coffee, then a strip.</i>', 'A cup you look forward to, and an Energy strip when you need it. No water needed.', [COF, 'tin-energy--cutout.png'], fine='Energy Strips contain caffeine; see product page for warnings.')
routine('D07v2-routine-2027_s2', '2 / 3', 'Build your 2027 routine', 'Midday:<br><i>keep it simple.</i>', 'Hydrate with your water routine. Iron in a strip that fits a pocket.', ['tin-hydrate--cutout.png', 'tin-iron--cutout.png'], fine='Iron: keep out of reach of children.')
routine('D07v2-routine-2027_s3', '3 / 3', 'Build your 2027 routine', 'Evening:<br><i>wind down.</i>', 'D3 + K2 in a strip, and a handmade soap for the end of the day.', ['tin-d3k2--cutout.png', 'everliv-milk-honey-soap--front-cutout-v2.png'])
add('D10v2-year-of-more_feed', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='align-items:center;text-align:center;gap:40px'>
  <div class='hd' style='font-size:124px'>Here's to<br>a year of <i>more.</i></div><div class='rule'></div>
  <div class='p' style='font-size:34px;opacity:.9'>More routines that fit. More to discover.<br>Happy New Year from EverLiv.</div></div>
<div class='eb' style='text-align:center;color:{GOLD};font-size:20px'>See you in 2027</div>""")

# --- January
add('J01b-year-of-up-to-20_feed', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:36px'>
  <div class='eb' style='color:{GOLD}'>January 1, 2027</div>
  <div class='hd' style='font-size:108px'>A new year.<br><i>Up to 20% off</i><br>all year long.</div>
  <div class='p' style='font-size:34px;opacity:.92'>Join by January 31 for $49.99. Enjoy up to 20% off eligible products for a full 12 months.</div>
  <div style='margin-top:6px'>{card(-4, .78)}</div>
</div>{foot(FINE_M)}""")
def ep(pid, n, ep_no, hd, body, imgs, fine=''):
    routine(f'{pid}_s{n}', f'{n} / 3', f'Routine series · episode {ep_no}', hd, body, imgs, fine=fine)
ep('J02-routine-morning', 1, 1, 'Morning,<br><i>made simple.</i>', 'Coffee first. Then an Energy strip on busy days.', [COF, 'tin-energy--cutout.png'], 'Energy Strips contain caffeine; see product page for warnings.')
ep('J02-routine-morning', 2, 1, 'Four<br><i>coffees.</i>', 'Hazelnut, Cocoa, Caramel and Mushroom. Medium and dark roasts.', ['everliv-cocoa-coffee-medium-roast--front-cutout-v2.png', 'everliv-caramel-coffee-dark-roast--front-cutout-v2.png'])
ep('J02-routine-morning', 3, 1, 'Make it<br><i>yours.</i>', 'Every product page shows its everyday and member price. Shop at everliv.life.', ['everliv-mushroom-coffee-medium-roast--front-cutout-v2.png', 'tin-energy--cutout.png'], 'Energy Strips contain caffeine.')
ep('J03-routine-midday', 1, 2, 'Midday,<br><i>on the move.</i>', 'Strips dissolve on your tongue. No water, no pills.', ['tin-hydrate--cutout.png', 'tin-iron--cutout.png'], 'Iron: keep out of reach of children.')
ep('J03-routine-midday', 2, 2, 'Hydrate<br><i>with your water.</i>', 'Seven botanicals, including turmeric and chicory, for your daily water routine.', ['tin-hydrate--cutout.png'])
ep('J03-routine-midday', 3, 2, 'Iron and<br><i>D3 + K2.</i>', 'Two strips, one tin each, 30 strips per tin.', ['tin-iron--cutout.png', 'tin-d3k2--cutout.png'], 'Iron: keep out of reach of children.')
for n, (hd, body, imgs) in enumerate([('Training day,<br><i>packed.</i>', 'Pure Creatine Monohydrate in the shaker, strips in the bag.', ['everliv-pure-creatine-monohydrate.jpg', 'tin-hydrate--cutout.png']),
                                       ('Creatine,<br><i>simply.</i>', 'Pure Creatine Monohydrate. Or Creatine + Electrolytes.', ['everliv-pure-creatine-monohydrate.jpg', 'everliv-creatine-electrolytes.jpg']),
                                       ('After,<br><i>the reset.</i>', 'A handmade soap for the shower after.', ['everliv-charcoal-soap--front-cutout-v2.png', 'everliv-clean-forrest-soap--front-cutout-v2.png'])], 1):
    routine(f'J04-routine-training_s{n}', f'{n} / 3', 'Routine series · episode 3', hd, body, imgs)
add('J08-slow-mornings_feed', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='gap:34px'><div class='photo' style='height:820px'><img src='{u('everliv-hazelnut-coffee--stone-plinth--social-1080x1350.png')}'></div>
<div><div class='eb' style='color:{LIME}'>January mornings</div><div class='hd' style='font-size:80px;margin-top:14px'>Slow down. <i>Pour another.</i></div></div></div>{foot(AI)}""")
add('J10-whats-next-TEMPLATE_feed', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:34px'>
  <div style='display:inline-block;align-self:flex-start;background:#F3DFA8;color:#5b4510;border-radius:999px;padding:10px 18px;font:700 18px Figtree;letter-spacing:.14em;text-transform:uppercase'>Template · hold until Restructuring confirms launch</div>
  <div class='eb' style='color:#3E5B41'>Discover What's Next · episode 2</div>
  <div class='hd' style='font-size:96px;color:{LEAF}'>[Product name]<br><i>is here.</i></div>
  <div style='height:420px;border:2px dashed rgba(42,66,42,.3);border-radius:28px;display:flex;align-items:center;justify-content:center;color:{MUTED};font:500 26px Figtree;text-align:center;padding:40px'>Approved supplier render goes here<br>(Mushroom Focus Strips, Hair, Skin &amp; Nails Strips, Hyaluronic Acid Serum, Complete Multivitamin or CoQ10)</div>
  <div class='p' style='font-size:30px'>[One factual line from the approved label. No benefit claims until reviewed.]</div>
</div>{foot('Not for publishing. Product not yet approved for sale.')}""")
add('J12-self-care_feed', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='gap:34px'><div class='photo' style='height:820px'><img src='{u('everliv-charcoal-soap--spa-counter--social-1080x1350.png')}'></div>
<div><div class='eb' style='color:{LIME}'>Self-care, scheduled</div><div class='hd' style='font-size:80px;margin-top:14px'>Handmade soaps, <i>six scents.</i></div></div></div>{foot(AI)}""")
add('J15-team-note_feed', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:30px'>
  <div class='eb' style='color:#3E5B41'>A note from the EverLiv team</div>
  <div class='hd' style='font-size:76px;color:{LEAF}'>Why we built a membership <i>instead of running sales.</i></div>
  <div class='p' style='font-size:32px;line-height:1.5'>We'd rather give the people who shop with us a fair price every time than chase one-day discounts. Join once, and eligible products are up to 20% off on every order for a full year.</div>
  <div class='p' style='font-size:30px;color:{MUTED}'>— The EverLiv team</div>
</div>{foot('Draft copy for owner approval; can also be filmed as a talking-head reel. ' + FINE_S)}""")
add('J19-poll_feed', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='align-items:center;text-align:center;gap:40px'>
  <div class='eb' style='color:{LIME}'>Tell us</div>
  <div class='hd' style='font-size:110px'>Morning person<br>or <i>night owl?</i></div>
  <div class='p' style='font-size:34px;opacity:.9'>Comment ☀️ or 🌙. We're building next month's routine posts around your answers.</div></div><div></div>""")
def countdown(pid, big, sub, cls='green'):
    add(pid, 'feed', cls, f"""{header(True)}
<div class='mid' style='align-items:center;text-align:center;gap:34px'>
  {emblem(150)}
  <div class='eb' style='color:{GOLD}'>Founding price · join by Jan 31</div>
  <div class='hd' style='font-size:112px'>{big}</div>
  <div class='p' style='font-size:36px'>{sub}</div>
  <div class='p' style='font-size:34px;color:{CHAMP}'>Your membership lasts a full 12 months.</div>
</div>{foot(FINE_M, 'center')}""")
countdown('J18-one-week_feed', 'One week left<br>to join at <i>$49.99.</i>', 'Up to 20% off eligible products for 12 months. From Feb 1, it costs $69.99 to join.')
countdown('J22-three-days_feed', '3 days left<br>to join at <i>$49.99.</i>', 'Up to 20% off eligible products for 12 months. Shop as often as you like.')
add('J20-math-before-after_feed', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:30px'>
  <div class='eb' style='color:#9C7A3A'>The honest math</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>Joining in January <i>costs less.</i></div>
  <table class='t' style='font-size:30px'><tr><td></td><td class='r'><b>Join by Jan 31</b></td><td class='r'><b>Join from Feb 1</b></td></tr>
   <tr><td>Price to join</td><td class='r'>$49.99</td><td class='r'>$69.99</td></tr>
   <tr><td>Break-even on 20% products</td><td class='r'>$249.95</td><td class='r'>$349.95</td></tr>
   <tr><td>Break-even on 15% products</td><td class='r'>$333.27</td><td class='r'>$466.60</td></tr>
   <tr><td>Membership length</td><td class='r'>12 months</td><td class='r'>12 months</td></tr></table>
  <div class='p' style='font-size:30px'>Break-even = price to join ÷ member discount. Savings depend on what you buy.</div>
</div>{foot(FINE_M)}""")
add('E08-email-header', 'email', 'green', f"""<div class='row' style='height:100%'><div>{logo(True, 40)}
<div class='hd' style='font-size:60px;margin-top:20px'>Your routine,<br><i>your member price.</i></div><div class='p' style='font-size:22px;margin-top:14px'>Up to 20% off eligible products for 12 months.</div></div>
<div style='display:flex;gap:14px'>{''.join(f"<img src='{TIN(t)}' style='width:130px'>" for t in ('hydrate', 'iron', 'd3k2'))}</div></div>""")
add('E11-email-header', 'email', 'green', f"""<div class='row' style='height:100%'><div>{logo(True, 40)}
<div class='hd' style='font-size:60px;margin-top:20px'>Last chance to join<br>at <i>$49.99.</i></div><div class='p' style='font-size:22px;margin-top:14px'>Your membership lasts a full 12 months.</div></div>
<div>{emblem(200)}</div></div>""")

# --- Story frame set (reusable; replaces 82 one-off frames)
STY = [('offer', 'green', 'Member Price Club', 'Up to<br><i>20% off.</i>', 'Eligible products, every eligible order, for 12 months.'),
       ('founding', 'green', 'Founding price', '$49.99 if you<br><i>join by Jan 31.</i>', 'Your membership lasts a full 12 months.'),
       ('strips', 'ivory', 'Meet the strips', 'Energy · Hydrate<br><i>Iron · D3 + K2</i>', 'Dissolve on your tongue. No water, no pills.'),
       ('coffee', 'ivory', 'Coffee', 'Four<br><i>coffees.</i>', 'Hazelnut · Cocoa · Caramel · Mushroom'),
       ('poll', 'green', 'Poll', 'Coffee or<br><i>a strip?</i>', '[Instagram poll sticker]'),
       ('quiz', 'ivory', 'Quiz', 'How long does<br><i>membership last?</i>', '[Quiz sticker · answer: 12 months]'),
       ('ten', 'green', 'Countdown', '10 days left<br>to join at <i>$49.99.</i>', 'Your membership lasts a full 12 months.'),
       ('week', 'green', 'Countdown', 'One week left<br>to join at <i>$49.99.</i>', 'Your membership lasts a full 12 months.'),
       ('tomorrow', 'green', 'Countdown', 'Tomorrow is the<br>last day to join<br>at <i>$49.99.</i>', 'Your membership lasts a full 12 months.'),
       ('last', 'green', 'Last chance', 'Last chance<br>to join at <i>$49.99.</i>', 'Your membership lasts a full 12 months.')]
for k, cls, eb, hd, sub in STY:
    mem = k in ('offer', 'founding', 'quiz', 'ten', 'week', 'tomorrow', 'last')
    dark = cls == 'green'
    add(f'stories-r2/story-{k}', 'story', cls, f"""<div style='display:flex;justify-content:center'>{logo(dark, 46)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:46px'>{emblem(150) if mem else ''}
<div class='eb' style='color:{GOLD if dark else '#9C7A3A'}'>{eb}</div><div class='hd' style='font-size:104px;{'' if dark else 'color:' + LEAF}'>{hd}</div>
<div class='p' style='font-size:36px;{'' if dark else 'color:' + INK}'>{sub}</div>
<div style='width:640px;height:150px;border-radius:26px;border:2px dashed {'rgba(233,228,223,.35)' if dark else 'rgba(42,66,42,.25)'};display:flex;align-items:center;justify-content:center;font:600 22px Figtree;opacity:.6'>Link sticker</div></div>
{foot(FINE_S, 'center') if mem else '<div></div>'}""")

if __name__ == '__main__':
    asyncio.run(B.main(sys.argv[1:] or None))
