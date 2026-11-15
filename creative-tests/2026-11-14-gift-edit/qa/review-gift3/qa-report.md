# EverLiv composite QA, round 3: independent review (2026-11-14)

Reviewer: independent, strict visual QA. I did not build these images. All coordinates are in the 2160x2700 frame. Crops and analysis views are in /home/claude/review-gift3/. The analysis scripts are in /home/claude/qa3tools/.

## Method
- I viewed each frame at 1080 px wide (`*_1080.png`) and at about 400 px (`thumbs_sheet.png`). I looked at every product edge at 100% and some at 2–4x nearest-neighbour.
- **Product pixel provenance check (new this round).** I template-matched each composite against its actual cut-out (`/home/claude/kit/cutouts/*`), divided the composite by the cut-out after a low-pass filter, and looked at the per-channel ratio map and the residual.
  - All four images give one uniform scalar with no chroma shift:

    | Image | Uniform scalar | Spread |
    |---|---|---|
    | Soap | 1.009 | ±0.003 |
    | Coffee | 0.951 | ±0.002 |
    | Charcoal | 0.978 | ±0.002 (interior) |
    | Hazelnut | 0.966 | ±0.002 |

  - The residual is luminance-only grain: SD 2.4 / 2.4 / 2.4 on coffee, 2.67 ×3 on hazelnut and 4.9 ×3 on charcoal.
  - **I found no relighting, gradient, recolour or local retouch on any product.**
- **Mirroring check.** The label NCC is 0.89–0.95 as placed and 0.35–0.78 when the template is mirrored. **No product is flipped**, and all text reads correctly.
- **Label check against the given reference.** I used an affine ECC alignment plus a difference map (`coffee3_label_diff_x4.png`, `soap5_label_diff_x4.png`).
  - Cocoa: ECC 0.959. Label chroma ratios match the reference within 1.3%. The only differences are on edges.
  - Soap: ECC 0.994.
