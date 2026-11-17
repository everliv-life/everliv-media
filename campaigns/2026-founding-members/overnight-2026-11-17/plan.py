"""EverLiv Founding Members campaign: master content plan (Nov 20 - Dec 31, 2026).
Single source of truth for the calendar, CSV/XLSX exports and the production manifest.
All prices verified live on everliv.life Nov 16, 2026 (product-page member rates). Re-verify before publishing."""
import datetime as dt
TZ = 'ET'
BASE = 'https://everliv.life'
def url(path, src, med, content):
    return f"{BASE}{path}?utm_source={src}&utm_medium={med}&utm_campaign=founding-members-2026&utm_content={content}"
MEM = '/pages/membership'
DISC = ("Member pricing: 20% or 15% off eligible one-time purchases, depending on the product; some products excluded; "
        "doesn't combine with Subscribe & Save, bundles or promo codes. $49.99 founding price through Jan 31, 2027 (ET); "
        "$69.99 from Feb 1, 2027. 12 months, no automatic renewal. Not available to residents of CA or NC. "
        "Terms: everliv.life/pages/membership-terms")
DISC_SHORT = "Eligible products only (20% or 15%). Terms & CA/NC exclusion: everliv.life/pages/membership-terms"
AI_DISC = "Product shown as supplied; scene digitally created."

# ---------------------------------------------------------------------------------------------
# Content pieces. Each piece = one creative idea published on one or more platforms.
# fmt: feed (static 4:5), carousel (4:5 multi), reel (9:16 video), email, text (Threads/X).
# kind: member (uses Member Club emblem) | brand (main logo only) | product
# asset: filename stem under assets/ (rendered by build_assets.py) or 'SPEC' if storyboard only.
# ---------------------------------------------------------------------------------------------
P = []
def piece(date, phase, pid, title, hook, caption, fmt, asset, cta, path, objective, kind='member',
          platforms=('IG', 'FB'), deps='', alt=None, short=None):
    P.append(dict(date=date, phase=phase, id=pid, title=title, hook=hook, caption=caption, fmt=fmt,
                  asset=asset, cta=cta, path=path, objective=objective, kind=kind, platforms=platforms,
                  deps=deps, alt=alt or [], short=short or hook))

PH_A = 'A · Teaser & reveal'
PH_B = 'B · Black Friday / Cyber Monday'
PH_C = 'C · Holiday gifting'
PH_D = 'D · Year-end routines'

# ===== PHASE A: teaser and reveal (Nov 20-26) ===============================================
piece('2026-11-20', PH_A, 'A01', 'Teaser 1: Something new at EverLiv',
      'Something new is taking shape at EverLiv.',
      "Something new is taking shape at EverLiv.\n\nA little gold. A lot more to discover.\nMore on Monday.",
      'feed', 'A01-teaser-something-new', 'Follow for Monday', '/', 'Curiosity, follows', kind='member',
      platforms=('IG', 'FB', 'Threads', 'X'),
      deps='Teasers must not imply membership is unavailable (it is live). Copy says "more on Monday", not "coming soon".')
piece('2026-11-21', PH_A, 'A02', 'Teaser 2: A little gold (motion)',
      'A little gold. A lot more to discover.',
      "Your wellness journey evolves. So does EverLiv.\n\nA little gold. A lot more to discover. Monday.",
      'reel', 'A02-teaser-reel', 'Follow / turn on notifications', '/', 'Reach, curiosity',
      platforms=('IG', 'FB', 'TikTok', 'YT'), deps='8-second motion asset rendered (see manifest).')
piece('2026-11-22', PH_A, 'A03', 'Brand story: strips, capsules, powders and more',
      'Strips, capsules, powders and more. One EverLiv.',
      "Strips that dissolve on your tongue. Daily capsules. Mix-in powders. Coffee and handmade body care.\n\n"
      "EverLiv is built around routines that fit real days, with every ingredient listed on the label.\n\n"
      "Explore the range at everliv.life.",
      'carousel', 'A03-brand-range', 'Shop the range', '/collections/all', 'Brand awareness, catalog breadth',
      kind='brand', platforms=('IG', 'FB'),
      deps='Main EverLiv logo only (no Member Club emblem on non-membership content).')
piece('2026-11-23', PH_A, 'A04', 'REVEAL: Introducing the Member Price Club',
      'Introducing the EverLiv Member Price Club.',
      "Introducing the EverLiv Member Price Club.\n\nBecome a Founding Member: pay $49.99 once and enjoy member pricing for 12 months, "
      "on every eligible order, as often as you shop. No monthly fees. No automatic renewal.\n\n"
      "Founding price through January 31, 2027. $69.99 from February 1.\n\nJoin through the link in bio.\n\n" + DISC,
      'feed', 'A04-reveal', 'Become a Founding Member', MEM, 'Paid membership enrollments',
      platforms=('IG', 'FB', 'Threads', 'X'),
      deps='GATE: Restructuring end-to-end enrollment/sign-in/checkout evidence before this date. Reveal reel A04R same day.',
      alt=['ALT-A04-1 "A new chapter of EverLiv." (story-led, emblem reveal)',
           'ALT-A04-2 "Your year. Your wellness. Your member price." (lifestyle-led)'])
