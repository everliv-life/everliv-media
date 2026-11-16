"""Generate EverLiv Packaging Reference Profiles (families + per-product inventory) from structured data.
Sources: live store products.json (everliv.life, fetched 2026-11-14), media library, Supliful catalog listings (checked 2026-11-14)."""
import json, os, csv, glob
from collections import OrderedDict

STORE = json.load(open('/home/claude/catalog/products.json'))
SUP = {x['slug']: x for x in json.load(open('/home/claude/catalog/supliful-confirmed.json'))['listings']}
LIB = '/home/claude/everliv-media-repo/library'
OUT = '/home/claude/everliv-media-repo/library/packaging-profiles'
os.makedirs(OUT + '/families', exist_ok=True)

V, E, M = 'VERIFIED', 'ESTIMATE', 'MISSING'

FAMILIES = OrderedDict()
def fam(fid, name, **k): FAMILIES[fid] = dict(id=fid, name=name, **k)

fam('PF-01', 'Airless pump bottle, 30 ml (overcap)',
    shape='Straight cylinder, white; airless pump under a separate full-diameter overcap; flat base with small rounded edge. No protruding collar: overcap meets body at a fine seam (two seam lines), body continues white to the label.',
    construction='Overcap (glossy) ends ~29% down from top; fine seam lines at cap edge and shoulder step; pump head with angled nozzle and stepped collar visible only with cap off (Supliful cap-off mockups). Front-render proportion H/D ~3.59 (silhouette 432 x 1550 px).',
    materials='Cap: glossy white plastic (visual). Body: satin white plastic (visual). Label: matte paper, slightly cooler white than plastic (visual). Opacity of cap/collar not documented.',
    dims=[('Volume', '1 fl oz / 30 ml', V, 'Supliful listing + label'), ('Gross weight', '1.76 oz / 50 g', V, 'Supliful listing'),
          ('Height, diameter, cap height', 'H/D ~3.59; cap ~29% of height', E, 'measured from supplier front render'),
          ('Label wrap', '~315 deg, label 1700x1360 artwork px', E, '3D accuracy test, Nov 14')],
    label='Wrap-around label; centre panel with logo, vertical title between gold rules, series line, net contents; left: suggested use/warnings/address; right: ingredients, QR, four claim badges.',
    refs='Store: front, cap-off, flat label (presentation image), texture. Supliful: cap-on blank, 2x cap-off blank, 3 lying bottles (side views).',
    gaps='Physical dimensions; resin/finish/opacity; print-ready label; wrap length & seam position; pump geometry; back/side branded views.',
    special='3D accuracy model exists (internal, provisional). Label questions open (Premium Body Care Series, Net Wt., badges).',
    safe='Front-on or near-eye-level only, using the authentic front render; no lifestyle with cap-off pump until pump geometry is verified.')
fam('PF-02', 'Square hinged metal tin, oral strips (30 strips in sachets)',
    shape='Square tin with rounded corners, black metal body, printed lid label on top face; hinged lid; contains individual foil sachets ("ORAL STRIP" generic sachets).',
    construction='Two-part hinged tin (lid + base); lid label covers top face inside a black rim; rim thickness and lid step visible in angled views; inner sachets are supplier-standard and not customised.',
    materials='Black (painted/coated) metal tin; printed paper or film lid label (finish unknown); sachets: printed foil, colour varies by product.',
    dims=[('Contents', '30 oral strips', V, 'labels'), ('Gross weight', '2.2-2.24 oz / 64 g', V, 'Supliful listings'),
          ('Tin width/height/depth, corner radius, rim width', 'square, ~1:1 face', E, 'front renders'), ('Hinge & lid step', 'visible in angled renders', E, 'store/Supliful angled renders')],
    label='Lid-label artwork per product (logo, product name, flavour, three feature words incl. "Natural Extracts", DIETARY SUPPLEMENT 30 ORAL STRIPS). Energy has a flat production label in library.',
    refs='Store: front, open tin, stack, tin+packet, packet+strip, facts. Supliful: blank lid front, open tins, sachets, tumbling tins.',
    gaps='Tin dimensions & corner radius; rim/lid depth; lid label finish (gloss/matte) and print files for 5 of 6 products; sachet artwork per flavour; back of tin.',
    special='Front-only renders read flat in angled scenes (Nov 14 tests): needs thickness, rim highlight, metal response. "Natural Extracts" unverified - blocks strip-tin content. Sleep Strips excluded from promotion.',
    safe='Straight-on, eye-level, soft frontal light; or use Supliful/store angled renders as-is.')
