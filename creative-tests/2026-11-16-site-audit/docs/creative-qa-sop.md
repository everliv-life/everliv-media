# EverLiv Creative QA — Standard Operating Procedure (v7, 2026-11-15 late: supplier-verified packaging facts)

Owner directives:
- **Do not ask Jeff to approve creative that has not been independently challenged, tested and verified.**
- **QA passing does not mean the creative is good enough.** Clean execution is not strong creative direction.
- **EverLiv creative must be accurate, technically polished, visually distinctive and genuinely engaging.** All four are required; none can be traded off against the others.
- **The objective is premium, believable commercial photography that customers can trust.** Attractive AI imagery alone does not meet it.
- **Target standard (Nov 14 PM): genuine luxury product photography, not a product image pasted onto an AI-generated background.**
- **NEW (owner, Nov 14 evening): every product must look like the actual EverLiv product, not a believable approximation. Physical packaging is established from authentic supplier references BEFORE any creative production (section I).**

This SOP applies to every Reel, TikTok, Short, Story, carousel, static post, ad, educational graphic, AI-assisted creative and landing-page visual. It applies whichever tool is used: ChatGPT, Gemini, 3D software, compositing or anything else.

## 1. Pipeline
**PACKAGING PROFILE CHECK (section I)** → DRAFT → INTERNAL QA → CORRECTIONS REQUIRED → QA PASSED → INDEPENDENT CREATIVE REVIEW → AWAITING OWNER APPROVAL → APPROVED → SCHEDULED → PUBLISHED

- **No product imagery is generated, composited or rendered until the product's Packaging Reference Profile has been checked and the authenticity gate (I.3) is recorded for that brief.**
- A piece cannot jump from DRAFT to AWAITING OWNER APPROVAL.
- **All gates (section 2) must pass, plus the independent review (section 3),** before a piece reaches AWAITING OWNER APPROVAL.
- **A missed numeric target is a failure, never an approval.** Example: label sharpness of 81% against an 85% target fails.
- **Stop-patching rule:** if a composite needs more than one corrective pass on the same structural problem (scale, pose, anatomy, shadow geometry, perspective, packaging geometry), stop patching. Re-plan from the start around the real product's documented geometry. Rejected images are archived as references, never deleted or overwritten.
- A failed gate means CORRECTIONS REQUIRED (fixable) or BLOCKED (needs an outside answer: supplier, Restructuring or owner).
- Only Jeff grants APPROVED, until he delegates in writing. Nothing is scheduled just because it is in the calendar.
- A first cut or storyboard sent for *direction* feedback is labelled as such, with its gate status.
- **No large batch** until the packaging-fidelity method (section H) is validated on one product.
- **Tracker:** the Calendar tab.
  - Columns R–AD hold IDs, verification and status.
  - AE holds Brand QA.
  - AF holds the Creative QA score.
  - AG holds the variety check.

## 2. The gates
| Gate | Question | Pass condition |
|---|---|---|
| **Product authenticity (pre-production)** | **Is the packaging established from authentic references, and can this composition carry it honestly?** | **Section I.3 recorded before generation; any unsupported geometry = BLOCKED or safer composition** |
| Technical | Is it correctly produced? | Section A checks all pass |
| Factual | Is it truthful and verified? | Section B; any supplier gap = BLOCKED |
| Brand / product fidelity | Does it represent EverLiv and the real product properly? | Section C, including label sharpness ≥ 85% of the source, packaging colour true to source, and no packaging defect |
| **Photographic realism** | **Does it look genuinely photographed, with no visible evidence of compositing?** | **Section C.7; perspective, light, contact, focus and material response all consistent at 100%, feed and thumbnail size** |
| **Human anatomy & interaction** | **Do people and hands look real and behave believably?** | **Section G; any conspicuous error blocks publication, even if the label passes** |
| Creative | Is it actually compelling? | Independent review ≥ 35/50, with hook ≥ 4, visual interest ≥ 4 and nothing below 3; variety check passes |
| Customer | Is it clear, relevant and trustworthy? | Section D; no blocking clarity or trust issue |

