# Holiday Gift Edit: hero pair, scene templates and cut-out kit (Nov 14, 2026)

Internal production archive. Nothing here has been published, scheduled or uploaded to Shopify.

## Method (authentic-asset compositing)
1. **Product pixels** come only from the supplier's own 2048 px front render (`/catalog/fronts`), cut out with `scripts/cutout.py`. Interior pixels are byte-identical to the source; only the edge band is decontaminated. See each `cutouts/*.json` report.
2. **Scenes** are AI-generated environments (Gemini, EverLiv Workspace account support@everliv.life) containing a *blank* stand-in block of the right shape. The generator never sees or draws the packaging.
3. **Clean plates** are the same scene with the stand-in removed (Gemini edit in the same chat).
4. **Compositing** with `scripts/compose_authentic.py`: one uniform scale (never above 1.0x of the cut-out), one uniform exposure scalar (0.85–1.08), luminance-only grain, no tint or colour shift. The shadow is either re-mapped from the stand-in or synthesized from the product's own silhouette. The report json records label sharpness and chroma shift against the cut-out.

## Contents
| Folder | What |
|---|---|
| `scenes/`, `plates/` | Scene with stand-in, and clean plate, for each template |
| `masks/` | Stand-in rectangles (numpy bool, 1856x2304 scene pixels) |
| `cutouts/` | 6 soap cut-outs (v2) + 4 coffee cut-outs (v2), each with a QA json |
| `composites/` | Current candidates: `soap_omh_v4`, `coffee_cocoa_v2`, template tests |
| `rejected/` | Earlier rejected/superseded versions, kept for the record |
| `scripts/` | `cutout.py` (v2, fixed label-end growth), `cutout_v1_buggy.py`, `compose_authentic.py` (v2: `--feather`, `--grain-sd`, `--grain-on-product`, `--contact`), `compose_authentic_v1.py` |
| `qa/` | Independent review reports and crops |

## Scene templates
| ID | File | Use | Stand-in (scene px, x0–x1, y0–y1) | Light | Recommended shadow |
|---|---|---|---|---|---|
| T1 Gift flat lay | `gift2_*` | Top-down soap, holiday (orange, star anise, cinnamon, pine, linen ribbon) | 487–1339, 834–1448 | Neutral daylight, upper left | `--topdown --fill=1.14 --scene-wb=0.6 --no-standin-shadow --synth-shadow=40,50,45,0.17` |
| T2 Travertine spa | `spa_*` | Top-down soap, everyday (lavender, oats, eucalyptus, waffle towel, ceramic dish) | 482–1365, 853–1433 | Neutral daylight, upper left | `--topdown --fill=1.1 --scene-wb=0.6 --no-standin-shadow --synth-shadow=40,50,45,0.17` |
| T3 Limestone plinth | `plinth_*` | Upright coffee carton, minimal (olive sprig vase, warm-neutral wall) | 637–1266, 446–1900 | Mirrored so light comes from the left | plate `plinth_plate_clean.png`; `--mirror --scene-wb=0.6 --no-standin-shadow --edge-choke=1 --feather=1.3 --grain-on-product=1.0 --contact=0.25 --ground-shadow=280,0.18,26,0.25` |
| T4 Holiday kitchen | `coffeeholiday_*` (= `g_b`/`g_c`) | Upright coffee carton, holiday (bokeh lights, mug, beans, gift box) | see `standin_coffee.npy` | Warm ambient; mirrored so key light comes from the left | plate `coffeeholiday_plate_clean.png`; `--mirror --scene-wb=0.5 --no-standin-shadow --edge-choke=1 --feather=1.3 --grain-on-product=1.0 --grain-sd=2.4 --contact=0.25 --ground-shadow=320,0.2,26,0.27`; plate cleaned with `clean_plate.py g_c.jpg standin_coffee.npy out 40 10 1940` plus one speck at (601,2068)` |

`gift1_*` (first gift flat lay) is retired: its block stand-in was about 2x real soap scale.

## Revision history (first independent review → fixes)
- Scene white point moved toward neutral (`--scene-wb`); the product is never tinted.
- Soap: the deep fixed drop shadow is replaced by a soft, light cast shadow (≥ 83% of surface brightness) plus a tight contact shadow.
- Coffee: scenes mirrored so the key light comes from the left, matching the supplier render's lit left panel. The product itself is never flipped or relit.
- Clean plates: generator residue around the removed stand-in is inpainted (`clean_plate.py`, scene only).
- Coffee matte choked by 1 px (`--edge-choke=1`) to remove the render's dashed dark outline on the slanted gable edges.
- Contact-shadow bug fixed: stray edge columns had produced dark specks mid-height on the carton edge.
- Second review → cartons: the hard drawn contact line is replaced by `--ground-shadow` (soft base shading + a cast shadow laid on the surface, away from the key light, fading out in front of the base). The cocoa table retouch is limited to above the table line, so the wood grain is untouched.

## Known limits
- Coffee render is a ~20° three-quarter view, so coffee belongs in eye-level upright scenes only. Soap render is a face-on view, so soap belongs in top-down scenes (or upright, propped, eye-level).
- Clean plates regenerate the fabric/stone texture slightly (median difference 5–18 levels). The plate is therefore used for the whole frame, not patched into the scene.
- Real physical dimensions are not published by the supplier; scale is set against props of known size.

## Scene prompts (summary)
All: photorealistic vertical 4:5 editorial product photograph, blank off-white stand-in of the stated shape and size, no text, no logos, no packaging. Clean plate: "Edit this exact image: remove the [stand-in] completely and show the [surface] exactly as it would look without it, including removing its shadow. Change NOTHING else: same framing, camera, light, every object, colours and grain, pixel-aligned."
- T1: exactly top-down; frame about 20x25 cm; blank bar 9x6.5x2.5 cm at about 45% of frame width; dried orange slice ~6 cm lower left; star anise ~3 cm and cinnamon stick ~8 cm at right; 1.5 cm linen ribbon along the top; small pine sprig bottom right; oat linen over pale oak; soft neutral daylight from a large north-facing window upper left, white-balanced (not warm, not golden).
- T2: exactly top-down travertine; blank bar stand-in; lavender, oats, eucalyptus, waffle towel, small ceramic dish; neutral daylight.
- T3: eye level; limestone plinth; blank kraft tent-top carton stand-in; olive sprig in stoneware vase; warm-neutral plaster wall; soft window light from left.
- T4: eye level; wooden kitchen counter; blank tent-top carton stand-in; mug, coffee beans, cinnamon, pine, gift box; bokeh string lights.
