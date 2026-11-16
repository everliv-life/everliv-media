# Strip-tin lineups (Marketing, Nov 16, 2026): recommended replacement for the clipped homepage strip image

**Status:** PROVISIONAL. This is a recommendation for Restructuring to place; Marketing has not uploaded anything to Shopify.

## Source and compositing
- **Source pixels:** authentic supplier front renders only.
  - Energy, Hydrate, Iron, Collagen and D3+K2 come from `library/<sku>/…--front`.
  - Sleep is the store's main image, saved to `sources/` on Nov 16.
- **Cut-outs:** made with `kit/cutout.py`. Interior pixels are byte-identical to the source; see `cutouts/*.log`.
- **Changes to the products:** one uniform scale only. No relighting, recolouring, mirroring or clipping. Every tin is fully inside the frame.
- **Shadow:** a soft contact shadow drawn on the background layer only.

## Files
| File | Contents | Use |
|---|---|---|
| `strips-lineup-5--row--transparent.png` / `--ivory-preview.jpg` (2700×900) | Energy, Hydrate, Iron, D3+K2, Collagen | Bundle section or wide banner, eligible strips only (Sleep sold out) |
| `strips-grid-5--3over2--…` (1800×1500) | same 5, 3 over 2 | Hero right half or a square card; no clipped tins |
| `strips-lineup-6-incl-sleep--row--…` (3200×900) | 6 tins including Sleep | **Hold:** use only once Sleep is restocked (Nov 25) and the owner lifts the Sleep exclusion |
| `strips-grid-6-incl-sleep--3over3--…` (1800×1500) | 6 tins, 3 over 3 | Same hold |

## Open issues that still apply
- **Claim:** every tin label carries "Natural Extracts", which is unverified. This is an open supplier question.
- **Strip dimensions:** unverified.
- **Label finish:** high-gloss BOPP (supplier-verified). The renders show low sheen, which is a visual approximation.
