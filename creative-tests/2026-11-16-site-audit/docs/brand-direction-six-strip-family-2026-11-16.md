# EverLiv brand direction and six-strip family imagery (Marketing, Nov 16, 2026)

**Source:** Jeff's direction, Nov 15, 11:52 PM ET.

**Status:**
- Recommendations and draft copy only.
- Nothing is published or uploaded to Shopify.
- No campaigns, spend or price changes.
- Restructuring owns all live implementation.

## 1. Six-tin strip family image
### Recommended assets
All in the `everliv-media` repo at `library/editorial/strips/`:

| Use | File | Size | Layout |
|---|---|---|---|
| **Desktop hero, strip section, email header** | `strips-family-6--desktop-3x2--transparent.png` (+ `--ivory-preview.jpg`) | 1920×1280 (3:2) | Top: Energy · Sleep · Hydrate. Bottom: Collagen · D3+K2 · Iron |
| **Mobile hero or stacked section** | `strips-family-6--mobile-2x3--transparent.png` (+ `--ivory-preview.jpg`) | 1080×1620 (2:3) | Energy · Sleep / Hydrate · Collagen / D3+K2 · Iron |
| Wide banner or collection header | `strips-lineup-6-incl-sleep--row--transparent.png` | 3200×900 | single row |
| Square card | `strips-grid-6-incl-sleep--3over3--transparent.png` | 1800×1500 | 3 over 3, more air |

The script that rebuilds these is `compose_six_family.py`.

**How they're built:**
- **Source:** authentic supplier front renders only. Five come from the library; Sleep comes from the store's main supplier render.
- **Fidelity:**
  - Product pixels are scaled once, uniformly. There is no recolouring, relighting, mirroring, redrawing or label editing.
  - The contact shadow sits on the background only.
- **Checks, run automatically:**
  - All six tins are fully inside the frame.
  - The opaque content clears every edge (desktop margin ≥ 93 px; mobile ≥ 92 px).
- **Order:** Energy, the best seller, leads. The two purple tins (Sleep, Iron) are kept apart.
- **Format:** the transparent PNGs drop onto the Capsule Ivory or white theme background.

### Desktop vs mobile
- **Desktop:** use the 3×2 image on the right half of the hero, beside the headline and CTA.
  - At a 600–700 px display width each tin is about 180 px wide, so every variety name is legible.
- **Mobile:** stack the headline and CTA above the 2×3 image.
  - At 390 px each tin is about 150 px wide.
  - Don't put the 3×2 behind text on mobile: the label text collides with the headline (current audit item B2).
- **Banner slots under 500 px tall:** use the 6-row lineup.

### Showing Sleep without implying it's in stock
- The image shows the product family only. It contains no price, stock or "available now" text.
- **Alt text:** "EverLiv oral strip family: Energy, Sleep, Hydrate, Collagen, D3 + K2 and Iron strip tins".
- **CTA:** link the image or CTA to the strip collection, where Sleep shows **Sold Out**.
- **Bundle:** don't make "Build your own" the image's CTA unless the bundle builder excludes or clearly marks Sleep while it is sold out (Restructuring).
- **Optional caption:** "Sleep Strips: sold out, back soon." Use a date only once Restructuring confirms the restock date. Nov 25 is the current plan, not a confirmed date.

### Sleep imagery quality
- **Verified:** Sleep's front render is the store's supplier render. Its label wording, layout and colour match the other five tins' system, and Raspberry flavor and 30 strips are shown.
- **Missing: a full-colour Sleep front render.** All Sleep images on the store are palette-reduced PNGs (112–256 colours); the other five tins are full-colour JPGs.
  - At hero sizes the effect is a slightly flatter tin face, with less tonal shading than its neighbours. It's visible on close inspection at 100%, but not at web display size.
  - **Request through Restructuring:** the original full-colour Supliful Sleep Strips front render (the same render type as the other five, not a new design). The composition rebuilds with no other change when it arrives.
- **Nothing else is missing.** No packaging or label artwork was invented.

### Correction to the overnight audit (item B5)
The pink, red and yellow "ORAL STRIP" sachets in the "EverLiv Difference" banner are not generic. They match the supplier's own sachet artwork, as shown in the store's Sleep supplier images. What remains unverified is whether each sachet colour matches its own variety.

## 2. Brand messaging: strips lead, the portfolio is broader
**Positioning (draft for approval):**
- EverLiv is a daily wellness brand.
- Its best-selling, most distinctive format is the oral strip.
- The full range spans strips, capsules and powders (plus coffee and body care), so customers choose the format that fits their day. They don't need every format.

**Hero options (pick one):**
1. **"Wellness in the format that fits your day."** Strips, capsules and powders. Start with our best-selling oral strips.
2. **"Start with a strip. Build from there."** Six oral strips, plus capsules and powders for the rest of your routine.
3. **"Your daily routine, your way."** Dissolvable strips, everyday capsules, mix-in powders.

