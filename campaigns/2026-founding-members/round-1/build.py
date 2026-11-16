"""EverLiv Founding Member campaign: round-1 creatives (HTML -> PNG via headless Chrome).
Product imagery: supplier renders used whole (square tiles) or the verified six-tin family cut-out; never redrawn.
Prices verified live on everliv.life, Nov 16 2026 ~9:35 AM ET."""
import pathlib, asyncio
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).parent; SRC = ROOT/'src'; OUT = ROOT/'out'; OUT.mkdir(exist_ok=True)
IVORY='#E9E4DF'; LEAF='#2A422A'; FRESH='#8BC343'; INK='#1E2B1E'
def u(f): return (SRC/f).resolve().as_uri()

BASE = f"""
@font-face{{font-family:'NR';src:url({u('newsreader-latin-400-normal.woff2')});font-weight:400}}
@font-face{{font-family:'NR';src:url({u('newsreader-latin-400-italic.woff2')});font-weight:400;font-style:italic}}
@font-face{{font-family:'NR';src:url({u('newsreader-latin-500-normal.woff2')});font-weight:500}}
@font-face{{font-family:'FT';src:url({u('figtree-latin-wght-normal.woff2')});font-weight:300 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:var(--w);height:var(--h);overflow:hidden;font-family:FT;-webkit-font-smoothing:antialiased}}
.frame{{position:relative;width:var(--w);height:var(--h);overflow:hidden}}
.green{{background:{LEAF};color:{IVORY}}}
.ivory{{background:{IVORY};color:{INK}}}
.serif{{font-family:NR;font-weight:400;letter-spacing:-0.015em}}
.eyebrow{{font-family:FT;font-weight:650;font-size:24px;letter-spacing:.2em;text-transform:uppercase}}
.fine{{font-family:FT;font-weight:450;font-size:22px;line-height:1.4;opacity:.78}}
.logo{{position:absolute;height:50px}}
.rule{{height:2px;background:{FRESH};width:72px}}
.card{{position:absolute;width:640px;height:400px;border-radius:30px;padding:44px 48px;
  background:linear-gradient(140deg,#355235 0%,{LEAF} 55%,#1f331f 100%);color:{IVORY};
  box-shadow:0 40px 80px -30px rgba(20,35,20,.55),0 0 0 1px rgba(255,255,255,.06) inset}}
.card .top{{display:flex;justify-content:space-between;align-items:center}}
.card .club{{font-size:19px;font-weight:650;letter-spacing:.22em;text-transform:uppercase;opacity:.85}}
.card .fm{{position:absolute;left:48px;bottom:92px;font-family:NR;font-style:italic;font-size:64px;line-height:1}}
.card .meta{{position:absolute;left:48px;right:48px;bottom:40px;display:flex;justify-content:space-between;
  font-size:21px;font-weight:550;letter-spacing:.12em;text-transform:uppercase;opacity:.8}}
.card .line{{position:absolute;left:48px;bottom:76px;width:56px;height:2px;background:{FRESH}}}
.tile{{background:#F7F7F7;border-radius:22px;overflow:hidden;box-shadow:0 18px 40px -24px rgba(30,43,30,.45)}}
.tile img{{width:100%;height:100%;object-fit:cover;display:block}}
.price-old{{text-decoration:line-through;opacity:.55}}
"""
def card(x,y,rot=0,scale=1,ondark=False):
    extra = "background:linear-gradient(140deg,#4a6b47 0%,#33503 2 55%,#253d25 100%);border:1.5px solid rgba(233,228,223,.35);box-shadow:0 40px 90px -30px rgba(0,0,0,.6)".replace("#33503 2","#335032") if ondark else ""
    return f"""<div class="card" style="left:{x}px;top:{y}px;transform:rotate({rot}deg) scale({scale});transform-origin:center;{extra}">
      <div class="top"><img src="{u('logo-white.svg')}" style="height:40px"><div class="club">Member Price Club</div></div>
      <div class="fm">Founding Member</div><div class="line"></div>
      <div class="meta"><span>12 months</span><span>Paid once</span></div></div>"""

FINE_FEED = ("Founding price $49.99 for memberships bought through Jan 31, 2027 (ET); $69.99 from Feb 1, 2027. One payment; 12 months from activation; no automatic renewal. "
             "Member pricing applies to every eligible one-time product purchase during your membership (not Subscribe & Save): 20% or 15% off depending on the product, some products excluded. "
             "Savings depend on what you buy. Not available to residents of CA or NC. Terms at everliv.life.")

def page(w,h,body,cls='green'):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{--w:{w}px;--h:{h}px}}{BASE}</style></head><body><div class='frame {cls}'>{body}</div></body></html>"

