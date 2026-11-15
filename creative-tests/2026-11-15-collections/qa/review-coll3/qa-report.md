# EverLiv collection composites: independent visual QA, round 3 (review-coll3)
Reviewer: independent QA (did not build these). Date: 2026-11-15. Scope: the 4 rebuilt masters. All coordinates are master px (x, y) unless marked otherwise.
Crops are in /home/claude/review-coll3/ (a*, b*, c*, d*, s1/s2 shadow maps where magenta = product, v_* half-size previews, c0_thumbs = 250 px 3:4 grid tiles plus 360 px tiles).

## Global checks (all 4)
- **Pixel fidelity (auth2.py):** the residual is −0.5 on every channel (uint8 truncation). SD 1.30–1.93 (grain only), chroma SD ≤0.24, per-channel gain equal to ±0.0008. Mirror test 11–29 against ≈1.9. One exposure scalar per image. No product is clipped, overlapped or mirrored. **Authenticity PASS 4/4.**
- **Exports:** every export matches crop+LANCZOS bit-exactly (max diff 0). The verticals use crop (6–1849), the wide is full-frame, and the bundle is an exact 2x reduction.
- **Layout matches the report.json files:** counter_vert x = 82/388/692/998 at w 275 (pitch 304–306); gift_vert x = 147/433/717/1003 at w 250 (pitch 284–286); the bundle base is at 897+903 = 1800.

---

## 1. soapcoll_stone_wide: PASS · **READY** · 84% (up from 83)
- Fix #1 (pit): **landed, with a residue.** The dark pit is gone: the region's minimum is 150, against 71 in round 2. The inpaint left a bright, smooth smudge in its place, about +14 levels over its surround (239 against 225–229), with lower fine texture (HP-SD 2.7 against 3–9 around it). At 2x on the 1920 export it reads as a small white hot-spot (a1, a2).
- Fresh pass: nothing else has changed. The bars are clean, and the headline zone is otherwise calm.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Inpaint left a bright, textureless smudge | (68–122, 752–780) | Low | Re-inpaint with matched tone and grain, or let headline type cover it |
| 2 | Bar shadows are slightly soft (carried over) | all bars | Low | strength 0.20→0.24 (optional) |

## 2. coffeecoll_counter_vert: PASS · **PROVISIONAL** · 74% (up from 73)
- Fix #1 (edge): **landed.** Hazelnut x0 is 82, which is ≈44 px from the edge on the 1080 export and ≈10 px inside the 3:4 grid crop. That is tight but not clipped.
- Fix #2 (shadows): **landed for tone.** The wedges sit at ratio 0.55 with a hard edge. The plate's saucer shadow is ≈0.40 and the bean dish ≈0.61, so the wedges are in family, and the direction (falling right) matches the plate.
- **New collision:** the wider row moved Caramel's right edge to x 1273, and the saucer's left tip is at x ≈1302. That leaves a **29 px gap (≈17 px at 1080)**. The longer Caramel wedge now runs across the saucer's left rim. The data shows ratio 0.55 on saucer pixels at (1300–1360, 1790–1845): the rim is darkened flat, and the shadow edge goes through the saucer without any offset for its height (b1, b4, s1). This is the same defect as counter_wide #2, now introduced here.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Caramel wedge is painted flat across the saucer rim | (1300–1366, 1785–1850) | **Med-Low** | Clip the Caramel wedge to exclude the saucer silhouette (mask from the plate) |
| 2 | Caramel crowds the saucer: 29 px gap | (1273–1302, 1780–1905) | Low-Med | w 265 / pitch 295 (centres 215/510/805/1100; right edge ≈1232). Or keep the spacing and accept it after fix 1 |
| 3 | Wedges start ≈60 px above the counter/wall junction (y≈1737), so they climb the wall as one smooth shape with no kink at the corner. This is visible behind Caramel at 1080 | wall bands (all gaps, plus 1273–1310, 1675–1737) | Low | Start the wedge at y≥1737, or put a kink at the junction |
| 4 | Each wedge disappears behind the next carton (carried over, accepted on the wide) | 30 px gaps | Low | Accept |

## 3. coffeecoll_gift_vert: PASS · **READY** · 77% (up from 76)
- Fix (w 250, pitch 285): **landed at 1080.** On the export each carton is ≈146 px wide and every flavour name reads clearly (c1).
- **Grid thumbnail: only marginal gain.** In a 250 px 3:4 tile, COCOA is borderline and HAZELNUT, MUSHROOM and CARAMEL are not legible; "COFFEE" and the colour cues do read (c0). At 360 px most names read. This is a hard limit: four cartons across a 4:5 frame cannot carry readable names at 250 px. Accept it, and don't rely on the grid tile to show the flavours.
- **Collisions:** none. Caramel ends at 1253, the nearest beans are at ≈1330, the napkin at ≈1370 and the dripper at ≈1640+ (c2). Hazelnut is ≈83 px from the edge at 1080, so it is safe in the grid crop.
- Shadows: soft, falling right, consistent (s2; p1 ratio 0.71). The dark specks on the beans in s2 are division noise on near-black pixels, not edits (mean |diff| 0.26).

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Flavour names unreadable in the 250 px grid tile | row (147–1253, 1279–1830) | Low | Accept; the names go in the caption or cover text |
| 2 | Row is left-weighted, with the props on the right (by design) | — | Info | — |

## 4. bundle_artisan_coffee: PASS · **READY** · 82% (up from 81)
- Fix #1 (choke 2): **did not land.** The grey-blue edge line is still visible at 4x (d1 against round-2 m14). Cause: the neutral grey sits *inside* the v2 cut-out at full alpha. At x = 172–179 the cut-out RGB is (156–176, neutral) with alpha 255. So eroding the soft alpha by 2 px leaves 3–5 px of neutral grey (lum 146–167, R−B < 20) along every carton's left gable edge, at y ≈ 930–1120 (Hazelnut x 158–183; the same pattern sits at x+490n on the others). At 1080 this is a ≈1.5–2 px grey outline.
- Fix #2 (baseline 1800): **landed.** The top margin is 897 and the bottom 900, so the row is geometrically centred and reads balanced; the shadows add the right amount of weight below it. The side margins are 140/140.

| # | Defect | Location | Sev | Fix |
|---|---|---|---|---|
| 1 | Neutral grey rim, 3–5 px, on each left gable edge (baked into the cut-out) | Hazelnut (158–185, 930–1120); Cocoa, Mushroom and Caramel at +490/+980/+1470 x | Low | Choke 4–5 on the left gable edge only, or check whether the unused `-v3` cut-outs are clean there and switch |

---

## Ranking (these four)
1. soapcoll_stone_wide 84 READY
2. bundle_artisan_coffee 82 READY (rim still open)
3. coffeecoll_gift_vert 77 READY
4. coffeecoll_counter_vert 74 PROVISIONAL: the new shadow-on-saucer collision. One fix (clip the Caramel wedge) should make it READY at about 77.

Fixes that landed: 5 of 7. The pit is removed but leaves a residue. The counter_vert spacing and shadows landed, but they caused a new saucer collision. The gift_vert sizing landed at 1080, though the grid tile is still limited. In the bundle, the baseline fix landed but the rim fix did not.
