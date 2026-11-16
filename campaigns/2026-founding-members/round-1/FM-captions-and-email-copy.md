# Founding Members: final-approval package (Round 1, revision 2)
**Revised:** Nov 16, 2026, about 12:45 PM ET.
**Status:** NOT scheduled, published or sent, and no paid ads. Launch depends on (a) Restructuring's shopping-flow repairs, verified end to end, and (b) Jeff's final approval.

## Revision 2 changes (targeted; design unchanged)
| # | Request | Change |
|---|---|---|
| 1 | Clean Story 3 | The "LINK STICKER HERE" placeholder is removed. The space between the price block and "Tap to join" stays clear for the real Instagram link sticker. |
| 2 | Founding Member card central; offer isn't strips-only | **Launch post:** the card is now the hero visual, replacing the strip tins, with the line "Member prices on every eligible order, as often as you shop: strips, capsules, powders and more." **Email header:** the card replaces the tins. **Story 2:** keeps the four available strips as supporting imagery, captioned "Oral strips shown. Member pricing covers eligible products across EverLiv." On green backgrounds the card has a lighter edge so it stands out. |
| 3 | Eye Gel-Cream discrepancy | **Replaced in carousel slide 3 by β-NMN:** everyday $49.99, member $39.99 (20%), live and available; Restructuring listed it as positive-margin. The Eye discrepancy has been sent to Restructuring (see the coordination doc). |
| 4 | Does "most 20%, some 15%" match the settings? | **No, so it's corrected.** All 44 live product pages were checked: **19 products at 20%, 21 at 15%, 4 with no member price** (membership, the 2 wheys, the Ultimate Bundle). "Most are 20%" is therefore inaccurate. Of products available today, it's 17 at 20% vs 21 at 15%, because Sleep and Collagen are unavailable. Every asset now says **"20% or 15% off, depending on the product."** The site's own "most eligible products 20%" wording was flagged to Restructuring. The conditional break-even and the "not guaranteed" disclosure are unchanged. |

## Visual check of the packaging shown
| Product | Image | Packaging status |
|---|---|---|
| NAD+ | supplier render (store main image) | Matches the store. The physical label is **not** on the handoff's "confirmed on a shipped unit" list, the same status as most of the catalog. |
| β-NMN | supplier render (store main image, includes loose capsules) | Same as NAD+ |
| Energy, Hydrate, Iron, D3+K2 strips | verified supplier cut-outs | D3+K2 was confirmed on a shipped unit; the others are supplier renders. "Natural Extracts" is still unverified (organic use only). |

**Note on swapping the Eye product:** the Eye product's physical label *was* confirmed on a shipped unit, and Supliful confirmed it matches our label file. The discrepancy is its **name**: the label says "Serum", while the store says "Gel-Cream". The swap follows your instruction. Strictly, NAD+ and β-NMN have weaker physical verification than the Eye product does. If you want only physically confirmed packaging, the alternative is D3+K2 Strips ($34.99 → $27.99, 20%), but Restructuring hasn't confirmed their margin.

## Live verification (12:10–12:40 PM ET, Nov 16)
| Item | Result |
|---|---|
| Membership product | $49.99, available |
| Membership page `/pages/membership` | 200 |
| Strips available | Energy ✓, Hydrate ✓, Iron ✓, D3+K2 ✓; Sleep ✗ (sold out); Collagen ✗ (unavailable) |
| Carousel price examples | NAD+ $59.99 → $47.99 member (20%); β-NMN $49.99 → $39.99 member (20%). Both read from the live product pages. |
| Noted | Iron and D3+K2 now list at $34.99. The Nov 11 handoff had $29.99. The creative doesn't use their prices. |

## Shopping-flow pre-check (Marketing, read-only, 12:30 PM ET)
| Check | Result |
|---|---|
| "Already a member? Sign in" link | ✓ Opens the Shopify sign-in page (email field present). Signing in was not tested; that needs a real member account. |
| "Join to unlock member pricing" link | ✓ 200 → membership product |
| Membership terms and details pages | ✓ 200 |
| Join button | Disabled until the terms box is ticked, which is intended. Enabling it and checking out were not tested (no purchase). |
| Mobile (375 px) NAD+ main "Add to Cart — $59.99" | ✓ Visible, enabled and tappable, with no horizontal overflow |
| Mobile secondary "Add to Cart" further down the page | ⚠ My automated check couldn't confirm it's tappable. Restructuring should test it by hand. |
| Member price after sign-in, cart, checkout, CA/NC restriction, purchase tracking | **Not testable by Marketing:** no accounts, purchases or test orders. These need Restructuring's end-to-end test. |