piece('2026-11-23', PH_A, 'A04R', 'REVEAL reel: the emblem and the offer',
      'This is the EverLiv Member Price Club.',
      "This is the EverLiv Member Price Club. $49.99 once. 12 months of member pricing on eligible products: strips, capsules, powders and more. "
      "No automatic renewal.\n\nFounding price through Jan 31, 2027.\n\n" + DISC,
      'reel', 'A04R-reveal-reel', 'Join: link in bio', MEM, 'Enrollments, reach',
      platforms=('IG', 'FB', 'TikTok', 'YT'), deps='Motion asset rendered.')
piece('2026-11-24', PH_A, 'A05', 'How it works (carousel)',
      'One payment. Twelve months of member pricing.',
      "How the EverLiv Member Price Club works, in four slides.\n\n1. Pay $49.99 once.\n2. Sign in with the same email.\n"
      "3. Member prices apply automatically on eligible products: 20% or 15% off, depending on the product.\n"
      "4. Shop as often as you like for 12 months. Nothing renews automatically.\n\n" + DISC,
      'carousel', 'A05-how-it-works', 'See how it works', MEM, 'Education, enrollments',
      platforms=('IG', 'FB', 'TikTok'))
piece('2026-11-25', PH_A, 'A06', 'Do the math: the break-even (calculator)',
      'Is membership worth it for you? Here is the math.',
      "Honest math, before you join.\n\nIf everything you buy is a 20%-off product: $49.99 / 0.20 = $249.95 of eligible purchases covers the fee.\n"
      "On 15% products: about $333.\n\nAbove that, the member price keeps working for you for the rest of your 12 months. Below it, everyday prices "
      "or Subscribe & Save may suit you better. Savings aren't guaranteed to exceed the fee.\n\n" + DISC,
      'carousel', 'A06-calculator', 'Do your own math', MEM, 'Qualified enrollments, trust',
      platforms=('IG', 'FB', 'Threads', 'X'))
piece('2026-11-26', PH_A, 'A07', 'Thanksgiving: thank you (no sell)',
      'Thank you for being part of EverLiv.',
      "To everyone who has tried a strip, brewed a cup or built a routine with us this year: thank you.\n\nHappy Thanksgiving from EverLiv.",
      'feed', 'A07-thanksgiving', 'None (brand)', '/', 'Community, goodwill', kind='brand',
      platforms=('IG', 'FB', 'Threads'))

# ===== PHASE B: Black Friday / Cyber Monday (Nov 27-30) =======================================
piece('2026-11-27', PH_B, 'B01', 'BLACK FRIDAY: Black Friday ends. Your membership doesn\'t.',
      "Black Friday ends tonight. Your membership doesn't.",
      "This Black Friday, we're not marking anything down for a day. We're opening membership.\n\n"
      "Become a Founding Member: $49.99, paid once, for 12 months of member pricing on every eligible order (strips, capsules, powders and more). "
      "No subscription. No automatic renewal.\n\nFounding price through January 31, 2027. $69.99 from February 1.\n\n" + DISC,
      'feed', 'B01-black-friday', 'Become a Founding Member', MEM, 'Paid membership enrollments',
      platforms=('IG', 'FB', 'Threads', 'X'),
      deps='GATE: shopping-flow evidence + stock/price re-check that morning.',
      alt=['ALT-B01-1 "One day of deals. A year of possibilities." (contrast-led, see B02)',
           'ALT-B01-2 "The only thing we\'re launching this Black Friday is a year." (editorial, no product)'])
piece('2026-11-27', PH_B, 'B01R', 'BLACK FRIDAY reel: one day vs 365',
      'Most Black Friday deals last a day. This one lasts 12 months.',
      "Most Black Friday deals last a day. EverLiv Founding Membership gives you member pricing on eligible products for 12 months, for $49.99 once.\n\n" + DISC,
      'reel', 'B01R-bf-reel', 'Join: link in bio', MEM, 'Reach, enrollments', platforms=('IG', 'FB', 'TikTok', 'YT'))
piece('2026-11-27', PH_B, 'E01', 'EMAIL 1: Black Friday launch',
      'Become a Founding Member',
      'Approved Round-1 email (see founding-members-email-shopify-build-sheet). Subject: "Become a Founding Member". Preheader: "A full year of member pricing. $49.99, paid once."',
      'email', 'E01-email-header', 'Become a Founding Member', MEM, 'Enrollments from subscribers',
      platforms=('Email',), deps='Opted-in subscribers only; Jeff explicit send approval; internal test first.')
