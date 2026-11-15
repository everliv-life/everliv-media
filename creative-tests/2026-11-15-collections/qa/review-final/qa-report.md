# Final finishing QA: six checks (2026-11-15)

Reviewer: independent and strict. I did not make these images.

**Method**
- **Authenticity:** an interior-masked fit of each supplier cut-out, testing per-channel gain, the chroma residual, the low-pass residual and a mirror test.
- **Changes:** v5/v6 difference maps.
- **Shadows:** maps of the shadow ratio against the plate.
- **Inspection:** 100–4x crops, plus a check of the 1080 and 1920 exports.
- **Scale:** pixel rulers, with a depth correction from the plane geometry, (y_base − y_horizon). The horizon comes from the rim/saucer ellipse angle and a 35–50 mm-equivalent lens.
- **Crops:** all are in `/home/claude/review-final/`.

**Scale caveat.** Prop sizes in AI plates are not physically exact. Every cm figure below is ±10–15%. Where the props disagree I give each ruler separately rather than averaging them away.

---

## 1. coffee_cocoa_v6 and ind_caramel_v2: Authenticity PASS · READY · 82% / 81%

**Authenticity**
- **Template match:** NCC 0.996 at 601×1324, xy (854, 1038).
- **Gain:** per channel 0.9515/0.9513/0.9511, so one scalar with no tint.
- **Residuals:** chroma SD 0.30; low-pass residual −0.28 to +0.04 (no relight); |d| 2.2 against 28.6 when mirrored (not flipped).
- **Caramel v2:** the same composite. It differs from Cocoa only inside the label.

**Placement**
- Bottom-anchored within 1 px (bottom 2362, v5 2363).
- Horizontal centre 1154.5 (v5 1155).
- The only changes from v5 are the old carton area and its shadow; the rest of the plate is bit-identical.

**Residue**
- None. At 100% I checked the uncovered gable and wall band (x 793–1517, y 768–1040) and the left and right strips (x 793–854 and 1455–1517, y 1040–2360). All are clean continuous bokeh, wall and wood, with no stand-in edge or plate seam (`r6`, `r7`, `r8`).

**Contact and shadow**
- The base reads as grounded at 100% and at 1080 (`r9`).
- The cast shadow was rescaled with the carton. It is shorter and fainter, still falls back and to the right like the mug's, and has no hard edge (`r10`).

**Proportion (measured)**

| Element | Measurement |
|---|---|
| Carton | 1324 px |
| Mug | ≈360 px tall on its axis (rim 1712 → base 2172), 494 px wide |
| Mug viewing angle | rim ellipse ≈14° |
| Depth factor, carton base (2350) vs mug base (≈2125) | ×1.17–1.22 |

This mug is a **squat wide cup** (width:height 1.39), not a typical 9–10 cm mug.

| Ruler | v6 carton | v5 carton |
|---|---|---|
| Mug height, read as 8 cm (what its shape suggests) | **≈24–26 cm** | ≈29–31 cm |
| Mug height, read literally as 9–10 cm | 27–32 cm | 33–38 cm |
| Mug rim diameter, 10–11 cm | 22–24.5 cm | — |
| Beans (≈60–70 px long, 1.0–1.2 cm, in the dish at about the same depth) | 23–26 cm | — |

**Verdict.** v6 now sits at or just above the 23–24 cm reference. v5 was about 25–30% over by the same rulers, so the 17% cut was the right size of move. It reads clearly more natural beside the cup, and I would not go below 0.80. If the owner still sees it as large, 0.78–0.80 is the floor.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | The JSON regressed: it dropped `supplier_source_render` and the QA exposure note, and `exposure_scalar` says 0.954 where I measure 0.951 | report.json (both) | Info | Restore the source path and set exposure to 0.951 |
| 2 | Carried over: a cool sliver on the left gable edge, native to the render | ≈(860–880, 1040–1400) | Accept | — |
| 3 | Advisory: the printed tagline "Pure Cellular Vitality" needs a claims check before paid use | label | Info | Compliance |

---

## 2. soapcoll_gift_vert_v2: Authenticity PASS · READY · 80%

**Authenticity**
- All 6 bars: gain 0.997 on every channel, chroma SD 0.24, mirror |d| 10–13 against about 2.

**Headline space**
- **Yes.** The first bar starts at y 872 (37.8%), and y 0–806 (35%) is clean linen with no props. The pine tips start at about y 820 at the far right (`s3`).
- The diagonal fold texture is soft and suits dark text. A light scrim may help a light headline.

**Prop scale (bar 380 px = 8.5 cm, so 44.7 px/cm)**
- Dried orange slices: 220 / 210 px, about **4.9 cm**. That is plausible for a small dried slice but about 18% under the 6 cm reference.
- Star anise: about 3 cm (plausible).
- Cinnamon: about 8.3 cm (plausible).