A = {}
# ---------- A. Launch graphic (Black Friday), 1080x1350 ----------
A['FM-01-launch-black-friday_1080x1350'] = (1080,1350,'green',f"""
<img class="logo" src="{u('logo-white.svg')}" style="left:84px;top:78px">
<div class="eyebrow" style="position:absolute;left:84px;top:196px;color:{FRESH}">Black Friday · Founding Member Launch</div>
<div class="serif" style="position:absolute;left:80px;top:248px;font-size:104px;line-height:1.0">Become a<br>Founding Member.</div>
<div style="position:absolute;left:84px;top:492px;font-size:36px;line-height:1.35;font-weight:450;opacity:.92">A full year of member pricing.<br><b style="font-weight:700;color:#fff">$49.99, paid once.</b></div>
<div style="position:absolute;left:84px;top:600px;font-size:25px;line-height:1.4;color:{FRESH};font-weight:600">Member prices on every eligible order, as often as you shop:<br>strips, capsules, powders and more.</div>
{card(220,712,-5,0.94,True)}
<div class="fine" style="position:absolute;left:84px;right:84px;bottom:56px">{FINE_FEED}</div>
""")

# ---------- B. Carousel, 5 slides 1080x1350 ----------
A['FM-02-carousel-1-cover_1080x1350'] = (1080,1350,'ivory',f"""
<img class="logo" src="{u('logo.svg')}" style="left:84px;top:78px">
<div class="eyebrow" style="position:absolute;left:84px;top:196px;color:{LEAF}">EverLiv Founding Members</div>
<div class="serif" style="position:absolute;left:80px;top:248px;font-size:104px;line-height:1.0;color:{LEAF}">Become a<br>Founding Member.</div>
<div style="position:absolute;left:84px;top:500px;font-size:36px;line-height:1.35;font-weight:450">A full year of member pricing.<br><b style="font-weight:700">$49.99, paid once.</b></div>
{card(220,700,-5)}
<div style="position:absolute;right:84px;bottom:70px;font-size:24px;font-weight:600;letter-spacing:.08em;color:{LEAF}">SWIPE →</div>
""")

A['FM-02-carousel-2-what-you-get_1080x1350'] = (1080,1350,'ivory',f"""
<img class="logo" src="{u('logo.svg')}" style="left:84px;top:78px;height:40px">
<div class="eyebrow" style="position:absolute;left:84px;top:180px;color:{LEAF}">How it works</div>
<div class="serif" style="position:absolute;left:80px;top:230px;font-size:84px;line-height:1.02;color:{LEAF}">One payment.<br>Twelve months<br>of member pricing.</div>
<div style="position:absolute;left:84px;right:84px;top:600px;display:grid;gap:34px">
 {''.join(f'<div style="display:flex;gap:30px;align-items:flex-start"><div class="serif" style="font-size:54px;line-height:1;color:{FRESH};width:56px;font-weight:500">{n}</div><div><div style="font-size:36px;font-weight:700;line-height:1.2">{t}</div><div style="font-size:27px;line-height:1.4;opacity:.75;margin-top:6px">{d}</div></div></div>' for n,t,d in [
  ('1','$49.99, charged once','Founding price through January 31, 2027. $69.99 from February 1, 2027.'),
  ('2','Up to 20% off eligible products','20% or 15% off depending on the product, across strips, capsules and powders. Some products excluded. Each product page shows its member price.'),
  ('3','Shop as often as you like','Member pricing applies every time you buy an eligible product during your 12 months. No product subscription required.'),
  ('4','No automatic renewal','Your membership ends after 12 months unless you choose to join again.')])}
</div>
<div class="fine" style="position:absolute;left:84px;right:84px;bottom:56px">Doesn't combine with Subscribe &amp; Save, bundles or promo codes. Not available to residents of CA or NC.</div>
""")

def ex(img,name,reg,mem,pct):
    return f"""<div style="display:flex;gap:40px;align-items:center">
     <div class="tile" style="width:270px;height:270px;flex:none"><img src="{u(img)}"></div>
     <div style="flex:1"><div style="font-size:38px;font-weight:750;line-height:1.15">{name}</div>
       <div style="display:flex;gap:44px;align-items:flex-end;margin-top:20px">
         <div><div style="font-size:21px;font-weight:700;letter-spacing:.14em;opacity:.6">EVERYDAY</div>
              <div style="font-size:44px;font-weight:500;line-height:1.1;margin-top:10px;margin-bottom:10px;opacity:.6">${reg}</div></div>
         <div><div style="font-size:21px;font-weight:750;letter-spacing:.14em;color:{LEAF}">MEMBER · {pct}% OFF</div>
              <div class="serif" style="font-size:92px;line-height:1.05;margin-top:12px;color:{LEAF};font-weight:500">${mem}</div></div>
       </div></div></div>"""
