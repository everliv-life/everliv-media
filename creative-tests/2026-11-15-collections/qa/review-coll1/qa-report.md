# EverLiv collection composites: independent visual QA (review-coll1)
Reviewer: independent QA (did not build these). Date: 2026-11-15.
Scope: 10 masters in /home/claude/coll/out/ (5 wide 2752x1536, 5 vert 1856x2304). Coordinates are in master pixels (x, y).
Crops: /home/claude/review-coll1/c00–c34*.png. Measurement scripts: /home/claude/review-coll1/tools/.

## Global checks (all 10)
- **Pixel fidelity, measured:** I re-rendered every product from its cut-out at the reported scale × the image's exposure scalar and compared it with the master. Residual mean is −0.5 on all channels equally (uint8 truncation), SD ≈1.9–2.7 (grain only). There is **no tint, relight or mirroring**. Mirror test: the flipped-product difference is 11–28 vs ≈1.6 for the true orientation. Each image uses one exposure scalar for every product.
- **Product identity:** the 6 soaps (Aloe & Cool Cucumber, Slumber [file `clean-forrest`, label reads SLUMBER], Charcoal, Oat Milk Honey, Rich Sandalwood, Coconut Beach) and the 4 coffees (Hazelnut, Cocoa, Mushroom, Caramel) are each present exactly once where expected. No product is duplicated or missing, and all text reads correctly.
- **Edges:** soaps are clean at 3x on light surfaces (c03, c04). Cartons have a 1-px light blue-grey rim on the left gable edge, which comes from the cut-out. It is invisible on light walls and faintly visible on the dark green wall (c24).
- **Cut-out version:** the coffee layouts use the `-v2` cut-outs, but `-v3` exists (6-px matte speck removed at 85–87,14–15). The effect is negligible at these scales (≈1 px), but switch to v3.
- **Vertical export warp:** 1856x2304 is 0.8056, but the export is 1080x1350 (0.800). The plain resize scales x by 0.5819 and y by 0.5859, a **0.7% non-uniform stretch of product pixels**. It is not visible, but it breaks the "uniformly resized" rule. Fix: centre-crop the master to 1843x2304 before resizing.
- **Light direction:** all upright plates have their key light on the left, and the product ground shadows are skewed right, so the direction is consistent everywhere. Carton cut-outs are brighter on the left of the front face, which is compatible with that light. Top-down scenes: the oat, lavender and spice shadows fall lower-right, matching the soap shadow offset (+dx, +dy).

---

## 1. soapcoll_stone_wide: Authenticity PASS · **READY** · 82%
Six bars in a 3x2 grid, x 922–2197, y 391–1131. The left 33.5% is calm travertine (luminance SD 13, the calmest headline zone in the set). Prop scale is consistent: oat flake ≈1.0 cm and lavender is plausible at 43 px/cm. Shadow direction matches the props.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Travertine pit in the headline zone | (65–120, 745–775) | Low | Clone it out of the plate (scene only) |
| 2 | Soap cast shadow is soft and light (edge 0.80–0.84, 0.92 at 50 px) next to crisper oat/lavender contact shadows; bars read slightly "laid on" | all bars | Low | contact 0.24→0.32, sigma 40→30, strength 0.20→0.24 |
| 3 | Rigid equal-gap grid (pitch 455 px), catalogue feel | grid | Low (style) | Optional: offset the bottom row by +60 px x |

## 2. soapcoll_stone_vert: PASS · **READY** · 80%
Products start at y=750 (32.6%), so the top 30% is clear. Names are legible at 1080.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Eucalyptus sprig sits in the top-right of the headline band | (1300–1856, 0–560) | Low | Keep the headline left or centre-left (x<1250) |
| 2 | Bottom-heavy: products end at y=2091 (9% margin) | bottom row | Low | Optional: shift the grid −40 px y |
| 3 | 0.7% export stretch | export | Low | Crop to 1843x2304 first |
| 4 | Same soft-shadow note as #1 | all | Low | contact 0.24→0.30 |

