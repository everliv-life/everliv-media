# Fix-verification QA, round 2 (2026-11-15)

Reviewer: independent and strict. I did not make these images.

**Method**
- **Authenticity:** an interior-masked fit of each supplier cut-out at its declared box (template-matched for the plinth images). I tested per-channel gain, the chroma residual, the low-pass residual and a mirror test.
- **Changes and residue:** diffs against the prior version and against the plate.
- **Shadows:** maps of the shadow ratio against the plate.
- **Inspection:** crops at 100–8x, plus 1080 and feed-size (390 px) simulations.
- **Crops:** all are in `/home/claude/review-final2/`.
- **Scale:** every cm figure is ±10–15%. AI plate props are not physically exact.

**Authenticity, all 18 product placements: PASS.**

| Image | Gain (R/G/B) | Chroma SD | Low-pass residual | Mirror test |
|---|---|---|---|---|
| counter_vert_v3 | 0.9897/0.9894/0.9890 (stated 0.9922) | 0.25 | within ±0.26 | 28 against 1.5 |
| mixed_vert_v3 | 0.911 (stated 0.913) | 0.24–0.25 | — | soaps 11, cartons 26 |
| gift_vert_v2 | 0.7975/0.7972/0.7968 (stated 0.80) | 0.24 | — | 22.5 |
| wide_tight | 0.888 (stated 0.891) | 0.25 | — | — |
| plinth hazelnut v4 / mushroom v4 | 0.9669/0.9668/0.9665 (stated 0.969) | 0.29 | −0.27 to +0.02 | 29 against 2.4 |

- **Placement:** each image used a single scalar.
- **Plinth v4:** NCC 0.995 at 601×1323, xy (752, 905).
- **Gain gaps:** the 0.2–0.3% shortfall against the stated scalar is the known grain and feather interaction, as in earlier rounds. The B channel is 0.05% low from resampling. No tint, no relight, no mirroring.
- **Residue:** I found none. Outside the product and shadow zones, no pixel differs from the WB-gained plate by more than 25, in any of the four collage images.

---

## 1. coffeecoll_counter_vert_v3: Authenticity PASS · READY · 77%

**The toe is gone.**
- The wedge's right edge now runs smoothly from (1215, 1700) to a clean diagonal tip at (1324, 1895). There is no vertical cut and no step (`c3`, `c2`).
- The slope bends once at about y 1740–1760, which is the wall/counter junction. That bend is physically correct.

**Saucer and cup are clean.**
- The ratio is 0.99–1.00 everywhere inside the ellipse and the rectangle (`c3`).
- **Note:** the shadow no longer reaches the saucer at all, so the ellipse and rectangle now exclude nothing. At y 1817 the shadow ends at x 1289, while the saucer's left vertex is at 1297. The tip finishes about 25 px left of, and in front of, the saucer's lower-left edge.
- So the shadow does not "continue around" the saucer. It ends just short of it. That reads naturally at 100% and at 1080 (`c7`), with no defect.

**Margins**

| Measure | Master | At 1080 |
|---|---|---|
| Left margin | 110 px | 64 px |
| Caramel to saucer | 86 px (1211 → 1297) | 50 px |
| Bean dish to right edge | unchanged | — |

**Grounding**
- The bases are grounded with soft contact (`c6`).

**Scale**

| Ruler | Implied carton |
|---|---|
| Cup (112 px axis, 7 cm, depth ×1.12–1.17) | ≈28.5–30.5 cm |
| Loose beans (≈25 px, 1.0–1.2 cm) | ≈21–25 cm |

- Read centrally, the carton is about 25–27 cm. That is just above the 23–24 target and matches counter_wide (≈25).
- Against the cup alone it is still about 8% larger than on counter_wide. That is within ruler tolerance.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Carried over: the wedges start about 50 px up the wall | y 1680–1737, all gaps | Low | Accept, or start the wedges at y ≥1737 |
| 2 | Carried over: the carton wedges (ratio 0.55) are darker and harder than the cup's own soft plate shadow | gaps | Low | Accept, or lighten to about 0.65 |
| 3 | The exclusion mask is now inert (the shadow does not reach it) | — | Info | Keep it as a safeguard if the shadow is lengthened |