A['FM-02-carousel-3-what-members-pay_1080x1350'] = (1080,1350,'ivory',f"""
<img class="logo" src="{u('logo.svg')}" style="left:84px;top:78px;height:40px">
<div class="eyebrow" style="position:absolute;left:84px;top:180px;color:{LEAF}">Real member prices</div>
<div class="serif" style="position:absolute;left:80px;top:228px;font-size:84px;line-height:1.02;color:{LEAF}">What members pay.</div>
<div style="position:absolute;left:84px;right:84px;top:410px;display:grid;gap:70px">
 {ex('everliv-nad.jpg','NAD+','59.99','47.99',20)}
 {ex('everliv-b-nmn.jpg','β-NMN','49.99','39.99',20)}
</div>
<div class="fine" style="position:absolute;left:84px;right:84px;bottom:56px">Prices on everliv.life as of Nov 16, 2026, and may change; your cart shows your exact price. Member pricing applies each time you buy an eligible product during your membership (one-time purchases, not Subscribe &amp; Save). Some products are 15% off and some are excluded.</div>
""")

A['FM-02-carousel-4-the-math_1080x1350'] = (1080,1350,'green',f"""
<img class="logo" src="{u('logo-white.svg')}" style="left:84px;top:78px;height:40px">
<div class="eyebrow" style="position:absolute;left:84px;top:180px;color:{FRESH}">Is it worth it? Do the math.</div>
<div style="position:absolute;left:84px;top:222px;font-size:26px;opacity:.8">If every purchase is a 20%-off product:</div>
<div class="serif" style="position:absolute;left:80px;top:280px;font-size:150px;line-height:1">$49.99 <span style="opacity:.5">÷</span> 20%</div>
<div class="serif" style="position:absolute;left:80px;top:445px;font-size:150px;line-height:1"><span style="opacity:.5">=</span> <span style="color:#fff">$249.95</span></div>
<div class="rule" style="position:absolute;left:84px;top:640px"></div>
<div style="position:absolute;left:84px;right:110px;top:690px;font-size:38px;line-height:1.35;font-weight:450">If everything you buy is eligible for the full 20%, membership covers its fee after about <b style="font-weight:750;color:#fff">$250 of purchases</b> in 12 months.</div>
<div style="position:absolute;left:84px;right:110px;top:900px;font-size:31px;line-height:1.45;opacity:.85">On 15% products it takes about $333, and a mix lands in between. Shop less than that? Everyday prices or Subscribe &amp; Save may suit you better.</div>
<div class="fine" style="position:absolute;left:84px;right:84px;bottom:56px">Savings depend on what you buy and aren't guaranteed to exceed the $49.99 fee. Eligible one-time product purchases only; some products excluded.</div>
""")

A['FM-02-carousel-5-founding-price_1080x1350'] = (1080,1350,'ivory',f"""
<img class="logo" src="{u('logo.svg')}" style="left:84px;top:78px;height:40px">
<div class="eyebrow" style="position:absolute;left:84px;top:180px;color:{LEAF}">The founding price</div>
<div style="position:absolute;left:84px;right:84px;top:250px;display:grid;grid-template-columns:1fr 1fr;gap:28px">
  <div style="background:{LEAF};color:{IVORY};border-radius:28px;padding:48px 44px;height:420px;position:relative">
    <div style="font-size:24px;font-weight:650;letter-spacing:.16em;text-transform:uppercase;color:{FRESH}">Founding</div>
    <div class="serif" style="font-size:120px;line-height:1;margin-top:28px">$49.99</div>
    <div style="font-size:28px;line-height:1.4;margin-top:22px">Memberships bought through<br><b>January 31, 2027</b> (ET)</div></div>
  <div style="border:2px solid rgba(42,66,42,.25);border-radius:28px;padding:48px 44px;height:420px">
    <div style="font-size:24px;font-weight:650;letter-spacing:.16em;text-transform:uppercase;opacity:.6">From Feb 1, 2027</div>
    <div class="serif" style="font-size:120px;line-height:1;margin-top:28px;opacity:.55">$69.99</div>
    <div style="font-size:28px;line-height:1.4;margin-top:22px;opacity:.75">Same 12-month membership.<br>Same benefits.</div></div>
</div>
<div class="serif" style="position:absolute;left:80px;top:760px;font-size:76px;line-height:1.05;color:{LEAF}">Join as a<br>Founding Member.</div>
<div style="position:absolute;left:84px;top:960px;display:inline-block;background:{LEAF};color:{IVORY};border-radius:999px;padding:26px 46px;font-size:30px;font-weight:650">everliv.life/pages/membership</div>
<div class="fine" style="position:absolute;left:84px;right:84px;bottom:56px">{FINE_FEED}</div>
""")

