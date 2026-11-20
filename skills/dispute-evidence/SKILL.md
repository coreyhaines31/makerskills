---
name: dispute-evidence
description: "When you want to add dispute/chargeback/refund evidence logging to an app (sign-in logs, access/download events, checkout ToS consent, policy versioning, email delivery tracking, dispute webhook alerts, admin evidence export, log retention). Triggers on \"dispute evidence,\" \"chargeback evidence,\" \"refund evidence,\" \"fight chargebacks,\" \"access activity log.\" Product instrumentation, not marketing copy — marketingskills refunds/paywalls write offers; this records proof of access. Load references/checklist.md and references/worked-example-swipefiles.md."
metadata:
  version: 0.1.0
---

# /dispute-evidence — Instrument an app so you can fight chargebacks

Turn "the buyer never used it" into rows: sign-ins, content views, downloads, checkout consent, mail delivery, and a support alert when a dispute opens. Evidence is **read-only for a human**. Nothing in this skill submits evidence to Stripe or changes a dispute's status.

Reference stack is Next.js + Prisma + Auth.js + Stripe + Resend (or similar). Adapt table/hook names to Rails, Laravel, etc. The checklist stays the same.

Worked example: Swipe Files draft PR [conversionfactory/swipefiles-nextjs#97](https://github.com/conversionfactory/swipefiles-nextjs/pull/97). Details in `references/worked-example-swipefiles.md`. Printable audit list in `references/checklist.md`.

## Hard rules (never skip)

1. **Never auto-submit evidence to Stripe.** Assemble a summary and alert a human. The human decides what to upload.
2. **Never change published refund policy windows** without an explicit product decision. If membership says 2 days and a course page says 30, flag it and leave both alone until the owner picks.
3. **Evidence writes are best-effort.** A failed AuthEvent / view / download / SentEmail write must never block sign-in, checkout, fulfilment, or mail send. Log and continue.
4. **New tables help only after deploy.** No backfill of past disputes. Say that clearly in the PR.
5. **Don't buy a log-drain vendor** without the owner's OK. Recommend options with retention ≥ ~120 days.

## Step 0 — Scope the target app

Confirm with the user:

- Which repo / production app.
- Payment provider (Stripe Card disputes, PayPal, etc.).
- Auth strategy (JWT sessions with no server session table? Cookie sessions? Devise?).
- Whether an admin surface already exists.
- Support alert destination (team inbox, Slack, both).

Read `CLAUDE.md` / `AGENTS.md` if present for stack defaults. Then load `references/checklist.md`.

## Step 1 — Audit for evidence gaps

Walk the app and score each row green / yellow / missing:

| Area | What "green" looks like |
|---|---|
| **Auth** | Successful sign-ins persisted with method, IP, user agent |
| **Content access** | First + last view on lessons/pages; separate download events for files |
| **Checkout consent** | Payment provider requires ToS acceptance; Purchase/Order stores acceptance time, buyer IP/UA, policy version |
| **Policies** | Refund/terms links resolve; product-specific vs membership policies are clear; conflicting windows flagged to a human |
| **Mail** | Provider message id stored per send; open/click tracking documented (off by default for magic links) |
| **Dispute webhook** | `charge.dispute.created` (or equivalent) alerts support with a read-only evidence summary |
| **Admin export** | Buyer timeline + CSV/JSON shaped for Stripe `access_activity_log`; admin-only |
| **Log retention** | Runtime logs kept ≥ ~120 days, or a drain recommended (not purchased) |

Show the gap table to the user before writing code. Prefer small issues or one PR covering the missing rows.

## Step 2 — Implement (stack-appropriate)

Order that usually unblocks evidence fastest:

1. **AuthEvent (or equivalent)** — on successful sign-in, record `userId`, method (`magic_link`, `oauth:google`, …), IP, UA, timestamp. Cap IP/UA strings (~500 chars). Prefer request headers `x-forwarded-for` (first hop) then `x-real-ip`.
2. **Content access** — on lesson/page load: set `firstViewedAt` once, always bump `lastViewedAt`. Do **not** mark complete. Downloads get their own event rows (slug, format, IP, UA), not a generic activity dump.
3. **Checkout consent** — Stripe: `consent_collection.terms_of_service = "required"` plus `custom_text.terms_of_service_acceptance` linking terms **and** refund policy. Stamp Purchase/Order with `termsAcceptedAt`, `buyerIp`, `buyerUserAgent`, `policyVersion`. Pass IP/UA/version through checkout metadata if fulfilment is async. Off-session one-click upsells: stamp IP/UA/version from the buyer's request; leave `termsAcceptedAt` null if no checkbox was shown.
4. **Policy versioning** — one constant (e.g. `CHECKOUT_POLICY_VERSION` date string) stamped on every new purchase. Bump whenever terms or refund copy changes. Fix broken refund links / redirects. Quote existing policy wording on product-specific pages; don't invent new day windows.
5. **SentEmail** — after the provider accepts the message, persist `to`, `subject`, provider, `messageId`, optional `userId`. Document open/click tracking caveats: click rewriting can burn single-use sign-in links; prefer open-only for transactional mail, or keep tracking off and look up delivery in the provider dashboard via `messageId`.
6. **Dispute webhook** — on `charge.dispute.created`: resolve buyer (PaymentIntent → Purchase, then charge metadata `userId`, then billing email), load the evidence bundle, email/Slack support with dispute id, amount, reason, due date, customer email, counts, UTC timeline, and admin deep link. Failed alert → non-2xx so the provider retries. **No Stripe evidence submit.**
7. **Admin buyer record** — search by email; detail page merges purchases, entitlements/access, progress, auth events, downloads, emails into one timeline. CSV export columns `at,kind,detail` for Stripe's access activity log. JSON for the full bundle. Admin-only (404 otherwise). Keep URLs out of marketing analytics if possible.
8. **Log drain note** — document that host runtime logs (~23h on typical Vercel plans) are gone by dispute time. Recommend a drain to Axiom / Better Stack / self-hosted object storage with ≥ ~120 day retention. List options; don't purchase.

All writers: try/catch, log failure, never throw into the user path.

## Step 3 — Tests and docs

- Unit/integration tests for: auth event write, lesson first/last view, download event, checkout consent fields / metadata, dispute alert assembler (mock provider; assert no evidence-submit API call).
- Short `docs/dispute-evidence.md` (or equivalent) listing tables, writers, deploy prerequisites, and any open policy conflicts.
- PR body must call out: no Stripe submit, no policy-window changes, rows only after deploy, and the deploy checklist below.

## Step 4 — Deploy prerequisites (PR checklist)

Before calling the work "done in production":

1. Payment dashboard public details: Terms of Service URL set (Stripe rejects ToS consent otherwise; some apps fall back to checkout *without* the checkbox — that means no consent captured).
2. Webhook endpoint includes `charge.dispute.created` (or the provider's dispute-opened event).
3. Migrations applied; optional `SUPPORT_EMAIL` / Slack webhook env set.
4. Smoke: one test sign-in, one content view, one checkout in test mode, confirm rows + admin export.
5. Remind the owner: **past disputes get nothing new** until this is live.

## Composes with

- `product-manager` — when an audit or launch checklist flags missing commerce trust / dispute readiness.
- `toolify` — wiring Stripe webhooks, Resend/Postmark, or a log-drain integration.
- `project-manager` — tracking the open policy-window decision and drain-vendor choice as owner decisions.
- `skillify` — when a second app teaches a better pattern; UPDATE this skill rather than forking it.

## Notes on quality

- **Human in the loop on disputes.** Auto-alert yes; auto-submit never.
- **Flag policy conflicts; don't silently pick a window.** The Swipe Files 2-day vs 30-day case is the worked example of what not to resolve alone (`references/worked-example-swipefiles.md`).
- **Best-effort or it will be deleted.** If evidence writes break checkout, someone will rip them out under incident pressure.
- **Views ≠ completions ≠ downloads.** Keep them separate so a "Mark complete" click can't be spun as the only proof of access.
- **JWT auth means no login history until you add it.** Don't assume a Session table exists.
- **Name capabilities, not host tools.** "Fetch the repo file," not a specific agent tool id.
- **v0.1 stays tight.** Checklist + one worked example. Add Rails/Laravel recipes only after a second real port.