**Crowding**
- The grid gaps are 70/73/76 px, even. The props sit apart in the right column. Not crowded.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | The lower orange slice nearly touches the frame (11 px; about 6 px at 1080) | (1635–1845, 1315–1525) | Low | Move the slice about 40 px left, or let it bleed off the edge deliberately |
| 2 | Orange slices are a little small (≈4.9 cm) | same | Low/Info | Optional: ×1.15 on the plate prop |
| 3 | The clean-forrest cut-out file reads SLUMBER (carried over) | — | Info | Copy must say Slumber |

---

## 3. coffeecoll_counter_vert_v2: Authenticity PASS · PROVISIONAL · 75%

**Authenticity**
- All 4 cartons: gain 0.997 (the B channel is 0.07% lower, from resampling), chroma SD 0.24, mirror |d| about 28.

**What landed**
- **Saucer is clean.** The ratio is 1.00 on all saucer and cup pixels (`c2`, `c3`).
- **Gap to the saucer** is 1243 → 1302 = 59 px (34 at 1080), up from 29.
- **Grounding:** the cartons are grounded with soft contact shadows (`c6`).
- **Edge margins:** left 94 px (55 at 1080; about 21 px inside a 3:4 grid crop). The bean dish is about 59 px from the right edge.

**New defect from the cut**
- The rectangle stops at y 1870, but the wedge runs to about y 1895. This leaves a dark **toe**, ratio 0.55, at x 1292–1345, y 1870–1895, sticking out past the straight vertical cut at x ≈1292.
- The shadow therefore ends as a stepped **L / boxy slab**, and this is visible at 1080 (`c4`, `c5`).
- A cast shadow from a carton's vertical edge would end on a diagonal, not on a vertical line plus a step.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Stepped L-shaped shadow end with a vertical cut | (1292–1350, 1700–1895) | **Med-Low** | Replace the rectangle with the saucer silhouette from the plate, dilated about 12 px and feathered about 15 px. Or extend the mask to y ≥1905 and angle its left edge to follow the wedge's direction |
| 2 | Wedges begin about 50 px above the counter/wall junction (≈1737) and climb the wall (carried over) | all gaps, y 1680–1737 | Low | Start at y ≥1737 or kink at the junction |
| 3 | Scale: the carton reads about 15% larger relative to the cup than on counter_wide (see §6) | — | Low | Optional: 250 px |

Fixing #1 should make this READY at about 77%.

---

## 4. mixed_holiday_vert_v2: Authenticity PASS · PROVISIONAL · 74%

**Authenticity**
- Gain 0.997, chroma SD 0.23–0.24, mirror test OK.

**Crowding**
- **Less crowded: yes.** The gaps went from 40 to 70/70/71 px (41 at 1080), and there are now 173 px from Sandalwood to the mug.
- The left margin is 110. The row reads as four separate objects instead of a wall.

**Headline space**
- The top 55% of the wall is clear apart from the garland at top right.

**The trade-off: scale**
- The products shrank from 276 to 250 px against a large mug: about 295 px axis height and 280 px wide, at the same depth.
- **Carton by the mug (9.5–10 cm): about 17.5–18.5 cm.** By the cinnamon sticks (225 px, 8–10 cm): 19–24 cm.
- This is now the **smallest coffee in the set**, about 15% smaller relative to the mug than mixed_holiday_wide. At 8.5 cm, the soap bars imply a mug about 12.5 cm tall.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Products undersized against the mug | row y 1417–1968 vs mug (1404–1684, 1663–1985) | Low-Med | Cartons about 280, soaps about 230, gaps about 50. This still clears the mug by about 90 px. Or accept, as an owner decision on the trade-off |

The 1080 export, grounding and shadows are fine (`m2`).

---

## 5. mixed_holiday_wide_tight: Authenticity PASS · READY (owner choice vs the approved wide) · 80%

**Authenticity**
- Gain 0.997, chroma SD 0.24, mirror test OK.
- The products are 1.224× the approved wide, matching the 1.223× plate upscale. The proportions are therefore identical to the approved version.

**Softness**
- The Laplacian variance of in-focus plate content (mug, linen) falls to about 53% of the original, and the products are crisper than the props.
- At 2560 and 1920 delivery this is barely visible.
- The wall is clean (SD 1.8), with no JPEG blocking or banding at 6x contrast (`w8`). The wreath is defocused anyway (`w5`).

**Scale vs the mug**
- Carton 665 visible against mug 310 axis gives **about 20.5–21.5 cm**, the same as the approved wide (20–22). Consistent.

