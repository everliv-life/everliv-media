"""Render EverLiv Founding Members campaign assets (HTML -> PNG, headless Chrome).
Brand: approved EverLiv logo + Member Club emblems from EverLiv-Brand-and-Member-Marks.zip (used unaltered),
Sentient (headings) + Figtree (body), Leaf Extract / ivory / restrained champagne-gold. Product imagery: unaltered
supplier renders, verified cut-outs and owner-approved editorial scenes (AI-scene disclosure where used)."""
import pathlib, asyncio, sys, json
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).parent; S = ROOT/'src'; OUT = ROOT/'assets'; OUT.mkdir(exist_ok=True)
def u(f): return (S/f).resolve().as_uri()
LEAF='#2A422A'; IVORY='#E9E4DF'; PAGE='#F1F1EE'; INK='#1A1C17'; CHAMP='#EADFC3'; GOLD='#C9B27C'; LIME='#8BC343'; MUTED='#6B6B6B'; DEEP='#1F331F'
CSS = f"""
@font-face{{font-family:'Sentient';src:url({u('Sentient-Regular.woff2')});font-weight:400}}
@font-face{{font-family:'Sentient';src:url({u('Sentient-Italic.woff2')});font-weight:400;font-style:italic}}
@font-face{{font-family:'Figtree';src:url({u('figtree-latin-wght-normal.woff2')});font-weight:300 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:var(--w);height:var(--h);overflow:hidden;font-family:Figtree;-webkit-font-smoothing:antialiased}}
.f{{position:relative;width:var(--w);height:var(--h);overflow:hidden;display:grid;grid-template-rows:auto 1fr auto;padding:var(--pad)}}
.green{{background:radial-gradient(120% 90% at 70% 10%,#35533a 0%,{LEAF} 55%,{DEEP} 100%);color:{IVORY}}}
.ivory{{background:{PAGE};color:{INK}}}
.champ{{background:linear-gradient(160deg,#F4EEDF 0%,{CHAMP} 100%);color:{INK}}}
.hd{{font-family:Sentient;font-weight:400;letter-spacing:-.012em;line-height:1.04}}
.hd i{{font-style:italic}}
.eb{{font-weight:650;font-size:24px;letter-spacing:.22em;text-transform:uppercase}}
.p{{font-weight:450;line-height:1.42}}
.fine{{font-size:21px;line-height:1.42;opacity:.75;font-weight:450}}
.row{{display:flex;align-items:center;justify-content:space-between}}
.mid{{display:flex;flex-direction:column;justify-content:center}}
.rule{{height:2px;width:84px;background:{GOLD}}}
.btn{{display:inline-block;border-radius:999px;padding:24px 42px;font-size:28px;font-weight:650}}
.tile{{background:#F7F7F7;border-radius:24px;overflow:hidden;box-shadow:0 22px 44px -28px rgba(30,43,30,.5)}}
.tile img{{width:100%;height:100%;object-fit:cover;display:block}}
.photo{{border-radius:26px;overflow:hidden}} .photo img{{width:100%;height:100%;object-fit:cover;display:block}}
.card{{position:relative;width:640px;height:400px;border-radius:30px;padding:42px 48px;color:{IVORY};
  background:linear-gradient(140deg,#3f5f3c 0%,#2f4a2f 52%,#1e321e 100%);border:1.5px solid {GOLD};
  box-shadow:0 44px 90px -34px rgba(0,0,0,.55)}}
.card .club{{display:flex;align-items:center;gap:12px;font-size:18px;font-weight:650;letter-spacing:.22em;text-transform:uppercase;color:{CHAMP}}}
.card .fm{{position:absolute;left:48px;bottom:96px;font-family:Sentient;font-style:italic;font-size:62px;line-height:1}}
.card .ln{{position:absolute;left:48px;bottom:78px;width:60px;height:2px;background:{GOLD}}}
.card .meta{{position:absolute;left:48px;right:48px;bottom:38px;display:flex;justify-content:space-between;font-size:20px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:{CHAMP};opacity:.9}}
.tag{{display:inline-flex;align-items:center;gap:10px;font-size:20px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}}
table.t{{width:100%;border-collapse:collapse;font-size:28px}} table.t td{{padding:16px 0;border-bottom:1px solid rgba(26,28,23,.12)}}
table.t td.r{{text-align:right;font-variant-numeric:tabular-nums}}
"""
FINE_M = ("Member pricing: up to 20% off eligible products (15% or 20%, depending on the product) on every eligible order for 12 months from activation; shop as often as you like. "
          "Some products excluded; not for Subscribe & Save, bundles or promo codes. Price to join: $49.99 for memberships bought through Jan 31, 2027 (ET); $69.99 to join from Feb 1, 2027. "
          "12 months, no automatic renewal. Savings depend on what you buy. Not available to residents of CA or NC. Terms at everliv.life.")
FINE_S = ("Up to 20% off eligible products for 12 months (15% or 20% by product); some excluded; not for Subscribe & Save, bundles or codes. $49.99 to join through Jan 31, 2027 (ET); "
          "$69.99 to join from Feb 1, 2027. Every membership lasts 12 months. No automatic renewal. Not available in CA or NC.")
AI = "Product shown as supplied; scene digitally created."
def logo(dark_bg, h=46): return f"<img src='{u('everliv-logo-white.svg' if dark_bg else 'everliv-logo.svg')}' style='height:{h}px;display:block'>"
def emblem(size=96): return f"<img src='{u('everliv-member-mark-gold-circle-leaf.svg')}' style='width:{size}px;height:{size}px;display:block'>"
def leaf(size=26): return f"<img src='{u('everliv-member-mark-gold-centre-leaf.svg')}' style='height:{size}px;display:inline-block;vertical-align:middle'>"
def card(rot=-4, scale=1.0):
    return f"""<div style='display:flex;justify-content:center'><div class='card' style='transform:rotate({rot}deg) scale({scale})'>
      <div class='row'>{logo(True,38)}<div class='club'>{leaf(24)}Member Price Club</div></div>
      <div class='fm'>Founding Member</div><div class='ln'></div><div class='meta'><span>12 months</span><span>Paid once</span></div></div></div>"""
def header(dark, member=True, right=''):
    r = right or (f"<div class='tag' style='color:{GOLD if dark else '#9C7A3A'}'>{leaf(24)}Member Price Club</div>" if member else '')
    return f"<div class='row'>{logo(dark)}{r}</div>"
SIZES = {'feed': (1080, 1350, '78px 84px 64px'), 'story': (1080, 1920, '250px 90px 340px'), 'email': (1200, 600, '56px 70px'),
         'square': (1080, 1080, '70px 80px 56px')}
A = {}  # name -> (fmt, cls, html)
def add(name, fmt, cls, body): A[name] = (fmt, cls, body)
def page(fmt, cls, body):
    w, h, pad = SIZES[fmt]
    return f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{--w:{w}px;--h:{h}px;--pad:{pad}}}{CSS}</style></head><body><div class='f {cls}'>{body}</div></body></html>"
def foot(text, align='left'): return f"<div class='fine' style='text-align:{align}'>{text}</div>"
G = lambda t: f"<span style='color:{GOLD}'>{t}</span>"