### A. Technical and visual
| Check | How |
|---|---|
| Export is 1080×1920 at 30 fps, H.264, yuv420p (video); 1080×1350 (feed) | [auto] `qa_export.py` / `qa_still.py` |
| Every frame decoded; blank or flat frames flagged | [auto] `qa_export.py` |
| Text inside the safe box, including animation offsets | [auto] per-frame registration |
| No sliced letters in label crops; annotations never overlap printed text | [auto] `check_crop()`; [manual] 100% crop |
| No two text blocks visible in the same zone at once | [manual] fade-window timeline check |
| Nothing too small at phone size (body text ≥ 46 px at 1080 wide) | [manual] 390 px phone sheet |
| No compositing artifacts: halos, stand-in remnants, ghost ledges, patch edges, seams | [manual] 100% crops around the whole product and every edited region |
| Correct file and version | Versioned filenames in the tracker |

### B. Product and factual accuracy
- Trace every product statement to the Product & Claims Library, the Supplement Facts panel or the live description.
- Check internal consistency: serving vs amount vs ingredients, net weight, and elemental vs compound amounts.
- Front-label structure/function claims are never edited. Featuring the package prominently requires supplier substantiation on file.
- If anything is uncertain, the piece is BLOCKED.

### C. Genuine product presentation and fidelity
1. **Product hero:** the complete authentic container, as the visual anchor.
2. **Compositing (v4):** the authentic supplier asset is scaled once to its final pixel size, light-only integration, at final resolution. Never warp, redraw, blur or sharpen the label. (Exception: section H, internal testing only.)
3. **Fidelity gate:**
   - Logo, typography and proportions within 1% of the source; no invented text.
   - **Label sharpness ≥ 85%** of the source at the same width.
   - **Packaging colour true to the source.** Measure the RGB of a flat label area against the source. **Never tint or recolour packaging to suit scene lighting (owner, Nov 14).** Scene colour may appear only as physically correct reflections, edge bounce and shadows; label inks and substrate keep their authentic colour.
   - **Packaging geometry matches the Packaging Reference Profile:** shape, cap or closure, seams, edges and proportions. Compare the silhouette against the supplier render at matched scale.
   - Realistic edges, reflections and contact shadows.
   - Product recognizable at thumbnail size.
4. **Scale:** the product is believable against hands and nearby objects (Eye Serum 30 ml: about 10 × 3 cm).
5. **Ingredients and contents:** no ingredient imagery that isn't the product's actual contents. Translucent packs (for example the gummy bottle) must show the real contents.
6. **Never** fabricate packaging, invent geometry or a comparison product.
7. **Photographic realism checks:**
   - The camera angle of the product matches the scene's. A front-on product with no top face must not sit in a scene seen from above.
   - Light direction and falloff on the product match the scene.
   - Material response is believable: thickness, edge highlights, metal or plastic behaviour.
   - Contact and cast shadows are consistent with the scene's light, and shadow colour is consistent with the surface.
   - Product focus is consistent with the scene's depth of field at the product's plane.
8. **Label finish (supplier-verified Nov 15):** every Supliful label is **high-gloss polypropylene (BOPP)**. Matte, metallic, foil and pearlescent finishes are not offered.
   - Never depict or describe a label, band or panel as matte, foil, metallic or pearlescent.
   - Gold or colour accents (for example the soap band corner or a capsule series band) are **printed**, not foil.
   - Gloss is never painted onto authentic render pixels. Under soft light, the supplier renders' low sheen is an accepted visual approximation, and the asset register records it as one. The exact sheen comes only from photographing physical samples.

