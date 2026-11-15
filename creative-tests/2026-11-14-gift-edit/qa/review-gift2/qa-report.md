# EverLiv composite QA — independent review (2026-11-14)

Reviewer: independent visual QA (did not build these). All coordinates are in the 2160x2700 frame. Crops and views are saved in /home/claude/review-gift2/.

## How I checked
- I viewed each frame at 1080 wide (`*_1080.png`) and at 400 px (`thumbs_sheet.png`).
- I cropped every product edge at 100%, and some at 4x nearest-neighbour (`*_4x.png`).
- I checked label authenticity two ways: by eye at 100% against the supplier front, and by template matching against the supplier JPG. For coffee I added an affine ECC alignment and a difference map (`coffee2_label_vs_ref_diff_x4.png`): ECC is 0.99, the transform is almost identity, and the only differences are along edges, from softening and grain. Label NCC: soap 0.97, charcoal 0.93, cocoa 0.89, hazelnut 0.85. The lower coffee scores come from softening (about 80% of source sharpness), not from redrawn content.
- I measured shadow profiles, white balance and high-pass noise (product compared with scene).
- I compared each scene with its stand-in version (`*_scene.jpg`) to work out the intended light direction.

## Defects shared by all four (a pipeline problem, not a per-image one)
- **White balance.** Product whites are neutral and the scenes are warm. Label paper measures B/R ≈ 0.97. Scene whites measure B/R ≈ 0.87–0.88 (soap ribbon, spa ceramic dish). This is the main reason the products look pasted in. Do not tint the product on its own, because that conflicts with the no-recolour rule. Instead apply one global grade to the whole finished frame, or neutralise the scene plate before compositing.
- **Drop shadows (soaps).** The shadow is a fixed "drop shadow": it falls to about 40% of the surface brightness, stays flat for about 90 px (about 0.9 cm at this scale), then fades over about 100 px. The props in the same scenes have faint, soft shadows. The shadow should be a tight contact occlusion (2–6 px, about 50–60% darkness) plus a very soft, light cast shadow (no darker than about 80–85% of the surface), pointing the same way as the prop shadows.
- **Cartons (coffee).** The cut-out keeps the studio lighting. The left side panel is the brightest face and the white back-panel sliver at the gable reads cool blue-grey. In both stand-in scenes the left face is the shaded face.

---

## 1. HERO SOAP — soap_omh_v4
**Authenticity: PASS.** All label text, the gold arc, "PREMIUM BODY CARE SERIES", the divider line, "Net Wt. 4oz (113g) e" and the logo match the supplier front. Nothing has been redrawn, recoloured or dropped.
**Verdict: PROVISIONAL.** **Quality: about 70% of a studio product photo.**

1. **Major. Shadow far too dense and flat.** It runs along the right edge (x 1515–1620, y 1150–1760) and below the bar (x 640–1520, y 1740–1870), at RGB about 83/78/74 against cloth at 206/193/184. The star anise (x 1770–2120, y 860–1200) and the cinnamon (x 1810–2160, y 1150–1780) only have faint shadows, so the bar looks lifted, with a "Photoshop drop shadow" look. *Fix:* use the contact plus soft cast shadow described above, and match the darkness of the anise shadow.
2. **Major. Label too neutral against a warm scene.** Paper (x 700–900, y 1170–1260) is 236/235/230; the ribbon is 216/201/190. *Fix:* global warm grade of the frame, or neutralise the plate.
3. **Minor. Perspective.** The bottom edge (y about 1700–1735) shows a pale bevel or lip from the supplier's slightly elevated front camera. The props are shot straight down, so the bar reads as slightly tipped. You only notice this at 100%. *Fix:* accept it, or crop the lip under the shadow.
4. **Minor. Grain.** Flat label paper has a high-pass SD of 2.2; the scene's flat wood is 4.9–6.9. The paper looks slightly cleaner than its surroundings. *Fix:* add about 1–1.5 more luminance grain on the product only.
5. **Edges: clean.** I found no halos, fringes or leftover background on any of the four sides at 100%.
6. **Scale: passes.** The bar is about 916 px wide (about 8.5 cm, about 108 px/cm). That gives star anise about 3.2 cm, cinnamon about 1.2 cm across, and orange slice about 8.9 cm, which is at the large end but believable.

