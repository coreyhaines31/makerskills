# Dispute evidence — audit checklist

Print or copy into the PR. Mark each row **green / yellow / missing**, then implement missing ones in stack-appropriate form.

Target app: _______________  
Date: _______________  
Auditor: _______________

## Auth

- [ ] Successful sign-ins are persisted (not only JWT/cookie issuance)
- [ ] Each row has: user id, method, IP, user agent, timestamp
- [ ] Write failures never block sign-in

## Content access

- [ ] Lesson/page load sets first-view once and bumps last-view
- [ ] "Mark complete" is separate from view tracking
- [ ] File/ebook downloads are distinct event rows (slug, format, IP, UA)
- [ ] Write failures never block the page or download

## Checkout consent

- [ ] Payment provider requires ToS acceptance at checkout
- [ ] Custom text links both terms and refund policy
- [ ] Purchase/Order stores: acceptance time, buyer IP, buyer UA, policy version
- [ ] Async fulfilment receives IP/UA/version via metadata (or equivalent)
- [ ] Off-session / one-click upsells documented (what is stamped vs left null)
- [ ] Dashboard public ToS URL is set (or consent is skipped — call that out)

## Policies

- [ ] `/refunds` (or equivalent) does not 404; redirects or links are fixed
- [ ] Product-specific vs membership refund policies are clearly separated
- [ ] Conflicting windows (e.g. 2 days vs 30 days) flagged to a human — **not silently resolved**
- [ ] Policy version constant exists and is stamped on new purchases
- [ ] Bump instructions documented for future copy edits

## Mail

- [ ] Provider message id persisted after accept (`SentEmail` or equivalent)
- [ ] Optional user id when known
- [ ] Open/click tracking: on/off documented; magic-link burn risk noted
- [ ] Write failures never block the send path after the provider accepts

## Dispute webhook

- [ ] Provider event for dispute opened is handled (`charge.dispute.created` on Stripe)
- [ ] Buyer resolved via PaymentIntent → order, then metadata, then billing email
- [ ] Support alert includes: dispute id, amount, reason, due date, email, counts, UTC timeline, admin link
- [ ] Failed alert returns non-success so the provider retries
- [ ] **No** call that submits evidence or updates dispute status

## Admin export

- [ ] Search buyer by email
- [ ] Detail page: purchases, entitlements/access, progress, auth, downloads, emails, merged timeline
- [ ] CSV shaped for Stripe `access_activity_log` (`at,kind,detail`)
- [ ] JSON full bundle
- [ ] Admin-only (404 for everyone else)
- [ ] Buyer PII URLs kept off marketing analytics where possible

## Log retention

- [ ] Host runtime log retention checked (often ~1 day)
- [ ] Drain options listed with ≥ ~120 day retention
- [ ] No vendor purchased without owner OK

## Ship gates

- [ ] Tests cover writers + dispute alert assembler (no submit API)
- [ ] Docs list tables, writers, deploy prerequisites, open policy questions
- [ ] PR states: no Stripe submit, no policy-window changes, no backfill
- [ ] Webhook event enabled in provider dashboard
- [ ] Migrations applied in production before calling it done
