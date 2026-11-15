# Restart checklist: EverLiv collection photography (Nov 15, 2026)

Use this if the session pauses. Everything below is in the `everliv-media` repo unless a path is given.

## State
- **4 owner-approved images:** `creative-tests/2026-11-14-gift-edit/approved/`, with metadata and `manifest.json`. Status: CREATIVELY APPROVED / PENDING VERIFICATION.
- **6 new single-product images:** `individual/`. Visual QA passed (`qa/review-ind6`).
- **10 collection and banner masters, plus exports:** `collections/`. QA rounds are in `qa/review-coll1` and `qa/review-coll2`.
- **2 bundle "what's included" images:** `bundles/`. Status: BLOCKED until Restructuring confirms the contents.
- **Cut-out kit:** `library/cutout-kit/` (10 cut-outs plus `manifest.json`).
- **Collagen cut-out:** replaced at `library/collagen-strips/` (the old one is in `superseded/`).

## How to rebuild
1. **Single images:** `/home/claude/scenes/compose_authentic.py`. The settings for each template are in `creative-tests/2026-11-14-gift-edit/README.md`.
2. **Group images:**
   - Run `python3 scripts/layouts.py` to write `layouts.json`.
   - Then run `python3 scripts/compose_group.py <one layout entry as json>` for each image.
   - Plates are in `plates/`. Cut-outs are in `/home/claude/kit/cutouts/*-v2.png`, a copy of `library/cutout-kit/`.
3. **Scene plates come from Gemini:**
   - Use the EverLiv Workspace account only (support@everliv.life, gemini.google.com/u/1/). Verify the account before every prompt.
   - Downloads arrive in ~/Downloads as `Gemini_Generated_Image_*.jpeg`, or as hidden `.Q6L2SF6YDW…` temp files. Stage them by path.
   - The browser wait tool caps at 10 s, so leave 20 s or more between download clicks.

## Rules
- Do not change Shopify. Do not publish. Do not contact Supliful; Restructuring coordinates supplier contact.
- Product pixels may only be a uniform resize, one exposure scalar shared by the whole image, and luminance grain. The scene can be white-balanced or mirrored; the product never.
- Every new image goes through an independent QA agent before it is labelled.

## Next steps if the session is interrupted
1. Apply any remaining round-2 QA fixes, then re-run QA.
2. Update `ASSET-REGISTER.md` labels.
3. Commit and push. Update the project doc `claude/collection-photography-2026-11-15.md`.
4. Once Restructuring answers the bundle, coffee-packaging and foil questions, move the affected assets out of PENDING VERIFICATION or BLOCKED.

## Update: Nov 15, final finishing pass
- The canonical library is now `library/editorial/`: individual, collections, bundles and templates, with `registry.json`, `ASSET-REGISTER.md` and `RESTRUCTURING-HANDOFF.md`.
- Finishing builds are in `creative-tests/2026-11-15-collections/finishing/`. QA for them is in `qa/review-final` and `qa/review-final2`.
- Coffee scale: the individual coffee images now use cut-out scale 0.83, which puts the carton at about 24–26 cm against a mug. The earlier approved versions are preserved.
- Waiting on the owner:
  - re-approval of the corrected coffee holiday mobile image
  - review of the 3 corrected mobile images and the tight desktop alternative
- Waiting on Restructuring and the supplier: the items in `RESTRUCTURING-HANDOFF.md` sections 2–4.