# ======================= PHASE A =======================
add('A01-teaser-something-new_feed', 'feed', 'green', f"""
{header(True, member=False)}
<div class='mid' style='align-items:center;text-align:center;gap:56px'>
  {emblem(150)}
  <div class='hd' style='font-size:92px'>Something new is<br><i>taking shape</i> at EverLiv.</div>
  <div class='rule'></div>
  <div class='p' style='font-size:32px;opacity:.85'>A little gold. A lot more to discover.</div>
</div>
<div class='eb' style='text-align:center;color:{GOLD};font-size:22px'>More on Monday</div>""")
add('A01-teaser-something-new_story', 'story', 'green', f"""
<div style='display:flex;justify-content:center'>{logo(True,48)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:60px'>
  {emblem(190)}
  <div class='hd' style='font-size:100px'>Something new<br>is <i>taking shape.</i></div>
  <div class='p' style='font-size:36px;opacity:.85'>A little gold.<br>A lot more to discover.</div>
</div>
<div class='eb' style='text-align:center;color:{GOLD}'>Monday</div>""")
for i, (l1, l2) in enumerate([("A little gold.", ""), ("A little gold.", "A lot more to discover."), ("Your wellness journey evolves.", "So does EverLiv."), ("Monday.", "")]):
    add(f'A02-teaser-reel_f{i+1}', 'story', 'green', f"""
<div style='display:flex;justify-content:center'>{logo(True,46)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:70px'>
  {emblem(230 if i != 2 else 160)}
  <div class='hd' style='font-size:{104 if len(l1) < 20 else 84}px'>{l1}{('<br><i>' + l2 + '</i>') if l2 else ''}</div>
</div><div></div>""")

PRODUCT_TILES = {'nad': 'everliv-nad.jpg', 'nmn': 'everliv-b-nmn.jpg', 'creatine': 'everliv-pure-creatine-monohydrate.jpg',
                 'creatine_e': 'everliv-creatine-electrolytes.jpg', 'energy': 'energy-strips--front.jpg'}
def tiles(keys, size):
    return "<div style='display:flex;gap:28px;justify-content:center'>" + ''.join(
        f"<div class='tile' style='width:{size}px;height:{size}px'><img src='{u(PRODUCT_TILES[k])}'></div>" for k in keys) + "</div>"
add('A03-brand-range_s1', 'feed', 'ivory', f"""
{header(False, member=False)}
<div class='mid' style='gap:44px'>
  <div class='eb' style='color:#3E5B41'>The EverLiv range</div>
  <div class='hd' style='font-size:100px;color:{LEAF}'>Strips, capsules,<br>powders <i>and more.</i></div>
  <div class='p' style='font-size:34px;max-width:860px'>Routines that fit real days, with every ingredient listed on the label.</div>
  <img src='{u('strips-available-4--row--transparent.png')}' style='width:100%;margin-top:10px'>
</div>
<div class='eb' style='font-size:20px;color:#3E5B41'>Swipe →</div>""")
add('A03-brand-range_s2', 'feed', 'ivory', f"""
{header(False, member=False)}
<div class='mid' style='gap:46px'>
  <div class='eb' style='color:#3E5B41'>Capsules and powders</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>The daily <i>classics.</i></div>
  {tiles(['nad','nmn'], 420)}
  {tiles(['creatine','creatine_e'], 420)}
</div><div></div>""")
add('A03-brand-range_s3', 'feed', 'ivory', f"""
{header(False, member=False)}
<div class='mid' style='gap:40px'>
  <div class='eb' style='color:#3E5B41'>Coffee and body care</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>The <i>everyday</i> rituals.</div>
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:26px'>
    <div class='photo' style='height:560px'><img src='{u('everliv-cocoa-coffee--holiday-kitchen--social-1080x1350.png')}'></div>
    <div class='photo' style='height:560px'><img src='{u('everliv-charcoal-soap--spa-counter--social-1080x1350.png')}'></div></div>
  <div class='p' style='font-size:30px'>Explore the full range at <b>everliv.life</b></div>
</div>{foot(AI)}""")

REVEAL_MID = f"""<div class='mid' style='align-items:center;text-align:center;gap:40px'>
  {emblem(170)}
  <div class='eb' style='color:{GOLD}'>Introducing the Member Price Club</div>
  <div class='hd' style='font-size:108px'>Become a<br><i>Founding Member.</i></div>
  <div class='p' style='font-size:36px'>Join by January 31 for $49.99. Enjoy <b>up to 20% off</b><br>eligible products for a full 12 months.</div>
</div>"""
add('A04-reveal_feed', 'feed', 'green', f"{header(True, member=False)}{REVEAL_MID}{foot(FINE_M,'center')}")
add('A04-reveal_story', 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,48)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:46px'>
  {emblem(200)}<div class='eb' style='color:{GOLD}'>Introducing the Member Price Club</div>
  <div class='hd' style='font-size:116px'>Become a<br><i>Founding<br>Member.</i></div>
  <div class='p' style='font-size:40px'>$49.99, paid once.<br><b>Up to 20% off</b> for 12 months.</div>
  <div class='btn' style='background:{CHAMP};color:{LEAF};margin-top:20px'>everliv.life/pages/membership</div>
</div>{foot(FINE_S,'center')}""")
for i, (eb, hd, sub) in enumerate([
        ('EverLiv', 'This is the<br><i>Member Price Club.</i>', ''),
        ('One payment', '$49.99,<br><i>paid once.</i>', 'No monthly fees. No automatic renewal.'),
        ('Twelve months', 'Member pricing on<br><i>every eligible order.</i>', 'Up to 20% off eligible products.<br>Shop as often as you like.'),
        ('Founding price to join', '$49.99 if you<br><i>join by Jan 31.</i>', 'Every membership lasts a full 12 months.<br>Join: link in bio.')]):
    add(f'A04R-reveal-reel_f{i+1}', 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,46)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:50px'>
  {emblem(180 if i == 0 else 120)}<div class='eb' style='color:{GOLD}'>{eb}</div>
  <div class='hd' style='font-size:108px'>{hd}</div>
  {f"<div class='p' style='font-size:38px;opacity:.9'>{sub}</div>" if sub else ''}
</div>{foot(FINE_S,'center') if i == 3 else '<div></div>'}""")

def steps_slide(n, title, body):
    return f"""{header(False)}
<div class='mid' style='gap:40px'>
  <div class='hd' style='font-size:230px;color:{GOLD};line-height:.9'>{n}</div>
  <div class='hd' style='font-size:90px;color:{LEAF}'>{title}</div>
  <div class='p' style='font-size:36px;max-width:880px'>{body}</div>
</div>{foot(FINE_M)}"""
add('A05-how-it-works_s1', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:36px'>
  <div class='eb' style='color:#9C7A3A'>How it works</div>
  <div class='hd' style='font-size:98px;color:{LEAF}'>One payment.<br><i>Twelve months</i> of<br>member pricing.</div>
  <div style='margin-top:30px'>{card(-4, .92)}</div>
</div><div class='eb' style='font-size:20px;color:#3E5B41'>Swipe →</div>""")
add('A05-how-it-works_s2', 'feed', 'ivory', steps_slide('1', 'Pay $49.99 <i>once.</i>', 'One payment covers 12 months of member pricing, from activation. Shop as often as you like. No monthly fees, no automatic renewal.'))
add('A05-how-it-works_s3', 'feed', 'ivory', steps_slide('2', 'Sign in with the <i>same email.</i>', 'Membership is linked to your EverLiv account. Member prices apply automatically at checkout.'))
add('A05-how-it-works_s4', 'feed', 'ivory', steps_slide('3', 'Up to <i>20% off.</i>', 'Eligible products are 15% or 20% off, depending on the product; every product page shows its member price. Some products are excluded, and member pricing doesn\'t combine with Subscribe &amp; Save, bundles or promo codes.'))
add('A05-how-it-works_s5', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:36px'>
  <div class='hd' style='font-size:230px;color:{GOLD};line-height:.9'>4</div>
  <div class='hd' style='font-size:96px'>Shop as often<br>as you <i>like.</i></div>
  <div class='p' style='font-size:36px;max-width:880px'>Up to 20% off eligible products, on every eligible order for 12 months, as often as you shop. Join by January 31, 2027 for $49.99.</div>
  <div><div class='btn' style='background:{CHAMP};color:{LEAF}'>everliv.life/pages/membership</div></div>
</div>{foot(FINE_M)}""")

