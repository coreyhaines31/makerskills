# Worked example — Swipe Files (`swipefiles-nextjs`)

Source implementation (draft): [PR #97](https://github.com/conversionfactory/swipefiles-nextjs/pull/97) on branch `feature/dispute-evidence`. Full in-repo guide: `docs/dispute-evidence.md` on that branch. Issues #89–#96.

This is a **Next.js + Prisma + Auth.js (JWT) + Stripe + PostShiba/Resend** port of the checklist. Use it as a shape, not a copy-paste into Rails or a different auth stack.

## Why it was needed

Before the PR, a dispute could only cite `User.createdAt`, the `Purchase` row, and `LessonProgress` rows that exist only when someone clicked "Mark complete". Sessions are JWT (no login history), mail had no local record, and Vercel logs roll off after about a day.

## What landed

| Evidence | Table / field | Writer |
|---|---|---|
| Successful sign-in (method, IP, UA) | `AuthEvent` | Auth.js `events.signIn` → `src/lib/auth-events.ts` |
| Lesson opened (first + last) | `LessonProgress.firstViewedAt` / `lastViewedAt` | Lesson page → `recordLessonView` in `src/lib/content-events.ts` |
| Ebook download | `DownloadEvent` | `/api/downloads/[slug]/[format]` → `recordDownload` |
| ToS checkbox + buyer meta | `Purchase.termsAcceptedAt`, `buyerIp`, `buyerUserAgent`, `policyVersion` | Checkout metadata → fulfilment; version from `CHECKOUT_POLICY_VERSION` in `src/lib/policy-version.ts` |
| Provider-accepted mail | `SentEmail` | `sendEmail` in `src/lib/mail.ts` |
| Dispute opened | Email to `SUPPORT_EMAIL` | `charge.dispute.created` in `src/app/api/stripe/webhook/route.ts` |
| Buyer record + export | `/admin/buyers`, `/admin/buyers/[userId]`, `…/export` | `src/lib/dispute-evidence.ts` |

Shared request meta: `src/lib/request-meta.ts` (`x-forwarded-for` → `x-real-ip` → `user-agent`, capped at 500 chars).

## Checkout consent details

`consent_collection.terms_of_service = "required"` with custom text linking:

- `https://www.swipefiles.com/legal/terms`
- `https://www.swipefiles.com/legal/course-refund-policy`

**Deploy prerequisite:** Stripe Dashboard → Settings → Public details must set a Terms of Service URL. If missing, the Swipe Files helper logs and retries checkout *without* the checkbox so payment still works — which means **no consent is captured**. Set the URL before relying on this.

One-click upsell (off-session): stamps IP/UA/policy version from the buyer's request; `termsAcceptedAt` stays null because no checkbox is shown.

## Policy work (and what was deliberately not decided)

- Fixed `terms.md` link to `/refunds` (404) → `/legal/refund-policy`, plus redirect.
- Added `/legal/course-refund-policy` that **quotes existing wording only** (no new day windows).
- `CHECKOUT_POLICY_VERSION` (`"2026-11-19"`) stamped on new purchases; bump on any terms/refund copy change.

### Example of what NOT to silently resolve

Published promises still conflict, and **PR #97 left both alone**:

- Membership `/legal/refund-policy`: "within **2 days**…"
- Course landing (`CourseLanding.tsx`): "email me within **30 days**…"

The course refund page presents each under its own heading because that is how each is written today. The open questions (does 2-day cover courses? do coupon/final-sale rules apply to the Masterclass?) were flagged to Corey through Support. Once decided, edit the policy files and bump `CHECKOUT_POLICY_VERSION`.

When you port this skill: **flag conflicting windows the same way. Do not pick a number.**

## Mail tracking caveats

`sendEmail` returns `{ ok, messageId? }` and writes `SentEmail` on success. Open/click tracking stayed **off** in code:

- Resend tracking is per-domain (dashboard), not per message in the installed SDK.
- PostShiba public docs did not list safe tracking fields; unknown fields risk rejecting sign-in mail.

`messageId` still lets support look up delivery in the provider dashboard. If tracking is enabled later, prefer **open-only** for transactional mail — click rewriting can burn single-use magic links (or a scanner can).

## Dispute alert

On `charge.dispute.created`: read charge (read-only) → resolve buyer → email `SUPPORT_EMAIL` (default `corey@swipefiles.com`) with id, amount, reason, due date, customer email, counts, UTC timeline, admin link. Failed send → 500 for Stripe retry. **No evidence submit.**

Webhook setup: add `charge.dispute.created` to the endpoint's events in Stripe.

## Admin

- `/admin/buyers?email=…` search
- `/admin/buyers/[userId]` merged timeline
- `export?format=csv` → `at,kind,detail` for Stripe `access_activity_log`
- `export?format=json` → full bundle
- Requires `User.isAdmin`; else 404. Under `src/app/admin/` (outside marketing `(site)`). `/admin` disallowed in `robots.txt`.

## Log retention

Vercel runtime logs ~23 hours on typical plans. PR documented drain options (Axiom, Better Stack, Datadog, self-hosted S3/R2) and recommended ≥ ~120 days. **No vendor purchased.**

## Limits to remember when reusing

- Rows exist **from deploy onward only** — no help for disputes already open.
- Evidence is for a human; Stripe submit stays manual.
- Policy day-windows are a product decision, not an engineering one.