## 3. soapcoll_gift_wide: PASS · **READY** (minor) · 76%
The staggered 3+3 layout works, and star anise (≈2.6 cm) and cinnamon (≈7.4 cm) are consistent with the bars.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Dried oranges measure ≈165 px ≈3.9 cm against ≈6 cm expected, so the bars look ~1.5x large next to them | oranges (1960–2290, 190–410) | Low-Med | Accept (small slices exist), or soap w 365→310 and re-space |
| 2 | Linen folds run under rigid bars with no deformation; Oat Milk Honey's left edge sits on a fold ridge | OMH (866–1231, 424–751) (c10) | Low | Move OMH +40 px x; contact 0.24→0.30 |
| 3 | Headline zone (x<963) is moderately textured (gradient 7.3 vs 5.4 for stone) | left 35% | Low-Med | Dark type with weight, or a 10–15% ivory scrim |
| 4 | Charcoal is crowded by the spices (≈40–60 px gap) | Charcoal (1956–2321, 840–1143) vs anise (≈2290–2400, 1180–1380) | Low | Move the bottom row −40 px x |

## 4. soapcoll_gift_vert: PASS · **PROVISIONAL** · 70%
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Top 30% is **not calm**: ribbon, pine and orange; gradient energy 15.3, 3–7x the other verticals | ribbon (660–1856, 0–330), pine (1250–1720, 150–600), orange (1150–1290, 280–450) | **Med** | Regenerate the plate with props kept below y≈700 on the right, or confine the headline to x<1100, y<650 over plain linen |
| 2 | Orange ≈175 px ≈3.3 cm at 53 px/cm, so the bars read ~1.8x oversized | orange (1380–1555, 690–870) (c09) | Med | Soap w 450→380 (scale ≈0.264), keep pitch ratio, re-centre |
| 3 | Bottom-heavy, products to y=2100 | grid | Low | Follows from fix 2 |
| 4 | 0.7% export stretch | export | Low | Crop 1843x2304 |

## 5. coffeecoll_counter_wide: PASS · **PROVISIONAL** · 72%
Clean, calm left 32% and correct scale (espresso cup ≈6.4 cm at 26 px/cm).
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | **Shadow mismatch.** The plate's cup and dish shadows are hard and dark (≈0.47 of lit counter) and ~150 px long for 3–5 cm objects. The carton ground shadows are 0.67–0.77 and ≈120 px long for 23 cm cartons. Caramel sits in the same hard light as the cup and casts almost nothing visible (c17) | Caramel (1805–2075, 690–1285); dish (2400–2640, 1140–1215) | **Med** | gstrength 0.27→0.45, glen 0.2→0.45, gsigma 9.5→5. Widen the pitch 310→330 so the shadows land on counter, not on the next carton (shadows may not touch products) |
| 2 | Identical spacing and orientation: lineup / catalogue look | row | Low | Optional: pitch variation ±20 px, or slight depth stagger with matching ±2% scale |
| 3 | v2 cut-outs | — | Info | Use v3 |

## 6. coffeecoll_counter_vert: PASS · **READY** · 76%
Top 58% is clear, and the soft shadows are visible and correctly directed (c18).
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Products are small for a feed post (each carton 258 px, 14% of width). Flavour names are readable on a phone but not in the grid thumbnail, and the empty area is far more than the 30% needed | row (117–1283, 1337–1905) | Low-Med | w 258→300 (scale 0.414), pitch 302→340, keep baseline 1905 |
| 2 | 0.7% export stretch | export | Low | Crop 1843x2304 |

## 7. coffeecoll_gift_wide: PASS · **PROVISIONAL** · 68%
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | **Cartons too small for a banner:** 182x401 px (6.6% of width). Flavour names are ≈13 px cap in the master, ≈9 px at 1920, so they are illegible on the homepage and on a mobile crop | row (1104–1976, 784–1185) | **Med** | w 182→240 (scale ≈0.33), pitch 230→300, baseline 1185→1215 |
| 2 | **Exposure too high for a dim room:** kraft median 157 and label white 215, while the ceramic dripper median is 88 and the napkin median 108 in the same light. The cartons look separately lit | all cartons | **Med** | expo 0.90→0.80 (single scalar) |
| 3 | Light gable-edge rim against the dark green wall | e.g. Hazelnut x≈1106–1112, y 790–900 (c20) | Low | choke 1→2 |
| 4 | Second sconce cut by the right frame edge | (2700–2752, 330–500) | Low | Clone it out, or crop 50 px |

