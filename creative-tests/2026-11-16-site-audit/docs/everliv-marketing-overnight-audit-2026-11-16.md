# EverLiv Marketing: overnight audit and brand readiness report
**For:** Jeff and Esther · **Prepared:** Nov 15–16, 2026 (site checked 11:00–11:15 PM ET Nov 15 / 04:00–04:15 UTC Nov 16)

**Marketing made no live changes.** That means no edits to Shopify, Metricool, email, ads or any supplier contact.

---

## 1. Executive summary
The site's structure, pricing pages and policies are in good shape. **Ways to Save is now live and largely accurate.** The launch risk is in **content, not mechanics**. There are three **Critical** items:

1. **The discontinued Quantus Testosterone & NAD+ product is the homepage hero and the first "Start here" card**, and it is still purchasable ($79.95).
2. **`/pages/solutions` and the homepage "Shop by Need" tiles make hormone, neuro, memory and fat-burning claims** ("Natural testosterone support", "Neuroprotective support", "Improved memory retention", "Burn smarter, not harder").
3. **Product copy across about 15 SKUs carries disease-adjacent claims** (blood sugar, cholesterol, blood pressure, fat burning, immunomodulation) with no substantiation on file.

All three are fixable in Restructuring's queue with copy already drafted here. The highest-value non-claim fix is **image alt text**: it is empty on all 43 products, and paste-ready text is provided.

## 2. What was actually done, and when
- **All work happened during this active session, between about 10:00 PM and 11:30 PM ET on Nov 15.** Nothing ran unattended overnight, and nothing is scheduled to run.
- **Method:**
  - read-only fetches of `everliv.life` (products.json, 43 product pages, 40 nav/footer pages)
  - 13 screenshots at desktop and 390-px mobile width
  - text scanning plus manual classification
- **Files:** the browser-download method was stopped at 11:10 PM per your instruction. All data is written straight to the workspace, the repo and the Project, and the consolidated copy is in your connected Downloads folder (see §19). No Save As dialogs were triggered after your message.
- **Browser:** the viewport has been reset to desktop.

