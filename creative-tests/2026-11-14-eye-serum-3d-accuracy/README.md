# Peptide Eye Serum: provisional 3D packaging-accuracy test (Nov 14, 2026)

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
