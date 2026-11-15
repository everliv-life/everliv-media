# Visual QA: six individual product images (ind_*_v1, 2160x2700), 2026-11-15

Reviewer: independent and strict. Benchmarks: the four approved templates (soap_omh_v5 at about 80%, spa_charcoal_v2 at about 78%, plinth_hazelnut_v3 at about 79%, coffee_cocoa_v5 at about 81%).

**Method:**
- Matched each cut-out (resized by the JSON scale) to the composite, and also checked it mirrored.
- Measured the exposure ratio per channel and the residual (low-pass sigma 15).
- Checked each cut-out against its supplier render.
- Measured edge-ring profiles and looked for white leftovers in the cut-out rings.
- Diffed each image against its template scene, both straight and flipped.
- Measured the shadow on each side as near/far luminance.
- Checked 100% and 5–8x crops, the 1080 exports and 216x270 thumbnails.
- Crops and maps are in this folder.

## Authenticity: all 6 PASS
| Image | Cut-out vs supplier render | NCC placed (mirrored) | Exposure B/G/R (JSON) | Grain SD | Low-pass shading |
|---|---|---|---|---|---|
| sandalwood | exact (NCC 1.0) | 0.997 (0.57) | 1.007/1.006/1.006 (1.009) | 2.6 | none above 3 levels |
| coconut | exact | 0.997 (0.64) | 1.004/1.004/1.007 (1.009) | 2.6 | none |
| slumber | exact | 0.996 (0.48) | 0.974/0.974/0.974 (0.976) | 2.4 | none |
| aloe | exact | 0.995 at 842x749 (0.71) | 0.978/0.978/0.978 (0.98) | 2.4 | none |
| mushroom | exact (MAD 0.9) | 0.997 (0.47) | 0.966/0.966/0.966 (0.969) | 2.7 | none |
| caramel | exact (MAD 0.9) | 0.997 (0.43) | 0.950/0.951/0.951 (0.954) | 2.4 | none |

- **No redraw, relight, warp or mirroring.** The residual is grain plus resampling edges only. All labels read correctly.
- **Chroma residual SD is 0.4 or less.** Coconut has a 0.003 R-channel offset, which is negligible.
- **Clipping:** sandalwood and coconut have about 1,300 product pixels clipped to 255, in the bbox x 623–1552, y 939–1634. These are label and foil highlights that are already 253 or more in the source, pushed over by the exposure scalar above 1.0 plus grain. It is not visible. If you want it gone, cap the grain at the source value.

## Scene and mirroring facts
- **Coconut and aloe:** these are the omh and spa scenes flipped horizontally, with a 1 px offset. Product shadows flip with them. Unmirrored bars cast right and down (near/far R 0.91, B 0.91). Mirrored bars cast left and down (coconut L 0.92, B 0.91; aloe L 0.88, B 0.89). The approved references show the same pattern. Prop shadows flip with the scene, so the direction is consistent.
- **Mushroom and caramel are NOT mirrored.** The brief says they are, but outside the product they are pixel-identical to hazelnut_v3 and cocoa_v5 (mean diff 0.00; flipped diff 34–70). They keep the approved light direction, so this is a labelling error in the brief, not a defect.
- **Sandalwood and slumber:** these match their templates outside the product footprint.
- **Mushroom has one change from the template:** the plinth front lip at x 784–1662, y 2225–2240 was darkened by 5–15 levels. This softens the hard lip highlight that v3 had and continues the carton's cast shadow over the lip. There is no seam: the row step is under 2 levels (`mushroom_lip_vs_hazelnut_2x.png`, top = mushroom). I accept it as a small improvement.
- **1080 exports:** they match a clean Lanczos downscale (MAD 0.0).

## Per image
| Image | Auth | Verdict | Quality | Notes |
|---|---|---|---|---|
| ind_sandalwood_v1 | PASS | READY (after owner approval) | ~80% | Edges are clean (`sandalwood_edges_2x`, `edge_specks_8x`). D1 (minor, native): the label end on the right has a 2–4 px white paper strip at x 1513–1518, y 1105–1634, with a small step at y 1137. Below the label there is a beige strip of about 3 px at x 1511–1514, y 1602–1640. Both are in the supplier render (the cut-out ring matches the source), so do not retouch. If it bothers you, trim the alpha by 1–2 px along x≥1513. |
| ind_coconut_v1 | PASS | READY (after owner approval) | ~79% | Edges are clean. The cut-out ring has no white leftovers. The pale strip in the source beyond the label end was already trimmed. The shadow is correct for the mirrored light. No defects. |
| ind_slumber_v1 | PASS | READY (after owner approval) | ~78% | Edges are clean (`slumber_labelends_5x`). D2 (minor, native): a white label-paper notch overhangs the soap edge by about 2 px at the bottom-left of the label (643, 1593) and along the right label end at x 1500–1503. Leave it. |
| ind_aloe_v1 | PASS | READY (after owner approval) | ~78% | Edges are clean (`aloe_edges_2x`). The pale speck at (1233, 981) is native soap texture. The 4 px pale strip at the right label end, x 1490–1494, y about 1105–1590, is native label paper. The shadow flips correctly. JSON note: `product_px` 842 is right (with 843 the residual SD rises to 8, so do not round up). |
| ind_mushroom_v1 | PASS | READY (after owner approval) | ~80% | Same placement as hazelnut_v3: the carton's front-bottom corner is about 5 px from the plinth lip at about (880, 2220), so the optional fix from round 4 still applies. Carried over: the cool back-panel sliver and native label softness. |
| ind_caramel_v1 | PASS | READY (after owner approval) | ~80% | Same placement and shadows as cocoa_v5. The diff is only on the label text. The JSON gives label sharpness as 77% of source, which is native. Carried over: small beans relative to the carton. |

No defects block any of the six images. All severities are minor or native. The new images sit within ±1 point of their approved templates.

## Feed and thumbnail
- **1080:** all names and Net Wt are readable. Soap taglines and the coffee tasting-note tables are legible (`feed1080_soaps.png`, `feed1080_coffee.png`).
- **216x270:** the coffee flavour names read clearly. Soap names are only just readable at thumbnail size, the same as the approved soap templates (`thumbs_216x270.png`).

## Housekeeping (not visual)
- **JSON exposure:** every `exposure_scalar` is 0.002–0.003 above my measurement. Correct to 1.006, 1.005, 0.974, 0.978, 0.966, 0.951.
- **JSON source path:** none of the six JSONs has a `supplier_source_render` field. Add it.
- **Mirroring flag:** fix the brief and the build log. Mushroom and caramel are not mirrored.
- **Slumber naming:** the cut-out and render files are named `clean-forrest`, but the label reads SLUMBER ("Relaxing lavender scent / Cedar forest aromatic blend"). Reconcile the SKU naming in the catalog before you publish.
- **Advisory (claims and compliance):** "PURE CELLULAR VITALITY" is on every pack. The mushroom carton states "Lion's Mane & Chaga". Check that against the current Supliful formulation before any use, especially paid ads.