## 3. Brand and visual audit (prioritized)
| # | Rating | Finding | Evidence |
|---|---|---|---|
| B1 | **Critical** | The Testosterone (Quantus) product is hero slide 1 and the first "Start here" card | shots 02, 09, 10 |
| B2 | **High** | On the mobile hero, the headline overlaps the product's label text | shot 09 |
| B3 | **High** | The hero strips image clips the Collagen tin at the right edge | shot 01 |
| B4 | **High** | "Start here" leads with member prices while enrollment is closed (in Restructuring's queue) | shots 04, 10 |
| B5 | **Medium** | "The EverLiv difference" banner shows the sold-out Sleep tin plus generic "ORAL STRIP" sachets and fruit (not our packaging) | shot 06 |
| B6 | **Medium** | The Shop by Need and Solutions people photos are of unknown origin and rights (agency or AI) | shot 05 |
| B7 | **Medium** | The Eye Serum main image is tiny in frame (about 15%); the Collagen Creamer and Chocolate Collagen backgrounds are grey | shot 12 |
| B8 | **Medium** | The Eye Serum block shows "5.0 · 1 review" | shot 07 |
| B9 | **Low** | The tagline "The 24-Hour Bio-Optimization System" (in the title tag and footer) is vague and the brand voice isn't approved | shot 08 |
| OK | — | The palette (Ivory, Leaf, Fresh Press), typography and nav are consistent; product main images are uniform 2048² supplier renders | shot 12 |

## 4. Product image and packaging accuracy (product by product)
| Product | Store main image | Accuracy status |
|---|---|---|
| 6 soaps | supplier render | Label is gloss BOPP with printed gold (supplier, Nov 15). **Unverified against the physical product**: needs a sample (not ordered) |
| 4 coffees | carton **plus a clear valve bag of beans** | **Format unconfirmed** (carton, bag or both?). The Mushroom image shows ground coffee: check the label form |
| Energy, Hydrate, Iron, D3+K2, Collagen strips | supplier tin render | Renders match the library. "Natural Extracts" on the tin is unverified |
| Sleep Strips | supplier render (7 images) | Accurate render; **sold out until Nov 25; excluded from promotion** |
| Peptide Eye Serum | supplier render | Label matches the supplier's label PDF exactly (verified Nov 15). Image crop is too small |
| Capsules, tubs, pouches, gummies (≈24) | supplier renders | Consistent; not individually checked against labels tonight |
| Testosterone & NAD+ | 1024² legacy image | **Discontinued: remove** |

## 5. Oral strip imagery (requested focus)
- **Best approved strip images (new tonight, no clipping):**
  - `library/editorial/strips/strips-grid-5--3over2--transparent.png` (1800×1500), the best fit for the hero's right half
  - `strips-lineup-5--row--transparent.png` (2700×900), for banners and email headers
  - ivory-preview JPGs of each
- **Sleep Strips status:** no approved lifestyle imagery exists. The `-6-incl-sleep` lineup versions are built but **on HOLD** until the Nov 25 restock and your OK.
- **Recommendation:** use the 5-tin grid in place of the current clipped hero image, without Sleep. Restructuring has the repo paths (handoff R5).
- **Caveat:** all strip tins carry the unverified "Natural Extracts". Organic use is acceptable per the current rules; no paid ads.

## 6. Copy and claims audit
Full table: `claude/claims-audit-2026-11-16.md`. Every statement is classified Verified / Needs substantiation / Potentially misleading / Requires legal review, and conservative rewrites are included.

| Severity | Items |
|---|---|
| Critical (3) | Testosterone product; Solutions page claims; Berberine (blood sugar, cholesterol, heart, weight) |
| High (9) | IgniteFX fat burning; homepage "Burn smarter"; Resveratrol cholesterol and fat storage; Magnesium blood pressure; Mushroom "immunomodulating"; protein weight and hunger claims; Eye Serum fine lines and sensitive skin; soap and coffee "Organic" and "fair trade"; Sleep "effectively improves… sleep" |
| Medium (~12) | Eye Serum label badges (GMP, Cruelty Free, Made in USA); "Grass-Fed"; "Natural Extracts"; "Science-backed"; "Verified Buyer" and "Real Results"; bundle "Ships in 1–2 days"; FAQ "lab documents" |

**Focus items:**
- **Eye Serum vs Gel-Cream:** the supplier name and the ingredients indicate a gel-cream, and our homepage already says "gel-cream". This is your decision (see §18).
- **Cruelty Free / GMP / Made in USA:** printed on the Eye Serum label, with **no documentation**. Never repeat them in marketing.
- **Sensitive skin and fine lines:** remove them until test data exists.
- **Coffee:** "energy, focus, vitality" on Mushroom; "Organic" mushrooms need a certificate.
- **Collagen Strips:** the copy still says the supplier's name "Beauty + Collagen Strips"; the Nov 14 documentation questions are unanswered.
- **Sleep Strips:** the efficacy claim needs rewriting before restock promotion; a sleep testimonial is on the reviews page.
- **Disease language:** listed in the claims audit §7 for the attorney.

## 7. Eye Serum asset clarity
- **v9 render = glossy label.** It reflects the supplier's high-gloss BOPP confirmation. It is the current *internal* reference only.
- **v1–v8 = matte label.** Superseded; do not use. This is documented in `creative-tests/2026-11-14-eye-serum-3d-accuracy/renders/STATUS.md`.
- **No 3D render is approved for customer-facing use.** The supplier render remains the only public Eye Serum image.

## 8. Homepage storytelling
**Current sequence:**
1. hero carousel (Testosterone → strips)
2. strip bundle
3. Start here (member prices)
4. Shop by Series
5. Shop by Need (people)
6. EverLiv difference
7. Eye Serum
8. Instagram
9. footer

**Problems:**
- It opens with a discontinued, claim-heavy product.
- It leads with closed-membership pricing.
- There are three "browse" grids in a row (Series, Need, Start here) before any brand story.

**Recommended order (no new claims):**
1. Hero: oral strips, "Your vitamins, minus the water bottle" (5-tin grid).
2. Any 3 Strips, $79.99, with the transparent savings line.
3. Start here: four best-sellers at the everyday price.
4. "How to buy": a three-column Everyday / Subscribe & Save / Member (opening soon) strip linking to Ways to Save.
5. Shop by Series.
6. A gifting moment (coffee and soap collections), once approved.
7. Ingredients transparency ("every ingredient, every amount"), linking to `/pages/ingredients`.
8. Reviews only once provenance is confirmed.

## 9. Ways to Save marketing review (live as of 11:15 PM ET)
**Verified good:**
- All three options are present.
- Membership: $49.99 once for 12 months; up to 20%; no auto-renewal; doesn't combine; **enrollment closed** is stated.
- Subscribe & Save: up to 15%; every 1–2 months; skip or cancel before billing.
- The comparison table is present.
- The example maths is correct ($34.99 → $27.99 member, 20%; $29.74 Subscribe & Save, 15%).
- It discloses "Neither is guaranteed to offer the lowest price" and that the final price shows in the cart.
- It is linked in the main nav.

**Issues:**
- **Medium:** "existing members" appears twice, while the membership page says enrollment has never opened. Confirm whether any members exist (handoff R20).
- **Medium:** the membership page's "Our best everyday pricing" contradicts the no-lowest-price disclosure, and member prices equal Subscribe & Save on 15% products (R21). This is attorney-pending.
- **Low:** the membership page's Founding renewal caps ($52.49 then $55.11) and the Jan 31, 2027 deadline are published while enrollment is closed. Leave for the attorney.

## 10. SEO plan
Full plan: `claude/seo-plan-2026-11-16.md`.
- alt text for all 43 main images
- `<Product> | EverLiv` titles
- 10 page meta descriptions
- claim-free collection intros
- naming fixes (EverGlo, Slumber/"Clean Forest", Oat Milk Honey)
- redirects for `/pages/about-us` and `/collections/bundles`
- a 90-day keyword focus on the strip format

## 11. Trust review
| Element | Status | Rating |
|---|---|---|
| Shipping policy (free U.S., 1–3 day processing, 3–7 day delivery) | Clear | OK |
| Refund policy, FAQ, privacy, terms, accessibility pages | Present and dated | OK |
| Business address and email (Sheridan, WY; support@) | Published | OK |
| FDA disclaimers | Present on supplement pages | OK |
| Reviews page "Verified Buyer / Real People, Real Results" | Provenance unconfirmed; may predate the supplier switch | **High** |
| 5.0 rating from 1 review | Misleading as a trust signal | Medium |
| Unsubstantiated label badges (GMP, Cruelty Free, Made in USA) | On packaging, not in marketing | Medium (legal) |
| "Lab documents" in the FAQ meta; "Science-backed" | Not backed by published COAs | Medium |
| Discontinued product purchasable | Fulfilment risk | **Critical** |
| Bundle "Ships in 1–2 days" vs policy | Inconsistent promise | Medium |

## 12. Asset inventory
- **Current editorial library** (`library/editorial/`, registry and `ASSET-REGISTER.md`):
  - 6 soap singles and collections
  - 4 coffee singles and collection
  - Holiday Gift Edit pair
  - **new:** strip lineups (5-tin approved-provisional; 6-tin on HOLD)
- **New lookup:** `library/BEST-VERIFIED-IMAGERY.md` lists, per product, the best verified source, the approved editorial versions, and what is not cleared for paid ads.
- **Eye Serum renders:** v9 gloss (current internal reference) vs v1–v8 matte (superseded), as in §7.
- **Unknown-rights store imagery:** the Shop by Need and Solutions people photos, and the EverLiv difference banner. Verify before any paid use.

## 13. Future marketing materials
In `claude/marketing-materials-pack-2026-11-16.md`, all marked DRAFT:
- brand intro (short and medium)
- the three-way pricing explainer and caption
- strip messaging with a do-not-say list
- transparent bundle maths ($104.97 → $79.99 = $24.98, 23.8%)
- 25-word conservative descriptions
- mobile promo lines
- launch checklist

**The proposed $84.99/$79.99 bundle structure is not used anywhere**; only the live $79.99 Any-3 bundle is used.

## 14. Coordination with Restructuring
`claude/restructuring-handoff-marketing-audit-2026-11-16.md` has 21 rows, each with the exact URL, screenshot reference, proposed fix and priority:
- Critical: R1 (Testosterone), R2 (Solutions claims)
- High: R3–R7 (bundle button and shipping, member-price display, clipped hero, alt text, reviews)
- Medium and Low: the rest

It does not touch checkout, pricing or membership mechanics.

## 15. Supplier status (via Restructuring; no Marketing contact)
**Answered Nov 15:**
- gloss BOPP labels
- no extra photos (a sample order would be needed)
- no 3D files
- photos with our labels are usable
- the Eye Serum label PDF matches ours

**Still open:**
- coffee format (carton vs bag)
- Collagen Strips source, amount, lactose-free status and origin
- "Natural Extracts"
- the front-label claims on IgniteFX and L-Glutamine
- certification documents
- paid-ad usage rights

## 16. Verified facts vs assumptions
**Verified tonight (live site or supplier documents):**
- the product list, prices and copy
- the Ways to Save content and maths
- the bundle maths
- empty alt fields
- the 404s
- the Testosterone product being live and featured
- the Eye Serum label text

**Assumptions or unverified:**
- whether any membership members exist
- review provenance
- the coffee pack format
- whether the Testosterone product can actually be fulfilled
- the source of the people photos
- whether the Restructuring fixes in its queue have since gone live (the site may change after 04:15 UTC)

## 17. Blockers
- No product samples (and none may be ordered), so physical accuracy can't be verified.
- No substantiation or certification files exist.
- The attorney review is pending for membership, claims and badges.
- Supplier answers are outstanding (§15).
- macOS Save As dialogs: avoided by writing files directly; no workaround to security controls was attempted.

## 18. Decisions needed from Jeff
1. Unpublish Testosterone & NAD+ (recommended: yes, today).
2. Approve the conservative Solutions and Shop by Need subheads, or hide those bullets until legal review.
3. Eye Serum: keep the name and call it a "gel-cream" texture, or rename at the next label run.
4. Do any Member Price Club members exist? This settles the "existing members" copy.
5. Approve the 5-tin strip grid as the new hero image.
6. Remove or hide reviews until their provenance is confirmed?

## 19. Files and where they are
- **Project docs:** this report, `claims-audit-2026-11-16.md`, `restructuring-handoff-marketing-audit-2026-11-16.md`, `seo-plan-2026-11-16.md`, `marketing-materials-pack-2026-11-16.md`.
- **Repo (`everliv-media`):**
  - `creative-tests/2026-11-16-site-audit/` (13 screenshots, site JSON, claims scans)
  - `library/editorial/strips/`
  - `library/BEST-VERIFIED-IMAGERY.md`
  - Eye Serum `renders/STATUS.md`
- **Your Mac:** `~/Downloads/EverLiv-Overnight-Audit-2026-11-16/` (report, docs and screenshots), written directly with no dialogs.

## 20. Morning visual inspection checklist (Jeff and Esther, about 15 minutes)
1. **[Critical]** Homepage desktop and phone: is the Testosterone slide or card still showing? Is the product page still buyable?
2. **[Critical]** `/pages/solutions`: are the testosterone, neuroprotective and memory lines still visible?
3. **[High]** Phone hero: does the headline overlap the label text?
4. **[High]** "Start here" and any product page: does the everyday price lead, or the member price?
5. **[High]** `/products/ultimate-bundle`: read the Add to Cart button. Any "/ month" on a one-time purchase?
6. **[High]** Hero strips slide: is the Collagen tin clipped? Compare with the 5-tin grid preview (`strips-grid-5--3over2--ivory-preview.jpg`).
7. **[Medium]** `/pages/ways-to-save`: is the "existing members" wording right, given that enrollment never opened?
8. **[Medium]** `/pages/reviews`: do you recognize these reviewers as real buyers of the current products?
9. **[Medium]** The Eye Serum product page: is the bottle tiny? Serum or gel-cream?
10. **[Low]** Coffee product images: carton plus bag. Which one does a customer actually receive?