## 2. HERO COFFEE — coffee_cocoa_v2
**Authenticity: PASS.** The label matches the reference exactly: "COCOA", Medium Roast with 3 of 5 dots, "Savory, Cocoa, Smooth", 100% Arabica Whole Bean, Net Wt 12oz / 340g, and the side panel "EVE…/COFFEE".
**Verdict: PROVISIONAL.** **Quality: about 68%.**

**Status of the v1 defects:**
- **Grain: fixed.** The product's flat panel is 2.4; the scene measures 2.3–2.6.
- **Contact shadow: improved.** v2 adds a dark contact line along the bottom edges (x 650–1360, y 2290–2360). It is acceptable, but still thin and uniform.
- **Right-edge stair-stepping: not fixed.** The straight lower edge (x about 1355–1360, y 1450–1900) is clean in both v1 and v2. The slanted section at x 1345–1360, y 1300–1450 still shows dashed or serrated matte ticks, and v2 is the same as v1 there (`coffee1_redge_4x.png` / `coffee2_redge_4x.png`, first tile).

**Defects:**
1. **Major. Lighting on the side panel is the wrong way round.** The stand-in has its left face much darker than its front (about 120 vs 210 luminance). The composite's left side panel (x 650–830, y 1100–2290) is brighter than the front (183/164/141 vs about 181/150/114 on the lower front). The carton is lit from a different direction than the scene. *Fix:* apply a luminance-only gradient to the side-panel region, dropping it about 25–35%. This is a lighting multiply, not a recolour, so record it in the build notes.
2. **Major. Overall colour too cool and flat for the amber bokeh and warm window light.** *Fix:* global warm grade.
3. **Major (minor at feed size). Dashed matte fringe on the slanted right edge** at x 1345–1360, y 1300–1450. *Fix:* rebuild the alpha on diagonal edges with a sub-pixel or feathered matte (for example a 0.7 px feather plus a 1 px choke), then decontaminate the edge colour.
4. **Minor. Cool blue-grey back-panel sliver** at x 720–745, y 790–1110. It is in the supplier render, but it reads blue in this warm scene. *Fix:* the global grade mostly solves it; otherwise leave it, because it is genuine product.
5. **Minor. Dark specks just outside the edge**, about 8–10 px each, at (645, 1965) and (1371, 1650). The same specks turn up around the same cut-out in template B, so they are probably in the matte. *Fix:* clean the cut-out alpha once at the source, then rebuild every scene that uses it.
6. **Minor. Dark wedge in the background** just left of the gable, at x 660–695, y 960–1035. It is probably left over from inpainting around the stand-in silhouette, and reads as a notch beside the carton. *Fix:* clone or inpaint from the surrounding bokeh.
7. **Minor. Label slightly soft** (about 80% of source sharpness). Letter edges at 100% are a little softer than the wood grain nearby. *Fix:* resample with Lanczos and apply light unsharp masking (radius 0.6, amount about 40%).
8. **Scale: passes.** The front face is about 540 px wide, so about 8 cm. That makes the carton about 23 cm tall, the bean dish about 7.8 cm across, and the beans about 0.7–0.8 cm, which is slightly small. The mug, about 7 cm and set further back, is plausible.

## 3. TEMPLATE TEST A — tmpl_spa_charcoal_test
**Authenticity: PASS.** "CHARCOAL", the three benefit lines, the gold arc, Net Wt and the black soap strip to the right of the label all match the supplier front.
**Verdict: REJECT as built.** The template idea is fine, but the shadow treatment has to be redone before this could post. **Quality: about 60%.**

