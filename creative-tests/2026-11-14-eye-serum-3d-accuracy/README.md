# Peptide Eye Serum: provisional 3D packaging-accuracy test (Nov 14, 2026)

> **FROZEN — v8 PROVISIONAL (owner, Nov 14, 7:24 PM ET).** No further modeling passes until Supliful supplies dimensions, print-ready artwork, closure details and material finishes. Not approved for lifestyle scenes, angled product photography or publication. Git tag: `eye-serum-3d-v8-provisional`.

**Internal test only. Not for publication.** Owner-approved (Nov 14, 17:48) as a neutral-model test only. There is no lifestyle scene, no other product and no batch.

## Inputs
- **Label texture:** `model/label_extracted.png`. This is an exact pixel crop (174,344)–(1874,1704) of the supplier presentation image `library/peptide-eye-serum/peptide-eye-serum--flat-label-ingredients.png`. It is unaltered and mapped at uniform scale. It is a 1700×1360 presentation image, **not print-ready artwork**.
- **Reference:** `library/peptide-eye-serum/peptide-eye-serum--front.jpg`, the supplier's front render at 2048 px.

## Method
Built in Blender 5.3 (free), with Cycles CPU rendering, Standard view transform, and a 2048 px frame matching the supplier render. Build script: `tools/build_eye_serum.py`, final version v4.

Geometry was solved from the supplier render:
- **Silhouette:** 432 px wide.
- **Camera:** about 8° viewpoint, from the base outline curvature. Distance is 5.5 model units, focal length 5496 px.
- **Label edges:** y 777 to 1741.
- **Label scale:** 0.682 units per 1000 label px, from logo-top→Net Wt and the gold-rule spacing.
- **Wrap:** about 319°.
- **Registration:** label column x=884 faces the camera, taken from both gold rules.

**All dimensions and materials are UNVERIFIED**:
- Cap and body are white plastic, satin finish, assumed.
- The label is matte paper, assumed.
- The collar is opaque, assumed.

## Iterations
| Version | Change | Result |
|---|---|---|
| v1 | Scale taken from the leaf bounding box (0.625) | Wrong: label about 9% too small |
| v2 | Vertical-distance scale (0.709), orthographic assumption | Label about 20 px low and 2% large |
| v3 | Perspective-solved camera | Registration within about 2 px |
| v4 | Matte-paper finish (lower sheen) | Inks no longer veiled. Final version |

## Independent review of v4: Gate 1 CONDITIONAL
**Matches:**
- Silhouette is within 1–3 px.
- Text, logo, rules and QR are registered within about 1–2 px horizontally and up to about 6 px vertically.
- Wrap geometry is correct.
- Logo green matches the supplier render relative to paper.
- All wording and layout are correct.
- The artwork is confirmed unaltered, and scale is uniform: 0.697 vertical vs 0.703 horizontal.

**Open items fixable in the model:**
1. Type softness at 100–200%: about half the supplier's sharpness. Caused by texture filtering, samples and grain.
2. Gold brighter and more yellow than the supplier render. The model is closer to the flat artwork, so the true ink needs a print proof.
3. Small edge-glyph and QR offsets of about 4–8 px.
4. Light direction is reversed relative to the supplier render.
5. Cap: fillet slightly large, a groove line that shouldn't be there, and a satin finish where the supplier shows gloss.
6. Collar renders opaque where the supplier's looks frosted.
7. Base rim too dark.

**Unverifiable without the supplier:**
- Real height, diameter and cap height.
- Resin, finish and opacity.
- Label stock and gold ink.
- Wrap length and seam position.
- Pump and base geometry.
- No 1% dimensional-accuracy claim is made.


## Correction under the product-authenticity standard (v5–v8, Nov 14 evening)
**Trigger:** the owner found that the v4 cap and upper packaging differed visibly from Supliful's mockups.