## Final launch-readiness checklist (to run after Restructuring reports its repairs complete; Marketing will re-run it)
1. Member sign-in link works (desktop and mobile).
2. Member prices are consistent between product page, cart and checkout for a signed-in member, on at least NAD+, Eye Gel-Cream and one strip.
3. Purchase buttons work on mobile (product page → cart → checkout).
4. Membership add-to-cart, terms checkbox and checkout work on mobile and desktop.
5. Purchase tracking for the membership product is confirmed (GA4 and Meta purchase events). This is required before any paid ads.
6. Strip availability is rechecked the morning of publishing. If Sleep or Collagen is back, the six-tin family image can return.
7. Prices in carousel slide 3 are rechecked the morning of publishing.
8. Ads geo-exclusion for CA and NC is confirmed in the ad account, if ads are approved later.

## Assets
**Feed, 1080×1350:**
- `FM-01-launch-black-friday_1080x1350.png`: launch post
- `FM-02-carousel-1…5_1080x1350.png`: cover · how it works · what members pay · the math · founding price

**Stories, 1080×1920:**
- `FM-03-story-1…3_1080x1920.png`: hook · benefits · CTA (with the link-sticker area marked)

**Email:**
- `FM-04-email-header_1200x600.png`: header image
- `FM-05-email-black-friday.html`: the email, plus `--preview-desktop.png` and `--preview-mobile.png`

**Type:**
- **Headlines:** Newsreader, standing in for the site's Sentient.
- **Body:** Figtree.

## Captions

### Black Friday launch: FM-01 (IG and FB, Fri Nov 27)
> **Become a Founding Member.**
> This Black Friday, we're not discounting products. We're opening membership.
>
> One payment of $49.99 gives you 12 months of EverLiv member pricing on every eligible order (strips, capsules, powders and more) as often as you shop. No subscription, and no automatic renewal.
>
> Founding price through January 31, 2027. From February 1, membership is $69.99.
>
> Join through the link in bio.
>
> *Member pricing applies to eligible one-time product purchases (not Subscribe & Save): 20% or 15% off depending on the product, some products excluded. Savings depend on what you buy. Not available to residents of CA or NC. Terms at everliv.life.*

**FB:** replace "link in bio" with the UTM link.

### Carousel: FM-02 (Sat Nov 28 / Sun Nov 29)
> One payment. Twelve months of member pricing on every eligible order. Swipe for how EverLiv Founding Membership works, what members actually pay, and the honest math on whether it's worth it for you.
>
> $49.99 through January 31, 2027 · $69.99 from February 1.
>
> *Eligible one-time product purchases; 20% or 15% depending on the product, some excluded. Prices as of Nov 16 and may change. Not available in CA or NC.*

### Cyber Monday: story set FM-03, plus a short feed caption (Mon Nov 30)
> Still deciding? Founding membership is $49.99, paid once, for 12 months of member pricing on every eligible order. The founding price runs through January 31. No auto-renewal, so you choose whether to join again next year.

### Alt text
- **FM-01:** "EverLiv Founding Member card. Become a Founding Member: a full year of member pricing, $49.99 paid once, on eligible strips, capsules, powders and more."
- **FM-02 cover:** "EverLiv Founding Member card. Become a Founding Member: a full year of member pricing, $49.99 paid once."
- **FM-02 slide 3:** "What members pay: NAD+ everyday $59.99, member $47.99. β-NMN everyday $49.99, member $39.99."
- **FM-02 slide 4:** "If every purchase is a 20%-off product, $49.99 divided by 20% equals $249.95."

### UTMs
`?utm_source=<instagram|facebook|email>&utm_medium=<social|email>&utm_campaign=founding-members-2026&utm_content=<asset-id>`

## Email (Black Friday launch)
**Send:** only to contacts with marketing consent, after final approval.

**Subject options:**
1. Become a Founding Member
2. This Black Friday, we're opening membership
3. A full year of member pricing, $49.99 once

**Preheader:** "A full year of member pricing. $49.99, paid once. Founding price through January 31, 2027."

**Body:** see `FM-05-email-black-friday.html`. On a 390 px phone screen it has no sideways scrolling, and the CTA is 300×52 px.

**Unsubscribe:** the `{{unsubscribe}}` placeholder must be replaced by Shopify Messaging's own unsubscribe link and footer when the email is rebuilt there. Send only to opted-in subscribers.

## Still on hold
- **Paid advertising.** Purchase tracking, the CA/NC geo-exclusion and membership restrictions all need to be verified first, and you need to approve a budget.
- **Strip tins in paid ads.** They carry the unverified "Natural Extracts", so they stay in organic posts only.