piece('2026-11-28', PH_B, 'B02', 'One day of deals vs a year of member pricing (comparison)',
      'One day of deals. Or a year of member pricing.',
      "Black Friday: one day.\nFounding Membership: 12 months of member pricing on eligible products, as often as you shop.\n\n"
      "We chose not to run one-day markdowns, so membership stays worth it. Pay $49.99 once.\n\n" + DISC,
      'carousel', 'B02-one-day-vs-year', 'Choose the year', MEM, 'Enrollments', platforms=('IG', 'FB', 'Threads'))
piece('2026-11-29', PH_B, 'B03', 'A real cart: member vs everyday (with the fee)',
      'We built a real cart. Here is what membership does, and doesn\'t, do.',
      "A real EverLiv cart: NAD+, Pure Creatine Monohydrate, Hydrate Strips and a Charcoal soap.\n\n"
      "Everyday: $150.96. Member: $123.56. Gross saving: $27.40.\n\nOne order like this doesn't cover the $49.99 fee on its own. "
      "Two orders like it over your 12 months clear it, by $4.81. That's the honest version.\n\n" + DISC,
      'carousel', 'B03-real-cart', 'Price your own cart', MEM, 'Trust, qualified enrollments',
      platforms=('IG', 'FB', 'TikTok'), deps='Prices re-verified on publish day. Two orders = $54.80 gross saving (> $49.99).')
piece('2026-11-29', PH_B, 'B03R', 'Checkout walkthrough (screen recording)',
      'Watch member pricing apply at checkout.',
      "Screen recording: product page member price -> cart -> checkout, on a real signed-in member account. Script in scripts/.",
      'reel', 'SPEC', 'Join: link in bio', MEM, 'Trust, education', platforms=('IG', 'TikTok', 'YT'),
      deps='Needs a real member account and a recording by Jeff/Esther (Claude cannot sign in or purchase). No order placed.')
piece('2026-11-30', PH_B, 'B04', 'CYBER MONDAY: one day vs 12 months',
      'Cyber Monday is one day. Member pricing lasts 12 months.',
      "Cyber Monday is one day. Founding Membership is 12 months of member pricing on eligible EverLiv products, for $49.99 once.\n\n"
      "No codes to chase. No automatic renewal. Founding price through January 31, 2027.\n\n" + DISC,
      'feed', 'B04-cyber-monday', 'Become a Founding Member', MEM, 'Enrollments',
      platforms=('IG', 'FB', 'Threads', 'X'),
      alt=['ALT-B04-1 "No codes. No countdown clocks. Just a year." (typographic)',
           'ALT-B04-2 Product-led: three member price tags (Energy, NAD+, Creatine) on ivory'])
piece('2026-11-30', PH_B, 'E02', 'EMAIL 2: Cyber Monday reminder',
      'One day vs. a whole year',
      'Subject: "Cyber Monday is one day. This lasts a year." Preheader: "Founding Membership: $49.99 once, 12 months of member pricing." Body: short reminder + break-even line + CTA. Build like E01.',
      'email', 'E02-email-header', 'Become a Founding Member', MEM, 'Enrollments', platforms=('Email',),
      deps='Exclude anyone who already joined (Shopify segment: not a member).')

# ===== PHASE C: holiday gifting (Dec 1-20) ===================================================
piece('2026-12-01', PH_C, 'C01', 'Giving Tuesday: no sell',
      'Today is for giving, not selling.',
      "Today is Giving Tuesday. No offers from us today; just a thank-you to our community, and a nudge to support a cause close to you.",
      'feed', 'C01-giving-tuesday', 'None (brand)', '/', 'Community', kind='brand', platforms=('IG', 'FB', 'Threads'))
piece('2026-12-02', PH_C, 'C02', 'The EverLiv Holiday Gift Guide',
      'The EverLiv Holiday Gift Guide is here.',
      "Six ways to give EverLiv this year: coffee for the office, handmade soaps, oral strips for stockings, training staples and more.\n\n"
      "Members: member pricing applies to eligible items in your own orders. Bundles have their own pricing.\n\n"
      "Free U.S. shipping on every order. " + AI_DISC,
      'carousel', 'C02-gift-guide', 'Shop the gift guide', '/collections/all', 'Product sales, discovery', kind='product',
      platforms=('IG', 'FB', 'Pinterest*'),
      deps='DECISION: can members buy gifts at member price? Terms say "personal use by one account". Until confirmed, the guide shows everyday prices only.')