**Format line (for homepage, collections and About):**
- **Oral strips:** dissolve on your tongue; no water, no pills. Six varieties.
- **Capsules:** a simple daily routine, from Magnesium to Testosterone & NAD+ Support.
- **Powders:** mix into water, shakes or coffee: creatine, collagen and protein.

**Short brand intro:**
> EverLiv makes daily wellness easy to fit into a real day. Start with our best-selling oral strips, which dissolve on your tongue with no water needed, then add the capsules or powders that suit your routine. Every ingredient is listed on our labels, with free U.S. shipping on every order.

**Do not say:**
- "complete system", "you need all three" or "24-hour system" (the latter is pending brand-voice approval)
- "absorbs faster" or "skips digestion"
- any testosterone "boost"
- "longevity"
- "men's formula" or "women's formula"

## 3. Recommended featured-product order (homepage)
This follows Jeff's order. It is a merchandising recommendation, and Restructuring implements it.

| # | Feature | Image | Copy direction | Gate before prominent use |
|---|---|---|---|---|
| 1 | **Oral strips / Build Your Own** (Any 3 Strips, $79.99, Save 24%) | 6-tin family (above) | "Six strips. Pick any three." Show the transparent maths: 3 × $34.99 = $104.97 → $79.99 | The bundle builder must handle the sold-out Sleep correctly. "Natural Extracts" on the tins is still unverified (organic use OK, no paid ads) |
| 2 | **Testosterone & NAD+ Support** | the current Quantus product image (1024 px) | Premium, ingredient-led and gender-neutral (below) | Hormone claim review; image accuracy; possible Quantus hold |
| 3 | **Pure Creatine Monohydrate** | supplier render | Plain and factual: "Creatine monohydrate, one ingredient" | **Open label discrepancy:** a 5.6 g scoop vs 5,000 mg declared. Don't show serving numbers until resolved |
| 4 | **Creatine+ Electrolytes** | supplier render | "Creatine with electrolytes, mixed in water" | Routine substantiation for front-label claims |

**Breadth row** (after the four features): three tiles, **Strips · Capsules · Powders**, each linking to a format collection. If format collections don't exist, Restructuring decides whether to create them. This shows the range without implying customers must buy every format.

## 4. Testosterone & NAD+ Support: premium positioning without overclaiming
**Verified from the live page:**
- Name, price ($79.95) and SKU EVERLIV-TS002.
- The copy reads: "Standardized botanical extracts. Zero proprietary blends. Fully transparent dosing… for men and women…".

**Not verified by Marketing:**
- the ingredient list and amounts (they're on the label image, not in the page text)
- the basis for "for men and women"
- substantiation for "testosterone", "fat metabolism", "nitric oxide" and "NAD+" benefits

**Gender positioning:**
- The page currently says "for men and women".
- **Neither** men-only **nor** "men and women" should be stated until Quantus's formulation and intended-use documents support it.
- Recommended interim wording: neutral. Describe the product and its label; name no audience.

**Draft premium copy (conservative, for owner and legal review):**
> **Testosterone & NAD+ Support.** Our premium daily formula: standardized botanical extracts and NAD+ support in one capsule, with every ingredient and amount listed on the label. No proprietary blends.

- "Standardized", "zero proprietary blends" and "every amount listed" must be confirmed against the actual label before use.
- Add any structure/function statement only after substantiation and legal review, with the FDA disclaimer.

**Avoid:** "boost", "raise", "restore" or "optimize testosterone"; "hormone balance"; "longevity" or "anti-aging"; "fat burning"; and any before/after or physique imagery.

## 5. Sleep Strips: individual visibility
- **Recommendation to Restructuring:** keep Sleep Strips published and visible in the strip collection and on its product page, marked **Sold Out**, until inventory returns.
  - No pre-order and no "back in stock" date unless confirmed.
  - An optional "notify me" only if an existing installed app supports it, with no new spend.
- **Copy:** before promoting Sleep individually after the restock, replace "effectively improves both the quality and quantity of sleep" with: "Melatonin may help support a normal sleep-wake cycle.*" (claims audit §4).

## 6. Notes corrected (discontinuation claims)
All Project docs and repo notes that called Testosterone & NAD+ "discontinued" now record it as **active**. Each correction is labelled.

**Project docs:**
- `everliv-marketing-overnight-audit-2026-11-16.md` (§21 evidence trail)
- `claims-audit-2026-11-16.md`
- `restructuring-handoff-marketing-audit-2026-11-16.md`
- `seo-plan-2026-11-16.md`
- `marketing-materials-pack-2026-11-16.md`
- `restructuring-request-2026-11-14-evening.md`
- `production-readiness-shortlist-2026-11-14.md`
- `marketing-status-2026-11-11.md`

**Repo:** `library/BEST-VERIFIED-IMAGERY.md`.

**Not edited:** `EverLiv-Marketing-Handoff-2026-11-11.md` is Restructuring's document. It says "not carried forward / Do not market these", not "discontinued". Its "do not market" line is superseded by Jeff's Nov 15 direction; Restructuring may want to annotate its own copy.