def calc_cover(dark=True):
    return f"""{header(dark)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:{GOLD}'>The honest math</div>
  <div class='hd' style='font-size:96px'>Is membership<br><i>worth it for you?</i></div>
  <div class='p' style='font-size:34px;opacity:.9;max-width:860px'>Four slides. Real numbers. Including the $49.99 fee.</div>
</div><div class='eb' style='font-size:20px;color:{GOLD}'>Swipe →</div>"""
add('A06-calculator_s1', 'feed', 'green', calc_cover())
def breakeven(rate, need, note):
    return f"""{header(False)}
<div class='mid' style='gap:30px'>
  <div class='eb' style='color:#9C7A3A'>On {rate}% products</div>
  <div class='hd' style='font-size:128px;color:{LEAF}'>$49.99 <span style='opacity:.45'>÷</span> {rate}%</div>
  <div class='hd' style='font-size:128px;color:{LEAF}'><span style='opacity:.45'>=</span> {need}</div>
  <div class='rule'></div>
  <div class='p' style='font-size:34px;max-width:880px'>{note}</div>
</div>{foot('Illustrative. Gross product discount at the member rate vs everyday price. Savings depend on what you buy and aren\'t guaranteed to exceed the fee.')}"""
add('A06-calculator_s2', 'feed', 'ivory', breakeven(20, '$249.95', 'If everything you buy is a 20%-off product, about <b>$250</b> of eligible purchases in 12 months covers the fee.'))
add('A06-calculator_s3', 'feed', 'ivory', breakeven(15, '$333.27', 'On 15%-off products it takes about <b>$333</b>. A mix of both lands somewhere in between.'))
add('A06-calculator_s4', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:#9C7A3A'>Gross vs net</div>
  <div class='hd' style='font-size:86px;color:{LEAF}'>Count the fee.<br><i>Always.</i></div>
  <table class='t'><tr><td>Gross saving</td><td class='r'>member price vs everyday, added up</td></tr>
   <tr><td>Minus</td><td class='r'>$49.99 membership fee</td></tr>
   <tr><td><b>Net saving</b></td><td class='r'><b>what you actually keep</b></td></tr></table>
  <div class='p' style='font-size:32px'>Above break-even, member pricing keeps working for the rest of your 12 months. Below it, everyday prices or Subscribe &amp; Save may suit you better.</div>
</div>{foot(FINE_M)}""")
add('A06-calculator_s5', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:40px;align-items:flex-start'>
  <div class='hd' style='font-size:96px'>Do <i>your</i> math.</div>
  <div class='p' style='font-size:36px;max-width:860px'>Every product page shows its member price. Add up what you buy in a year, take off the $49.99 fee, and decide.</div>
  <div class='btn' style='background:{CHAMP};color:{LEAF}'>everliv.life/pages/membership</div>
</div>{foot(FINE_M)}""")
add('A07-thanksgiving_feed', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='align-items:center;text-align:center;gap:44px'>
  <div class='hd' style='font-size:120px;color:{LEAF}'>Thank <i>you.</i></div>
  <div class='rule' style='background:{LIME}'></div>
  <div class='p' style='font-size:36px;max-width:820px'>To everyone who tried a strip, brewed a cup or built a routine with us this year.</div>
</div><div class='eb' style='text-align:center;font-size:20px;color:#3E5B41'>Happy Thanksgiving from EverLiv</div>""")

# ======================= PHASE B =======================
BF_FINE = FINE_M
add('B01-black-friday_feed', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:{GOLD}'>Black Friday · Founding Members</div>
  <div class='hd' style='font-size:102px'>Black Friday ends.<br><i>Your membership<br>doesn't.</i></div>
  <div class='p' style='font-size:34px;opacity:.9'>$49.99, paid once. <b>Up to 20% off</b> eligible products on<br>every eligible order for 12 months: strips, capsules, powders and more.</div>
  <div style='margin-top:18px'>{card(-4,.82)}</div>
</div>{foot(BF_FINE)}""")
add('B01-black-friday_story', 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,48)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:44px'>
  <div class='eb' style='color:{GOLD}'>Black Friday</div>
  <div class='hd' style='font-size:96px'>Black Friday ends.<br><i>Your membership<br>doesn't.</i></div>
  {card(-4,.78)}
  <div class='p' style='font-size:40px'>$49.99, paid once.</div>
