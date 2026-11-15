# EverLiv collection composites: independent visual QA, round 2 (review-coll2)
Reviewer: independent QA (did not build these). Date: 2026-11-15.
Scope: 12 masters in /home/claude/coll/out/. The wide masters are 2752x1536, the vertical masters 1856x2304, and the bundle masters 2160x2700. All coordinates are master pixels (x, y).
Crops are in /home/claude/review-coll2/ (c00_*, m01–m19, s01–s03 shadow maps where magenta = product). Scripts are in /home/claude/review-coll2/tools/ (auth2.py, smap.py, kraft.py, crop.py, shad.py, ushad.py).

## Global checks (all 12)
- **Pixel fidelity, measured (auth2.py, 4-px-eroded interior):** I re-rendered every product from its cut-out at the reported scale × the image's exposure scalar. The residual is −0.5 on all channels equally (uint8 truncation), SD 1.30–1.95 (grain only), chroma SD ≤0.25 and per-channel gain identical to ±0.001. This means **no tint, relight or warp**. Mirror test: the flipped difference is 10–29 against ≈1.9 for the true orientation, so **no mirroring**. Each image uses one exposure scalar. No product is clipped by the frame. Products never overlap, so no product is occluded.
- **Identity:** each product appears at most once in every image, and no text is mirrored. The soap and coffee collections and both bundles contain the full set: 6 soaps or 4 coffees. The mixed images are deliberately partial: the wide has Sandalwood, Cocoa, Oat Milk Honey, Caramel and Charcoal (5); the vertical has Cocoa, Oat Milk Honey, Caramel and Sandalwood (4). Copy must not call them "the full collection".
- **Exports, fixed:** the vertical exports are now centre-cropped to (6–1849) x 2304 and then resized, with non-uniformity 0.011%. The wide exports differ by ≤0.035%, which is integer rounding and <1 px across the frame. The bundles are an exact 2.000x reduction. Every export matches crop+LANCZOS bit-exactly (max diff 0).
- **Cut-outs:** the coffee images still use `-v2`; `-v3` is unused. The effect is negligible (≈1 px speck) but still open (info).
- **Naming:** the `clean-forrest` cut-out's label reads **SLUMBER**. Bundle and listing copy must say Slumber.

---

## 1. soapcoll_stone_wide: Authenticity PASS · **READY** · 83%
Round 1: #1 pit **not fixed** (plate unchanged; min lum 71 against a 228 median, m18). #2 soft shadow **improved**: contact 0.32 and sigma 30 bring the edge ratio to 0.78–0.82 and 0.93 at 50 px (m04). Cast strength stayed at 0.20; I had suggested 0.24. #3 rigid grid **unchanged** (optional).
Fresh pass: the edges are clean and the props are to scale. The left 33% is calm (SD 13, the best headline zone in the set). Names are legible at 1920 and at 600 px.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Travertine pit in the headline zone | (65–120, 745–775) | Low | Clone it out of the plate |
| 2 | Bars still read slightly "laid on" next to the crisper oat contact | all bars | Low | strength 0.20→0.24 |

## 2. soapcoll_stone_vert: PASS · **READY** · 81%
Round 1: #1 eucalyptus in the top-right of the headline band: **unchanged** (layout guidance still applies). #2 bottom-heavy: unchanged, but now acceptable (≈11% bottom margin). #3 export stretch: **fixed**. #4 shadow: **improved**.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Eucalyptus in the top-right of the headline band | (1300–1856, 0–560) | Low | Headline at x<1250 |

## 3. soapcoll_gift_wide: PASS · **READY** · 78%
Round 1: #1 orange scale **fixed**. At w 310 the orange ≈180 px ≈58% of the bar width, about 4.9 cm (m05). #2 fold under OMH **improved** by the re-layout, though the folds still run under the rigid bars. #3 headline texture **not fixed** (plate unchanged; SD 29, gradient 5.4). #4 Charcoal/spice crowding **fixed**: the gap is now ≥70 px.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Linen folds in the headline zone | (0–963, all) | Low-Med | Heavy dark type, or a 10–15% ivory scrim |
| 2 | Folds pass under the bars with no deformation | e.g. OMH (957–1267, 474–750) | Low | Accept |

