# Photoreal product-composite tests — 2026-11-14 (INTERNAL, NOT FOR PUBLICATION)

This folder archives every iteration, source, prompt, tool and QA finding from the Nov 14 photoreal tests.
- Nothing here is approved for publication.
- Rejected images are kept on purpose, as creative references and QA examples.
- Do not overwrite anything. New tests go in a new dated folder.

## Status
| Product | Best image | Independent verdict |
|---|---|---|
| Peptide Eye Serum | `composites/serum15-2160x2700.png` | Fixable, about 70–75% of studio standard. It fails on two counts: label and cap warmed to cream, and a residual elevated-camera mismatch. |
| Collagen Oral Strips | `composites/tin12-2160x2700.png` | Reject, about 45–55%. The tin reads as flat (no thickness or edge response), the colour drifts, and its shadow is grey. |

**Owner direction (Nov 14, 17:43):** stop patching these two. Fresh tests start once the supplier packaging assets arrive (label artwork, dimensions, materials, angles, 3D models).

## Lineage
The serum5–15 and tin5–12 composites, with QA sheets and reports, are in `composites/` and `qa-sheets/`.

| Iteration | Scene | Notes |
|---|---|---|
| serum5–6 | Gemini, elevated camera (`serumscene.jpg` / `serumplate.jpg`) | Round 1. Failed realism. |
| serum7–9 | Gemini, eye-level attempt (`serumE.jpg` / `serumEplate.jpg`) | serum8 added `--wrap`. serum9 tested a 9% reduction on that scene. |
| serum10–15 | Gemini, low camera (`serumL.jpg` / `serumLplate.jpg`) | serum13 added `--ring`. serum15 added `--grad`, with label sharpness at 91%. |
| tin5 | ChatGPT flat lay (`tinscene.png` / `tinplate_0.png`) | Rejected for perspective. |
| tin6–9 | Gemini, upright tin (`tinUgem.jpg` / `tinUplate.jpg`) | tin7 and later use `cutouts/collagen-front-cutout-v2.png`, because the library cutout is degraded. tin8–9 tested `--plane` light. |
| tin10–12 | Gemini, lower camera, owner's preferred composition (`tinL.jpg` / `tinLplate.jpg`) | tin12 measures the stand-in footprint directly. |

**Alternative scene:** `tinUgpt_0.png` is the ChatGPT upright-tin scene. It was kept for comparison but not used.

## Gemini prompts (EverLiv Workspace account, support@everliv.life)

**Eye Serum scene (serumL):**
> Create a photorealistic vertical 4:5 product photograph for a premium skincare brand. Camera: LOW, EXACTLY AT EYE LEVEL with the middle of the object, lens perfectly level (no downward tilt), 85mm, so the countertop surface is seen almost edge-on (only a thin sliver of the counter top visible) and round objects show NO visible top ellipse. Subject: a plain matte off-white cylinder with a flat top, about 3.5 times taller than it is wide, standing upright on a warm beige travertine bathroom counter, slightly left of centre, occupying about 35% of the frame height. Lighting: large SOFT diffused window light from camera-left and slightly front, gentle gradual falloff, soft short shadow, no hard sun, no strong highlights. Right side: a relaxed woman's hand resting flat on the counter, fingertips about 3 cm away from the cylinder, not touching, natural five fingers, cream knit sleeve. Background: softly out-of-focus warm neutral wall, a small eucalyptus sprig in a ceramic vase far behind. Calm, editorial, natural light, real photograph, no text, no logos.

**Collagen scene (tinL):**
> Create a photorealistic vertical 4:5 editorial still-life photograph. Set: a warm peach-pink textured plaster wall; a smooth cream sculptural arch (an upside-down U shape) standing on top of a peach plaster plinth block; a peach silk cloth draped over the plinth's left edge; a small shallow clear glass dish on the right. Subject: a flat, thin, square silver metal tin with rounded corners, standing UPRIGHT on its edge, facing the camera squarely, centred in front of the arch, about 27% of the frame height. CAMERA: exactly level with the centre of the tin, lens perfectly horizontal (no downward tilt), 100mm, so the top surface of the plinth is seen edge-on (not visible) and NO top or lid surface of the tin is visible, only its flat front face. LIGHT: soft warm late-afternoon light from camera-left and slightly in front, evenly lighting the front of the tin with a gentle falloff toward the right; a soft-edged palm-leaf shadow falls on the wall in the upper left only, behind the objects, not crossing the tin. Soft natural shadows, no harsh contrast. Real photograph, no text, no logos.

**Clean plate (same chat, both products):**
> Edit this exact image: remove the [stand-in] completely and show the [background] exactly as they would look without it, including removing its shadow. Change NOTHING else: same framing, camera, light, objects, colours and grain, pixel-aligned.

The prompts for the earlier scenes are recorded in the Marketing project docs (eye-serum-visual-test, three-format-test, gemini-access-and-test-protocol).

## Key QA lessons
1. **Light the product; never tint the packaging.** A scene-colour tint on the product reads as a packaging colour change. Owner rule (Nov 14): do not change packaging colours to fit scene lighting.
2. **Generators don't fully level the camera.** Gemini lowered it when asked but left a 10–20° elevation. A frontal render therefore always shows a perspective mismatch.
3. **Match the scene's focus.** Shallow depth of field around a razor-sharp render reads as pasted.
4. **Auto-detection misses low-contrast bases.** It stopped short on a white stand-in on beige and a silver tin on peach. Measure the footprint from the scene–plate difference instead.
5. **Supplier assets are the binding constraint.** Flat, orthographic, evenly lit renders cannot show thickness, edge highlights, a top face or label wrap.
6. **Route to the target standard:** original label artwork mapped onto dimensionally accurate 3D package models, independently fidelity-checked. Approved for internal testing only.

## Contents
| Folder | What it holds |
|---|---|
| `scenes-and-plates/` | Generator scenes and clean plates |
| `composites/` | All iterations at 1080 and 2160, plus metric reports |
| `qa-sheets/` | Feed, 100% and thumbnail sheets, and crops |
| `reviews/` | Independent reviewers' crop evidence (review-cp*) |
| `tools/` | Compositor (`cp_composite.py` v5.1, with `--wrap`, `--ring`, `--grad`, `--plane`), run scripts and the v4 pipeline |
| `cutouts/` | Collagen front cutout v2, rebuilt from `collagen-strips--front.png` (the library's `--front-cutout.png` is degraded) |
| `earlier/` | Same-day three-format test, ChatGPT-vs-Gemini head-to-head, and the Eye Serum v1–v2 pipeline outputs |