# ---------- C. Stories, 1080x1920 (safe area: top 250, bottom 340 kept clear) ----------
FINE_STORY = "Founding price through Jan 31, 2027 (ET); $69.99 from Feb 1, 2027. 12 months, no automatic renewal. Applies to eligible one-time product purchases (not Subscribe & Save): 20% or 15% by product, some excluded. Not available in CA or NC."
A['FM-03-story-1-hook_1080x1920'] = (1080,1920,'green',f"""
<img class="logo" src="{u('logo-white.svg')}" style="left:50%;transform:translateX(-50%);top:270px;height:48px">
<div class="eyebrow" style="position:absolute;left:0;right:0;text-align:center;top:420px;color:{FRESH}">Black Friday</div>
<div class="serif" style="position:absolute;left:0;right:0;text-align:center;top:480px;font-size:112px;line-height:1.0">Become a<br>Founding<br>Member.</div>
{card(220,900,-5,1,True)}
<div style="position:absolute;left:0;right:0;text-align:center;top:1390px;font-size:40px;font-weight:600">$49.99, paid once.</div>
""")
A['FM-03-story-2-benefits_1080x1920'] = (1080,1920,'ivory',f"""
<img class="logo" src="{u('logo.svg')}" style="left:50%;transform:translateX(-50%);top:270px;height:44px">
<div class="serif" style="position:absolute;left:90px;right:90px;top:400px;font-size:96px;line-height:1.02;color:{LEAF}">A full year of member pricing.</div>
<div style="position:absolute;left:90px;right:90px;top:780px;display:grid;gap:30px">
 {''.join(f'<div style="display:flex;align-items:center;gap:26px;font-size:40px;line-height:1.25;font-weight:650"><span style="width:18px;height:18px;border-radius:50%;background:{FRESH};flex:none"></span>{t}</div>' for t in ['12 months of member pricing','Every eligible order, as often as you shop','Up to 20% off (20% or 15%, by product)','One payment. No automatic renewal'])}
</div>
<img src="{u('strips-available-4--row--transparent.png')}" style="position:absolute;left:90px;top:1150px;width:900px">
<div style="position:absolute;left:90px;right:90px;top:1440px;font-size:26px;font-weight:600;color:{LEAF};opacity:.8">Oral strips shown. Member pricing covers eligible products across EverLiv.</div>
<div class="fine" style="position:absolute;left:90px;right:90px;top:1510px;font-size:24px">{FINE_STORY}</div>
""")
A['FM-03-story-3-cta_1080x1920'] = (1080,1920,'green',f"""
<img class="logo" src="{u('logo-white.svg')}" style="left:50%;transform:translateX(-50%);top:270px;height:48px">
<div class="eyebrow" style="position:absolute;left:0;right:0;text-align:center;top:430px;color:{FRESH}">Founding price</div>
<div class="serif" style="position:absolute;left:0;right:0;text-align:center;top:490px;font-size:220px;line-height:1">$49.99</div>
<div style="position:absolute;left:0;right:0;text-align:center;top:760px;font-size:40px;line-height:1.4">through <b>January 31, 2027</b> (ET)<br><span style="opacity:.7">$69.99 from February 1, 2027</span></div>

<div style="position:absolute;left:0;right:0;text-align:center;top:1290px;font-size:36px;font-weight:600">Tap to join</div>
<div class="fine" style="position:absolute;left:90px;right:90px;top:1420px;text-align:center;font-size:24px">{FINE_STORY}</div>
""")

# ---------- D. Email header 1200x600 ----------
A['FM-04-email-header_1200x600'] = (1200,600,'green',f"""
<img class="logo" src="{u('logo-white.svg')}" style="left:70px;top:60px;height:40px">
<div class="eyebrow" style="position:absolute;left:70px;top:150px;color:{FRESH};font-size:20px">Black Friday · Founding Members</div>
<div class="serif" style="position:absolute;left:66px;top:190px;font-size:70px;line-height:1.02">Become a<br>Founding<br>Member.</div>
<div style="position:absolute;left:70px;top:445px;font-size:27px;line-height:1.35">A full year of member pricing.<br><b>$49.99, paid once.</b></div>
{card(560,120,-5,0.82,True)}
""")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        for name,(w,h,cls,body) in A.items():
            html = OUT/f'{name}.html'; html.write_text(page(w,h,body,cls))
            pg = await b.new_page(viewport={'width':w,'height':h}, device_scale_factor=1)
            await pg.goto(html.as_uri()); await pg.wait_for_timeout(400)
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(OUT/f'{name}.png')); await pg.close()
            print(name)
        await b.close()
asyncio.run(main())