</div>{foot(FINE_S,'center')}""")
for i, (eb, hd, sub) in enumerate([
        ('Black Friday', 'Most deals<br>last <i>a day.</i>', ''),
        ('EverLiv Founding Membership', 'This one lasts<br><i>12 months.</i>', 'Member pricing on every eligible order, as often as you shop.'),
        ('One payment', '$49.99.<br><i>No renewal.</i>', 'Up to 20% off eligible products, as often as you shop.'),
        ('Founding price to join', '$49.99 if you<br><i>join by Jan 31.</i>', 'Your membership lasts a full 12 months.<br>Join: link in bio.')]):
    add(f'B01R-bf-reel_f{i+1}', 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,46)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:46px'>
  {emblem(130) if i else ''}<div class='eb' style='color:{GOLD}'>{eb}</div><div class='hd' style='font-size:118px'>{hd}</div>
  {f"<div class='p' style='font-size:38px;opacity:.9'>{sub}</div>" if sub else ''}
</div>{foot(FINE_S,'center') if i == 3 else '<div></div>'}""")
add('B02-one-day-vs-year_s1', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:20px'>
  <div class='eb' style='color:#9C7A3A'>Black Friday, done differently</div>
  <div class='hd' style='font-size:92px;color:{LEAF}'>One day of deals.<br>Or <i>a year</i> of<br>member pricing.</div>
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:40px'>
    <div style='border:2px solid #DFDDD8;border-radius:28px;padding:40px'><div class='hd' style='font-size:150px;opacity:.4'>1</div><div class='p' style='font-size:30px;opacity:.6'>day of a typical<br>Black Friday deal</div></div>
    <div style='background:{LEAF};color:{IVORY};border-radius:28px;padding:40px;border:1.5px solid {GOLD}'><div class='hd' style='font-size:150px;color:{CHAMP}'>12</div><div class='p' style='font-size:30px'>months of member<br>pricing, $49.99 once</div></div>
  </div></div>
<div class='eb' style='font-size:20px;color:#3E5B41'>Swipe →</div>""")
add('B02-one-day-vs-year_s2', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:36px'>
  <div class='eb' style='color:#9C7A3A'>Why no Black Friday markdowns?</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>So membership<br>stays <i>worth it.</i></div>
  <div class='p' style='font-size:36px;max-width:880px'>We chose not to run one-day discounts for everyone. Members get up to 20% off eligible products every time they shop, for 12 months.</div>
</div>{foot(FINE_M)}""")
add('B02-one-day-vs-year_s3', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:38px;align-items:center;text-align:center'>
  {emblem(150)}<div class='hd' style='font-size:100px'>Choose <i>the year.</i></div>
  <div class='p' style='font-size:36px'>$49.99 once · up to 20% off for 12 months · join by Jan 31</div>
  <div class='btn' style='background:{CHAMP};color:{LEAF}'>everliv.life/pages/membership</div>
</div>{foot(FINE_M,'center')}""")
CART = [('NAD+', 59.99, 47.99, '20%'), ('Pure Creatine Monohydrate', 34.99, 29.74, '15%'), ('Hydrate Strips', 34.99, 27.99, '20%'), ('Charcoal Soap', 20.99, 17.84, '15%')]
def cart_table(c, mult=1):
    rows = ''.join(f"<tr><td>{n} <span style='opacity:.5;font-size:22px'>{r}</span></td><td class='r' style='opacity:.6'>${e:.2f}</td><td class='r'><b>${m:.2f}</b></td></tr>" for n, e, m, r in c)
    te = sum(x[1] for x in c); tm = sum(x[2] for x in c)
    return f"""<table class='t'><tr style='font-size:20px;letter-spacing:.14em;text-transform:uppercase;opacity:.6'><td>Item</td><td class='r'>Everyday</td><td class='r'>Member</td></tr>{rows}
    <tr><td><b>Order total</b></td><td class='r' style='opacity:.6'>${te:.2f}</td><td class='r'><b>${tm:.2f}</b></td></tr></table>"""
add('B03-real-cart_s1', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:#9C7A3A'>A real EverLiv cart</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>What membership <i>does,</i><br>and doesn't, do.</div>
  {cart_table(CART)}
  <div class='p' style='font-size:32px'>Gross saving on this order: <b>$27.40</b></div>
</div>{foot('Live everliv.life prices, Nov 16, 2026; may change. Your cart shows your exact price. ' + FINE_S)}""")
add('B03-real-cart_s2', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:30px'>
  <div class='eb' style='color:#9C7A3A'>Now count the fee</div>
  <table class='t' style='font-size:34px'>
   <tr><td>1 order like this</td><td class='r'>$27.40 saved</td><td class='r' style='color:#B81E1E'>−$22.59 net</td></tr>
   <tr><td>2 orders over 12 months</td><td class='r'>$54.80 saved</td><td class='r' style='color:#3E5B41'><b>+$4.81 net</b></td></tr>
   <tr><td>3 orders over 12 months</td><td class='r'>$82.20 saved</td><td class='r' style='color:#3E5B41'><b>+$32.21 net</b></td></tr></table>
  <div class='hd' style='font-size:66px;color:{LEAF};margin-top:20px'>One order won't do it.<br><i>Two will.</i></div>
</div>{foot('Net = gross product discount minus the $49.99 fee. Illustrative; savings depend on what you buy and aren\'t guaranteed. ' + FINE_S)}""")
add('B03-real-cart_s3', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:36px'>
  <div class='hd' style='font-size:96px'>Price <i>your</i> cart.</div>
  <div class='p' style='font-size:36px;max-width:860px'>Every product page shows its member price next to the everyday price. If two or more orders a year sound like you, membership is likely worth a look.</div>
  <div><div class='btn' style='background:{CHAMP};color:{LEAF}'>everliv.life/pages/membership</div></div>
</div>{foot(FINE_M)}""")
add('B04-cyber-monday_feed', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:{GOLD}'>Cyber Monday · Founding Members</div>
  <div class='hd' style='font-size:100px'>Cyber Monday is<br>one day. <i>Member<br>pricing lasts 12 months.</i></div>
  <div class='p' style='font-size:34px;opacity:.9'>No codes to chase. Up to 20% off for 12 months. $49.99, paid once.</div>
  <div style='display:flex;gap:22px;margin-top:20px'>{''.join(f"<div style='flex:1;border:1.5px solid {GOLD};border-radius:22px;padding:26px 22px'><div class='p' style='font-size:24px;opacity:.8'>{n}</div><div class='hd' style='font-size:58px;color:{CHAMP}'>${m}</div><div style='font-size:20px;opacity:.7'>everyday ${e}</div></div>" for n,e,m in [('Energy Strips','34.99','27.99'),('NAD+','59.99','47.99'),('β-NMN','49.99','39.99')])}</div>
</div>{foot(FINE_M)}""")
add('B04-cyber-monday_story', 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,48)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:46px'>
  {emblem(150)}<div class='eb' style='color:{GOLD}'>Cyber Monday</div>
  <div class='hd' style='font-size:110px'>One day.<br><i>Or 12 months.</i></div>
  <div class='p' style='font-size:40px'>Founding Membership · $49.99 once</div>
</div>{foot(FINE_S,'center')}""")