fam('PF-03', 'Round capsule bottle, white, screw cap (60-120 ct)',
    shape='White round supplement bottle with shoulder, short neck and white ribbed screw cap; wrap-around label on body.',
    construction='Bottle + screw cap (+ likely induction seal); label panel on straight body section; Supplement Facts on side panel.',
    materials='White plastic bottle (HDPE likely, not documented); white cap; label finish not documented (appears matte with metallic/colour series band).',
    dims=[('Counts', '60 caps (Lion\'s Mane, Ashwagandha, Moringa, Berberine); others per label', V, 'Supliful listings / labels'), ('Gross weights', '45-113 g', V, 'store/Supliful'),
          ('Bottle size(s)', 'likely 2-3 sizes (gross weight 45-113 g)', E, 'unverified - may differ between products'), ('Label height/wrap', '-', M, '')],
    label='Series design: logo, series band ("Premium Botanical/Longevity Series"), product name, descriptor, count; colour varies (white, burgundy, blue).',
    refs='Store: front, open/tumbling bottles, capsules, facts. Supliful: blank bottle front/side/open/tumbling.',
    gaps='Bottle size per SKU (likely more than one); cap dimensions/ribs; label print files & wrap; back panel views.',
    special='Do not assume all 10 products share one bottle size; verify per SKU before any shared geometry is used.',
    safe='Authentic front renders; label side panel only via facts image.')
fam('PF-04', 'Gummy bottle (dark/amber, wide-mouth)',
    shape='Wide-mouth bottle with white cap; dark (amber/brown) body with gummies visible; wrap label.',
    construction='Bottle + screw cap; contents visible through body.',
    materials='Dark translucent plastic (visual, unverified); white cap.',
    dims=[('Contents', '60 gummies', V, 'Supliful listing'), ('Gross weight', '7.2 oz / 204 g', V, 'Supliful'), ('Bottle dims', '-', M, '')],
    label='Mushroom Extract Blend label; contents visible.', refs='Store: front, tumbling, open with gummies, facts. Supliful: blank bottle views.',
    gaps='Bottle dims, translucency/colour spec, label files.', special='Translucent body: contents must look like the actual gummies (shape/colour).', safe='Authentic renders only.')
fam('PF-05', 'Short wide powder tub, white (creatine/glutamine)',
    shape='Short, wide white tub with large white screw lid; wrap-around label (blue series).', construction='Tub + screw lid; scoop inside.',
    materials='White plastic tub and lid (finish semi-gloss, visual).',
    dims=[('Creatine net', '9.9 oz / 281 g', V, 'Supliful'), ('Creatine gross', '10.9 oz / 308 g', V, 'Supliful'), ('Creatine + Electrolytes gross', '13.6 oz / 386 g', V, 'Supliful'), ('Tub dims', '-', M, '')],
    label='Blue series label, product name, descriptor; Creatine+Electrolytes flat label image exists on store.', refs='Store: front, lid-off, stack, powder+scoop, facts. Supliful: blank tub front, angled, top/lying.',
    gaps='Tub/lid dims, scoop geometry, label files (2 of 3).', special='Creatine scoop discrepancy (5.6 g vs 5,000 mg) open; no serving-weight visuals.', safe='Authentic renders; lid-off/scoop only from authentic images.')
fam('PF-06', 'Short wide powder jar, black (Vitamin C & Prebiotic Mushroom Blend)',
    shape='Short wide jar, black body/black lid, white-panel label.', construction='Jar + screw lid.', materials='Black plastic (visual).',
    dims=[('Gross weight', '272 g (store)', V, 'store variant weight'), ('Jar dims', '-', M, '')], label='Premium series label on black.', refs='Store: front, open, powder, facts.',
    gaps='Supliful listing match, dims, finish, label files.', special='Dark packaging: needs rim/specular light to read.', safe='Authentic renders.')
fam('PF-07', 'Tall powder tub, white (collagen, bee bread, cleanse)',
    shape='Tall white tub, white screw lid; wrap label (taupe/sage series).', construction='Tub + lid; Bee Bread contains sachets.',
    materials='White plastic (visual).',
    dims=[('Collagen Peptides Chocolate net', '378 g', V, 'Supliful'), ('Collagen Peptides Chocolate gross', '499 g', V, 'Supliful'), ('Others', 'gross 159-376 g', V, 'store weights'), ('Tub sizes', 'possibly 2 sizes', E, 'unverified')],
    label='Premium Nutrition Series labels; collagen peptides flat label image on store.', refs='Store: front, scoop, facts, flat label (1). Supliful: blank tall tub, lying tub.',
    gaps='Tub size per SKU, lid dims, label files (4 of 5).', special='Bee Bread: sachet format inside - confirm before showing contents.', safe='Authentic renders.')
