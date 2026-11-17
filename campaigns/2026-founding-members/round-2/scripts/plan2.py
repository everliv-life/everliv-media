"""Round 2 calendar (Nov 18, 2026 - Jan 31, 2027). Builds on plan.P (round 1) and records every revision.
rev: KEPT | REVISED (wording/asset updated in place) | NEW | REPLACED (new primary asset, old kept as backup) | HOLD | REMOVED
status: READY | MOTION (proposed motion primary) | CONCEPT | TEMPLATE | NOT PRODUCED"""
import copy, datetime as dt
import plan
from plan import url, MEM, DISC, DISC_SHORT, AI_DISC
P = [copy.deepcopy(p) for p in plan.P]
ById = {p['id']: p for p in P}
for p in P: p.update(rev='REVISED' if p['kind'] == 'member' else 'KEPT', motion=[], music='', status='READY', note='')
PH_E = 'E · New Year & final window'
STRIP = "Dissolves on your tongue. No water, no pills. 30 strips per tin."

# Music: Instagram catalog tracks found via the Instagram Audio API through Metricool (searched Nov 17, 2026).
M = {'we_grow': 'We Grow · erloom · 2005304820346232', 'understory': 'Understory · Ross Lara · 1866485437031985',
     'carry_on': 'Carry On (Instrumental) · Giulio Cercato · 1197857668796525', 'stardust': 'Stardust (Instrumental) · Giulio Cercato · 1540755600953104',
     'deck': 'Deck The Halls (Jazz) · Global Genius · 322565551554019', 'bells': 'Holiday Bells · Scott Dugdale · 193842924859531',
     'carol': 'Carol of Broken Bells · Marshall Watson · 351338975683164', 'first_snow': 'First Snow · Giulio Cercato · 1637199290067753',
     'november': 'November · Giulio Cercato · 2397710587111621', 'slow': 'Slow It Down (Instrumental) · Deuxhyun · 1392368834824673',
     'soft_cut': 'Soft Cut · Afterlight · 1701552717766360'}
DRAFTED = {'A04R': '431839446', 'C02R': '431839580', 'D03': '431839632'}   # Metricool draft ids (unpublished)

def add(date, phase, pid, title, hook, caption, fmt, asset, kind, platforms=('IG', 'FB'), path='/', cta='Shop now', obj='Discovery',
        rev='NEW', status='READY', motion=None, music='', deps='', note=''):
    P.append(dict(date=date, phase=phase, id=pid, title=title, hook=hook, caption=caption, fmt=fmt, asset=asset, cta=cta, path=path,
                  objective=obj, kind=kind, platforms=platforms, deps=deps, alt=[], short=hook, rev=rev, motion=motion or [],
                  music=music, status=status, note=note))
def upd(pid, **k): ById[pid].update(k)

# ---------- Nov 18-19: fill the opening gap (today is Nov 17: nothing backdated)
add('2026-11-18', plan.PH_A, 'N03', 'Meet the strips: Hydrate', 'Hydrate Oral Strips.',
    "Meet Hydrate Oral Strips: seven botanicals, including turmeric and chicory, in a dissolvable strip for your daily water routine.\n\n" + STRIP +
    "\n\nShop at everliv.life.", 'feed', 'N03-hydrate-spotlight', 'product', ('IG', 'FB', 'Threads', 'X'), '/products/hydrate-strips')
add('2026-11-19', plan.PH_A, 'P19', 'Cozy coffee: Cocoa', 'Cozy season, brewed.',
    "Cozy season, brewed. Cocoa Coffee, medium roast.\n\nFree U.S. shipping on every order.\n\n" + AI_DISC, 'feed', 'COFFEE2-cocoa-steam', 'product',
    ('IG', 'FB', 'Threads'), '/collections/coffee', status='MOTION', motion=['COFFEE2-cocoa-steam'], music=M['first_snow'])
# ---------- Nov 23-30: lighten the membership run
add('2026-11-24', plan.PH_A, 'N01', 'Meet the strips: Iron', 'Iron Oral Strips.',
    "Meet Iron Oral Strips: iron in a dissolvable oral strip.\n\n" + STRIP + "\nKeep out of reach of children.\n\nShop at everliv.life.",
    'feed', 'N01-iron-spotlight', 'product', ('IG', 'FB', 'Threads'), '/products/iron-strips')
upd('A07', asset='PR01-thanksgiving-table', rev='REPLACED', status='MOTION', motion=['PR01-thanksgiving-table', 'A07-thanksgiving--animated'], music=M['november'],
    note='Photoreal Thanksgiving table replaces the text card; original still and line-art leaves kept as backups.')