# ======================= PHASE C =======================
add('C01-giving-tuesday_feed', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='align-items:center;text-align:center;gap:44px'>
  <div class='eb' style='color:#3E5B41'>Giving Tuesday</div>
  <div class='hd' style='font-size:104px;color:{LEAF}'>Today is for <i>giving,</i><br>not selling.</div>
  <div class='rule' style='background:{LIME}'></div>
  <div class='p' style='font-size:34px;max-width:820px'>No offers from us today. Just thanks, and a nudge to support a cause close to you.</div>
</div><div></div>""")
def gift_slide(eb, hd, img, sub, price):
    return f"""{header(False, member=False)}
<div class='mid' style='gap:28px'>
  <div class='eb' style='color:#3E5B41'>{eb}</div>
  <div class='hd' style='font-size:78px;color:{LEAF}'>{hd}</div>
  <div class='photo' style='height:640px'><img src='{u(img)}'></div>
  <div class='row'><div class='p' style='font-size:30px'>{sub}</div><div class='hd' style='font-size:52px;color:{LEAF}'>{price}</div></div>
</div>{foot(AI + ' Free U.S. shipping on every order.')}"""
add('C02-gift-guide_s1', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='gap:32px'>
  <div class='eb' style='color:{LIME}'>The EverLiv Holiday Gift Guide</div>
  <div class='hd' style='font-size:104px'>Gifts that fit<br><i>real routines.</i></div>
  <div class='photo' style='height:520px'><img src='{u('everliv-holiday-gift-edit--mixed--desktop--desktop-1920x1072.png')}' style='object-position:50% 50%'></div>
</div>{foot(AI)}""")
add('C02-gift-guide_s2', 'feed', 'ivory', gift_slide('For the office', 'Coffee <i>they\'ll actually drink.</i>', 'everliv-hazelnut-coffee--stone-plinth--social-1080x1350.png', 'Hazelnut · Cocoa · Caramel · Mushroom', 'from $32.99'))
add('C02-gift-guide_s3', 'feed', 'ivory', gift_slide('For the self-care lover', 'Handmade <i>soaps.</i>', 'everliv-oat-milk-honey-soap--gift-flatlay--social-1080x1350.png', 'Six scents, handmade bars', '$20.99'))
add('C02-gift-guide_s4', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:#3E5B41'>For every stocking</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>Oral strips, <i>pocket-sized.</i></div>
  <img src='{u('strips-available-4--2x2--transparent.png')}' style='width:620px;align-self:center'>
  <div class='row'><div class='p' style='font-size:30px'>Energy · Hydrate · Iron · D3 + K2<br><b>Any 3 for $79.99</b> (Build Your Own Bundle)</div><div class='hd' style='font-size:52px;color:{LEAF}'>$34.99</div></div>
</div>{foot('Energy Strips contain caffeine; see each product page for warnings. Bundles have their own pricing.')}""")
add('C02-gift-guide_s5', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:36px'>
  <div class='eb' style='color:#3E5B41'>For the one who trains</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>Training-day <i>staples.</i></div>
  {tiles(['creatine','creatine_e'], 440)}
  <div class='row'><div class='p' style='font-size:30px'>Pure Creatine Monohydrate · Creatine+ Electrolytes</div><div class='hd' style='font-size:52px;color:{LEAF}'>$34.99</div></div>
</div>{foot('Ingredients, directions and warnings on each product page.')}""")
add('C02-gift-guide_s6', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='gap:38px'>
  <div class='hd' style='font-size:96px'>Free U.S. shipping<br><i>on every order.</i></div>
  <div class='p' style='font-size:34px;opacity:.9;max-width:860px'>Orders are processed in 1 to 3 business days. Shop the full gift guide at everliv.life.</div>
  <div><div class='btn' style='background:{IVORY};color:{LEAF}'>everliv.life</div></div>
  <div class='p' style='font-size:28px;opacity:.8;margin-top:30px'>Shopping for yourself too? Ask us about the Member Price Club.</div>
</div><div></div>""")
add('C03-office-coffee_feed', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:#3E5B41'>Gifts for the office</div>
  <div class='hd' style='font-size:92px;color:{LEAF}'>The easiest office gift:<br><i>good coffee.</i></div>
  <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:18px;align-items:end'>{''.join(f"<div style='text-align:center'><img src='{u(f)}' style='width:100%'><div class='p' style='font-size:24px;margin-top:8px'>{n}<br><b>${p}</b></div></div>" for f,n,p in [('everliv-hazelnut-coffee-medium-roast--front-cutout-v2.png','Hazelnut','32.99'),('everliv-cocoa-coffee-medium-roast--front-cutout-v2.png','Cocoa','32.99'),('everliv-caramel-coffee-dark-roast--front-cutout-v2.png','Caramel','32.99'),('everliv-mushroom-coffee-medium-roast--front-cutout-v2.png','Mushroom','37.99')])}</div>
</div>{foot('Free U.S. shipping on every order. Prices as of Nov 16, 2026.')}""")
add('C04-member-vs-subscribe_s1', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:32px'>
  <div class='eb' style='color:#9C7A3A'>Two ways to save</div>
  <div class='hd' style='font-size:90px;color:{LEAF}'>Membership or<br>Subscribe &amp; Save?<br><i>It depends.</i></div>
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:20px'>
   <div style='border:2px solid #DFDDD8;border-radius:26px;padding:34px'><div class='eb' style='font-size:20px;color:#3E5B41'>Subscribe &amp; Save</div><div class='p' style='font-size:28px;margin-top:14px'>Up to 15% off one product on a set schedule. No fee. Skip or cancel before billing.</div></div>
   <div style='background:{LEAF};color:{IVORY};border-radius:26px;padding:34px;border:1.5px solid {GOLD}'><div class='eb' style='font-size:20px;color:{GOLD}'>Membership</div><div class='p' style='font-size:28px;margin-top:14px'>Up to 20% off eligible products, whenever you shop, for 12 months. $49.99 once.</div></div></div>
</div><div class='eb' style='font-size:20px;color:#3E5B41'>Swipe →</div>""")
add('C04-member-vs-subscribe_s2', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:30px'>
  <div class='eb' style='color:#9C7A3A'>Example: one tin of Energy Strips a month</div>
  <table class='t' style='font-size:32px'><tr><td>Subscribe &amp; Save ($29.74 × 12)</td><td class='r'><b>$63.00 saved</b></td></tr>
   <tr><td>Membership ($27.99 × 12, minus $49.99)</td><td class='r'><b>$34.01 net</b></td></tr></table>
  <div class='hd' style='font-size:66px;color:{LEAF}'>Same product, every month?<br><i>Subscribe &amp; Save wins.</i></div>
  <div class='p' style='font-size:32px'>Membership fits better when you buy a mix of products, on your own schedule.</div>
</div>{foot('Illustrative, live prices Nov 16, 2026. Programs don\'t combine. Subscribe &amp; Save availability varies by product. ' + FINE_S)}""")
add('C05-stocking-strips_feed', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:{LIME}'>Stocking stuffers</div>
  <div class='hd' style='font-size:96px'>The stocking stuffer<br>that fits <i>in a pocket.</i></div>
  <img src='{u('strips-available-4--row--transparent.png')}' style='width:100%'>
  <div class='p' style='font-size:32px'>30 strips per tin, $34.99 · <b>Any 3 for $79.99</b></div>
</div>{foot('Energy Strips contain caffeine; see product pages for warnings. Build Your Own Bundle has its own pricing (no member price).')}""")
add('C06-card-reminder_feed', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:40px'>
  <div class='eb' style='color:#9C7A3A'>Founding Members</div>
  <div class='hd' style='font-size:100px;color:{LEAF}'>A year of member pricing.<br><i>$49.99, paid once.</i></div>
  <div style='margin-top:30px'>{card(-4, .95)}</div>
</div>{foot(FINE_M)}""")
add('C07-soap-gifts_s1', 'feed', 'ivory', gift_slide('Self-care gifts', 'Six handmade soaps.<br><i>One easy gift.</i>', 'everliv-soap-collection--travertine--mobile--mobile-social-1080x1350.png', 'Charcoal · Slumber · Oat Milk Honey · Sandalwood · Coconut Beach · Aloe &amp; Cucumber', '$20.99'))
add('C07-soap-gifts_s2', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:30px'>
  <div class='hd' style='font-size:76px;color:{LEAF}'>Pick a <i>scent.</i></div>
  <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:26px'>{''.join(f"<div style='text-align:center'><img src='{u(f)}' style='width:100%'><div class='p' style='font-size:24px'>{n}</div></div>" for f,n in [('everliv-charcoal-soap--front-cutout-v2.png','Charcoal'),('everliv-clean-forrest-soap--front-cutout-v2.png','Slumber'),('everliv-milk-honey-soap--front-cutout-v2.png','Oat Milk Honey'),('everliv-sandalwood-soap--front-cutout-v2.png','Rich Sandalwood'),('coconut-beach-soap--front-cutout-v2.png','Coconut Beach'),('everliv-aloe-cool-cucumber-soap--front-cutout-v2.png','Aloe &amp; Cool Cucumber')])}</div>
  <div class='p' style='font-size:30px;text-align:center'>$20.99 each · free U.S. shipping</div>
</div><div></div>""")
add('C08-training-gifts_feed', 'feed', 'ivory', gift_slide('For the one who trains', 'For the friend whose <i>gym bag is always packed.</i>', 'everliv-pure-creatine-monohydrate.jpg', 'Pure Creatine Monohydrate', '$34.99').replace(AI + ' ', ''))
C3 = [('NAD+', 59.99, 47.99, '20%'), ('Hydrate Strips', 34.99, 27.99, '20%'), ('Pure Creatine Monohydrate', 34.99, 29.74, '15%')]
add('C09-member-math-3-orders_s1', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:30px'>
  <div class='eb' style='color:#9C7A3A'>Member math · worked example</div>
  <div class='hd' style='font-size:80px;color:{LEAF}'>Three orders.<br><i>One year.</i></div>
  {cart_table(C3)}
  <div class='p' style='font-size:30px'>Bought three times over 12 months:</div>
  <table class='t' style='font-size:32px'><tr><td>Everyday</td><td class='r'>$389.91</td></tr><tr><td>Member</td><td class='r'>$317.16</td></tr>
   <tr><td>Gross saving</td><td class='r'>$72.75</td></tr><tr><td><b>Net after $49.99 fee</b></td><td class='r'><b>$22.76</b></td></tr></table>
</div>{foot('Illustrative; live prices Nov 16, 2026. Savings depend on what you buy and aren\'t guaranteed. ' + FINE_S)}""")
add('C10-longevity-pair_feed', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:#9C7A3A'>The Longevity Series</div>
  <div class='hd' style='font-size:86px;color:{LEAF}'>NAD+ and <i>β-NMN.</i></div>
  {tiles(['nad','nmn'], 420)}
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:28px;text-align:center'>
   <div><div class='p' style='font-size:26px;opacity:.6'>Everyday $59.99</div><div class='tag' style='color:{LEAF};margin-top:8px'>{leaf(22)}Member</div><div class='hd' style='font-size:64px;color:{LEAF}'>$47.99</div></div>
   <div><div class='p' style='font-size:26px;opacity:.6'>Everyday $49.99</div><div class='tag' style='color:{LEAF};margin-top:8px'>{leaf(22)}Member</div><div class='hd' style='font-size:64px;color:{LEAF}'>$39.99</div></div></div>
</div>{foot('Full labels, ingredients and directions on each product page. ' + FINE_S)}""")
add('C12-read-the-label-energy_s1', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:#3E5B41'>Read the label</div>
  <div class='hd' style='font-size:92px;color:{LEAF}'>What's in an<br><i>Energy Strip?</i></div>
  <div style='display:flex;gap:40px;align-items:center'>
   <div class='tile' style='width:400px;height:400px;flex:none'><img src='{u('energy-strips--front.jpg')}'></div>
   <table class='t' style='font-size:32px'><tr><td>Caffeine (green tea)</td><td class='r'><b>50 mg</b></td></tr><tr><td>L-theanine</td><td class='r'><b>30 mg</b></td></tr><tr><td>Vitamin B12</td><td class='r'><b>per label</b></td></tr><tr><td>Flavor</td><td class='r'>Cranberry</td></tr></table></div>
</div>{foot('Contains caffeine. Not for children, pregnant or nursing women, or anyone sensitive to caffeine. Amounts per strip as printed on the Supplement Facts; check the label on the product page.')}""")
add('C13-order-timing_feed', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:40px'>
  <div class='eb' style='color:#3E5B41'>Holiday timing</div>
  <div class='hd' style='font-size:96px;color:{LEAF}'>How holiday<br><i>timing works.</i></div>
  <table class='t' style='font-size:34px'><tr><td>Processing</td><td class='r'><b>1–3 business days</b></td></tr><tr><td>Delivery after that</td><td class='r'><b>typically 3–7 days</b></td></tr><tr><td>U.S. shipping</td><td class='r'><b>Free, every order</b></td></tr></table>
  <div class='p' style='font-size:32px'>The earlier you order, the more breathing room you have.</div>
</div>{foot('Per EverLiv shipping policy. Delivery times are estimates, not guarantees.')}""")
FAQ = [('Does it renew automatically?', 'No. One payment covers 12 months. Nothing renews on its own.'),
       ('Is everything 20% off?', 'No. 15% or 20%, depending on the product. Some products are excluded.'),
       ('Does it combine with Subscribe &amp; Save?', 'No. Member pricing applies to regular orders, not Subscribe &amp; Save subscriptions. Shop as often as you like.'),
       ('What if I change my mind?', 'Full refund within 3 business days. Other refund rules are in the Membership Terms.')]
add('C14-member-faq_s1', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:30px'>
  <div class='eb' style='color:#9C7A3A'>Member Price Club FAQ</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>Your questions,<br><i>answered.</i></div>
  {''.join(f"<div><div class='p' style='font-size:32px;font-weight:700'>{q}</div><div class='p' style='font-size:29px;opacity:.8'>{a}</div></div>" for q,a in FAQ)}
</div>{foot('Full terms: everliv.life/pages/membership-terms. Not available to residents of CA or NC.')}""")
add('C15-edit-under-35_feed', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:30px'>
  <div class='eb' style='color:#3E5B41'>The EverLiv Edit</div>
  <div class='hd' style='font-size:96px;color:{LEAF}'>Gifts <i>under $35.</i></div>
  <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:24px;align-items:end'>
   <div style='text-align:center'><img src='{u('everliv-milk-honey-soap--front-cutout-v2.png')}' style='width:100%'><div class='p' style='font-size:26px'>Handmade soap<br><b>$20.99</b></div></div>
   <div style='text-align:center'><img src='{u('everliv-cocoa-coffee-medium-roast--front-cutout-v2.png')}' style='width:80%'><div class='p' style='font-size:26px'>Hazelnut, Cocoa or Caramel coffee<br><b>$32.99</b></div></div>
   <div style='text-align:center'><img src='{u('energy-strips--front.jpg')}' style='width:100%;border-radius:20px'><div class='p' style='font-size:26px'>Any oral strip tin<br><b>$34.99</b></div></div></div>
</div>{foot('Prices as of Nov 16, 2026. Free U.S. shipping on every order. Energy Strips contain caffeine.')}""")
add('C17-gift-yourself_feed', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:36px'>
  <div class='eb' style='color:{GOLD}'>For you, this time</div>
  <div class='hd' style='font-size:100px'>Done shopping for<br>everyone else?<br><i>This one's yours.</i></div>
  <div style='margin-top:26px'>{card(-4,.88)}</div>
</div>{foot(FINE_M + ' Membership is for personal use by the account holder.')}""")