fam('PF-08', 'Large protein tub (whey / plant)',
    shape='Large white tub with white lid; wrap label (white or sage).', construction='Tub + lid; scoop.', materials='White plastic (visual).',
    dims=[('Gross weight', '~907-924 g', V, 'store'), ('Tub dims', '-', M, '')], label='Pure Whey / Plant Protein labels.', refs='Store: front, powder, facts.',
    gaps='Supliful listing match, dims, label files.', special='-', safe='Authentic renders.')
fam('PF-09', 'Kraft coffee bag, 12 oz / 340 g',
    shape='Kraft stand-up gusseted bag (block-bottom), EVERLIV COFFEE print with flavour label panel; angled render shows a carton/sleeve form.',
    construction='Flexible bag - shape varies with fill and folding; flavour label panel on front.', materials='Kraft paper (visual); clear/foil inner not documented.',
    dims=[('Net weight', '12 oz / 340 g', V, 'label'), ('Gross', '383 g', V, 'store'), ('Bag dims', '-', M, '')],
    label='Flavour panel (FLAVOR / roast / tasting notes / bean form / Net Wt); flat label images in library.', refs='Store: bag front, angled, with beans, flat label; Supliful listings exist (slugs confirmed for 4 flavours by name).',
    gaps='Bag dims, gusset, valve, carton vs bag configuration (angled render differs), label files.', special='Flexible packaging: no 3D model; authentic renders only. Clarify bag vs carton.', safe='Authentic renders only.')
fam('PF-10', 'Bar soap with paper band label, 4 oz / 113 g',
    shape='Rectangular handmade soap bar; paper band/sleeve label around the middle; soap colour/texture visible at ends.',
    construction='Natural bar (variable surface); printed band.', materials='Soap (handmade, each bar varies); paper band (finish unknown, gold foil corner visual).',
    dims=[('Net weight', '4 oz / 113 g', V, 'Supliful'), ('Gross', '4.3-4.48 oz / 122-127 g', V, 'Supliful'), ('Bar & band dims', '-', M, '')],
    label='Band label per scent (logo, name, descriptor, Net Wt) with full back text; flat label images for all 6 in library/store.', refs='Store: bar front, flat label; Supliful: blank bars and bands, stacked views.',
    gaps='Bar/band dims, band finish (gold foil?), soap colour per batch.', special='Natural product: soap texture/colour must match the specific scent; no invented soap colours.', safe='Authentic renders; flat label usable for 3D band mapping once dims known.')

