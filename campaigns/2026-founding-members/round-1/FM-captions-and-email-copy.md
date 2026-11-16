# Founding Members: final-approval package (Round 1, revised)
**Revised:** Nov 16, 2026, about 12:15 PM ET.
**Status:** NOT scheduled, published or sent, and no paid ads. Waiting for (a) Restructuring's shopping-flow fixes to be verified and (b) Jeff's final approval.

The design direction is unchanged. These are targeted refinements only.

## What changed from Round 1
| # | Your note | Change |
|---|---|---|
| 1 | Repeated use, not a one-time discount | Launch post adds "Member prices on every eligible order, as often as you shop." Carousel slide 2, point 3, is now "Shop as often as you like." Story 2 adds "Every eligible order, as often as you shop." The email now says "member pricing every time you buy an eligible product, as often as you like." Fine print reads "One payment… member pricing applies to every eligible one-time product purchase during your membership (not Subscribe & Save)." |
| 2 | Unavailable strips | All purchase-driving creative (launch post, story 2, email header) now shows only the **four strips available today**: Energy, Hydrate, Iron, D3+K2. Sleep (sold out) and Collagen (paused) are removed from this campaign's imagery. The six-tin family image stays in the library for brand use once both are available again. |
| 3 | Conditional break-even | Slide 4 now opens with "If every purchase is a 20%-off product:" and reads "If everything you buy is eligible for the full 20%… about $250. On 15% products it takes about $333, and a mix lands in between." Fine print: "aren't guaranteed to exceed the $49.99 fee." The email uses the same wording. |
| 4 | CTA and URL | The CTA is `everliv.life/pages/membership`, which returns 200 as of 12:10 PM. The email button links there with UTMs. The full join flow on mobile and desktop **must be re-tested after Restructuring's repairs** (checklist below). |
| 5 | Disclosures, and the email on mobile | All disclosures are kept. The email was rebuilt to fit phones: at 390 px there is no horizontal scroll (it previously overflowed at 624 px), the CTA is 300×52 px, and side padding tightens on small screens. |
| 6 | Claims and images | No product claims added. The images are unaltered supplier renders. The Eye Gel-Cream example stays, named as on the store; the physical label still reads "Peptide Eye Serum" (with the supplier). |
| 7–8 | Hold | Nothing scheduled or sent. Paid ads stay on hold. |

## Live verification (12:10 PM ET, Nov 16)
| Item | Result |
|---|---|
| Membership product | $49.99, available |
| Membership page `/pages/membership` | 200 |
| Strips available | Energy ✓, Hydrate ✓, Iron ✓, D3+K2 ✓; Sleep ✗ (sold out); Collagen ✗ (unavailable) |
| Carousel price examples | NAD+ $59.99 → $47.99 member (20% list); Peptide Eye Gel-Cream $44.99 → $35.99 (20% list) |
| Noted | Iron and D3+K2 now list at $34.99. The Nov 11 handoff had $29.99. The creative doesn't use their prices. |

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
> One payment of $49.99 gives you 12 months of EverLiv member pricing on every eligible order, as often as you shop. No subscription, and no automatic renewal.
>
> Founding price through January 31, 2027. From February 1, membership is $69.99.
>
> Join through the link in bio.
>
> *Member pricing applies to eligible one-time product purchases (not Subscribe & Save): most eligible products 20% off, some 15%, some excluded. Savings depend on what you buy. Not available to residents of CA or NC. Terms at everliv.life.*

**FB:** replace "link in bio" with the UTM link.

### Carousel: FM-02 (Sat Nov 28 / Sun Nov 29)
> One payment. Twelve months of member pricing on every eligible order. Swipe for how EverLiv Founding Membership works, what members actually pay, and the honest math on whether it's worth it for you.
>
> $49.99 through January 31, 2027 · $69.99 from February 1.
>
> *Eligible one-time product purchases; some 15%, some excluded. Prices as of Nov 16 and may change. Not available in CA or NC.*

### Cyber Monday: story set FM-03, plus a short feed caption (Mon Nov 30)
> Still deciding? Founding membership is $49.99, paid once, for 12 months of member pricing on every eligible order. The founding price runs through January 31. No auto-renewal, so you choose whether to join again next year.

### Alt text
- **FM-01:** "Become a Founding Member. A full year of member pricing, $49.99 paid once. EverLiv Energy, Hydrate, Iron and D3 + K2 oral strip tins."
- **FM-02 cover:** "EverLiv Founding Member card. Become a Founding Member: a full year of member pricing, $49.99 paid once."
- **FM-02 slide 3:** "What members pay: NAD+ everyday $59.99, member $47.99. Peptide Eye Gel-Cream everyday $44.99, member $35.99."
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

**Body:** see `FM-05-email-black-friday.html`.

## Still on hold
- **Paid advertising.** Purchase tracking, the CA/NC geo-exclusion and membership restrictions all need to be verified first, and you need to approve a budget.
- **Strip tins in paid ads.** They carry the unverified "Natural Extracts", so they stay in organic posts only.