# ======================= PHASE D =======================
add('D01-start-before-january_feed', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:40px'>
  <div class='hd' style='font-size:120px;color:{LEAF}'>You don't have<br>to wait for <i>January.</i></div>
  <div class='rule' style='background:{LIME}'></div>
  <div class='p' style='font-size:36px;max-width:860px'>Routines that last rarely start on January 1. They start on an ordinary Monday.</div>
</div><div class='eb' style='font-size:20px;color:#3E5B41'>everliv.life</div>""")
HAB = ['A glass of water, first thing', 'A set time for your daily capsule', 'A coffee you actually look forward to', 'A two-minute evening wind-down', 'One new product at a time']
add('D02-consistency_s1', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:{LIME}'>Five small habits</div>
  <div class='hd' style='font-size:104px'>Consistency<br>beats <i>intensity.</i></div>
  {''.join(f"<div class='row' style='justify-content:flex-start;gap:26px;font-size:32px'><span class='hd' style='font-size:46px;color:{LIME};width:40px'>{i+1}</span>{h}</div>" for i,h in enumerate(HAB))}
</div><div class='eb' style='font-size:20px;color:{LIME}'>No quick fixes. Just routines that fit.</div>""")
add('D04-holiday-greeting_feed', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='align-items:center;text-align:center;gap:40px'>
  <div class='hd' style='font-size:118px'>Happy <i>holidays.</i></div><div class='rule' style='background:{LIME}'></div>
  <div class='p' style='font-size:34px;opacity:.9'>Wishing you a calm, warm and well-rested season.<br>From all of us at EverLiv.</div>
</div><div></div>""")
add('D05-year-ahead_feed', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:36px'>
  <div class='eb' style='color:{GOLD}'>Founding Members</div>
  <div class='hd' style='font-size:88px'>Twelve months.<br>Every eligible order.<br><i>One payment.</i></div>
  <div class='p' style='font-size:34px;opacity:.9'>Join this week and your 12 months cover nearly all of 2027.</div>
  <div style='margin-top:12px'>{card(-4,.72)}</div>
</div>{foot(FINE_M)}""")
add('D06-find-your-format_s1', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:34px'>
  <div class='hd' style='font-size:92px;color:{LEAF}'>Strips, capsules<br>or powders: <i>what<br>fits your day?</i></div>
  <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:22px;text-align:center'>
   <div><div class='tile' style='height:300px'><img src='{u('energy-strips--front.jpg')}'></div><div class='p' style='font-size:28px;margin-top:12px'><b>Strips</b><br>dissolve on the tongue</div></div>
   <div><div class='tile' style='height:300px'><img src='{u('everliv-nad.jpg')}'></div><div class='p' style='font-size:28px;margin-top:12px'><b>Capsules</b><br>the classic routine</div></div>
   <div><div class='tile' style='height:300px'><img src='{u('everliv-pure-creatine-monohydrate.jpg')}'></div><div class='p' style='font-size:28px;margin-top:12px'><b>Powders</b><br>mix into anything</div></div></div>
  <div class='p' style='font-size:32px'>Tell us in the comments.</div>
</div><div></div>""")
add('D07-routine-2027_s1', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:28px'>
  <div class='eb' style='color:#9C7A3A'>Build your 2027 routine</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>One product for each<br><i>moment of your day.</i></div>
  <table class='t' style='font-size:32px'><tr><td>Morning</td><td class='r'>Coffee or Energy Strips</td></tr><tr><td>Midday</td><td class='r'>Hydrate Strips</td></tr><tr><td>Training days</td><td class='r'>Pure Creatine Monohydrate</td></tr><tr><td>Evening</td><td class='r'>A handmade soap</td></tr></table>
  <div class='p' style='font-size:30px'>Members get up to 20% off eligible products for a full 12 months.</div>
</div>{foot(FINE_M)}""")
add('D09-one-month-left_feed', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:38px'>
  <div class='eb' style='color:{GOLD}'>Founding price</div>
  <div class='hd' style='font-size:118px'>One month left<br>to join at <i>$49.99.</i></div>
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:24px'>
   <div style='border:1.5px solid {GOLD};border-radius:26px;padding:34px'><div class='eb' style='font-size:20px;color:{GOLD}'>Join by Jan 31, 2027</div><div class='hd' style='font-size:84px;color:{CHAMP};margin-top:10px'>$49.99</div></div>
   <div style='border:1.5px solid rgba(233,228,223,.3);border-radius:26px;padding:34px;opacity:.7'><div class='eb' style='font-size:20px'>Join from Feb 1, 2027</div><div class='hd' style='font-size:84px;margin-top:10px'>$69.99</div></div></div>
  <div class='p' style='font-size:32px;opacity:.9'>Either way, your membership lasts a full 12 months.</div>
</div>{foot(FINE_M)}""")
add('D10-year-of-more_feed', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='align-items:center;text-align:center;gap:40px'>
  <div class='hd' style='font-size:124px'>Here's to<br>a year of <i>more.</i></div>
  <div class='rule'></div>
  <div class='p' style='font-size:34px;opacity:.9'>More routines that fit. More to discover.<br>Happy New Year from EverLiv.</div>
  <div class='p' style='font-size:28px;color:{CHAMP}'>{leaf(24)} Join by Jan 31 for the $49.99 founding price</div>
</div>{foot(FINE_S,'center')}""")
add('D08-discover-whats-next_feed', 'feed', 'ivory', f"""{header(False, member=False)}
<div class='mid' style='gap:40px'>
  <div class='eb' style='color:#3E5B41'>A new series</div>
  <div class='hd' style='font-size:110px;color:{LEAF}'>Discover<br><i>what's next.</i></div>
  <div class='p' style='font-size:36px;max-width:860px'>Your wellness journey evolves. So does EverLiv. Follow along as the range grows.</div>
</div><div></div>""")

