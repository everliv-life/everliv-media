# Founding Members: final-approval package (Round 1, revision 3)
**Revised:** Nov 16, 2026, about 2:55 PM ET.
**Status:** NOT scheduled, published or sent, and no paid ads. Launch depends on (a) Restructuring's shopping-flow repairs, verified end to end, and (b) Jeff's final approval.

## Revision 3 changes (minor; design unchanged)
1. **Carousel slide 3:** the prices are restructured for phone legibility. Each product now shows an "EVERYDAY" label over a 44 px grey price, then a "MEMBER · 20% OFF" label over a 92 px forest-green price. The product name is larger, at 38 px, and the tiles are slightly larger. The two prices sit side by side with clear labels, so they're easy to tell apart.
2. **Story 3 link sticker:** the clean space is kept. **Place the sticker centred horizontally at about y = 1,000–1,240 px** of the 1,920 px frame, in the open green band between "$69.99 from February 1, 2027" and "Tap to join." It covers no text and stays clear of Instagram's top (250 px) and bottom (340 px) interface zones. In the app, that's roughly the middle of the screen, just above "Tap to join."
3. **Email:**
   - **Header image:** a Shopify Messaging build sheet is added (`FM-05-email-shopify-messaging-build-sheet.md`). The header is uploaded into a native Image block, so Shopify hosts it.
   - **Footer:** the manual unsubscribe and address lines are removed from the reference HTML. Shopify Messaging adds the required footer and a working unsubscribe link.
   - **CTA:** the URL with UTMs was re-verified at 2:50 PM and returns 200. The mobile layout was re-checked (fits 390 px).
4. **Restructuring handoff:** updated in place, so it remains the single handoff. It now lists the five pages still showing "most eligible 20%" and states that CA/NC is **disclosed, not technically blocked**. It also asks only for evidence of checks that are genuinely outstanding, and confirms no change to Testosterone & NAD+ placements.
5. **No other changes.** The card stays the primary visual, the "strips, capsules, powders and more" message stays, the break-even appears only in the carousel and email (not the launch image), and NAD+ and β-NMN remain the examples.

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
| Member price after sign-in, cart, checkout, purchase tracking. (CA/NC is disclosed but not technically blocked, per owner.) | **Not testable by Marketing:** no accounts, purchases or test orders. These need Restructuring's end-to-end test. |

## Final launch-readiness checklist (to run after Restructuring reports its repairs complete; Marketing will re-run it)
1. Member sign-in link works (desktop and mobile).
2. Member prices are consistent between product page, cart and checkout for a signed-in member, on at least NAD+, Eye Gel-Cream and one strip.
3. Purchase buttons work on mobile (product page → cart → checkout).
4. Membership add-to-cart, terms checkbox and checkout work on mobile and desktop.
5. Purchase tracking for the membership product is confirmed (GA4 and Meta purchase events). This is required before any paid ads.
6. Strip availability is rechecked the morning of publishing. If Sleep or Collagen is back, the six-tin family image can return.
7. Prices in carousel slide 3 are rechecked the morning of publishing.
8. If ads are approved later, the CA/NC geo-exclusion is set in the ad account. The restriction is disclosed on site but not technically blocked at checkout.

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

**Build:** in Shopify Messaging, use `FM-05-email-shopify-messaging-build-sheet.md`. Shopify hosts the header image and adds the footer and a working unsubscribe link. Send only to opted-in subscribers, after explicit approval.

## Still on hold
- **Paid advertising.** Purchase tracking, the CA/NC geo-exclusion and membership restrictions all need to be verified first, and you need to approve a budget.
- **Strip tins in paid ads.** They carry the unverified "Natural Extracts", so they stay in organic posts only.

## Launch-readiness summary (2:55 PM ET, Nov 16)
**Marketing: complete, pending your final approval**
- Final assets: the launch post, 5-slide carousel, 3 stories and the email header.
- Captions, alt text and UTMs.
- The Shopify Messaging build sheet and reference email.
- **Live check, 2:50 PM:**
  - NAD+ $59.99 → $47.99 and β-NMN $49.99 → $39.99, both 20% and both available.
  - The membership offer text ($49.99 through Jan 31, 2027 ET; $69.99 from Feb 1, 2027) is live.
  - The CTA URL works.

**Outstanding: Restructuring** (see the single handoff)
1. Fix "most eligible 20%" on 5 pages. The terms page wording is the owner's or attorney's call.
2. Evidence of enrollment, sign-in, cart and checkout passing on mobile and desktop.
3. The secondary mobile "Add to Cart" button.
4. GA4 and Meta Purchase events.
5. Whether a CA/NC checkout block is planned.
6. Inventory and price checks on launch morning.

**Then:**
- **Marketing:** a final live re-check on Nov 26 or 27, followed by your go/no-go.
- **Jeff:** authorise publishing, the email send and (separately) any paid ads.
