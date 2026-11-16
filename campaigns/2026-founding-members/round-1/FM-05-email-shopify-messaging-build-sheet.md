# Founding Members launch email: Shopify Messaging build sheet
**Status:** ready to build. **Do not send or schedule.** Send only to opted-in subscribers, and only after Jeff's explicit approval. **No test sends to customers.**

## Why build it natively
- **Header image:** uploading it into a Shopify Messaging **Image** block makes Shopify host it on its own CDN, so it displays in the sent email. Never point to a local filename.
- **Footer:** Shopify Messaging adds the store address, a working **unsubscribe** link and the required footer to every marketing email. No manual unsubscribe link is needed; the reference HTML no longer contains one.

## Blocks, in order
| # | Shopify Messaging block | Content |
|---|---|---|
| — | **Subject** | Become a Founding Member *(alternatives: "This Black Friday, we're opening membership" · "A full year of member pricing, $49.99 once")* |
| — | **Preview text** | A full year of member pricing. $49.99, paid once. Founding price through January 31, 2027. |
| 1 | **Image** | Upload `FM-04-email-header_1200x600.png`. Full width. Alt text: "EverLiv Founding Member card. Become a Founding Member: a full year of member pricing, $49.99 paid once." Link it to the CTA URL below. |
| 2 | **Text** | This Black Friday, we're not discounting products. We're opening membership. |
| 3 | **Text** | Join EverLiv Member Price Club as a Founding Member for **$49.99, paid once**. For the next 12 months, you get **member pricing every time you buy an eligible product**, as often as you like, across strips, capsules, powders and more. |
| 4 | **Text** (or a shaded section) | ✓ Member pricing on every eligible order for 12 months<br>✓ Up to 20% off: 20% or 15%, depending on the product<br>✓ One $49.99 payment. No automatic renewal<br>✓ No product subscription required<br>✓ Founding price through January 31, 2027 (ET) |
| 5 | **Text** | **Is it worth it?** If everything you buy is eligible for the full 20%, membership covers its fee after about $250 of purchases in 12 months. On 15% products it takes about $333. If you shop less often, everyday prices or Subscribe & Save may suit you better. |
| 6 | **Button** | Label: **Become a Founding Member** · colour #2A422A, text #E9E4DF · URL below |
| 7 | **Text** (small, centred) | From February 1, 2027, membership is $69.99. |
| 8 | **Text** (small, grey) | Founding price $49.99 applies to memberships bought through January 31, 2027 (Eastern Time); $69.99 from February 1, 2027. Membership is a single payment, lasts 12 months from activation and does not renew automatically. During your membership, member pricing applies to every eligible one-time product purchase (not Subscribe & Save): 20% or 15% off depending on the product, some products excluded. Doesn't combine with Subscribe & Save, bundles, partner pricing or promo codes. Savings depend on what you buy and aren't guaranteed to exceed the fee. Refunds: full refund within 3 business days; within 30 days, a full refund if member pricing is unused, otherwise the fee minus savings received. Not currently available to residents of California or North Carolina. See the Membership Terms at everliv.life. |
| — | **Footer** | Shopify's automatic footer: address and unsubscribe. Confirm it in the preview. |

**CTA URL** (verified 200 at 2:50 PM ET, Nov 16):
`https://everliv.life/pages/membership?utm_source=email&utm_medium=email&utm_campaign=founding-members-2026&utm_content=bf-launch`

**Audience:** email subscribers who have accepted marketing (Shopify's "Email subscribers" segment). No purchased or imported lists without a consent record.

## Pre-send checks (after building, before Jeff's approval)
1. In Shopify Messaging's **desktop and mobile previews**, the header image displays and the button is full-width on mobile.
2. The footer shows the store address and an unsubscribe link.
3. Send a **test to an internal address only** (e.g. support@everliv.life), not to customers. Then confirm on a real phone:
   - the image loads
   - the button opens the membership page with the UTM intact
   - the unsubscribe link works
4. Recheck prices and dates the morning of the send.

The reference layout is `FM-05-email-black-friday.html`, with previews `--preview-desktop.png` and `--preview-mobile.png`. It fits a 390 px screen with no horizontal scroll, and the CTA is 300×52 px.
