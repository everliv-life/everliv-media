# Supliful response (Gino, Nov 15, 2026): verified facts, creative impact, open items

**Source:** the support@everliv.life thread "Order #1096 (SPL1252388) — status and tracking". Gino replied at 6:35 PM ET to EverLiv's packaging-asset request of Nov 14, 6:08 PM, which went to Karl.

**Attachment:** `Peptide Eye Gel-Cream-label.pdf`. It is archived unaltered in everliv-media at `library/peptide-eye-serum/supplier/`.

Marketing did not contact Supliful and has not replied.

## 1. What our Nov 14 request asked, mapped to Gino's numbered answers

| # | We asked | Gino's answer | Status |
|---|---|---|---|
| 1 | Print-ready label artwork / dieline (Eye Serum and Collagen Oral Strips) | "See attached for the label file we have for this product." | **Partly answered.** Eye Serum only: a 3.75 × 3.00 in label as a 600 ppi raster. No vector, dieline or bleed. **Nothing for Collagen Oral Strips.** |
| 2 | Packaging specifications: dimensions, construction, closure, materials | "Packaging will depend on the order itself," plus a link to the standard-packaging article | **Not answered.** The article covers shipping only (FedEx boxes or bubble mailers, sizes, kraft-paper fill, store-name shipping label). It says nothing about containers, cartons vs bags, or dimensions. |
| 3 | Finishes and colour references | All labels are high-gloss polypropylene BOPP; only gloss is available; matte, metallic, foil and pearlescent are not offered | **VERIFIED** (finish). Pantone/CMYK references not provided. |
| 4 | High-resolution product photography | Only what is already generated in our account; for more, place a sample order | **VERIFIED:** no further supplier photos exist. |
| 5 | Additional angles (back, sides, top, open/closed) | "Same as #4" | No additional angles exist. |
| 6 | **3D models or packaging mockups** | "This is not available." | **VERIFIED:** no 3D models or mockups. *This is the "question 6" Jeff asked about.* |
| 7 | Usage rights | "Yes, you may use any photos with your labels on them." | **VERIFIED** for photos showing our labels. Not explicitly addressed: paid advertising restrictions and credits. Marketing reads "any photos" as including paid use; Restructuring may want written confirmation. |
| Extra | Product name/format; Eye Serum badge substantiation; Collagen Strips source, amount, "Lactose Free", origin, testing | Not answered | **OPEN** |

## 2. Peptide Eye Serum: supplier label file vs our product

The supplier file is **content-identical to the flat label already in our library**. After registration, the mean pixel difference is 1.8 levels, which is resampling only. So the artwork we have used is the supplier's artwork.