piece('2026-12-03', PH_C, 'C02R', 'Gift guide in 15 seconds (reel)',
      'Six gifts, fifteen seconds.',
      "Coffee, handmade soap, oral strips and training staples: the EverLiv gift guide in fifteen seconds. Free U.S. shipping. " + AI_DISC,
      'reel', 'SPEC', 'Shop gifts', '/collections/all', 'Reach, product discovery', kind='product',
      platforms=('IG', 'FB', 'TikTok', 'YT'), deps='Edit from approved lifestyle stills (storyboard in scripts/).')
piece('2026-12-03', PH_C, 'E03', 'EMAIL 3: Holiday gift guide',
      'Gifts that fit real routines',
      'Subject: "The EverLiv Holiday Gift Guide". Blocks: header (gift edit image), 4 category tiles (coffee, soap, strips, training), membership strip at bottom ("Shopping for yourself too? Founding Membership"). Everyday prices only.',
      'email', 'C02-gift-guide', 'Shop the gift guide', '/collections/all', 'Product sales', kind='product', platforms=('Email',))
piece('2026-12-04', PH_C, 'C03', 'Coffee for the office',
      'The easiest office gift: good coffee.',
      "Four EverLiv coffees for the people who keep the office running: Hazelnut, Cocoa and Caramel ($32.99) and Mushroom ($37.99). "
      "Whole-office gift? Mix the flavours.\n\nFree U.S. shipping. " + AI_DISC,
      'feed', 'C03-office-coffee', 'Shop coffee', '/collections/coffee', 'Product sales', kind='product',
      platforms=('IG', 'FB', 'Threads'),
      deps='Coffee format (carton vs bag) unresolved: no copy about packaging. No bulk-discount promise.')
piece('2026-12-05', PH_C, 'C04', 'Member or Subscribe & Save? Pick what fits',
      'Membership or Subscribe & Save? Honestly, it depends.',
      "Two ways to save, built for different shoppers.\n\nSubscribe & Save: up to 15% off one product on a set schedule. No fee.\n"
      "Membership: 20% or 15% off eligible products whenever you shop, for 12 months. $49.99 once.\n\n"
      "Buying the same thing every month? Subscribe & Save may be the better deal. Buying a mix, on your own schedule? Membership usually fits better. "
      "They don't combine.\n\n" + DISC,
      'carousel', 'C04-member-vs-subscribe', 'Compare ways to save', '/pages/ways-to-save', 'Trust, qualified enrollments',
      platforms=('IG', 'FB', 'Threads', 'X'))
piece('2026-12-06', PH_C, 'C05', 'Stocking stuffers: oral strips',
      'The stocking stuffer that fits in a pocket.',
      "Oral strips for every stocking: Energy, Hydrate, Iron and D3 + K2. Thirty strips per tin; they dissolve on the tongue, no water needed.\n\n"
      "Build Your Own Strip Bundle: any 3 for $79.99.\n\nEnergy Strips contain caffeine; see each product page for warnings.",
      'feed', 'C05-stocking-strips', 'Choose any 3', '/pages/ultimate-bundle', 'Product / bundle sales', kind='product',
      platforms=('IG', 'FB', 'TikTok'),
      deps='Bundle app free plan: 50 bundle orders/month. Confirm capacity with Jeff before pushing. Sleep/Collagen excluded unless restocked.')
piece('2026-12-07', PH_C, 'C06', 'Founding Member reminder: the card',
      'A year of member pricing. $49.99, paid once.',
      "Holiday shopping for yourself too? Founding Membership: $49.99 once for 12 months of member pricing on eligible products. "
      "Founding price through January 31.\n\n" + DISC,
      'feed', 'C06-card-reminder', 'Become a Founding Member', MEM, 'Enrollments', platforms=('IG', 'FB', 'X'))
piece('2026-12-08', PH_C, 'C07', 'Self-care gifts: handmade soaps',
      'Six handmade soaps. One very easy gift.',
      "Charcoal, Slumber, Oat Milk Honey, Rich Sandalwood, Coconut Beach and Aloe & Cool Cucumber: handmade bars, $20.99 each.\n\n"
      "Free U.S. shipping. " + AI_DISC,
      'carousel', 'C07-soap-gifts', 'Shop body care', '/collections/premium-body-care-series', 'Product sales', kind='product',
      platforms=('IG', 'FB', 'Pinterest*'), deps='Cosmetic descriptors only. No "organic"/"sensitive skin" claims.')
piece('2026-12-09', PH_C, 'C08', 'For the one who trains',
      'For the friend whose gym bag is always packed.',
      "Training-day staples from EverLiv: Pure Creatine Monohydrate and Creatine+ Electrolytes.\n\nIngredients and directions on every product page.",
      'feed', 'C08-training-gifts', 'Shop training staples', '/collections/fitness', 'Product sales', kind='product',
      platforms=('IG', 'FB', 'TikTok'),
      deps='No performance claims. Creatine scoop/serving discrepancy open: no serving numbers.')