### D. Customer comprehension and brand trust
Answer as a first-time viewer:
1. What will they think this means?
2. Could they draw a false conclusion?
3. Is it relevant?
4. Does any disclaimer raise a doubt?
5. Would a reasonable customer trust EverLiv more?

Never add unverified generalizations about other brands.

### E. Platform and publishing readiness
- Safe areas and mobile readability.
- AI labels, UTM links, approved date.
- The Metricool asset matches the approved file.
- Working disclosure in asset metadata and documentation: "Product shown as supplied; scene digitally created."

### F. Creative standards
**Criteria** (each 1–5): hook; visual interest; clarity; pacing; originality; premium feel; storytelling; watch-through; save/share; customer trust.

**Variety check:** compare against the previous 7 days. The piece fails if it shares 3 or more attributes with either of the two pieces before it. Never run two pieces teaching the same lesson in the same week.

**Not allowed by default:** text-on-flat-background as the main format; the same end card on consecutive posts; a series on consecutive days.

**Concept first:** for hero pieces, write 2–3 concepts and recommend one before production.

### G. Human anatomy & interaction gate (owner, Nov 14; publication-blocking)
Applies whenever people, hands or body parts appear.

1. **Anatomy:** hands have believable anatomy, proportions, skin texture, nails and finger positioning.
   - Five digits where visible; joints bend naturally.
   - No extra, fused, missing or rubbery fingers.
2. **Continuity:** fingers, thumbs, wrists, arms and sleeves are never stretched, fused, disconnected, floating or unnaturally cropped.
3. **Cropping:** a hand or limb may leave the frame only where it looks intentional and photographically natural, for example cropped at the wrist or forearm.
   - Never a thumb or fingertip clipped at the frame edge.
   - Never a hand cut off mid-gesture.
4. **Interaction:** hands interact with the product in a physically credible way that respects how the packaging actually works.
   - No pressing a capped pump.
   - No floating "about to touch" gestures that read as staged.
   - No grip that hides the brand.
   - Prefer natural, relaxed moments: setting down, holding, lifting, opening the correct closure, or a hand resting nearby.
5. **No retrofitting:** never move, stretch or distort anatomy to make a product composite fit.
   - Plan the pose and framing in the scene prompt around the real product's dimensions.
   - If it doesn't work, regenerate the scene.
6. **Inspection:** check people and hands at 100%, feed size and thumbnail size.
   - The independent reviewer must include this gate whenever people or hands appear.
7. **Result:** any conspicuous anatomical or interaction error is a publication-blocking failure, even if the label passes.

**Scene-planning checklist for lifestyle shots** (written before generating):
- Stand-in dimensions in real units, matching the actual package silhouette **from the Packaging Reference Profile**.
- Complete hand pose: which fingers touch where, and where the thumb is.
- Crop lines that keep the whole hand in frame or crop at the forearm.
- Camera height **compatible with the available authentic views** (I.3).
- Product size as a % of frame height (aim for ≥ 30–35% for a hero; check the thumbnail).

### H. 3D packaging-fidelity method (owner approval Nov 14: INTERNAL TESTING ONLY)
Applies when building a digital model of a real package.

1. **Inputs:**
   - **The product's Packaging Reference Profile, and every authentic reference it lists.** That includes Supliful blank-container renders (cap-on, cap-off, side and angled views), not only the branded front render.
   - Supplier label artwork, used unaltered. Print-ready files are preferred; when only a presentation image exists, the profile says so.
   - Dimensions and material specifications. Without supplier measurements, every dimension is marked PROVISIONAL and no 1% accuracy claim is made.
2. **Geometry:**
   - Built from supplier references, never from a generic container of the same type.
   - Each cap, closure, seam, edge radius and step must be traced to a specific reference image.
   - **Camera solved before geometry:** the reference camera's height, distance and tilt are derived from at least two ellipse cues (for example the top and the base). This keeps camera perspective from being misread as product shape.
