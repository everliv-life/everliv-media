# Visual QA round 4: coffee cartons (independent review, 2026-11-14)

Scope: `coffee_cocoa_v4-2160x2700.png` (prior v3) and `tmpl_plinth_hazelnut_v3-2160x2700.png` (prior v2).
Method: v(n) vs v(n-1) ratio maps, 100% and 2–3x crops, 1080 downscales, template-matched authenticity check against the supplier `bag-front.jpg` renders. Crops are in `/home/claude/review-gift4/`.

**Source path note.** Both report JSONs give the source as `library/everliv-<sku>/everliv-<sku>--bag-front.jpg`, but that folder does not exist. The real path is `library/<sku>/<sku>--bag-front.jpg` (for example `library/cocoa-coffee-medium-roast/cocoa-coffee-medium-roast--bag-front.jpg`). Fix the JSON field.

---

## 1. coffee_cocoa_v4

**Authenticity: PASS.**
- **Match to source:** NCC 0.998 against `cocoa-coffee-medium-roast--bag-front.jpg` at scale 1.0.
- **Not mirrored:** the mirrored NCC is 0.24.
- **Exposure:** a uniform scalar of about 0.946 that is the same on all three channels (R/G/B 0.946/0.945/0.945), so there is no tint. The JSON says 0.954. The gap is small, but the JSON value does not match my measurement.
- **Residual:** luminance grain only (SD 2.41).
- **No shading on the product:** the low-pass residual inside the carton is within ±0.35 levels everywhere, including the bottom 10–300 px.

**Verdict: PROVISIONAL.** **Quality: about 76%** of a professional studio product photo (v3 was about 75%). The shadow work is good, but a new seam and the unfixed smear cancel most of the gain.

**Prior defects:**
1. **Carton not grounded: improved, not fully fixed.**
   - **Cast shadow:** added to the right and back, at x about 1510–1800, y about 2140–2360. It is soft with no hard edges (`coffee4_ratio_base.png`, `coffee4_base_r_3x.png`).
   - **Direction:** plausible. The mug and dish shadows also fall to the right (`coffee4_prop_shadows.png`).
   - **Density:** the core is 0.71–0.76 of the plate. That is darker than the 0.85–0.90 in the brief, but lighter than the scene's own prop shadows (dish about 0.5), so it reads naturally.
   - **Front edge (x 1000–1500):** occlusion is only about 25 px at 0.89–0.95, and it is clipped off by the seam below (new defect A). At feed size the front edge still sits on a pale band and reads slightly floated (`coffee4_1080_base_2x.png`).
   - **Left panel edge:** acceptable.
2. **Dark contact line: fixed.** The v3 6 px line was lightened (ratio 1.2–1.5 on the edge). No dark blobs.
3. **Table retouch smear (x 1080–1340, y 2340–2390): not fixed.**
   - The stippled, posterised patch with no wood grain is still there at x about 1000–1330, y about 2340–2392 (`coffee4_seam_2x.png`, `coffee4_table_smear_3x.png`).
   - The v4 edit actually made the area 3–10% brighter than in v3 (ratio 1.03–1.11 below y 2360), so it is now more visible as a pale strip at feed size.

**New defects:**
- **A. MAJOR: hard horizontal seam at y 2359/2360, across x about 1000–1800.**
  - Problem: luminance steps +12 to +16 levels in one row. For example, at x 1200–1450 the rows above average 110 and the rows below average 126.
  - Cause: the occlusion and cast-shadow layer is clipped by a rectangular bound at y 2359. Below that line the table is a brighter fill.
  - Visibility: clearly visible at 100% (`coffee4_seam_2x.png`, `coffee4_seam_y2360_3x.png`). At 1080 it shows as the pale band under the front face.
  - Fix: remove the y-clip. Let the occlusion fade over 30–60 px below the front edge, and let the cast shadow's lower edge fall off softly rather than stop at a row. Re-inpaint y 2330–2400, x 980–1350 with a grain-aware clone from the wood at x 600–900 or 1550–1850 at the same y, matched to the surrounding luminance (about 105–115), not brighter.