---

## 2. mixed_holiday_vert_v3: Authenticity PASS · PROVISIONAL · 72%

**What landed**
- **Scale is fixed.** Cartons are 617 px tall, about 20–21 cm by the mug and 21–27 by the cinnamon. That is now consistent with mixed_holiday_wide (≈21–22).
- **Soaps:** a 230 px soap at 8.5 cm implies a mug of about 10.9 cm, which is plausible.
- **Crowding:** the gaps are 50 px (29 at 1080). The row still reads as four separate objects and is not a wall. The left margin is 95 (55 at 1080).
- **Mug clearance:** 135 px from Sandalwood (x 1265) to the mug (≈1400). That is more than the 90 px predicted.
- **Headline space** is unchanged. The bases are grounded (`m4`).

**New and more visible defect: wrong occlusion order (`m3`, `m5`)**
- The Sandalwood bar (x 1035–1265, base y 1968) is pasted **over** the left end of the rear cinnamon stick, which starts at x ≈1216 at y 1934–1990.
- That stick's contact line (≈1990) is lower in the frame than the soap's base (1968), so the stick is *in front of* the soap. It should occlude the soap, not be hidden by it.
- A sliver of that stick shows below the soap's bottom edge, which makes the error readable. The front angled stick also abuts the soap's right edge (0–5 px).
- It is visible at 1080 as cinnamon that looks tucked behind the soap.
- The same overlap existed in v2 by about 15 px, and the previous review missed it. v3 makes it about 50 px.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | The soap occludes a prop that sits in front of it; the soap is tangent to the front stick | (1216–1265, 1930–1970) | **Med** | Keep the sizes and set x0 = 80, gaps = 30, so Sandalwood ends at 1190 (≈26 px clear). Or use cartons 265 and soaps 220 with gaps 45 from x0 90 (ends ≈1195). Do not cover the stick with a plate matte over the product |

Fixing #1 should make this READY at about 78%.

---

## 3. coffeecoll_gift_vert_v2: Authenticity PASS · PROVISIONAL (owner re-approval) · 74%

**What changed**
- Cartons went from 250 to 190 px wide (419 px tall).
- The base line is unchanged at 1830, and the group is re-centred (253–1147).
- There is no residue where the old cartons stood. The contact shadows are soft and grounded (`g5`).

**Implied height now**

| Ruler | Implied carton |
|---|---|
| Dripper width | ≈26 cm |
| Dripper + carafe stack, read as 20 cm | ≈25 cm |
| Beans | 23–30 cm |

- **About 24–27 cm.** That is consistent with gift_wide (22–25) and the set target. It was 32–35 cm before.
- 190 px is about 5% above the 180 px I suggested, which is acceptable.

**Legibility (`g2`, `g3`, `g4`)**
- At 1080 the flavour-name cap height is about 8 px (it was about 10.5). The names read cleanly at 1080 at 100%.
- At phone-feed size (≈390 px wide), COCOA and CARAMEL are just readable. HAZELNUT and MUSHROOM blur into shapes. The approved v1 was also marginal at feed size, but better.
- The cartons now fill about 18% of the frame height, against 24% before. The image reads more as "room with coffee" than "coffee collection".

**Is the change defensible?**
- **Yes, as an accuracy correction.** The approved image overstates package size by roughly 35–40% against the in-scene dripper, carafe and beans. That is a consumer-facing misrepresentation of product size, and correcting it outranks a prior aesthetic approval.
- **But it is a change to an owner-approved asset, so it needs re-approval.** The legibility cost is real.
- **Mitigations:**
  - (a) Name all four flavours in the caption or overlay copy.
  - (b) Use gift_wide or counter_vert_v3 as the lead flavour-identification image, and keep this one as mood.
  - (c) Regenerate the plate with larger props or a closer camera if larger cartons are wanted.

I do not recommend going back to 250 on this plate.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Flavour names not reliably legible at feed size (HAZELNUT, MUSHROOM) | labels, y ≈1590–1610 | Low-Med | Name the flavours in the copy, or use (b)/(c) above |
| 2 | Reduced product presence and a large empty wall | — | Low | Owner decision. The space does suit a headline |
| 3 | Carried over: product shading does not follow the plate's light pool | — | Info | Accept |