3. **Label mapping:**
   - The artwork is wrapped onto the geometry exactly as printed and applied: uniform scale, no stretch.
   - No rewriting, redrawing, recolouring, cropping or hiding of text or claims.
   - Registration comes from at least two independent label features, for example both gold rules.
4. **Materials:**
   - **Labels are high-gloss BOPP film (VERIFIED, supplier, Nov 15).** Model the label with a glossy film surface (low roughness, clear coat). Never use matte paper.
   - Cap and body plastics follow the supplier renders (gloss cap, satin body). They stay UNVERIFIED until the supplier specifies them.
   - Brand colours are verified under neutral light before scene lighting is applied.
5. **Fidelity check (independent):** the neutral render is compared against the supplier render at matched camera and scale. Checks:
   - silhouette overlay
   - cap and closure close-up
   - text identity
   - colour, relative to paper
   - label sharpness
   - QR or code placement
   - materials and lighting
6. **Scene integration:** physically based lighting, reflections and shadows that match the scene camera. Packaging colour is never shifted.
7. **Release:** nothing customer-facing until the owner approves the accuracy of the method on one product.

### I. Product-authenticity process (owner, Nov 14 evening; MANDATORY for all products and all tools)
1. **Supplier references first.** Before creating, compositing or rendering any product imagery, inspect every authentic source already accessible:
   - Supliful product listing: amount, gross weight and all mockups, including blank container views
   - the live store product images, and any flat label artwork
   - the media library
   - the product's Packaging Reference Profile
   - open supplier questions

   Never assume a resource is unavailable without checking. Never substitute a generic container for supplier-specific references.
2. **Packaging Reference Profile.** Every product or distinct packaging configuration has a profile in everliv-media `library/packaging-profiles/`. It holds a family file plus the per-product `inventory.csv` row, and records:
   - product name, SKU and supplier identity
   - shape and construction: cap, closure, seams, edges
   - dimensions
   - materials, colour, finish, translucency and reflectivity
   - label artwork, placement and wording
   - available views and source links
   - each fact labelled VERIFIED, ESTIMATE or MISSING
   - open authenticity or label-compliance questions

   Products with identical physical packaging share a family geometry profile but keep their own label and product-specific details. A new product gets a profile before any creative.
3. **Authenticity gate (recorded per brief, before generation).** Confirm and write down:
   - **(a)** that the shape and packaging configuration match the profile and its authentic references
   - **(b)** that label wording, typography, colours and proportions come from authentic artwork
   - **(c)** that the chosen camera angle and lighting can realistically carry this packaging with the views available. For example, a front-only render needs an eye-level, soft-light composition.
   - **(d)** the asset type: authentic source imagery, or a validated 3D model. Use authentic source imagery whenever a reliable 3D model is not available.
4. **When references are insufficient:**
   - Record the gap in the profile.
   - Choose a safer composition, such as a straight-on view, the authentic render as-is, or a label-detail inset.
   - Route the asset request through Restructuring.
   - Never improvise the packaging.
5. **Generators (ChatGPT, Gemini):** used for environments, lighting and disclosed people only. **They may never draw, invent, redesign, relabel or "improve" EverLiv packaging.** Any packaging a generator draws is discarded. A generated stand-in object only marks placement and light.
6. **Maintenance:**
   - Profiles are updated whenever supplier assets, labels or packaging change.
   - Superseded facts are struck through with a date, not deleted.
   - All prior tests, models, prompts, scripts and QA results are preserved.
7. **Supplier-verified facts (Gino, Supliful, Nov 15, support@everliv.life thread "Order #1096"):**
   - **Labels:** high-gloss BOPP only. No matte, metallic, foil or pearlescent.
   - **Photography:** no product photos exist beyond those already generated in the account. New authentic photography requires a **sample order**.
   - **3D models and packaging mockups:** not available.
   - **Photo rights:** EverLiv may use any photos showing its labels.
   - **Shipping packaging** (help-centre article): FedEx boxes or bubble mailers with kraft-paper fill. This is not product packaging.
   - **Label file received:** "Peptide Eye Gel-Cream-label.pdf" (3.75 × 3.00 in, 600 ppi raster). It is content-identical to the flat label already in the library.
   - **Not answered:**
     - coffee carton or bag
     - container dimensions
     - Pantone/CMYK colour references
     - product-name/format, badge and Collagen Strips substantiation questions