- **B. Minor (positive change, recorded): the background right of the carton was replaced.**
  - Where: x about 1500–1640, y 750–2110.
  - Change: the v3 darker ghost band is now 10–30% brighter.
  - Check: at 100% the result is clean, with continuous cabinet and wood (`coffee4_bg_right_100.png`). Nothing odd.
- **C. Trivial: a 3 px white speck at (1462, 2424).** It is from the plate and unchanged since v3. Fix: a clone-stamp.
- **Carried over (accepted, minor):** source-render tick line at x 1490–1500, y 1290–1390; cool back-panel sliver; native label softness; small beans.

---

## 2. tmpl_plinth_hazelnut_v3

**Authenticity: PASS.**
- **Match to source:** NCC 0.997 against `hazelnut-coffee-medium-roast--bag-front.jpg` at scale 1.0.
- **Not mirrored:** the mirrored NCC is 0.26.
- **Exposure:** a uniform scalar of about 0.961 on all channels (JSON 0.969).
- **Residual:** grain only (SD 2.67).
- **No shading on the product:** the low-pass residual inside the carton is within ±0.34.

**Verdict: READY (after owner approval).** **Quality: about 79%** (v2 was about 74%).

**Prior defects:**
1. **Drawn-outline contact line: fixed.** The v2 dark line was lifted, and the base now has soft occlusion. Along the left panel the stone grades from about 150 to 185 over about 40–60 px. Under the front face the strip to the lip is about 0.8 (`plinth3_base_l_3x.png`, `plinth3_front_2x.png`).
2. **Dark corner blobs at (695, 2148) and (1406, 2176): fixed.** Both corners are clean (`plinth3_base_l_3x.png`, `plinth3_base_r_3x.png`).
3. **Cast shadow missing: fixed.**
   - Where: the plinth top, toward the right and back, at x about 1400–1720, y about 2020–2225.
   - Edges and darkness: soft, with no hard edges, and a core of 0.75–0.79. That is darker than the 0.85–0.90 in the brief, but much lighter than the plinth's floor shadow (about 0.5), so it is plausible.
   - Direction: consistent with the plinth and vase shadows, which fall to the right.
   - Edge of the shadow: it ends at y 2225, which is the plinth's front lip. That matches the change of plane, so it is not a seam.
4. **Grounding at feed size: good.** The carton reads as sitting on the stone (`plinth3_1080_base_2x.png`).

**New and other defects:**
- **A. Minor (positive, recorded): wall brightened right of the carton.**
  - Where: x 1400–1500, y 650–2000.
  - Change: the v2 darker band is now even with the wall (151 to 179). It is clean at 100% (`plinth3_wall_right.png`).
- **B. Minor (composition): the carton's front-bottom corner sits within about 5 px (under 1 mm at scale) of the plinth lip, at (880, 2220).**
  - This was the same in v2. It reads as edge-balanced on close inspection.
  - Optional fix: move the carton (with its shadow layers) up and back about 40–80 px.
- **C. Minor: the cast shadow is subtle at feed size.** This is acceptable. Optionally deepen the near-field part to about 0.7 for the first 30 px.
- **Carried over (accepted, minor):** tick line at x 1387–1398, y 1150–1260; faint line on the gable top; cool back-panel sliver; native label softness.

---

## Summary
| Image | Authenticity | Verdict | Quality | Remaining to fix |
|---|---|---|---|---|
| coffee_cocoa_v4 | PASS (x0.946, not mirrored, no product shading) | PROVISIONAL | about 76% | Hard seam at y 2360 (x 1000–1800). Smear not fixed and now brighter. Front-edge occlusion clipped. |
| tmpl_plinth_hazelnut_v3 | PASS (x0.961, not mirrored, no product shading) | READY (after owner approval) | about 79% | None blocking. Optional: move the carton back from the lip. |

**Also fix:** the `supplier_source_render` paths in both JSONs (the `everliv-` folder prefix does not exist), and the JSON exposure scalars, which are 0.008 above what I measured.