**References audited:**
- the Supliful listing `supliful.com/catalog/peptide-eye-gel-cream`: 1 fl oz / 30 ml, 50 g gross, plus blank cap-on, cap-off and lying-bottle renders
- the store's cap-off render
- a 200% audit of the supplier front render

**Root cause:** the v1–v4 geometry was inferred from a single front render using a generic airless-bottle assumption. That assumption produced a protruding grey collar ring, and the camera position was guessed rather than solved.

| Version | Change |
|---|---|
| v5 | Collar ring removed; seam lines added at the cap edge and shoulder step; glossy cap and satin body; light mirrored to match the supplier |
| v6 | Camera re-solved from the top and base ellipses; cap corner radius measured from the silhouette |
| v7 | Point-sampled label with a 0.5 px filter. Label sharpness rose from 86% to 97% (p99 gradient) |
| v8 | Cap and body rebuilt as a single lathed profile: a sharp cap lower edge, fine grooves, rounded top only; softer cap gloss |

**v8 metrics:**
- Silhouette IoU: 0.983.
- Label sharpness against the supplier render: 88–99% by region.
- Colour relative to paper: matches the artwork for green, dark type and gold.

### Independent review of v8: CONDITIONAL
**Confirmed:**
- Construction matches: the overcap is the same diameter as the body, with a cap-edge seam and a shoulder seam, and there is no collar.
- The label is unaltered and scaled uniformly (0.712 vs 0.708).
- Centre registration is within 1–3 px.
- Sharpness is 0.93–1.01 by the reviewer's own metric.
- Colour matches the artwork.

**Remaining, all fixable in the model:**
1. Cap about 13 px short: its edge sits at y692 instead of 705.
2. Missing step shadow line at the label top.
3. Label edges curve where the supplier's are flat. As a result, edge text sits 7–16 px high, including the QR.
4. Cap has a clipped highlight and its edges are too dark.
5. Body plastic should read about 15–18 levels brighter than the label, and the base darkens.
6. Top corner slightly tight at y255–258.
7. Render noise.

**Note on item 3:** the supplier render's cues conflict. A flat label top implies a camera at label height, while the base sag implies a higher camera. Supplier mockups may apply the label in 2D, so only physical specifications can settle the true geometry.

**Not verifiable without supplier specifications:**
- real dimensions and corner radii
- whether the shoulder band is frosted or translucent
- cap gloss
- label stock and white point
- label wrap length and seam position
- base profile

**Compliance flag** (back panel, not visible in front views): the "GMP CERTIFIED" badge and the "Manufactured in the USA" line are unverified.

## v9 (Nov 15, late): label-finish correction from supplier facts (internal only)
- **Why:** on Nov 15 Supliful confirmed that every label is high-gloss polypropylene (BOPP), and that matte, metallic, foil and pearlescent finishes are not offered. v1–v8 modelled the label as matte paper (roughness 0.85), so their label finish is **inaccurate**. v1–v8 are preserved unchanged.
- **Change 1, label material:** glossy film (roughness 0.18, clear coat 0.8 with coat roughness 0.04). The finish is verified; the exact values are rendering estimates.
- **Change 2, label texture:** now the supplier's own file, `Peptide Eye Gel-Cream-label.pdf`. Its embedded 2250×1800 raster was extracted losslessly. It has the same aspect ratio as the earlier crop and is content-identical, so the UV mapping is unchanged.
- **Unchanged:** geometry, camera and the cap and body materials are the frozen v8 values. No new geometric assumptions were made.
- **Light scale:** LS=0.27, calibrated so the unchanged cap matches v8 (cap mean 225.4 in both renders). The label mean is 203.1 in v8 and 203.8 in v9.
- **Result:** the label now shows specular film highlights. In this all-white studio the gloss coat also slightly veils the dark inks; that effect depends on the environment.
- **Status:** PROVISIONAL, internal. It has not been independently reviewed. Dimensions are still unverified.