piece('2026-12-10', PH_C, 'C09', 'Member math: holiday edition (calculator)',
      'Three orders. One year. Here is the math.',
      "Worked example over 12 months (illustrative): three orders of NAD+, Hydrate Strips and Pure Creatine Monohydrate.\n\n"
      "Everyday: $389.91. Member: $317.16. Gross saving $72.75, minus the $49.99 fee = $22.76 net.\n\n"
      "Your numbers will differ. Every product page shows its member price.\n\n" + DISC,
      'carousel', 'C09-member-math-3-orders', 'Do your own math', MEM, 'Qualified enrollments',
      platforms=('IG', 'FB', 'Threads'), deps='Recompute with live prices on publish day.')
piece('2026-12-10', PH_C, 'E04', 'EMAIL 4: Member math + gifts',
      'The honest math on membership',
      'Subject: "The honest math on membership". Body: calculator visual (C09) + "where Subscribe & Save fits better" + CTA. Footer gift-guide link.',
      'email', 'C09-member-math-3-orders', 'Do the math', MEM, 'Enrollments', platforms=('Email',))
piece('2026-12-11', PH_C, 'C10', 'For the longevity-curious: NAD+ and β-NMN',
      'Two capsules our longevity series is built around.',
      "From the EverLiv Longevity Series: NAD+ ($59.99, member $47.99) and β-NMN ($49.99, member $39.99).\n\n"
      "Read the full label, ingredients and directions on each product page.\n\n" + DISC,
      'feed', 'C10-longevity-pair', 'See the Longevity Series', '/collections/premium-longevity-series', 'Product sales, enrollments',
      platforms=('IG', 'FB'),
      deps='NO benefit claims (no "anti-aging", "cellular repair"). Names/prices only. Collection URL verified in audit.')
piece('2026-12-12', PH_C, 'C11', 'Behind the brand: how we\'d build a first order',
      'If we were starting from zero, this is our first cart.',
      "Talking-head or voiceover reel (script in scripts/): a team member builds a first EverLiv order on screen, shows member vs everyday prices, and explains when membership is and isn't worth it.",
      'reel', 'SPEC', 'Build your first cart', MEM, 'Trust, enrollments', platforms=('IG', 'FB', 'TikTok', 'YT'),
      deps='Needs filming by Jeff/Esther. No testimonial or results claims.')
piece('2026-12-13', PH_C, 'C12', 'Read the label: what is in an Energy Strip',
      'What is actually in an Energy Strip?',
      "Read the label with us: green-tea caffeine 50 mg, L-theanine 30 mg and vitamin B12, in a cranberry-flavoured strip that dissolves on the tongue.\n\n"
      "Contains caffeine. Not for children, pregnant or nursing women, or anyone sensitive to caffeine.",
      'carousel', 'C12-read-the-label-energy', 'See the full label', '/products/energy-strips', 'Education, product sales',
      kind='product', platforms=('IG', 'FB', 'Threads'), deps='Amounts from the printed Supplement Facts; re-check label before publishing.')
piece('2026-12-14', PH_C, 'C13', 'Order timing (no deadline promise)',
      'Shopping for the holidays? Here is how timing works.',
      "Orders are processed in 1 to 3 business days and typically arrive 3 to 7 days after that, with free U.S. shipping on every order.\n\n"
      "The earlier you order, the more breathing room you have.",
      'feed', 'C13-order-timing', 'Shop now', '/collections/all', 'Product sales', kind='brand',
      platforms=('IG', 'FB'), deps='Restate shipping policy only. NO "order by" date or delivery guarantee unless Jeff approves one.')
piece('2026-12-15', PH_C, 'C14', 'Member FAQ',
      'Your Member Price Club questions, answered.',
      "Does it renew automatically? No.\nDo all products get 20%? No: 20% or 15%, depending on the product; some are excluded.\n"
      "Does it combine with Subscribe & Save? No.\nWhat if I change my mind? Full refund within 3 business days; see the terms for the rest.\n\n" + DISC,
      'carousel', 'C14-member-faq', 'Read the full terms', '/pages/membership-terms', 'Trust, objection handling',
      platforms=('IG', 'FB', 'TikTok'))
piece('2026-12-16', PH_C, 'C15', 'The EverLiv Edit: gifts under $35',
      'Gifts under $35, chosen by us.',
      "Handmade soaps ($20.99), Hazelnut, Cocoa or Caramel coffee ($32.99), any oral strip ($34.99) and Pure Moringa ($24.99).\n\n"
      "Free U.S. shipping on every order.",
      'carousel', 'C15-edit-under-35', 'Shop the Edit', '/collections/all', 'Product sales', kind='product',
      platforms=('IG', 'FB', 'Pinterest*'), deps='Names and prices only; no benefit claims.')