| Item | Supplier label (PDF) | Live store listing (Nov 14 snapshot) | Finding |
|---|---|---|---|
| Product name | PEPTIDE EYE SERUM | EverLiv Peptide Eye Serum | Match. **The supplier's catalog/file name is "Peptide Eye Gel-Cream".** |
| Format | Ingredients include emulsifiers (Cetearyl Alcohol, Cetearyl Glucoside) and gums (Acacia Senegal, Xanthan) | Called a "serum"; copy says "lightweight, non-greasy texture" | **FLAG:** the formula reads as a gel-cream. "Serum" may misdescribe the format. Not renamed; an owner and Restructuring decision. |
| Ingredients | Aqua, Vitis Vinifera (Grape) Seed Oil, Cetearyl Alcohol, Cetearyl Glucoside, Acacia Senegal Gum, Xanthan Gum, Acetyl Tetrapeptide-5, Sodium Hyaluronate, 1,2-Hexanediol, Phyllostachys Bambusoides Extract | Same list, same order | **Match** |
| Directions | Once or twice daily, a dime-sized amount to the under-eye area and along the orbital bone | Same | **Match** |
| Warnings | External use only; avoid contact with eyes; discontinue if irritation occurs; keep out of reach of children; store cool and dry | Same, plus "not intended to be ingested" | Consistent |
| Net contents | "Net Wt. 1 fl oz (30ml)" | Not stated in the description | **FLAG (open since Nov 14):** a weight term is paired with a volume. Should be "Net Contents" or "Net Vol." |
| Series line | PREMIUM BODY CARE SERIES | Tag `series-body-care` | **FLAG (open):** "body care" on an eye product |
| Badges | Cruelty Free, Paraben Free, Sulfate Free, GMP Certified | Not in the description | Paraben-free and sulfate-free are consistent with the ingredient list. **Cruelty Free and GMP Certified are unsubstantiated** (the supplier didn't answer). Not used in marketing. |
| Origin | "Manufactured in the USA using globally sourced ingredients" | Not in the description | **Unsubstantiated** (not answered). Not used in marketing. |
| Distributor | EverLiv LLC, 30 N Gould St, Ste R, Sheridan, WY 82801; support@everliv.life; everliv.life | none | Informational |
| **Store-only marketing claims** | none | "effectively reduces the appearance of puffiness and plumps fine lines"; "deep hydration"; "antioxidant protection, promoting overall skin health around the eyes"; "suitable for all skin types, including sensitive skin"; "without settling into fine lines"; "youthful, radiant-looking eyes" | **FLAG:** none of these are on the label, and no substantiation is on file. "Plumps fine lines" (without "the appearance of") and "promoting overall skin health" read as more than cosmetic. "Sensitive skin" implies testing. Recommend a copy review. Marketing will not repeat them. |

## 3. Creative specifications updated

| Spec | Before | Now |
|---|---|---|
| Label finish, all families | Matte paper (Eye Serum, assumed), "finish unknown" (tin lids), "appears matte with metallic series band" (capsule bottles), "gold foil corner?" (soap band) | **High-gloss BOPP (VERIFIED).** Series bands and the soap gold corner are **printed**, not metallic or foil. |
| Packaging Reference Profiles | v1 (Nov 14) | Regenerated: PF-01, 02, 03, 09 and 10 updated. The v1 generator is kept as `build_profiles_v1_2026-11-14.py`. |
| Creative QA SOP | H.4 said "matte label" | v7: C.8 adds the label-finish rule, H.4 requires gloss film labels, and I.7 records the supplier facts. |
| Asset register (23 images) | "Soap foil unverified" | Soap finish verified: gloss, gold printed. Remaining: whether the renders match the physical product (needs a sample). Coffee stays unresolved: carton vs bag. A label-finish note and the photo-rights confirmation are added to every asset. |

## 4. Existing images checked against the verified finish

| Asset(s) | Depicts | Verdict | Action |
|---|---|---|---|
| Eye Serum 3D neutral renders v1–v8 (internal, frozen) | **Matte paper label** (roughness 0.85, low sheen) | **INACCURATE finish** | **Corrected as v9:** same frozen geometry and camera; the label texture is now the supplier's own label file; the label material is gloss BOPP film. v1–v8 are preserved. Still internal and provisional (dimensions unverified). |
| 23 editorial images (soaps, coffees, collections, bundles) | Supplier render pixels, unaltered. Labels show low sheen under soft light; the soap gold corner shows as a printed gradient | **Not inaccurate**, but a **visual approximation** of gloss | No pixel change: painting gloss onto authentic renders would break the authenticity rule. Recorded as an approximation; exact sheen needs physical-sample photography. |
| Captions, alt text, copy | Searched: no "foil", "matte", "metallic" or "pearlescent" in any asset text | OK | Rule added: never describe the gold accents as foil. |
| Earlier Eye Serum and strip-tin concept tests (Nov 13–14) | Rejected or internal | No action | Archived |

## 5. What genuinely depends on physical samples or the supplier

**Physical samples** (a sample order, which needs the owner's approval to spend):
- real label sheen and colour under our lighting
- whether the soap renders match the bars (soap colour and texture vary by batch)
- the coffee pack actually received (carton, bag or both) and its dimensions
- Eye Serum bottle dimensions and cap and collar finish
- tin and bottle dimensions across all families

**Supplier answers still outstanding** (via Restructuring):
1. Coffee: carton or bag, and its dimensions.
2. Container dimensions for any family.
3. Pantone/CMYK references.
4. Eye Serum: product-name and format confirmation; substantiation for Cruelty Free, GMP Certified and Made in USA; the "Net Wt." and "Body Care Series" wording.
5. Collagen Oral Strips: label file, collagen source, 100 mg per strip, "Lactose Free", country of manufacture, testing.
6. Written confirmation that "any photos" includes paid advertising (optional, but recommended).