upd('B02', platforms=('Threads', 'X'), rev='REVISED', note='Moved off the Instagram/Facebook feed (text posts only) to make room for product content.')
add('2026-11-28', plan.PH_B, 'N02', 'Meet the strips: D3 + K2', 'D3 + K2 Oral Strips.',
    "Meet D3 + K2 Oral Strips: vitamin D3 and K2 together in a dissolvable strip.\n\n" + STRIP + "\n\nShop at everliv.life.",
    'feed', 'N02-d3k2-spotlight', 'product', ('IG', 'FB'), '/products/d3-k2-strips')
add('2026-11-29', plan.PH_B, 'N04', 'Meet the strips: Energy', 'Energy Oral Strips.',
    "Meet Energy Oral Strips: 50 mg green-tea caffeine, 30 mg L-theanine and B12 in a cranberry strip.\n\n" + STRIP + "\nContains caffeine; see product page for warnings.",
    'feed', 'N04-energy-spotlight', 'product', ('IG', 'FB', 'TikTok'), '/products/energy-strips')
upd('B03R', rev='REMOVED', status='NOT PRODUCED', note='Recommend dropping: a real checkout recording needs a member account and a live order. B03 (real cart) covers the message.')
# ---------- December: photoreal holiday primaries, product variety
upd('C03', asset='COFFEE2-cocoa-steam', rev='REPLACED', status='MOTION', motion=['COFFEE2-cocoa-steam'], music=M['first_snow'], note='Smaller coffee bag; steam and lights.')
upd('C05', asset='PR02-fireplace-stocking-stuffers', rev='REPLACED', status='MOTION', motion=['PR02-fireplace-stocking-stuffers', 'C05-stocking-stuffer--animated'], music=M['bells'])
upd('C07', rev='REVISED', status='MOTION', motion=['PR07-workshop-soaps'], music=M['carol'])
upd('C08', motion=['PRICE-creatine'], music=M['slow'])
upd('C10', motion=['PRICE-nad'], music=M['slow'])
upd('C11', title='Gifts that won\'t melt: Hydrate and D3 + K2', hook='Gifts that won\'t melt.', kind='product', fmt='feed', asset='PR03-snowman-gifts',
    caption="Gifts that won't melt. Hydrate and D3 + K2 oral strips, 30 strips per tin, $34.99.\n\n" + STRIP + "\n\n" + AI_DISC,
    rev='REPLACED', status='MOTION', motion=['PR03-snowman-gifts'], music=M['first_snow'], note='Replaces the unproduced first-order reel (C11).')
upd('C12', motion=['PRICE-energy'], music=M['slow'])
upd('C13', asset='PR06-tree-train-gifts', rev='REPLACED', status='MOTION', motion=['PR06-tree-train-gifts'], music=M['carol'])
upd('C16', music=M['bells'], note='Product reel: plain ending (gold-leaf sign-off reserved for membership).')
upd('C17', asset='PR08-door-wreath-founding-member', rev='REPLACED', status='MOTION', motion=['PR08-door-wreath-founding-member', 'C17-mistletoe-card--animated'], music=M['understory'])
upd('C18', rev='HOLD', status='NOT PRODUCED', note='Hold until verified label panels are on file (no-proprietary-blend check).')
add('2026-12-19', plan.PH_C, 'P1219', 'Cozy coffee: Caramel', 'Pour. Sip. Slow down.',
    "Pour. Sip. Slow down. Caramel Coffee, dark roast.\n\nFree U.S. shipping on every order.\n\n" + AI_DISC, 'feed', 'COFFEE2-caramel-steam', 'product',
    ('IG', 'FB', 'Threads'), '/collections/coffee', status='MOTION', motion=['COFFEE2-caramel-steam'], music=M['slow'], note='Takes the C18 slot while C18 is on hold.')
upd('A02', motion=['A02-teaser-reel--with-logo-outro'], music=M['understory'])
upd('A04', motion=['A04-reveal--animated', 'ANIM-3-price-to-join'], music=M['we_grow'])
upd('A04R', motion=['A04R-reveal-reel--with-logo-outro'], music=M['we_grow'])
upd('A05', motion=['ANIM-2-card-tilt'])
upd('A01', motion=['ANIM-1-teaser-foil-shimmer'])
upd('B01R', motion=['B01R-bf-reel--with-logo-outro'], music=M['carry_on'])
upd('C19', motion=['C19-math-reel--with-logo-outro'], music=M['slow'])
upd('C02R', music=M['deck'])
upd('D03', music=M['first_snow'], note='Product reel: plain ending.')
upd('D04', asset='PR04-santa-christmas-eve', title='Christmas Eve: merry & bright', rev='REPLACED', status='MOTION',
    motion=['PR04-santa-christmas-eve', 'D04-holiday-greeting--animated'], music=M['carol'])
