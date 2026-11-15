# QA review: coffee_cocoa_v5 (2160x2700), compared with v4

Reviewer: independent, strict. Method: v5/v4 difference map, template match against the supplier render, 100% and 2–4x crops, a 1080 downscale and a 216x270 thumbnail. Crops are in `/home/claude/review-gift5/`.

## Authenticity: PASS
- **Match to source:** NCC 0.948 on the central 70% of the carton against `cocoa-coffee-medium-roast--bag-front.jpg` at scale 1.0, unrotated. The mirrored NCC is 0.40, so the carton is not flipped.
- **Exposure:** one uniform scalar. Per channel B/G/R is 0.943/0.944/0.946, so about 0.944 with no tint. The chroma residual SD is 1.0.
- **Residual:** luminance grain only (robust SD 2.4). The low-pass residual inside the carton is within ±0.7 levels, including the bottom 300 px, so there is no painted shading on the product. The only outliers are anti-aliased silhouette edges.
- **Unchanged since v4:** inside the carton, v5 is identical to v4. The edit touched only the table.
- **JSON still wrong:** `exposure_scalar` says 0.954 but I measure 0.944. Correct the field.

## Verdict: READY (publishable after owner approval)
**Quality: about 81%** of a professional studio product photo (v4 was about 76%).

## v4 defects
| # | Defect | Status | Evidence |
|---|---|---|---|
| A | Hard seam at y 2359/2360, x 1000–1800 | **FIXED** | The largest row-mean step in x 1000–1800 dropped from 5.4 to 1.2 levels. The per-column step at y 2359 is gone; the remaining steps of about 6 levels are the carton's own bottom edge. No line is visible at 100% (`cocoa5_seam_100.png`). |
| B | Stippled pale patch with no grain, x 1000–1330, y 2340–2392 | **FIXED** | Continuous wood grain now runs under the front face (`cocoa5_smear_2x.png`). High-pass SD is 10.8 there vs 11.0 in reference wood. Mean luminance is 115 vs 117 nearby, so it is no longer a bright strip. Best match against the rest of the table is 0.48 or less, so there is no visible clone repeat. |
| B2 | Front-edge occlusion clipped | **FIXED** | The occlusion now peaks at about 0.85–0.90 of the open table 10–25 px below the edge and fades out by about 50 px. At 1080 the carton reads as sitting on the table (`cocoa5_1080_base_2x.png`). |
| C | White speck at (1462, 2424) | **FIXED** | The peak there went from 197 to 118, which is the table level (`cocoa5_speck_4x.png`). |

## Fresh pass
- **Edges at 100%:** top, left, right and both bottom corners are clean, with no halo or fringe. At y 1300 the right edge steps straight from about 180 to 220. Crops: `cocoa5_top_100.png`, `cocoa5_edges_2x.png`, `cocoa5_botleft_2x.png`, `cocoa5_botright_2x.png`.
- **Shadows and grounding:** good. The cast shadow falls back and to the right, the same way as the mug and dish shadows. The bottom-left corner has a natural dark contact (about 70 against a table of about 90).
- **Colour:** the carton is neutral to slightly cool against warm bokeh light. It is plausible and not distracting.
- **Feed size (1080):** the label is readable ("COCOA", "Net Wt 12oz / 340g"). The published 1080 matches a clean downscale (MAD 0.7).
- **Thumbnail (216x270):** the carton and the word COCOA read clearly. The composition and hierarchy hold.
- **Scene:** no new artifacts found in the props, background, bokeh or table.

## New defects
None blocking.

## Carried over (accepted, minor)
These are native to the source render and must not be retouched:
- tick line at x about 1490–1500, y 1290–1390
- cool sliver on the back panel along the left edge
- native label softness

Also carried over: the beans are small relative to the carton.

## Advisory (not visual)
The printed tagline "PURE CELLULAR VITALITY" is native to the pack, but it should go through the claims and compliance check before any paid use.

## To do before publishing
- Owner approval.
- Correct the JSON `exposure_scalar` (0.944).
- The source path is not recorded in the v5 JSON. Add it as `library/cocoa-coffee-medium-roast/cocoa-coffee-medium-roast--bag-front.jpg`.