## 4. soapcoll_gift_vert: PASS · **PROVISIONAL** · 71%
Round 1: #1 busy top 30% **not fixed**. The plate is unchanged: the ribbon, pine and orange are still in the band (gradient 10.9, the highest in the set; m06). #2 orange scale **improved**: the bars are now 380 px and the orange ≈184 px ≈4.1 cm, small but plausible. #3 bottom-heavy: improved. #4 export: **fixed**.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Headline band not calm | ribbon (560–1856, 0–330), pine (1250–1720, 150–600), orange (1150–1330, 280–460) | **Med** | Regenerate the plate with the props kept below y≈700 on the right, or confine the headline to x<700, y<690 (SD 30) |

## 5. coffeecoll_counter_wide: PASS · **READY** · 78% (up from PROVISIONAL)
Round 1: #1 shadow mismatch **fixed**. The carton ground shadows now reach a 0.55 ratio (the plate cup shadow is ≈0.47–0.50). They are long hard wedges rising to the counter's back edge, and they read as the same sun (m07, s02). #2 lineup look: unchanged; the pitch is 330. #3 v2: unchanged.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Each wedge runs behind the next carton. Physically it would also darken that carton's left panel, which is not allowed, so the shadow just vanishes. This is only visible on close inspection | gaps (1090–1150, 1050–1285) etc. | Low | Accept, or pitch 330→360 |
| 2 | The Caramel wedge is drawn flat across the saucer's left rim, so it ignores the saucer's height | (2078–2150, 1120–1210) (m08) | Low | Move the row −40 px x, or clip the wedge at x 2075 |

## 6. coffeecoll_counter_vert: PASS · **PROVISIONAL** · 73% (down from READY)
Round 1: #1 carton size **fixed** (w 300, pitch 340; the names are now readable at 1080). #2 export: **fixed**. The enlargement introduced new problems:
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | **Hazelnut is 30 px from the left frame edge**, ≈14 px after export. Instagram's 3:4 profile-grid crop removes about 34 px a side at 1080, so it will clip the carton | Hazelnut (30–330, 1244–1905) (m19) | **Med** | w 275, pitch 305, centres 220/525/830/1135 (spans x 82–1272 and clears the cup at ≈1340) |
| 2 | Shadow mismatch: the wide's fix was not carried over. The carton shadows are soft and short (gstrength 0.27, glen 0.2, ratio ≈0.73), while the plate's saucer and dish shadows are hard and dark (m12, s03) | all cartons | Low-Med | Use the wide's values: gstrength 0.45, glen 0.45, gsigma 5 |

## 7. coffeecoll_gift_wide: PASS · **READY** · 76% (up from PROVISIONAL)
Round 1: #1 size **improved** (w 240; the flavour cap is ≈12 px at 1920, legible on desktop). #2 exposure **fixed** (0.80; kraft median ≈117 now sits with the napkin and dripper; m09). #3 gable rim **fixed** (choke 2; only a faint dark line at 4x, m10). #4 sconce at the right edge **not fixed** (m11).
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Sconce cut by the frame edge | (2700–2752, 330–500) | Low | Clone it out, or crop |
| 2 | Headline zone includes the bright window (254), so it is mixed bright and dark | (0–255, 0–1100) | Low | Set type over the dark wall at x 270–960 |
| 3 | Names still small on mobile crops | row | Low | Accept |

## 8. coffeecoll_gift_vert: PASS · **READY** · 76% (up from PROVISIONAL)
Round 1: #1 exposure **fixed**, #2 rim **fixed**, #3 export **fixed**. The top 30% is a clean dark wall.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Cartons are 220 px (11.9% of the width), so the names are illegible in the grid thumbnail (c00_thumbs_vert) | row (200–1200, 1345–1830) | Low-Med | w 250, pitch 285 (fits x ≈160–1265) |

## 9. mixed_holiday_wide: PASS · **READY (minor)** · 72% (up from REJECT 55)
Round 1: #1 flat-card soaps **largely fixed**. At a 3–5° camera a 2.5 cm bar's top face projects to ≈1–2 px, so a face-only view is now geometrically correct, and the bars read as soaps standing on edge (m01, m02). #2 headline zone **fixed**: wall at x<963, y<1100 has SD 15.6. #3 label/scene WB **fixed**: scene B/R 0.94 against label 0.967. #4 soap shadows **improved**: contact line plus a right-falling ground shadow (s01). Scale is consistent: the mug is ≈10 cm and the cinnamon ≈8.6 cm at 24 px/cm, with all items on one baseline (1268).
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Mixed viewpoints. The carton cut-outs were shot from about 10° above and rotated about 25°, so the base is a V with a 25 px corner drop, and the left panel shows. The soaps are dead-frontal and the plate is 3–5°. The difference is subtle at banner size and visible at 100% | Cocoa base (1064–1314, 1240–1268), Caramel base (1588–1838, 1240–1268) | Low-Med | Only fixable with supplier carton shots at a lower angle. Otherwise accept |
| 2 | Soap faces carry flat top-down light while the cartons show left-key modelling | soaps | Low | Accept (rules forbid relighting) |
| 3 | Tight 35 px gaps between soap and carton | e.g. (1029–1064, 1086–1268) | Low | Pitch 262→280 if the room allows (mug at ≈2250) |
| 4 | Soap names unreadable below ≈1280 px width | soaps | Low | Expected for a banner |