add('2026-12-25', plan.PH_D, 'X25', 'Christmas Day greeting (no sell)', 'Merry Christmas.',
    "Merry Christmas. Wishing you a slow, warm morning.\n\nFrom all of us at EverLiv.", 'feed', 'PR05-christmas-morning', 'brand',
    ('IG', 'FB', 'Threads', 'X'), '/', cta='None', obj='Community', status='MOTION', motion=['PR05-christmas-morning'], music=M['bells'])
upd('D07', asset='D07v2-routine-2027', kind='product', rev='REVISED', title='Build your 2027 routine (products)',
    caption="Build your 2027 routine.\n\nMorning: coffee, then an Energy strip when you need it.\nMidday: Hydrate with your water routine, Iron in a pocket-size strip.\n"
            "Evening: D3 + K2 and a handmade soap.\n\nEnergy Strips contain caffeine. Iron: keep out of reach of children.", note='Now product-led (was a membership carousel).')
upd('D10', asset='D10v2-year-of-more_feed', kind='brand', rev='REVISED', caption="Here's to a year of more. More routines that fit. More to discover.\n\nHappy New Year from EverLiv.",
    note='New Year\'s Eve is now brand-only.')

# ---------- January 2027
J = plan.PH_D
def jm(date, pid, title, hook, cap, fmt, asset, plats=('IG', 'FB', 'Threads', 'X'), **k): add(date, PH_E, pid, title, hook, cap + "\n\n" + DISC, fmt, asset, 'member', plats, MEM, 'Join now', 'Enrollments', **k)
def jp(date, pid, title, hook, cap, fmt, asset, plats=('IG', 'FB', 'Threads'), path='/collections/all', **k): add(date, PH_E, pid, title, hook, cap, fmt, asset, 'product', plats, path, **k)
jp('2027-01-01', 'J01a', 'New year, simple routines', 'Simple routines, every day.', "New year. Simple routines, every day.\n\nHydrate, Iron and D3 + K2 oral strips. " + STRIP + "\n\n" + AI_DISC,
   'feed', 'PR09-new-year-kitchen', status='MOTION', motion=['PR09-new-year-kitchen'], music=M['soft_cut'])
jm('2027-01-01', 'J01b', 'A new year of up to 20% off', 'Up to 20% off all year long.',
   "A new year. Up to 20% off eligible products, all year long.\n\nJoin by January 31 for $49.99. Enjoy up to 20% off eligible products for a full 12 months.", 'feed', 'J01b-year-of-up-to-20_feed')
add('2027-01-01', PH_E, 'E07', 'EMAIL 7: New year, member pricing', 'Start 2027 with up to 20% off',
    'Subject: "Start 2027 with up to 20% off". Header J01b. Body: approved Founding Member statement + CTA. Opted-in subscribers only.', 'email', 'J01b-year-of-up-to-20_feed', 'member', ('Email',), MEM, 'Join now', 'Enrollments')
jp('2027-01-02', 'J02', 'Routine series ep. 1: Morning', 'Morning, made simple.', "Routine series, episode 1: Morning.\n\nCoffee first. Then an Energy strip on busy days.\n\nEnergy Strips contain caffeine.", 'carousel', 'J02-routine-morning', plats=('IG', 'FB', 'TikTok'))
jp('2027-01-03', 'J03', 'Routine series ep. 2: Midday', 'Midday, on the move.', "Routine series, episode 2: Midday.\n\nHydrate, Iron and D3 + K2 oral strips. " + STRIP + "\nIron: keep out of reach of children.", 'carousel', 'J03-routine-midday', plats=('IG', 'FB', 'TikTok'))
jp('2027-01-04', 'J04', 'Routine series ep. 3: Training day', 'Training day, packed.', "Routine series, episode 3: Training day.\n\nPure Creatine Monohydrate, strips in the bag, a handmade soap after.\n\n" + AI_DISC,
   'carousel', 'J04-routine-training', plats=('IG', 'FB', 'TikTok'), status='MOTION', motion=['PR10-entryway-gym-bag'], music=M['carry_on'])
jm('2027-01-05', 'J05', 'Member math refresher', 'Here\'s the honest math.', "Up to 20% off, and the honest math behind it.\n\nRe-price every example on Jan 4 before posting.", 'carousel', 'A06-calculator',
   rev='REVISED', note='Reuses A06 slides; re-check live prices on Jan 4.')