# ======================= Email headers + story templates =======================
add('E01-email-header', 'email', 'green', f"""<div class='row'>{logo(True,40)}<div class='tag' style='color:{GOLD};font-size:16px'>{leaf(20)}Member Price Club</div></div>
<div style='display:grid;grid-template-columns:1.05fr 1fr;align-items:center'><div><div class='eb' style='color:{GOLD};font-size:18px'>Black Friday · Founding Members</div>
<div class='hd' style='font-size:66px;margin-top:16px'>Become a<br><i>Founding Member.</i></div><div class='p' style='font-size:24px;margin-top:16px'>Up to 20% off for 12 months.<br><b>$49.99, paid once.</b></div></div>
{card(-4,.72)}</div><div></div>""")
add('E02-email-header', 'email', 'green', f"""<div class='row'>{logo(True,40)}<div class='tag' style='color:{GOLD};font-size:16px'>{leaf(20)}Member Price Club</div></div>
<div style='display:grid;grid-template-columns:1.1fr 1fr;align-items:center'><div><div class='eb' style='color:{GOLD};font-size:18px'>Cyber Monday</div>
<div class='hd' style='font-size:64px;margin-top:16px'>One day.<br><i>Or 12 months.</i></div><div class='p' style='font-size:24px;margin-top:16px'>Founding Membership · $49.99 once</div></div>
<div style='display:flex;justify-content:center'>{emblem(230)}</div></div><div></div>""")
for i, (eb, hd) in enumerate([('Founding Members', 'Your headline<br><i>goes here.</i>'), ('Poll', 'Coffee or<br><i>soap?</i>'), ('Did you know?', 'Member pricing lasts<br><i>12 months.</i>'), ('Founding price to join', '$49.99 if you<br><i>join by Jan 31.</i>')]):
    add(f'stories/story-template-{i+1}', 'story', 'green' if i % 2 == 0 else 'ivory', f"""<div style='display:flex;justify-content:center'>{logo(i % 2 == 0,46)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:50px'>{emblem(140) if i != 1 else ''}<div class='eb' style='color:{GOLD if i % 2 == 0 else '#9C7A3A'}'>{eb}</div>
<div class='hd' style='font-size:108px;{'' if i % 2 == 0 else 'color:' + LEAF}'>{hd}</div>
<div style='width:720px;height:190px;border-radius:28px;border:2px dashed {'rgba(233,228,223,.35)' if i % 2 == 0 else 'rgba(42,66,42,.25)'}'></div></div>
{foot(FINE_S,'center') if i != 1 else '<div></div>'}""")

for i, (eb, hd, sub) in enumerate([
        ('The honest math', '$49.99<br><i>÷ 20%</i>', ''),
        ('On 20% products', '= <i>$249.95</i>', 'of eligible purchases covers the fee.'),
        ('On 15% products', '≈ <i>$333</i>', 'A mix of both lands in between.'),
        ('Above that', 'Member pricing<br><i>keeps working.</i>', 'For the rest of your 12 months. Savings aren\'t guaranteed to exceed the fee.')]):
    add(f'C19-math-reel_f{i+1}', 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,46)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:46px'>
  {emblem(120)}<div class='eb' style='color:{GOLD}'>{eb}</div><div class='hd' style='font-size:130px'>{hd}</div>
  {f"<div class='p' style='font-size:38px;opacity:.9;max-width:820px'>{sub}</div>" if sub else ''}
</div>{foot(FINE_S,'center') if i == 3 else '<div></div>'}""")

# ======================= BACKUP CONCEPTS (genuinely different directions) =======================
add('ALT-A04-1-new-chapter_feed', 'feed', 'champ', f"""{header(False)}
<div class='mid' style='align-items:center;text-align:center;gap:44px'>
  {emblem(260)}
  <div class='hd' style='font-size:104px;color:{LEAF}'>A new chapter<br>of <i>EverLiv.</i></div>
  <div class='p' style='font-size:34px'>The Member Price Club is here. Join for $49.99 and enjoy<br>up to 20% off eligible products for a full 12 months.</div>