- **Provenance note on the coffee cartons.** This explains a discrepancy the previous reviewer read as a lighting problem.
  - The coffee cut-outs do not come from the catalog "front" image (`catalog/fronts/*-coffee-*.jpg` is the supplier's "bag-with-beans" render). They are an exact crop (NCC 1.000, scale 1.00) of a different supplier render: `library/<sku>/<sku>--bag-front.jpg`.
  - In that render the left side panel is shaded differently from the catalog front.
  - So the side-panel luminance and colour differ from the catalog JPG (side panel about 0.75x, warmer). That difference is **genuine supplier pixels and not an edit**.
  - Authenticity should be judged against `bag-front.jpg`. Compared with it, the product is bit-faithful apart from the scalar and the grain.
  - Recommendation: record the source file in each composite's report JSON, so that future QA compares against the correct render.

---

## 1. HERO SOAP: soap_omh_v5 (reference everliv-milk-honey-soap.jpg)
**Authenticity: PASS.** Every label element matches the reference:
- the logo and "PURE CELLULAR VITALITY"
- "OAT MILK HONEY" and "HANDCRAFTED SOAP"
- "Moisturizing" (with the reference's own long-s ligature) and "Gentle exfoliation for sensitive skin"
- the gold arc and "PREMIUM BODY CARE SERIES"
- the divider, the double frame and "Net Wt. 4oz (113g) e"

The product is not mirrored. Its pixels equal the cut-out x 1.009 plus grain.

**Verdict: READY (after owner approval).** **Quality: about 80% of a professional studio product photograph** (up from about 70%).

**Prior defects:**
1. **Heavy flat drop shadow: fixed.**
   - There is now a tight contact (y about 1736–1740, falling to about 35% for 2–4 px).
   - Below it is a soft cast shadow: about 163 against cloth at 195–205 (about 80–83%), fading over about 150 px toward the lower right (x 1515–1680, y 1740–1890).
   - It points the same way as the star-anise and cinnamon shadows and has a similar density.
2. **Neutral label against a warm scene: fixed.** The plate's white point is now neutral: the brightest ribbon pixels are 247/246/244 (B/R 0.99) and the label paper is B/R 0.97. The linen (B/R 0.93) and the oak (0.82) are warm by material, not because of a cast.
3. **Perspective lip on the bottom edge: not fixed (accepted).** The pale bevel at y about 1700–1735 is still there. It is only visible at 100%.
4. **Paper grain too clean: not fixed.** The paper's high-pass SD is 2.35, against 2.2 before. It is minor at 100% and invisible at feed size.
5. **Edges: still clean** on all four sides. I found no halo or fringe (`soap_tl_2x`, `soap_tr_2x`, `soap_bl_2x`, `soap_br_2x`).
6. **Scale: still passes.**

**New defects:**
- **Minor: shadow now slightly too weak at feed size.**
  - Where: bar outline x 606–1520, y 927–1740.
  - Problem: at 1080 px the bar reads a little like a flat card laid on the cloth. The linen also shows no compression or fold response under a 2.5 cm bar.
  - Fix (optional): deepen the near-field part of the cast to about 75% for the first 20–30 px, keeping the long falloff.

## 2. HERO COFFEE: coffee_cocoa_v3 (reference everliv-cocoa-coffee-medium-roast.jpg; actual source bag-front.jpg)
**Authenticity: PASS.** These all match:
- EVERLIV arc, leaf/pulse mark, COFFEE, PURE CELLULAR VITALITY
- the FLAVOR / COCOA panel, MEDIUM ROAST with 3 of 5 dots, "Savory, Cocoa, Smooth"
- 100% ARABICA WHOLE BEAN, Net Wt: 12oz / 340g
- the side panel EVE… / COFFEE

The carton is not mirrored even though the scene was. Its pixels equal the cut-out x 0.951 plus grain, so it was not relit.

**Verdict: PROVISIONAL.** It is close, and two fixes would make it READY. **Quality: about 75%** (up from about 68%).

**Prior defects:**
1. **Side-panel lighting the wrong way round: fixed.** The mirrored plate now has its key light from the left: window at left, mug lit on its left, and the dish and mug shadows falling right. That matches the render's light left side panel and darker front.
2. **Colour too cool and flat: improved.** Label cream is B/R 0.89. Scene creams (mug glaze, dish rim) are B/R 0.76, which is partly material and partly the warm ambient light. At feed size the carton now sits in the scene acceptably. At 100% the label cream is still slightly cooler than the ceramics.
3. **Dashed fringe on the slanted right edge: mostly fixed.**
   - The upper slant (x 1420–1530, y 760–1000) is now clean (`coffee3_redge_slant_4x.png`).
   - A faint dashed tick line remains 2–5 px inside the edge at x 1490–1500, y 1290–1390 (`coffee3_redge_mid_4x.png`). It is luminance 161 against 182, so faint.
   - It is in the supplier render's own pixels (`cutout_cocoa_redge_4x.png`), so it is not a compositing error. It is minor and invisible at feed size.
   - Fix (optional): a 2 px alpha choke on that segment only.
4. **Cool blue-grey back-panel sliver: not fixed (genuine product).** It is at x about 830–880, y 790–1100 (`coffee3_gable_left_3x.png`). It still reads cool grey against the warm bokeh at 100% and faintly at 1080. Minor; leave it.
5. **Dark specks outside the edge: fixed.** An automated ring scan 1–12 px outside the matte found no dark components except the intended base contact line.
6. **Dark wedge beside the gable: fixed.** The background around the gable is clean (`coffee3_bg_around_gable.png`).
7. **Label softness: not fixed, and it cannot be fixed this way.** The cut-out is placed at 1:1 native resolution from `bag-front.jpg`. That is the render's own resolution, not a resampling loss. Fix: a higher-resolution supplier render, or accept it. Minor.
8. **Bean scale: unchanged, minor.** The beans are about 0.55–0.6 cm at the carton's scale, which is small.

**New defects:**
- **Major: no grounding beyond a 6 px contact line.**
  - Measured profile: the contact drops to about 67% for about 6 px, then returns fully to the table value with no falloff (`coffee3_base.png`).
  - Where: base x 800–1517, y 2290–2360. The cast shadow is missing to the right and behind, at x 1517–1800, y 2150–2360.
  - Problem: a 23 cm carton lit by a left window should throw a soft cast shadow to the right and back, and have ambient occlusion spreading 1–3 cm around the base. The mug and the dish both have this. Without it the carton looks set on top of the plate.
  - Fix: add a soft occlusion band (about 30–60 px wide, darkest at about 85%) along both bottom edges. Add a cast shadow polygon from the right edge toward the upper right (about 300–500 px long, feathered, about 85–90%). Multiply both onto the plate only.
- **Major at 100%, minor at feed size: clean-plate retouch residue on the table** just below the front face.
  - Where: x about 1080–1340, y about 2340–2390 (`coffee3_table_smear_3x.png`).
  - Problem: a mottled, posterised, speckled patch where the wood grain is lost. Its high-pass SD is 6.9, against 3.2 on the wood around it. At 1080 it reads as a pale smear under the carton.
  - Fix: re-inpaint with a grain-aware clone from the wood immediately left or right, or hide it under the new occlusion and cast shadow.

## 3. TEMPLATE A: tmpl_spa_charcoal_v2 (reference everliv-charcoal-soap.jpg)
**Authenticity: PASS.** These all match:
- "CHARCOAL" and "HANDCRAFTED SOAP"
- the three benefit lines ("With activated charcoal for a deep cleanse / Leaves skin feeling fresh and clean / Uplifting mint and tea tree scent")
- the gold arc and PREMIUM BODY CARE SERIES, Net Wt. 4oz (113g) e
- the black soap strip to the right of the label

It is not mirrored. Its pixels equal the cut-out x 0.978 plus grain.

**Verdict: READY (after owner approval)** as a template test. **Quality: about 78%** (up from about 60%).

**Prior defects:**
1. **Muddy brown drop shadow (blocker): fixed.**
   - There is a tight contact at y about 1704–1712.
   - The soft cast shadow is about 160 against stone at about 185–198 (about 82–85%). It fades over about 120 px below the bar (x 640–1520, y 1712–1830) and to the right (x 1515–1620).
   - I could see no stain at 1080 px or in the thumbnail.
2. **Neutral label against warm stone: fixed.** The ceramic dish is now B/R 0.94 against paper at 0.97. The travertine's warmth (B/R 0.80) is the material's own colour.
3. **Grain: not fixed (minor).** Paper SD is 2.34. It is invisible at feed size.
4. **Prop scale: improved, minor.** The oats now measure about 0.65–0.7 cm, against about 0.5 before. Real oats are about 0.8–1 cm, so this is close. The dish is still about 5 cm (x 1610–2160, y 1940–2540), which reads as a small trinket dish. Accept it, or regenerate the plate.
5. **Edges: still clean** (`spa2_tl_2x`, `spa2_tr_2x`, `spa2_bl_2x`, `spa2_br_2x`).

**New defects:**
- **Minor: a light bevel along the bar's left edge.** At x about 630–640, y 960–1700 there is a light bevel highlight. It is in the supplier render, so leave it.
- **Minor: the bar reads slightly flat at feed size.** This is the same note as for the soap. Optional fix: about 75% near-field cast.

## 4. TEMPLATE B: tmpl_plinth_hazelnut_v2 (reference everliv-hazelnut-coffee-medium-roast.jpg; actual source bag-front.jpg)
**Authenticity: PASS.** These all match:
- HAZELNUT and FLAVOR
- MEDIUM ROAST with 3 of 5 brown dots, "Citrus, Nutty, Maple Syrup"
- 100% ARABICA WHOLE BEAN, Net Wt: 12oz / 340g
- the brand block and the side panel

It is not mirrored. Its pixels equal the cut-out x 0.966 plus grain.

**Verdict: PROVISIONAL.** **Quality: about 74%** (up from about 65%).

**Prior defects:**
1. **Dark specks on the plain wall: fixed.** The ring scan found none outside the base contact line.
2. **Dashed line on the right gable edge (x 1375–1400, y 650–800): fixed.**
   - The upper right edge is clean (`plinth2_gable_tr_3x.png`).
   - What remains is the same faint source-render tick line as on the cocoa carton, at x 1387–1398, y 1150–1260 (`plinth2_redge_slant_3x.png`). It is slightly more visible here against the plain grey wall at 100%, and invisible at 1080. Minor.
   - A very faint darker line along the gable top (y about 641–645) is barely visible.
3. **Side panel lit the wrong way round: fixed.** The plate's key light is now from the left: the plinth casts its shadow to the right on the floor at x > 1780, y 2150–2450. That matches the render.
4. **Cool back-panel sliver: not fixed (genuine product).** It is at x about 745–790, y 650–1100 and reads as cool grey against the beige wall. Minor.
5. **Pale line inside the right edge: fixed.** The edge at x about 1410, y 1300–1950 is clean (`plinth2_redge_4x.png`).
6. **Label softness: not fixed.** It is the native resolution of the render. Same note as coffee item 7.
7. **Contact and scale: scale passes, contact regressed in look (see below).**

White balance is good: label cream B/R 0.90 and plinth top 0.90.

**New defects:**
- **Major: the contact reads as a drawn dark outline, with no ambient occlusion or cast shadow.**
  - Profile: it drops to 111 against stone at 170 (65%) for about 8 px, then is flat again within 12 px (`plinth2_base.png`).
  - On the plain light travertine this reads as a pencil line along x 695–1410, y 2148–2215.
  - There are small dark blobs at both bottom corners, at (695, 2148) and (1406, 2176) (`plinth2_base_l_3x.png`, `plinth2_base_r_3x.png`).
  - The plinth itself throws a clear shadow to the right, so the carton should too.
  - Fix:
    1. Reduce the line to about 80% darkness.
    2. Remove the corner blobs.
    3. Add occlusion spreading 30–60 px.
    4. Add a soft cast shadow toward the right and back on the plinth top (about 85–90%).

---

## Summary
| Image | Authenticity | Verdict | Quality | Remaining to fix |
|---|---|---|---|---|
| Soap OMH v5 | PASS | READY (after owner approval) | ~80% | Optional: slightly stronger near-field shadow |
| Coffee Cocoa v3 | PASS | PROVISIONAL | ~75% | Major: add occlusion and cast shadow. Major at 100%: retouch the table smear at x 1080–1340, y 2340–2390 |
| Template A, spa charcoal v2 | PASS | READY (after owner approval) | ~78% | Minor: prop scale (dish), paper grain |
| Template B, plinth hazelnut v2 | PASS | PROVISIONAL | ~74% | Major: contact line reads as an outline with corner blobs; add occlusion and cast shadow |

**Status of the shared defects from round 2:**
- **White balance: fixed** in all four.
- **Soap drop shadows: fixed.**
- **Carton side-panel lighting: fixed** by mirroring the plates. The product pixels are verified untouched.
- **Matte specks and dashes: fixed.** The only residue is faint ticks that are in the supplier render itself.

What is left applies only to the cartons: one shared grounding model (contact plus occlusion plus cast shadow), and one retouch on the cocoa table. With those done, I expect both cartons to reach about 80% and READY.

**Process note.** The coffee build reports and the QA reference should name `library/<sku>/<sku>--bag-front.jpg` as the source render. The catalog front JPG is a different render whose side panel is shaded differently. Comparing against the catalog JPG gives a false "relit/recoloured side panel" signal.