jm('2027-01-07', 'J06', 'How member pricing shows up', 'Everyday $34.99. Member $27.99.', "Every product page shows its everyday and member price. Hydrate Oral Strips: $34.99 everyday, $27.99 for members (20% off).\n\nUp to 20% off eligible products for 12 months.",
   'feed', 'PRICE-hydrate', status='MOTION', motion=['PRICE-hydrate'], music=M['slow'], note='Replaces the planned filmed checkout walkthrough.')
add('2027-01-08', PH_E, 'E08', 'EMAIL 8: Your routine, your member price', 'Your routine, your member price.',
    'Subject: "Your routine, your member price". Header E08. Routine series recap + up to 20% off + CTA. Opted-in subscribers only.', 'email', 'E08-email-header', 'member', ('Email',), MEM, 'Join now', 'Enrollments')
jp('2027-01-09', 'J08', 'January mornings', 'Slow down. Pour another.', "Slow down. Pour another. Hazelnut Coffee, medium roast.\n\n" + AI_DISC, 'feed', 'J08-slow-mornings_feed', path='/collections/coffee')
jm('2027-01-10', 'J09', 'Member FAQ', 'Your questions, answered.', "Does it renew? No. Is everything 20% off? It's up to 20%: eligible products are 15% or 20% off, depending on the product. Does it work with Subscribe & Save? No.", 'carousel', 'C14-member-faq', rev='REVISED', note='Reuses C14 (updated wording).')
add('2027-01-12', PH_E, 'J10', "Discover What's Next ep. 2 (template)", '[New product] is here.', 'TEMPLATE. Publish only after Restructuring confirms label, listing and launch approval for one of: Mushroom Focus Strips, Hair, Skin & Nails Strips, Hyaluronic Acid Serum, Complete Multivitamin, CoQ10.',
    'feed', 'J10-whats-next-TEMPLATE_feed', 'product', ('IG', 'FB'), status='TEMPLATE', rev='HOLD')
jp('2027-01-14', 'J11', 'Strips spotlight (reel)', 'Four strips. No water needed.', "Energy, Hydrate, Iron and D3 + K2. " + STRIP + "\n\nEnergy Strips contain caffeine. Iron: keep out of reach of children.",
   'reel', 'J11-strips-family--reel', plats=('IG', 'FB', 'TikTok', 'YT'), status='MOTION', motion=['J11-strips-family--reel'], music=M['soft_cut'])
jp('2027-01-16', 'J12', 'Self-care, scheduled', 'Handmade soaps, six scents.', "Self-care, scheduled. Handmade soaps in six scents, from $20.99.\n\n" + AI_DISC, 'feed', 'J12-self-care_feed', path='/collections/soap')
jm('2027-01-17', 'J13', 'Two orders and you\'re ahead (re-priced)', 'One order won\'t do it. Two will.', "A real cart, the $49.99 fee included. Re-price on Jan 16.", 'carousel', 'B03-real-cart', rev='REVISED', note='Reuses B03; re-check prices.')
add('2027-01-19', PH_E, 'J14', 'Tell us: morning person or night owl?', 'Morning person or night owl?', "Morning person or night owl? Comment ☀️ or 🌙.", 'feed', 'J19-poll_feed', 'brand', ('IG', 'FB', 'Threads', 'X'), '/', 'Comment', 'Engagement')
add('2027-01-20', PH_E, 'J15', 'A note from the EverLiv team', 'Why we built a membership instead of running sales.', "Why we built a membership instead of running sales. (Draft for owner approval; can be filmed as a talking-head reel.)",
    'feed', 'J15-team-note_feed', 'brand', ('IG', 'FB', 'Threads', 'X'), MEM, 'Read', 'Brand trust', status='READY', note='Owner to approve the voice; filming optional.')
jm('2027-01-21', 'J16', 'Final ten days', '10 days left to join at $49.99.', "10 days left to join at $49.99. Your membership lasts a full 12 months.\n\nUp to 20% off eligible products, as often as you shop.", 'feed', 'J16-ten-days-left',
   status='MOTION', motion=['J16-ten-days-left'], music=M['understory'])
add('2027-01-21', PH_E, 'E09', 'EMAIL 9: 10 days left', 'Last 10 days to join at $49.99', 'Subject: "10 days left to join at $49.99". Header E11 variant. Pair with "Your membership lasts a full 12 months."', 'email', 'E11-email-header', 'member', ('Email',), MEM, 'Join now', 'Enrollments')
jp('2027-01-22', 'J17', 'Packed for the new year', 'Packed for the new year.', "Hydrate and Energy oral strips: they fit in any bag.\n\nEnergy Strips contain caffeine.\n\n" + AI_DISC, 'feed', 'PR10-entryway-gym-bag',
   status='MOTION', motion=['PR10-entryway-gym-bag'], music=M['carry_on'])