# product -> family, supliful slug, notes
P = OrderedDict([
 ('everliv-peptide-eye-serum', ('PF-01', 'peptide-eye-gel-cream', 'Label wording questions open (Q4).')),
 ('energy-strips', ('PF-02', 'energy-strips', 'Flat production label in library.')),
 ('everliv-sleep-strips', ('PF-02', 'sleep-strips', 'EXCLUDED from promotion (owner).')),
 ('everliv-hydrate-strips', ('PF-02', None, '')),
 ('everliv-iron-strips', ('PF-02', 'iron-strips', '')),
 ('everliv-k2-d3-strips', ('PF-02', 'bone-support-strips', 'Library cutout failed; use render.')),
 ('everliv-collagen-strips', ('PF-02', 'beauty-collagen-strips', 'Library front-cutout degraded; use cutout v2 (creative-tests/2026-11-14-photoreal).')),
 ('everliv-everglo-essentials', ('PF-03', None, 'Supliful name likely "Hair, Skin & Nails Essentials" (SKU HSANE) - confirm.')),
 ('everliv-ignitefx-with-mct', ('PF-03', None, 'Supliful name likely "Fat Burner with MCT" (SKU FBWM) - confirm.')),
 ('everliv-lions-mane-mushroom', ('PF-03', 'lions-mane-mushroom-capsules', '')),
 ('everliv-ashwagandha-black-pepper', ('PF-03', 'ashwagandha-capsules', '')),
 ('everliv-pure-moringa', ('PF-03', 'moringa-pure-capsules', '')),
 ('everliv-resveratrol-600mg', ('PF-03', None, '')),
 ('everliv-nad', ('PF-03', None, '')),
 ('everliv-magnesium-glycinate', ('PF-03', 'magnesium-glycinate-capsules', 'Magnesium form question open (Q3).')),
 ('everliv-granular-berberine', ('PF-03', 'berberine-capsules', 'Store says Granular Berberine; Supliful listing "Berberine" - confirm same SKU.')),
 ('everliv-β-nmn', ('PF-03', None, '')),
 ('everliv-mushroom-extract-gummies', ('PF-04', 'mushroom-extract-gummies', '')),
 ('everliv-pure-creatine-monohydrate', ('PF-05', 'creatine-monohydrate-powder', 'Scoop 5.6 g vs 5,000 mg open (Q1).')),
 ('everliv-pure-l-glutamine-powder', ('PF-05', None, '')),
 ('everliv-creatine-electrolytes', ('PF-05', 'creatine-hydration-powder', 'Flat label image on store page (not yet in library).')),
 ('everliv-vitamin-c-prebiotic-mushroom-blend', ('PF-06', None, '')),
 ('everliv-collagen-creamer-vanilla', ('PF-07', None, '')),
 ('everliv-collagen-peptides-powder', ('PF-07', None, 'Flat label image on store page (not yet in library).')),
 ('everliv-collagen-peptides-powder-chocolate', ('PF-07', 'grass-fed-collagen-peptides-powder-chocolate', '')),
 ('everliv-bee-bread-powder', ('PF-07', None, 'Sachets inside tub.')),
 ('everliv-natures-ultra-cleanse-smoothie-greens', ('PF-07', None, '')),
 ('everliv-pure-whey-protein-isolate-chocolate', ('PF-08', None, '')),
 ('everliv-pure-whey-protein-isolate-vanilla', ('PF-08', None, '')),
 ('everliv-pure-plant-protein-chocolate', ('PF-08', None, '')),
 ('everliv-pure-plant-protein-vanilla', ('PF-08', None, '')),
 ('everliv-hazelnut-coffee-medium-roast', ('PF-09', None, 'Supliful listing exists by name (slug not yet confirmed).')),
 ('everliv-cocoa-coffee-medium-roast', ('PF-09', None, '')),
 ('everliv-mushroom-coffee-medium-roast', ('PF-09', None, '')),
 ('everliv-caramel-coffee-dark-roast', ('PF-09', None, '')),
 ('everliv-clean-forrest-soap', ('PF-10', 'slumber-soap', 'Store title "Slumber Soap"; handle says clean-forrest. Flat band label image on store page (not yet in library).')),
 ('everliv-charcoal-soap', ('PF-10', 'charcoal-soap', 'Flat band label image on store page (not yet in library).')),
 ('coconut-beach-soap', ('PF-10', 'coconut-beach-soap', 'Flat band label image on store page (not yet in library).')),
 ('everliv-sandalwood-soap', ('PF-10', 'rich-sandalwood-soap', 'Flat band label image on store page (not yet in library).')),
 ('everliv-aloe-cool-cucumber-soap', ('PF-10', 'aloe-cool-cucumber-soap', 'Flat band label image on store page (not yet in library).')),
 ('everliv-milk-honey-soap', ('PF-10', 'oat-milk-honey-soap', 'Flat band label image on store page (not yet in library).')),
])
NONCAT = {'ultimate-bundle': 'Bundle of PF-02 tins (choose 3) - uses strip-tin profiles.',
          'everliv-testosterone-nad-support': 'EXCLUDED: discontinued Quantus product (owner); do not use.',
          'black-friday-aroma-therapy-bundle': 'Bundle of PF-10 soaps.', 'black-friday-sale-coffee-gift-pack': 'Bundle of PF-09 coffees.'}

by = {p['handle']: p for p in STORE}
missing = [h for h in P if h not in by]; extra = [h for h in by if h not in P and h not in NONCAT]
assert not missing and not extra, (missing, extra)

def lib_dir(h):
    for d in os.listdir(LIB):
        if d != 'packaging-profiles' and (h.endswith(d) or d in h.replace('everliv-', '')): return d
    return None

rows = []
for h, (fid, slug, note) in P.items():
    p = by[h]; v = p['variants'][0]; ld = lib_dir(h)
    libfiles = sorted(os.listdir(f'{LIB}/{ld}')) if ld else []
    flat = any('flat' in f for f in libfiles)
    rows.append(OrderedDict(handle=h, title=p['title'], sku=v.get('sku'), family=fid, price=v['price'], store_grams=v.get('grams'),
        store_url=f'https://everliv.life/products/{h}', store_images=len(p['images']),
        supliful_url=(f'https://supliful.com/catalog/{slug}' if slug else 'TO CONFIRM'),
        supliful_gross_weight=SUP.get(slug, {}).get('gross_weight', ''), supliful_amount=SUP.get(slug, {}).get('amount', ''),
        media_library=(f'library/{ld}/ ({len(libfiles)} files)' if ld else 'NOT IN LIBRARY'), flat_label_in_library=('yes' if flat else 'no'),
        notes=note))