1. **Blocker for publishing. Muddy brown drop shadow** below and to the right of the bar, at x 640–1700, y 1700–1900. Its core is 83–97/74–85/64–73 on stone of about 205/181/155. It is a flat smudge over the travertine pores, it reads as a dirty stain at 1080 px, and you can still see it in the thumbnail. The eucalyptus (x 150–750, y 2000–2500) and lavender cast only faint shadows. *Fix:* the shadow rebuild described above. Because the bar is black, keep the shadow smaller and lighter than the bar so the bar still separates from it.
2. **Major. Neutral label on warm stone** (label 229/228/223; ceramic dish 196/186/170). *Fix:* global grade.
3. **Minor. Grain.** Paper SD is 2.2; stone ranges from 7.7 to 25 because of its texture. Fine at feed size, slightly clean at 100%.
4. **Minor. Prop scale.** The bar is 902 px wide (about 8.5 cm, about 106 px/cm). Oat flakes come out at about 0.5 cm, which is small (real ones are about 0.8–1 cm). The dish (x 1610–2160, y 1940–2540) comes out at about 5–6 cm, a very small dish. *Fix:* scale the props up or regenerate the plate with larger oats.
5. **Edges: clean.** I found no halos at 100% on any side.

## 4. TEMPLATE TEST B — tmpl_plinth_hazelnut_test
**Authenticity: PASS.** "HAZELNUT", "Citrus, Nutty, Maple Syrup", Medium Roast with 3 of 5 dots and Net Wt 12oz / 340g all match the reference.
**Verdict: PROVISIONAL.** **Quality: about 65%.**

1. **Major. Dark specks visible at 1080 px on the plain wall:**
   - (1468, 1520), right edge
   - (748, 1833), left edge
   - (748, 1988), left edge
   - (about 1465, 1945), right edge

   This is the same cut-out problem as coffee item 5, but here it shows against a clean background. *Fix:* clean the matte.
2. **Major. Dashed dark matte line along the right gable edge** at x 1375–1400, y 650–800, plus a faint line along the gable top at y about 640–650. It is clearly visible against the plain wall at 100%. *Fix:* the same alpha rebuild as coffee item 3.
3. **Major. Side panel lit the wrong way round.** The scene's cast shadow falls to the left on the plinth (x 600–780, y 2130–2230), so the key light is on the right. The left side panel (x 750–950) is still the brightest face. *Fix:* the same luminance gradient as coffee item 1.
4. **Minor. Cool blue-grey back-panel sliver** at x 800–840, y 640–1100. It stands out more against the beige wall than in the coffee scene. *Fix:* global grade.
5. **Minor. Thin pale line just inside the right edge** at x about 1460, y 1350–1950. *Fix:* choke the alpha by 1 px.
6. **Minor. Label softness** (about 79% of source). Same fix as coffee item 7.
7. **Contact and scale: pass.** The carton stands about 60 px behind the plinth's front edge, has a contact line, and does not overhang. The scale is consistent with the stand-in footprint.

---

## Summary
| Image | Authenticity | Verdict | Quality | Main things to fix |
|---|---|---|---|---|
| Soap OMH v4 | PASS | PROVISIONAL | ~70% | Heavy drop shadow; neutral white balance in warm scene |
| Coffee Cocoa v2 | PASS | PROVISIONAL | ~68% | Side-panel lighting reversed; stair-step on slanted edge still there; specks; WB |
| Template A, spa charcoal | PASS | REJECT (as built) | ~60% | Muddy brown shadow; WB; small props |
| Template B, plinth hazelnut | PASS | PROVISIONAL | ~65% | Matte specks and dashed gable line visible on plain wall; side-panel lighting; WB |

None of the four is ready to publish. The label work is faithful in all four. The remaining problems are in the compositing: one shared matte cleanup for the coffee cut-out, one shared shadow model, one global white-balance grade, and a luminance-only side-panel correction for the cartons. Doing those four would probably bring all of them to about 80–85%.