## 8. coffeecoll_gift_vert: PASS · **PROVISIONAL** · 72%
The top 30% is a clean dark wall and the holiday mood is strong. The dripper and server (≈23 cm) match the carton scale.
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Same over-bright cartons (expo 0.9; napkin median 100) | all cartons | Med | expo 0.90→0.80 |
| 2 | Gable rim visible at 100% on the dark wall | Hazelnut (212–225, 1345–1480) (c24); same on all four | Low | choke 2 |
| 3 | 0.7% export stretch | export | Low | Crop 1843x2304 |

## 9. mixed_holiday_wide: PASS · **REJECT** · 55%
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | **Upright soaps read as flat cards, not bars.** The cut-outs are top-down face shots stood on edge. The camera is about 20° above the table (runner and top clearly foreshortened), so a 2.5 cm bar should show its top face (≈55–60 px) and some edge. None is visible, and the label face carries top-down lighting (c21) | soaps (973–1739, 999–1196) | **High** | Cannot be fixed under the rules with these cut-outs (no warp or redraw). Options: (a) supplier photos of the bars standing or at 3/4 view; (b) regenerate the plate with the camera at table height (≤5° elevation, table top nearly edge-on); (c) drop the soaps from the upright scene and use the top-down soap images |
| 2 | Headline zone (x<963) has a blown window (254), curtain and table corner: luminance SD 78, no stable background for either light or dark type | (0–963, 0–1536) (c31) | Med | Regenerate with a plain wall on the left, or move the window out of frame |
| 3 | Labels are neutral-cool (B/R 0.97) in a warm scene (surface B/R ≈0.86), so they look slightly pasted | all labels | Low-Med | scene_wb 0.3→0.55 (scene only) |
| 4 | Soap shadows are faint (median 0.91) | soaps | Low | gstrength 0.27→0.35 for the soaps |
Scale is fine: mug ≈9 cm and cinnamon ≈8.6 cm at 25 px/cm. Cocoa is 5% larger than Caramel, consistent with its nearer baseline.

## 10. mixed_holiday_vert: PASS · **REJECT** · 55%
| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | **Flat-card soaps**, more obvious at 262–266 px width (c22) | soaps (199–1082, 1702–1942) | **High** | As #9.1 |
| 2 | The mug, at the same depth as Cocoa (base ≈1815), measures ≈7.8 cm tall at 30 px/cm, so the products are ~15–25% oversized | mug (≈1505–1700, 1590–1830) | Low-Med | Scale all products ×0.85 and re-space |
| 3 | Crowded overlap: soaps hide the carton bases and contact, and cast no shadow onto the cartons (not allowed by the rules), so the layering reads stuck-on | Sandalwood over Cocoa (365–461, 1702–1815); Charcoal over Caramel (818–1061, 1719–1790) | Med | Separate the depths: spread the soaps or remove the overlap (e.g. move the cartons −60 px y and the soaps apart) |
| 4 | Warm-scene / neutral-label WB | labels | Low-Med | scene_wb 0.3→0.55 |
Top 30% is clear (calm wall, SD 36).

---

## Ranking (best → worst)
1. soapcoll_stone_wide (82, READY)
2. soapcoll_stone_vert (80, READY)
3. soapcoll_gift_wide (76, READY minor)
4. coffeecoll_counter_vert (76, READY)
5. coffeecoll_counter_wide (72, PROVISIONAL)
6. coffeecoll_gift_vert (72, PROVISIONAL)
7. soapcoll_gift_vert (70, PROVISIONAL)
8. coffeecoll_gift_wide (68, PROVISIONAL)
9. mixed_holiday_wide (55, REJECT)
10. mixed_holiday_vert (55, REJECT; worst: flat-card soaps are most visible, plus crowding)

**Summary:** 4 READY, 4 PROVISIONAL, 2 REJECT. Authenticity passes 10/10.

The top-down soap scenes are the strongest, because a face-on cut-out matches a top-down camera. The coffee scenes need parameter fixes only: expo, shadow strength and length, and carton scale. Answer to the mixed-image question: no, the upright soaps read as flat cards. This is a geometry limit of the top-down cut-outs, and no parameter change can fix it.