## 10. mixed_holiday_vert: PASS · **PROVISIONAL** · 68% (up from REJECT 55)
Round 1: #1 flat cards **largely fixed**, as in #9. #2 oversized products **fixed**: on the new plate the mug is ≈12 cm and the cinnamon ≈9.2 cm at 26 px/cm, which is consistent. #3 overlaps **fixed**: there are none. #4 WB **fixed**. The top 30% is calm at x<1300 (SD 3.9), and the garland sits in the top-right (x>1300; SD 58).
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Same mixed carton/soap viewpoint as #9, and more visible because the cartons are 276 px | Cocoa (95–371), Caramel (675–951), bases at 1968 (m16, m17) | Low-Med | As #9.1 |
| 2 | Crowded row with 40 px gaps. At grid size the soaps are label-only blobs and the names are illegible (c00) | row (95–1215, 1360–1968) | Low-Med | Drop to 3 items, or set the soaps at w 250 with 70 px gaps |
| 3 | Cocoa's left edge is 89 px from the frame edge after export; the 3:4 grid crop leaves about 18 px | Cocoa x0 = 95 | Low | Shift the row +40 px x |
| 4 | Headline must avoid the garland | (1300–1856, 0–690) | Low | Headline at x<1300 |

## 11. bundle_aromatherapy (NEW): PASS · **READY** · 84%
All 6 soaps appear once, on a plain backdrop with no props or wrapping, in a 2x3 grid at w 640. Every name is legible at 1080 and mostly legible at 250 px. Edges are clean at 4x (m13). Shadows are soft and consistent (edge 0.87, 0.96 at 50 px). The export is an exact 2x reduction.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | The "Slumber" cut-out file is named clean-forrest | — | Info | Listing copy must say Slumber |

## 12. bundle_artisan_coffee (NEW): PASS · **READY** · 81%
All 4 cartons appear once, on a plain seamless backdrop with no props. Names, roast and net weight are legible at 1080. Grounding is good (m15).
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Grey-blue 1–2 px rim on the left gable edge against the near-white backdrop (choke 1) | e.g. Hazelnut (155–185, 1110–1300) (m14); all four | Low | choke 2 |
| 2 | Row sits low: top margin ≈1120 against bottom ≈690, with ~41% empty backdrop above | row (135–2225, 1120–2010) | Low | Baseline 2010→1800 |

---

## Ranking (best → worst)
1. bundle_aromatherapy (84, READY)
2. soapcoll_stone_wide (83, READY)
3. bundle_artisan_coffee (81, READY)
4. soapcoll_stone_vert (81, READY)
5. soapcoll_gift_wide (78, READY)
6. coffeecoll_counter_wide (78, READY)
7. coffeecoll_gift_wide (76, READY)
8. coffeecoll_gift_vert (76, READY)
9. coffeecoll_counter_vert (73, PROVISIONAL: edge clipping risk, shadow fix not carried over)
10. mixed_holiday_wide (72, READY minor)
11. soapcoll_gift_vert (71, PROVISIONAL: busy headline band)
12. mixed_holiday_vert (68, PROVISIONAL)

**Summary:** 9 READY (one of them minor), 3 PROVISIONAL, 0 REJECT. Authenticity passes 12/12 (measured). The export warp is fixed everywhere.

The low-camera plates solve the flat-card soap problem. The remaining mixed-scene tell is that the cartons were shot from about 10° above while the soaps are frontal; it is not visible at banner size.

Quick wins:
- counter_vert: re-space the row and use the wide's shadow values.
- coffee bundle: choke 2 and raise the row.
- gift_vert soap: needs a new plate; parameters cannot fix it.
