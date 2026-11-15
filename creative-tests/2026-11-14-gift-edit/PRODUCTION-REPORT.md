# Holiday Gift Edit: production report (Nov 14, 2026, late evening)

Nothing has been published, scheduled, sent to Supliful, or changed on Shopify. Every image below is an internal candidate awaiting owner approval.

**Status labels**
- **READY:** passed an independent QA review. Can be used once Jeff approves it.
- **PROVISIONAL:** usable for internal work. Not yet independently reviewed in a finished image.
- **BLOCKED:** waiting on a supplier specification, claim substantiation, or an owner decision.

## 1. Hero pair

| Asset | File | Status | Independent QA |
|---|---|---|---|
| Oat Milk Honey soap, top-down holiday flat lay | `composites/soap_omh_v5-2160x2700.png` (+1080x1350) | **READY** | Authenticity PASS, ~80% of studio quality (v4 was ~70%). Review rounds 2 and 3. |
| Cocoa coffee, eye-level holiday kitchen | `composites/coffee_cocoa_v5-2160x2700.png` (+1080x1350) | **READY** | Authenticity PASS, ~81% (v1 was ~82% with authenticity only, v2 ~68% under stricter review, v4 ~76%). Review rounds 2 to 5. |

**How authenticity was checked.** The packaging is the supplier's own render. It has one uniform exposure scalar and luminance grain, and nothing else. There is no tint, redraw, relighting or mirroring. Independent QA verified this by template match against the source (cocoa NCC 0.95–0.998, mirrored 0.24–0.40) and by residual maps.

**Known minor issues, accepted.** These are native to the supplier render and must not be retouched:
- the coffee label is slightly soft
- a faint tick line inside the carton's right edge
- a cool sliver on the carton's back panel
- a pale lip along the bottom edge of the soap bar

**Advisory:** the printed tagline "PURE CELLULAR VITALITY" should go through the claims check before any *paid* use.

## 2. Scene templates (4)

| ID | Template | Validated with | Status |
|---|---|---|---|
| T1 | Gift flat lay (linen, orange, anise, cinnamon, pine), top-down soap | Oat Milk Honey hero | **READY** |
| T2 | Travertine spa (lavender, oats, eucalyptus, waffle towel), top-down soap | Charcoal test, `tmpl_spa_charcoal_v2` (QA: READY, ~78%) | **READY**. Minor: oats and dish run slightly small. |
| T3 | Limestone plinth, minimal, upright coffee | Hazelnut test, `tmpl_plinth_hazelnut_v3` (QA: READY, ~79%) | **READY** |
| T4 | Holiday kitchen, upright coffee | Cocoa hero | **READY** |

Each template has its scene, a clean plate, a stand-in mask, and recorded compositor settings (`README.md`). The first gift flat lay (`gift1`) is retired because its stand-in was at the wrong scale.

## 3. Cut-out kit (10)

Every cut-out has interior pixels byte-identical to the supplier source, which is verified in each `.json` file.

| Product | Cut-out | Status | Notes |
|---|---|---|---|
| Oat Milk Honey soap | v2 | **READY** | Fixed the v1 pale-strip defect, then reviewed in the hero |
| Charcoal soap | v2 | **READY** | Reviewed in T2 |
| Coconut Beach, Rich Sandalwood, Aloe & Cool Cucumber, Slumber soaps | v2 | **PROVISIONAL** | Automated edge scan done. Small steps at the label ends are real bar geometry. Needs a 100% review in a finished image. |
| Cocoa coffee | v2 | **READY** | Composite uses `--edge-choke=1` |
| Hazelnut coffee | v2 | **READY** | Reviewed in T3 |
| Mushroom, Caramel coffee | v2 | **PROVISIONAL** | Same method; not yet in a reviewed image |

## 4. Product-by-product visual status (41 Supliful products)