piece('2026-12-17', PH_C, 'C16', 'Last-minute gifting (reel)',
      'Still shopping? Three gifts that are hard to get wrong.',
      "Coffee, a handmade soap or a tin of oral strips. Free U.S. shipping; orders are processed in 1 to 3 business days.",
      'reel', 'SPEC', 'Shop now', '/collections/all', 'Product sales', kind='product', platforms=('IG', 'FB', 'TikTok', 'YT'),
      deps='No delivery-by-Christmas promise.')
piece('2026-12-17', PH_C, 'E05', 'EMAIL 5: Last-minute gifts',
      'Three easy gifts',
      'Subject: "Three gifts that are hard to get wrong". Coffee / soap / strips tiles, shipping-policy line (no guarantee), membership footer.',
      'email', 'C16-last-minute', 'Shop now', '/collections/all', 'Product sales', kind='product', platforms=('Email',))
piece('2026-12-18', PH_C, 'C17', 'Gift yourself a year',
      'Done shopping for everyone else? This one is for you.',
      "Founding Membership: $49.99 once, 12 months of member pricing on eligible products for your own routine. No automatic renewal.\n\n" + DISC,
      'feed', 'C17-gift-yourself', 'Become a Founding Member', MEM, 'Enrollments', platforms=('IG', 'FB', 'X', 'Threads'),
      deps='Must not suggest you can buy a membership for someone else (gift memberships not offered).')
piece('2026-12-19', PH_C, 'C18', 'Behind the brand: why we print every amount',
      'Why every EverLiv label shows every amount.',
      "No proprietary blends on our labels: each ingredient and its amount is printed, so you can see what you're taking.\n\nRead any label at everliv.life.",
      'carousel', 'C18-label-transparency', 'Read a label', '/pages/ingredients', 'Brand trust', kind='brand',
      platforms=('IG', 'FB', 'Threads'),
      deps='VERIFY: "no proprietary blends" must be true for every product shown. Keep to products checked.')
piece('2026-12-20', PH_C, 'C19', 'Member math in 20 seconds (reel)',
      '$49.99 divided by 20 percent. Here is why that number matters.',
      "The break-even in 20 seconds: $249.95 on 20% products, about $333 on 15% products. Above that, member pricing keeps working for your 12 months.\n\n" + DISC,
      'reel', 'C19-math-reel', 'Join: link in bio', MEM, 'Enrollments', platforms=('IG', 'FB', 'TikTok', 'YT'))

# ===== PHASE D: year-end routines (Dec 21-31) ================================================
piece('2026-12-21', PH_D, 'D01', 'Start before January',
      'You don\'t have to wait for January.',
      "Routines that last rarely start on January 1. They start on an ordinary Monday.\n\nStart yours this week: everliv.life",
      'feed', 'D01-start-before-january', 'Explore EverLiv', '/collections/all', 'Brand, product discovery', kind='brand',
      platforms=('IG', 'FB', 'Threads', 'X'))
piece('2026-12-22', PH_D, 'D02', 'Consistency over quick fixes',
      'Consistency beats intensity.',
      "Five small habits that are easier to keep than a resolution: a glass of water first thing, a set time for your daily capsule, "
      "a coffee you actually look forward to, a two-minute evening wind-down, one product at a time.\n\nNo quick fixes. Just routines that fit.",
      'carousel', 'D02-consistency', 'Build your routine', '/collections/all', 'Engagement, saves', kind='brand',
      platforms=('IG', 'FB', 'TikTok'), deps='Habit content only; no health outcome claims.')
piece('2026-12-23', PH_D, 'D03', 'The morning ritual (reel)',
      'A morning routine in four quiet steps.',
      "Coffee, a strip, a minute of stillness, then the day. A morning ritual with EverLiv.\n\n" + AI_DISC,
      'reel', 'SPEC', 'Explore EverLiv', '/collections/all', 'Reach, brand', kind='product', platforms=('IG', 'FB', 'TikTok', 'YT'))
piece('2026-12-24', PH_D, 'D04', 'Holiday greeting (no sell)',
      'From all of us at EverLiv: happy holidays.',
      "Wishing you a calm, warm and well-rested holiday. From all of us at EverLiv.",
      'feed', 'D04-holiday-greeting', 'None (brand)', '/', 'Community', kind='brand', platforms=('IG', 'FB', 'Threads', 'X'))
piece('2026-12-26', PH_D, 'D05', 'The year ahead: member pricing for all of it',
      'Twelve months. Every eligible order. One payment.',
      "Join this week and your 12 months of member pricing cover nearly all of 2027. $49.99 once, founding price through January 31.\n\n" + DISC,
      'feed', 'D05-year-ahead', 'Become a Founding Member', MEM, 'Enrollments', platforms=('IG', 'FB', 'X'),
      deps='Term = 12 months from activation; "nearly all of 2027" true for joins Dec 26-31.')