with open(OUT + '/inventory.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def readiness(fid, rs):
    if fid == 'PF-01': return 'Partial: 3D accuracy model (provisional); needs dims/materials/print file'
    if fid in ('PF-09', 'PF-10'): return 'Authentic 2D renders sufficient for straight-on use; flexible/natural - special handling'
    return 'Authentic 2D front renders sufficient for straight-on use; 3D needs dims + print files'

for fid, F in FAMILIES.items():
    rs = [r for r in rows if r['family'] == fid]
    L = [f"# {fid} — {F['name']}", '', f"**Products ({len(rs)}):** " + ', '.join(r['title'] for r in rs), '',
         f"**Status:** {readiness(fid, rs)}", '', '## Packaging type and visible shape', F['shape'], '',
         '## Cap, closure, seams, edges, construction', F['construction'], '', '## Materials, colour, finish, translucency, reflectivity', F['materials'], '',
         '## Dimensions and proportions', '| Item | Value | Status | Source |', '|---|---|---|---|']
    L += [f'| {a} | {b} | {c} | {d} |' for a, b, c, d in F['dims']]
    L += ['', '## Label artwork, placement, wording, branding', F['label'], '', '## Available references', F['refs'], '',
          '## Source links (per product)', '| Product | SKU | Store page | Supliful listing | Media library | Flat label |', '|---|---|---|---|---|---|']
    L += [f"| {r['title']} | {r['sku']} | {r['store_url']} | {r['supliful_url']} | {r['media_library']} | {r['flat_label_in_library']} |" for r in rs]
    L += ['', '## Verified vs estimated vs missing', '- VERIFIED = printed on the label or stated on the Supliful listing / store data.', '- ESTIMATE = measured from supplier renders; never claim as dimension.', '- MISSING = not available in any accessible source.', '',
          '## Missing information (request via Restructuring)', F['gaps'], '', '## Special handling / open authenticity or label-compliance questions', F['special']]
    pn = [f"- {r['title']}: {r['notes']}" for r in rs if r['notes']]
    if pn: L += [''] + pn
    L += ['', '## Safe composition when references are insufficient', F['safe'], '']
    slug = F['name'].split(',')[0].lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '')
    open(f"{OUT}/families/{fid}-{slug}.md", 'w').write('\n'.join(L))

# index markdown
idx = ['# EverLiv Packaging Reference Profiles — index (v1, 2026-11-14)', '',
       'Mandatory input for ANY product imagery (generator, compositing or 3D). See library/README.md "Product-authenticity process".', '',
       f'Live store: {len(STORE)} listings = {len(P)} Supliful products + {len(NONCAT)} non-catalog listings. (Restructuring handoff states 42 products — store shows {len(P)}; one product unaccounted for.)', '',
       '## Families', '| ID | Family | Products | Readiness |', '|---|---|---|---|']
for fid, F in FAMILIES.items():
    rs = [r for r in rows if r['family'] == fid]; idx.append(f"| {fid} | {F['name']} | {len(rs)} | {readiness(fid, rs)} |")
idx += ['', '## Non-catalog listings'] + [f'- `{k}`: {v}' for k, v in NONCAT.items()]
idx += ['', '## Per-product inventory', 'See `inventory.csv` (handle, SKU, family, store/Supliful links, weights, library coverage, notes).', '',
        '| Product | SKU | Family | Supliful listing | Library | Flat label |', '|---|---|---|---|---|---|']
idx += [f"| {r['title']} | {r['sku']} | {r['family']} | {r['supliful_url'].replace('https://supliful.com/catalog/','')} | {'yes' if 'NOT' not in r['media_library'] else 'no'} | {r['flat_label_in_library']} |" for r in rows]
open(OUT + '/README.md', 'w').write('\n'.join(idx) + '\n')
print(len(rows), 'products;', sum(1 for r in rows if 'NOT' not in r['media_library']), 'in library;', sum(1 for r in rows if r['supliful_url'] != 'TO CONFIRM'), 'supliful confirmed;', sum(1 for r in rows if r['flat_label_in_library'] == 'yes'), 'flat labels in library')
for fid in FAMILIES: print(fid, sum(1 for r in rows if r['family'] == fid))