| Product(s) | Status | Reason |
|---|---|---|
| Oat Milk Honey, Charcoal soaps | **READY** | Finished and reviewed images exist |
| Cocoa, Hazelnut coffee | **READY** | Finished and reviewed images exist |
| Coconut Beach, Sandalwood, Aloe & Cucumber, Slumber soaps; Mushroom, Caramel coffee | **PROVISIONAL** | Cut-out and templates ready. About 15 minutes each to composite, plus a QA review. |
| 17 claim-gated products (collagen, botanicals, NAD+/β-NMN, proteins, Creatine + Electrolytes) | **BLOCKED** for prominent imagery | Front-label claim substantiation is not on file |
| Energy, Hydrate, Iron, D3+K2 and Collagen strips; Magnesium; Creatine; Peptide Eye Serum; Berberine; IgniteFX; L-Glutamine; Resveratrol; Nature's Ultra Cleanse | **BLOCKED** | Specific label or claim issues (see the readiness shortlist) |
| Sleep Strips | Excluded | Owner exclusion |

## 5. Open supplier-specification and claim-substantiation requests
Everything here goes through Restructuring and is unchanged from `restructuring-request-2026-11-14-evening.md`:
- **C:** Packaging assets for all SKUs: dielines, dimensions, finishes, closures, 3000 px+ multi-angle renders, 3D models and usage rights. **New for the gift edit:**
  - the soap band corner: is it gold foil?
  - the coffee format: is it a carton or a valve bag? The renders show both. A higher-resolution coffee render (the current one is 724x1595) would fix the label softness.
- **D:** Peptide Eye Serum label wording, badges and packaging questions.
- **E:** front-label claim substantiation.
  - Priority, higher risk: Berberine, IgniteFX, L-Glutamine, Resveratrol, Nature's Ultra Cleanse, the strip tins, Creatine and Magnesium.
  - Routine: the 17 claim-gated products.
  - **New, low priority:** the soap cosmetic claims "Gentle exfoliation for sensitive skin" and "deep cleanse", and the brand tagline "Pure Cellular Vitality". This needs checking before paid use only.

## 6. OWNER ACTION REQUIRED: consolidated checklist

| # | Item | What's needed from Jeff | What it blocks |
|---|---|---|---|
| 1 | Hero pair (soap and cocoa) | Approve or reject for use | Any use of the hero pair |
| 2 | Two template images (Charcoal spa, Hazelnut plinth) | Approve or reject as additional assets | Their use |
| 3 | AI-scene disclosure | Decide the wording, e.g. "Product shown as supplied; scene digitally created" | Publishing any composite |
| 4 | Testosterone & NAD+ (live, purchasable, ex-Quantus) | Decide whether to unpublish (Restructuring acts) | Nothing in marketing; it's excluded |
| 5 | Two 2025 Black Friday bundles (live) | Decide whether they're intended for 2026 (Restructuring acts) | Any gift-bundle promotion |
| 6 | 42nd Supliful product | Confirm whether one exists | Catalog records only |
| 7 | Restructuring sending C–E to Supliful | Confirm it was sent, with the two new gift-edit questions | Everything BLOCKED, plus angled or 3D work |
| 8 | Collagen library cut-out | Approve swapping the degraded library cut-out for a fresh one from the 2048 px render | Collagen imagery once its claims clear |
| 9 | Next batch | Approve compositing the 6 remaining soap and coffee products into T1–T4 | 6 more READY images |

## 7. Restructuring handoff (no Shopify action taken by Marketing)
The handoff package is everything in this folder. If Jeff approves, Restructuring decides whether and where to use the images (for example, a gift-guide collection banner or a homepage holiday block).
- **Recommendation:** do not replace product main images. Shopify main images should stay the plain supplier renders.
- **Formats:**
  - 2160x2700 masters
  - 1080x1350 feed versions
  - transparent cut-outs for any further layout
- **Suggested alt text:**
  - "EverLiv Oat Milk Honey handcrafted soap on linen with dried orange, star anise and cinnamon"
  - "EverLiv Cocoa medium-roast coffee carton on a wooden kitchen counter with a mug of coffee"