piece('2026-12-27', PH_D, 'D06', 'Find your format (poll-led)',
      'Strips, capsules or powders: what fits your day?',
      "Strips dissolve on the tongue. Capsules are the classic daily routine. Powders mix into water, shakes or coffee.\n\nWhich fits your day? Tell us below.",
      'carousel', 'D06-find-your-format', 'Comment / poll', '/collections/all', 'Engagement', kind='brand',
      platforms=('IG', 'FB', 'TikTok', 'Threads'))
piece('2026-12-28', PH_D, 'D07', 'Build your 2027 routine',
      'Build a 2027 routine around what you already like.',
      "Pick one product per moment of your day: morning (coffee or Energy Strips), midday (Hydrate Strips), training days (creatine), evening (a handmade soap).\n\n"
      "Members get 20% or 15% off eligible products, all year.\n\n" + DISC,
      'carousel', 'D07-routine-2027', 'Build your routine', MEM, 'Enrollments, discovery', platforms=('IG', 'FB'))
piece('2026-12-28', PH_D, 'E06', 'EMAIL 6: Start the year as a Founding Member',
      'Start 2027 with member pricing',
      'Subject: "Start 2027 with member pricing". Body: D07 routine visual + offer block + break-even line + CTA. Founding price through Jan 31.',
      'email', 'D07-routine-2027', 'Become a Founding Member', MEM, 'Enrollments', platforms=('Email',))
piece('2026-12-29', PH_D, 'D08', 'Discover What\'s Next (series intro)',
      'EverLiv keeps evolving. So will this feed.',
      "Introducing Discover What's Next: a regular look at how EverLiv is growing, from new ways to use the range to what we're working on.\n\n"
      "Your wellness journey evolves. So does EverLiv.",
      'feed', 'D08-discover-whats-next', 'Follow along', '/', 'Brand, retention', kind='brand', platforms=('IG', 'FB', 'Threads'),
      deps='Must not promise products, dates or exclusive access until Restructuring confirms new products.')
piece('2026-12-30', PH_D, 'D09', 'One month left at the founding price',
      'One month left at $49.99.',
      "The $49.99 founding price runs through January 31, 2027 (ET). From February 1, membership is $69.99.\n\n"
      "Same 12 months of member pricing either way; joining earlier just costs less.\n\n" + DISC,
      'feed', 'D09-one-month-left', 'Become a Founding Member', MEM, 'Enrollments', platforms=('IG', 'FB', 'X', 'Threads'),
      deps='Feb 1 price change: Restructuring Shopify Flow enabled; re-confirm before publishing.')
piece('2026-12-31', PH_D, 'D10', 'A Year of More',
      'Here is to a year of more.',
      "More routines that fit. More to discover. More of what works for you.\n\nHappy New Year from EverLiv. Founding Membership: $49.99 through January 31.\n\n" + DISC,
      'feed', 'D10-year-of-more', 'Become a Founding Member', MEM, 'Brand + enrollments', platforms=('IG', 'FB', 'Threads', 'X'))

# ---------------------------------------------------------------------------------------------
# Stories (IG + FB) daily themes. Story sets are templated frames (assets/stories/).
STORY_THEMES = {
    'A · Teaser & reveal': ['Countdown sticker to Monday', 'Poll: "What do you think is coming?"', 'Emblem close-up'],
    'B · Black Friday / Cyber Monday': ['Offer frame + link sticker', 'Quiz: "How long does member pricing last?"', 'Break-even frame'],
    'C · Holiday gifting': ['Gift-guide frame + link', 'Poll: "Coffee or soap?"', 'Member reminder frame'],
    'D · Year-end routines': ['Question box: "Your 2027 routine?"', 'Founding price reminder', 'Routine frame'],
}
TIMES = {'IG feed': '11:30', 'IG carousel': '11:30', 'IG reel': '18:30', 'IG story': '09:00 & 19:30', 'FB feed': '12:00',
         'FB reel': '18:30', 'FB story': '09:00 & 19:30', 'TikTok': '19:00', 'YT': '17:00', 'Threads': '09:30', 'X': '10:00',
         'Email': '10:00', 'Pinterest*': '20:00'}

def phase_for(d):
    if d <= dt.date(2026, 11, 26): return PH_A
    if d <= dt.date(2026, 11, 30): return PH_B
    if d <= dt.date(2026, 12, 20): return PH_C
    return PH_D

