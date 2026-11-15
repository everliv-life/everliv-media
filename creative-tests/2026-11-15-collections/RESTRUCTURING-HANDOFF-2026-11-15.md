# EverLiv Marketing → Restructuring: imagery handoff and open questions (Nov 15, 2026)

This document stands alone. Marketing has **not** changed Shopify, replaced any image, published anything, or contacted Supliful. Jeff keeps final publication approval. Restructuring owns storefront implementation.

Every image file carries the working disclosure **"Product shown as supplied; scene digitally created."** in its metadata or build report.

---

## A. Placement strategy (owner-approved Nov 15)

| Placement | What to use | Rule |
|---|---|---|
| Product page, first image, and product-card default | The **authentic supplier render**, unchanged | Do not replace with lifestyle imagery |
| Product page, secondary gallery | The approved individual lifestyle image for that product | Only once packaging accuracy is verified (see C) |
| Homepage / collection pages | Six-soap and four-coffee collection banners (desktop 16:9 + mobile 4:5) | Category features; headline space is built in |
| Holiday Gift Edit / gift guide | Soap gift, coffee gift and mixed Holiday Gift Edit banners | Must not imply the pictured assortment is one bundle |
| Bundle listings | Only the bundle-specific "what's included" images | Only after the contents are confirmed (see B) |

**Recommended visible disclosure:** no overlay on the images themselves. Suggested placements for a visible line ("Product shown as supplied; scene digitally created."):
- the gift-guide or collection page footer
- a small caption under homepage banners
- for any paid ad, the ad text where the platform requires AI-content labelling

The product page main image is the plain supplier render, so it needs no disclosure.

## B. Bundles: please confirm (images are BLOCKED until you do)

Public store data from the Nov 14 snapshot, read-only:

| Listing | Price | Published | Contents stated? | What the listing photos suggest |
|---|---|---|---|---|
| Ultimate Bundle (EV-ULTIMATE-BUNDLE) | $79.99 | 2026-11-03 | Yes: any 3 oral strips, customer's choice | n/a. Strip imagery is blocked for claim reasons ("Natural Extracts"). |
| EverLiv Aromatherapy Bundle (`black-friday-aroma-therapy-bundle`) | $100.75 | 2025-11-21 | **No** | All 6 soaps, one of each ($100.75 = 80% of 6 × $20.99) |
| Artisan Coffee Bundle (`black-friday-sale-coffee-gift-pack`) | $110.24 | 2025-11-21 | **No** | All 4 coffees, one of each (about 80% of $136.96, not exact) |

**Please confirm for each:**
1. Exact products and quantities.
2. Whether it is current for 2026, available, and fulfillable through Supliful as a set.
3. The intended price. Marketing will not use any savings claim unless you confirm it is current and compliant, and does not stack.
4. Whether the listing copy should state the contents. Both descriptions currently say nothing about what's inside.

Marketing has prepared **"what's included" images** for the two gift bundles:
- `bundle_aromatherapy`: the 6 soaps
- `bundle_artisan_coffee`: the 4 coffees

They are plain backdrops, with no props or wrapping. They stay **BLOCKED** until you confirm items 1–3.

## C. Packaging questions for Supliful (please add to your existing outreach; Marketing has not contacted them)

1. **Coffee:** is the product the customer receives the **kraft gable-top carton**, the **valve bag**, or the bag inside the carton?
   - The supplier renders and the store's bundle photo show both.
   - All coffee imagery is **PROVISIONAL FOR PUBLIC USE** until this is answered.
   - Also needed: carton dimensions (height × width × depth). Marketing assumed about 22–24 cm tall.
2. **Soap band:** is the gold corner on the band actually **gold foil** or printed gold? Also the bar and band dimensions. Marketing assumed the bar is about 8.5 × 7.5 cm.
3. **Render fidelity:** are the supplier renders faithful to the physical soaps and coffee packs? This covers label stock and finish, colour, bar colour and texture, and carton proportions.
4. **Higher-resolution coffee renders** (3000 px or larger). The current ones are 724 × 1595 px, which limits label sharpness.

## D. Catalog and compliance items noticed during production

- **Slumber soap:** the store handle is `everliv-clean-forrest-soap`, but the label says **SLUMBER**. Please reconcile the handle, title and SKU naming (and note the "forrest" spelling).
- **Mushroom Coffee:** the label states "Lion's Mane & Chaga". Please confirm it matches the current Supliful formulation.
- **Claims to review before any paid use. They are printed on the packs; Marketing will not expand them:**
  - "Pure Cellular Vitality" (on every pack)
  - "Gentle exfoliation for sensitive skin" (Oat Milk Honey)
- Earlier open items still stand:
  - Testosterone & NAD+ is live and purchasable (ex-Quantus).
  - The 2025 Black Friday bundles are still live.
  - Is there a 42nd Supliful product?
  - Sections C–E of the Nov 14 request.

## E. Files

Location: `everliv-media` repo.

- `creative-tests/2026-11-14-gift-edit/approved/`: the 4 owner-approved images, with metadata and a manifest.
- `creative-tests/2026-11-15-collections/`:
  - `individual/`: 6 new single-product images
  - `collections/`: soap, coffee and mixed banners in desktop, mobile and social sizes
  - `bundles/`
  - `ASSET-REGISTER.md`: per-asset status, placement and alt text
- `library/cutout-kit/`: the 10 verified cut-outs and their manifest.
