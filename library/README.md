# EverLiv verified product-asset library

This library is the source for any recognizable EverLiv product in social creative. The full index (SKU, source, last-checked date, discrepancies and photos still needed) is the **Product assets** tab of the EverLiv Product & Claims Library + Content Calendar.

## Authenticity standard (owner-approved, Nov 14 2026; compositing rule v4)

1. **Use only authentic source imagery.** Every recognizable product comes from the files in this library. These are supplier (Supliful) renders with EverLiv's production labels, as published on the live product pages. Real product photography is not part of current production (owner, Nov 14).
2. **AI never draws packaging.** AI may make environments, lighting, disclosed people/hands, and blank stand-in objects used only as lighting and placement references. It never draws, redraws, warps or relabels packaging.
3. **Composite at final resolution, light only (v4).**
   - **Scale once:** the authentic cutout is scaled uniformly, once, straight from the source to its final pixel size. No perspective warping, no redrawing, no retouching of label art, and no blur or sharpening of the label.
   - **Light only:**
     - The render's own studio shading may be removed.
     - The scene's light may be applied: key colour, cylinder falloff and terminator, specular and rim, and scene shadows falling across the object.
     - Cast and contact shadows must match the scene.
   - **Build at output size:** prepare the scene at the output size first (2160×2700 master, 1080×1350 feed), then place the product. Never composite at a smaller size and upscale.
   - **Allowed alpha edits:** feathering the cutout's edge, shaping its base to the camera's ellipse, and restoring scene elements that sit in front of the product (for example, fingertips).
   - This replaces the earlier "uniform exposure only / no relighting maps" rule.
4. **No label edits to hide claims.** Never edit a label to hide or replace printed claims. Use a crop, a different angle or a different image instead.
5. **Exclude storefront infographics.** The infographic gallery images on the store (index 02 for most products) carry structure/function claims. They are not in this library and must not be used.
6. **Product-fidelity gate before review.** This gate blocks publication regardless of any review score.
   - **At 100%:**
     - The label matches the source: logo, typography and proportions within 1%, with no invented text.
     - The logo and name are sharp. Target: label sharpness ≥ 85% of the source at the same width.
     - Edges, reflections and shadows are realistic.
   - **At feed size:** the product is prominent and the branding is clear.
   - **At thumbnail size (~150 px):** the product is recognizable.
   - **Independent review:** a fresh reviewer checks against the four benchmark references and the product source.

## Product presentation (owner standard, Nov 14 2026)
- **Hero:** when the product is the subject, show the complete authentic container (cap, label, base) as the visual anchor, with breathing room. If it doesn't fit, scale it down or rebalance the layout. Never cut it off.
- **Believable handling:** hands interact the way the packaging actually works and never block the branding. Scale stays realistic relative to hands and nearby objects.
- **Label education:** use a deliberate, clearly labeled close-up of the facts panel or label, designed as a detail inset, not a cropped product.
- **No half-products:** no half-containers in rounded frames, and no crops that show only the brand or product name.
- **QC:** check every frame at full size, feed size and thumbnail size. No overlapping or clipped text; disclosures readable.

## File naming
`library/<shopify-handle>/<handle>--<view>.<ext>`

- **Views:** front, supplement-facts, packet-and-strip, open-tin, stack, front-cutout (transparent PNG), and so on.
- **Sources:** all files were downloaded from https://everliv.life/products/<handle> on 2026-11-14. The Energy flat production label comes from the Supliful product page.
- **What the files are:** supplier renders, not photographs.