**Headline and button space**
- A full-height left column, x 60–680 (22%), is clear.
- So is a top band, x 80–1550, y 60–500. The carton tops are at y 534 and the wreath is at x >1580. At 1920 this is about 1025×307 px.
- That is enough for a headline plus a button, but tighter than the original. Confirm with a real type mock-up.

**Bundle implication**
- None physical: no box, ribbon, tissue or tray. Four products alternating on a runner read as a collection.
- Copy must not say "set" or "bundle" unless one is offered.

**Seasonal feel**
- Kept: wreath bokeh, cinnamon and pine.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Caramel's base is about 20 px from the cinnamon (near-tangent; cinnamon in front) | (1937–1957, 1150–1250) | Low | Shift the Caramel carton 30–40 px left |
| 2 | The plate is slightly soft against the crisp products | mug, linen | Low | Accept, or redo the plate at native resolution |

---

## 6. Coffee scale consistency

Target: 23–24 cm. Each figure is the carton height implied by each ruler, after depth correction.

| Image | Carton px | Ruler readings | Implied carton | Flag |
|---|---|---|---|---|
| coffee_cocoa_v6 / ind_caramel_v2 | 1324 | squat cup at 8 cm → 24–26; beans → 23–26 | **≈24–26 cm** | OK |
| coffeecoll_counter_wide | 595 | cup (7 cm, 132 px axis, ×1.12–1.17 depth) → 26.5–28; loose beans (≈28 px) → ≈22 | **≈22–28 cm, about 25** | OK |
| coffeecoll_counter_vert_v2 (for reference) | 584 | cup (112 px) → 31–33; beans → ≈24 | ≈24–33 cm | Mildly large relative to the cup |
| coffeecoll_gift_wide | 529 | dripper top width 235 px (V60-02 ≈11.6 cm) → ≈25; beans (20–27 px) → 21–24; dripper + carafe stack 395 px → 25 at a 20 cm stack | **≈22–25 cm** | OK |
| **coffeecoll_gift_vert** | 551 | dripper width 185 px → ≈34; stack 329 px → 33 at 20 cm; beans (15–20 px) → 30–39 | **≈32–35 cm** | **OUTLIER, about 40% over.** It is 32% larger relative to the same props than gift_wide |
| mixed_holiday_wide | 551 | mug (255 px axis, 9.5–10 cm) → 20–21; cinnamon (205 px, 8–10 cm) → 21–26 | **≈21–22 cm** | OK (slightly small) |
| mixed_holiday_wide_tight | 674 | mug (310 px) → 20.5–21.5 | ≈21 cm | OK, matches the wide |
| mixed_holiday_vert_v2 | 551 | mug (295 px) → 17.5–18.5; cinnamon → 19–24 | **≈18–20 cm** | Low outlier (see §4) |
| tmpl_plinth_hazelnut_v3 / ind_mushroom_v1 | 1595 (scale 1.0, same as cocoa v5) | olive bud vase 462 px tall (1619–2081), behind the plinth; depth ×1.1–1.3; vase 10–14 cm → 26–43 | **≈30–35 cm, weak ruler** | Likely large: this is the same scale the owner rejected on cocoa v5 |

**Note on the dripper reference.** "Dripper + carafe ≈25 cm" is probably too tall. A V60-02 on a 600 ml server stacks to about 19–21 cm. With the 25 cm figure, gift_wide would read about 31 cm and gift_vert about 41 cm.

**Fixes**
- **coffeecoll_gift_vert:** scale the cartons to about 0.72× (250 → 180 px wide) to match gift_wide. This conflicts with the earlier readability request (250 px for 1080 legibility). The plate's props are simply small, so the honest options are: accept the oversize, use a plate with larger props, or reduce to 3 cartons.
- **Plinth hazelnut and mushroom:** apply the same 0.83 as cocoa v6 if they will appear alongside it. There is no mug, so this matters less in isolation.
- **mixed_holiday_vert_v2:** see §4.

---

## Summary

| Image | Auth | Verdict | % |
|---|---|---|---|
| coffee_cocoa_v6 | PASS | READY | 82 |
| ind_caramel_v2 | PASS | READY | 81 |
| soapcoll_gift_vert_v2 | PASS | READY | 80 |
| coffeecoll_counter_vert_v2 | PASS | PROVISIONAL (stepped shadow end) | 75 |
| mixed_holiday_vert_v2 | PASS | PROVISIONAL (scale vs mug) | 74 |
| mixed_holiday_wide_tight | PASS | READY | 80 |
| Scale outliers | — | gift_vert ≈+40% (high); plinth hazelnut and mushroom likely high; mixed_vert_v2 low | — |

READY means publishable after owner approval.