</div>{foot(FINE_M,'center')}""")
add('ALT-A04-2-your-year_feed', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:30px'>
  <div class='hd' style='font-size:92px;color:{LEAF};margin-top:20px'>Your year.<br>Your wellness.<br><i>Your member price.</i></div>
  <div style='display:grid;grid-template-columns:1fr 1fr;gap:22px'>
    <div class='photo' style='height:420px'><img src='{u('everliv-caramel-coffee--holiday-kitchen--social-1080x1350.png')}'></div>
    <div class='photo' style='height:420px'><img src='{u('everliv-slumber-soap--spa-counter--social-1080x1350.png')}'></div></div>
  <div class='p' style='font-size:32px'>Founding Membership: $49.99 once, 12 months.</div>
</div>{foot(AI + ' ' + FINE_S)}""")
add('ALT-B01-2-launching-a-year_feed', 'feed', 'ivory', f"""{header(False)}
<div class='mid' style='gap:30px'>
  <div class='eb' style='color:#9C7A3A'>Black Friday at EverLiv</div>
  <div class='hd' style='font-size:300px;color:{GOLD};line-height:.85'>365</div>
  <div class='hd' style='font-size:84px;color:{LEAF}'>The only thing we're<br>launching is <i>a year.</i></div>
  <div class='p' style='font-size:32px'>Founding Membership: up to 20% off eligible products for 12 months. $49.99 once.</div>
</div>{foot(FINE_M)}""")
add('ALT-B04-1-no-codes_feed', 'feed', 'green', f"""{header(True)}
<div class='mid' style='gap:26px'>
  <div class='hd' style='font-size:116px;opacity:.35;text-decoration:line-through;text-decoration-thickness:4px'>Codes.</div>
  <div class='hd' style='font-size:116px;opacity:.35;text-decoration:line-through;text-decoration-thickness:4px'>Countdown clocks.</div>
  <div class='hd' style='font-size:116px'>Just <i>a year.</i></div>
  <div class='p' style='font-size:34px;opacity:.9'>Cyber Monday at EverLiv: Founding Membership, $49.99 once, up to 20% off for 12 months.</div>
</div>{foot(FINE_M)}""")
add('ALT-C02-1-give-the-routine_feed', 'feed', 'champ', f"""{header(False, member=False)}
<div class='mid' style='gap:34px'>
  <div class='eb' style='color:#3E5B41'>Holiday Gift Guide</div>
  <div class='hd' style='font-size:100px;color:{LEAF}'>Give the routine,<br><i>not the clutter.</i></div>
  <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;align-items:end'>
    <img src='{u('everliv-caramel-coffee-dark-roast--front-cutout-v2.png')}' style='width:100%'>
    <img src='{u('everliv-sandalwood-soap--front-cutout-v2.png')}' style='width:100%'>
    <img src='{u('everliv-milk-honey-soap--front-cutout-v2.png')}' style='width:100%'></div>
  <div class='p' style='font-size:32px'>Coffee from $32.99 · handmade soap $20.99 · free U.S. shipping</div>
</div><div></div>""")
add('ALT-D10-1-your-wellness-evolves_feed', 'feed', 'green', f"""{header(True, member=False)}
<div class='mid' style='gap:40px'>
  <div class='hd' style='font-size:110px'>Your wellness<br>journey evolves.<br><i>So does EverLiv.</i></div>
  <img src='{u('strips-available-4--row--transparent.png')}' style='width:100%'>
  <div class='p' style='font-size:32px;opacity:.9'>Happy New Year. Here's to what's next.</div>
</div><div></div>""")

# ======================= Reels from approved stills =======================
def still_frame(name, img, eb, hd, last=False, fine=AI):
    add(name, 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,46)}</div>
<div class='mid' style='gap:44px'>
  <div class='photo' style='height:960px'><img src='{u(img)}'></div>
  <div style='text-align:center'><div class='eb' style='color:{LIME}'>{eb}</div><div class='hd' style='font-size:84px;margin-top:18px'>{hd}</div></div>
</div>{foot(fine,'center')}""")
still_frame('C02R-gift-reel_f1', 'everliv-hazelnut-coffee--stone-plinth--social-1080x1350.png', 'For the office', 'Coffee they\'ll <i>actually drink.</i>')
still_frame('C02R-gift-reel_f2', 'everliv-oat-milk-honey-soap--gift-flatlay--social-1080x1350.png', 'For the self-care lover', 'Handmade <i>soaps.</i>')
still_frame('C02R-gift-reel_f3', 'everliv-coconut-beach-soap--gift-flatlay--social-1080x1350.png', 'From $20.99', 'Six scents, <i>handmade.</i>')
still_frame('C02R-gift-reel_f4', 'everliv-cocoa-coffee--holiday-kitchen--social-1080x1350.png', 'Free U.S. shipping', 'Shop the <i>gift guide.</i>', fine=AI + ' Free U.S. shipping on every order.')
still_frame('C16-last-minute-reel_f1', 'everliv-caramel-coffee--holiday-kitchen--social-1080x1350.png', 'Still shopping?', 'A good <i>coffee.</i>')
still_frame('C16-last-minute-reel_f2', 'everliv-rich-sandalwood-soap--gift-flatlay--social-1080x1350.png', 'Or', 'A handmade <i>soap.</i>')
add('C16-last-minute-reel_f3', 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,46)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:50px'>
  <img src='{u('strips-available-4--2x2--transparent.png')}' style='width:760px'>
  <div class='eb' style='color:{LIME}'>Or</div><div class='hd' style='font-size:90px'>A tin of <i>oral strips.</i></div>
  <div class='p' style='font-size:34px;opacity:.9'>Free U.S. shipping · orders processed in 1–3 business days</div>
</div>{foot('Delivery times are estimates. Energy Strips contain caffeine.','center')}""")
still_frame('D03-morning-ritual-reel_f1', 'everliv-cocoa-coffee--holiday-kitchen--social-1080x1350.png', 'Step one', 'A coffee you <i>look forward to.</i>')
add('D03-morning-ritual-reel_f2', 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,46)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:50px'>
  <div class='tile' style='width:760px;height:760px'><img src='{u('energy-strips--front.jpg')}'></div>
  <div class='eb' style='color:{LIME}'>Step two</div><div class='hd' style='font-size:90px'>A strip, <i>no water needed.</i></div>
</div>{foot('Energy Strips contain caffeine. Not for children, pregnant or nursing women, or anyone sensitive to caffeine.','center')}""")
add('D03-morning-ritual-reel_f3', 'story', 'green', f"""<div style='display:flex;justify-content:center'>{logo(True,46)}</div>
<div class='mid' style='align-items:center;text-align:center;gap:40px'><div class='eb' style='color:{LIME}'>Step three</div>
  <div class='hd' style='font-size:120px'>A minute<br>of <i>stillness.</i></div></div><div></div>""")
still_frame('D03-morning-ritual-reel_f4', 'everliv-aloe-cool-cucumber-soap--spa-counter--social-1080x1350.png', 'Then', 'The day <i>is yours.</i>')

async def main(only=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page(device_scale_factor=1)
        done = []
        for name, (fmt, cls, body) in A.items():
            if only and not any(name.startswith(o) for o in only): continue
            w, h, _ = SIZES[fmt]; out = OUT/f'{name}.png'; out.parent.mkdir(parents=True, exist_ok=True)
            html = OUT/'_html'/f'{name}.html'; html.parent.mkdir(parents=True, exist_ok=True); html.write_text(page(fmt, cls, body))
            await pg.set_viewport_size({'width': w, 'height': h}); await pg.goto(html.as_uri())
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(250)
            ov = await pg.evaluate("""()=>{const f=document.querySelector('.f');const r=f.getBoundingClientRect();const bad=[];
              for(const el of f.querySelectorAll('*')){const b=el.getBoundingClientRect();if(b.width&&b.height&&(b.right>r.right+1||b.bottom>r.bottom+1||b.left<r.left-1||b.top<r.top-1)){bad.push(el.tagName+'.'+el.className)}}
              const g=[...f.children].map(c=>c.scrollHeight>c.clientHeight+2?c.className:null).filter(Boolean);return bad.slice(0,5).concat(g)}""")
            await pg.screenshot(path=str(out)); done.append((name, ov))
        await b.close()
    for n, ov in done: print(n, ('OVERFLOW ' + str(ov)) if ov else 'ok')
if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:] or None))