---

## 4. mixed_holiday_wide_tight: Authenticity PASS · READY · 81%

**Clearance (`w2`)**
- Caramel's right edge is at 1891. The rear cinnamon stick's left end is at about x 1957, so the clearance is about 66 px (≈46 at 1920). The near-tangent is resolved.
- The base (≈1208) sits behind the cinnamon contact (≈1250+), so the depth order is correct.

**Row spacing**
- The box gaps are 36/37/36 px by the JSON boxes, not the 30 that was stated. This is probably transparent cut-out margin. Either way it is tight but separated, at about 25 px at 1920.
- The soap and carton bases match (1208).

**Headline space**
- A clear left column runs x 60–650 (about 21%, roughly 33 px narrower than before).
- The top band x 80–1550, y 60–500 is unchanged: carton tops at 534, wreath at x >1580.
- That is still enough for a headline and a button. Confirm with a type mock-up.

**Composition**
- The row centre is at 1280 against the frame centre at 1376. The mug and pine on the right balance it.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Carried over: the plate is slightly soft against the crisp products | mug, linen | Low | Accept |
| 2 | The JSON does not record the gap actually used, which differs from the brief | report.json | Info | Note it |

---

## 5. ind_hazelnut_plinth_v4 / ind_mushroom_plinth_v4: Authenticity PASS · READY · 80% / 80%

**Layout**
- The two images have the same geometry. The carton is 601×1323 at (752, 905), a scale of 0.83.
- The base is anchored to the previous contact line (≈2225), centred at x 1052 (48.7%).

**Residue**
- None. The previous carton's footprint (697–1404 × 639–2225) has been rebuilt with continuous wall bokeh and stone.
- I checked the old gable area at 100% (`p2`) and the old side strips at 5x contrast (`p5`). There are no seams. The only edge is the new carton's own side.

**Grounding (`p3`, `p6`)**
- There is a faint, soft contact shadow under the front base edge. Luminance is 170 at the edge and recovers to 184 over about 40 px, against about 184 flat in v3, so it now reads better grounded.
- The front corner sits about 65 px behind the plinth's front arris, so the carton is clearly on the plinth.

**Composition**
- The carton top is at 33.5% of the height. The upper third is clean wall, which gives good copy space.
- The vase at right balances the carton. At 0.83, the plinth reads proportionally larger, which is a calmer, more premium layout and looks fine.

**Scale against the olive bud vase**
- The vase is 462 px tall (base 2081). The depth factor to the carton base is ×1.1–1.3.
- That gives a carton of 2.2–2.6× the vase: **about 22–31 cm, centrally about 25–29**.
- This is consistent with cocoa v6 (24–26). It is a weak ruler, but it is no longer an outlier.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | The JSON regressed again: it dropped `supplier_source_render`, `disclosure` and `template`. `exposure_scalar` says 0.969 where I measure 0.967 | both report.json | Info | Restore the fields and note the measured exposure |
| 2 | Advisory: the printed tagline "Pure Cellular Vitality" needs a claims check before paid use (carried) | label | Info | Compliance |

---

## Summary

| Image | Auth | Verdict | % | Key point |
|---|---|---|---|---|
| coffeecoll_counter_vert_v3 | PASS | **READY** | 77 | Toe gone; shadow ends cleanly short of the saucer; carton about 25–27 cm |
| mixed_holiday_vert_v3 | PASS | **PROVISIONAL** | 72 | Scale fixed (~20–22 cm), but Sandalwood now covers a cinnamon stick that sits in front of it. Shift: x0 80, gaps 30 |
| coffeecoll_gift_vert_v2 | PASS | **PROVISIONAL** (owner re-approval) | 74 | Scale is now correct (~24–27 cm) and the correction is defensible. Flavour names are marginal at feed size |
| mixed_holiday_wide_tight | PASS | **READY** | 81 | Caramel clears the cinnamon by about 66 px; headline space intact |
| ind_hazelnut_plinth_v4 | PASS | **READY** | 80 | 0.83 is consistent with cocoa v6; clean, grounded |
| ind_mushroom_plinth_v4 | PASS | **READY** | 80 | Same |

READY means publishable after owner approval.