def adapt(p, plat):
    """Platform-specific caption."""
    c = p['caption']
    if plat in ('X',):
        s = p['short'] if len(p['short']) < 150 else p['hook']
        tail = ' ' + url(p['path'], 'x', 'social', p['id'].lower())
        txt = s + ('\n' + DISC_SHORT if p['kind'] == 'member' else '')
        return (txt + tail)[:600]
    if plat == 'Threads':
        body = c.split('\n\n' + DISC)[0]
        return body + ('\n\n' + DISC_SHORT if p['kind'] == 'member' else '') + '\n' + url(p['path'], 'threads', 'social', p['id'].lower())
    if plat == 'TikTok':
        body = c.split('\n\n' + DISC)[0]
        return body + ('\n\n' + DISC_SHORT if p['kind'] == 'member' else '') + '\nLink in bio. #EverLiv #wellnessroutine'
    if plat == 'YT':
        return p['hook'] + ' | EverLiv' + ('\n' + DISC_SHORT if p['kind'] == 'member' else '')
    if plat == 'FB':
        return c.replace('Join through the link in bio.', 'Join: ' + url(p['path'], 'facebook', 'social', p['id'].lower())).replace(
            'link in bio', url(p['path'], 'facebook', 'social', p['id'].lower()))
    return c

def rows():
    out = []
    for p in P:
        d = dt.date.fromisoformat(p['date'])
        for plat in p['platforms']:
            if plat == 'Email':
                fmt = 'Email'; t = TIMES['Email']; dest = url(p['path'], 'email', 'email', p['id'].lower())
            elif plat in ('IG', 'FB'):
                f = {'feed': 'feed', 'carousel': 'carousel', 'reel': 'reel'}[p['fmt']]
                fmt = f'{plat} {f}'; t = TIMES.get(fmt, TIMES['IG feed'] if plat == 'IG' else TIMES['FB feed'])
                dest = url(p['path'], 'instagram' if plat == 'IG' else 'facebook', 'social', p['id'].lower())
            else:
                fmt = {'TikTok': 'TikTok video' if p['fmt'] == 'reel' else 'TikTok photo carousel', 'YT': 'YouTube Short',
                       'Threads': 'Threads post', 'X': 'X post', 'Pinterest*': 'Pinterest pin'}[plat]
                t = TIMES[plat]; src = {'TikTok': 'tiktok', 'YT': 'youtube', 'Threads': 'threads', 'X': 'x', 'Pinterest*': 'pinterest'}[plat]
                dest = url(p['path'], src, 'social', p['id'].lower())
            asset = p['asset']
            prod = 'SPEC (needs filming/editing)' if asset == 'SPEC' else 'see manifest'
            dep = p['deps']
            if plat == 'Pinterest*': dep = ('Pinterest account not confirmed among EverLiv\'s six accounts; include only if one exists. ' + dep).strip()
            if plat == 'X': dep = (dep + ' X is a paid Metricool add-on: post natively.').strip()
            out.append(dict(Date=p['date'], Day=d.strftime('%a'), Time=f"{t} {TZ}", Platform=plat, Format=fmt, Phase=p['phase'],
                            ID=p['id'], Title=p['title'], Hook=p['hook'], Caption=adapt(p, plat), Asset=asset, CTA=p['cta'],
                            URL=dest, Objective=p['objective'], Production=prod, Approval='Awaiting review',
                            Dependencies=dep, Alternates=' | '.join(p['alt'])))
    # daily stories
    d = dt.date(2026, 11, 20)
    while d <= dt.date(2026, 12, 31):
        if d != dt.date(2026, 12, 25):
            ph = phase_for(d); th = STORY_THEMES[ph][(d.toordinal()) % 3]
            for plat in ('IG', 'FB'):
                out.append(dict(Date=d.isoformat(), Day=d.strftime('%a'), Time=f"{TIMES['IG story']} {TZ}", Platform=plat,
                                Format=f'{plat} story (2-4 frames)', Phase=ph, ID=f"S{d.strftime('%m%d')}", Title=f"Stories: {th}",
                                Hook=th, Caption='Frames from the story template set; link sticker to the day\'s destination.',
                                Asset='stories/story-template-set', CTA='Link sticker', URL=url(MEM, 'instagram' if plat == 'IG' else 'facebook', 'story', f"s{d.strftime('%m%d')}"),
                                Objective='Daily visibility, link taps', Production='Template ready; daily frame to assemble',
                                Approval='Awaiting review', Dependencies='Use same-day feed asset when relevant.', Alternates=''))
        else:
            out.append(dict(Date=d.isoformat(), Day='Fri', Time='10:00 ET', Platform='IG', Format='IG story (1 frame)', Phase=PH_D,
                            ID='S1225', Title='Stories: holiday greeting', Hook='Happy holidays', Caption='Single greeting frame (D04 asset). No sell.',
                            Asset='D04-holiday-greeting', CTA='None', URL='', Objective='Community', Production='Ready (reuse D04)',
                            Approval='Awaiting review', Dependencies='', Alternates=''))
        d += dt.timedelta(days=1)
    out.sort(key=lambda r: (r['Date'], r['Time'], r['Platform']))
    return out

if __name__ == '__main__':
    r = rows(); print(len(P), 'pieces', len(r), 'rows')