jm('2027-01-24', 'J18', 'One week left', 'One week left to join at $49.99.', "One week left to join at $49.99. Your membership lasts a full 12 months. From February 1, it costs $69.99 to join.", 'feed', 'J18-one-week_feed')
jp('2027-01-25', 'J19', 'Meet the strips: Hydrate (repost)', 'Hydrate Oral Strips.', "Hydrate Oral Strips. " + STRIP, 'feed', 'N03-hydrate-spotlight', rev='REVISED', note='Re-uses N03 with January caption.')
jm('2027-01-27', 'J20', 'Joining in January costs less', 'The honest math.', "Break-even = price to join ÷ member discount. Join by Jan 31: $49.99. From Feb 1: $69.99. Either way, your membership lasts 12 months.", 'feed', 'J20-math-before-after_feed')
jp('2027-01-28', 'J21', 'Coffee, the January edit', 'Four coffees.', "Hazelnut, Cocoa, Caramel and Mushroom. Medium and dark roasts.", 'carousel', 'J02-routine-morning', rev='REVISED', path='/collections/coffee', note='Reuses J02 slides 2-3.')
jm('2027-01-29', 'J22', '3 days left', '3 days left to join at $49.99.', "3 days left to join at $49.99. Your membership lasts a full 12 months.", 'feed', 'J22-three-days_feed')
add('2027-01-29', PH_E, 'E10', 'EMAIL 10: 3 days left', '3 days left to join at $49.99', 'Subject: "3 days left to join at $49.99". Opted-in subscribers only.', 'email', 'E11-email-header', 'member', ('Email',), MEM, 'Join now', 'Enrollments')
jm('2027-01-31', 'J24', 'Last chance to join at $49.99', 'Last chance to join at $49.99.', "Last chance to join at $49.99. Your membership lasts a full 12 months. From February 1, it costs $69.99 to join.", 'reel', 'J24-last-chance--reel',
   plats=('IG', 'FB', 'TikTok', 'YT', 'Threads', 'X'), status='MOTION', motion=['J24-last-chance--reel', 'J24-last-chance--feed'], music=M['stardust'])
add('2027-01-31', PH_E, 'E11', 'EMAIL 11: Last chance (morning)', 'Last chance to join at $49.99', 'Subject: "Last chance to join at $49.99". Preheader: "Your membership lasts a full 12 months." Send 9:00 ET.', 'email', 'E11-email-header', 'member', ('Email',), MEM, 'Join now', 'Enrollments')

P.sort(key=lambda p: (p['date'], p['id']))
LIVE = [p for p in P if p['rev'] not in ('REMOVED',)]

def mix(start, end):
    ps = [p for p in LIVE if start <= p['date'] <= end and p['fmt'] != 'email' and ('IG' in p['platforms'] or 'FB' in p['platforms']) and p['status'] not in ('TEMPLATE',) and p['rev'] != 'HOLD']
    from collections import Counter
    c = Counter(p['kind'] for p in ps); return len(ps), c

STORY = {'A': ['story-strips', 'story-offer', 'story-coffee'], 'B': ['story-offer', 'story-quiz', 'story-strips'], 'C': ['story-coffee', 'story-strips', 'story-poll', 'story-offer'],
         'D': ['story-coffee', 'story-founding', 'story-strips'], 'E': ['story-founding', 'story-strips', 'story-poll', 'story-offer']}
COUNTDOWN = {'2027-01-21': 'story-ten', '2027-01-24': 'story-week', '2027-01-30': 'story-tomorrow', '2027-01-31': 'story-last'}
def story_for(d):
    iso = d.isoformat()
    if iso in COUNTDOWN: return COUNTDOWN[iso]
    if iso in ('2026-12-24', '2026-12-25'): return None
    ph = 'A' if iso <= '2026-11-26' else 'B' if iso <= '2026-11-30' else 'C' if iso <= '2026-12-20' else 'D' if iso <= '2026-12-31' else 'E'
    s = STORY[ph]; return s[d.toordinal() % len(s)]

if __name__ == '__main__':
    for a, b in [('2026-11-18', '2026-12-31'), ('2026-11-23', '2026-11-30'), ('2026-12-26', '2026-12-31'), ('2027-01-01', '2027-01-31'), ('2026-11-18', '2027-01-31')]:
        n, c = mix(a, b); print(a, b, n, dict(c), {k: round(100 * v / n) for k, v in c.items()})