## 3. Independent review (approved by Jeff, Nov 14)
- **Reviewer:** a fresh reviewer agent for every pass. Self-scoring is never called independent.
- **Inputs:** only the exported asset(s), the platform, the caption, the product source image **and the relevant authentic packaging references from the profile**, in a clean folder, plus the benchmark references.
- **Evaluates:**
  - first impression, visual interest, clarity, originality and premium feel
  - product fidelity, **including packaging geometry against the profile (section C)**
  - photographic realism (C.7)
  - **human anatomy & interaction (section G)** whenever people or hands appear
  - technical defects
- **Blocking:** any significant hook, visual, factual, trust, packaging, realism or anatomy issue blocks owner approval regardless of score.
- **Disagreement:** I may reject a suggestion only when following it would break a factual, authenticity or compliance rule, and I record why.
- **Comparisons between tools or methods:** file names are randomized so the reviewer is blind to the method.

## 4. Independent final technical review
Open the exported files, not the project. Review the phone sheet, then native frames, and hunt for new defects across all gates.

**Limitations:** no in-app preview; safe areas are approximations.

## 5. Reporting rules
Never call creative "final", "verified", "independent" or "ready" unless that check ran. Report what was checked and how, what was found and corrected, what remains uncertain, and status per gate. Numeric targets are reported as pass or fail against the target. Dimensions without supplier measurements are reported as provisional.

## 6. Tools and accounts
- **Claude** orchestrates.
- **Generators:** ChatGPT and Gemini are both kept as production tools. They are chosen per brief on image quality, realism, composition and packaging fidelity. Neither is the permanent winner, and neither may author packaging (I.5).
- **Gemini account:** only the EverLiv Workspace account support@everliv.life (gemini.google.com/u/1/). **Verify the signed-in account before every prompt**, because the built-in browser's default Gemini sign-in is a different Google account. Business production stays separate from other Google accounts.
- **Packaging Reference Profiles:** everliv-media `library/packaging-profiles/`, containing `README.md`, `inventory.csv` and `families/PF-01…PF-10`. They are generated by `build_profiles.py`, which is kept with them; the v1 generator is preserved as `build_profiles_v1_2026-11-14.py`.
- **3D:** Blender 5.3 (free).
  - Build script: `creative-tests/2026-11-14-eye-serum-3d-accuracy/tools/build_eye_serum.py`.
  - `build_eye_serum_v9.py` is the same frozen geometry with the supplier label file and a gloss BOPP label.
  - Compare tools: `compare.py` and `extras.py`.
- **Compositors:** `library/editorial/templates/compose_authentic.py` for single products and `creative-tests/2026-11-15-collections/scripts/compose_group.py` for groups.
- **`/home/claude/cp/cp_composite.py` (v5.1):** clean-plate compositor, with options `--wrap`, `--ring`, `--grad` and `--plane`. Archived in `creative-tests/2026-11-14-photoreal/`.
- **`/home/claude/serum/pipeline.py`, `transfer.py`, `relight.py`, `measure.py`:** the v4 pipeline and metrics.
- **`qa_export.py`, `qa_still.py`:** export QA.
- **Asset library:**
  - everliv-media repo `library/`. The approved creative library is `library/editorial/`, with `registry.json` and `ASSET-REGISTER.md`.
  - Collagen Strips cut-out was replaced on Nov 15 (owner-approved). The degraded v1 is preserved in `library/collagen-strips/superseded/`.
