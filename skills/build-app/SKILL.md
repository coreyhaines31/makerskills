---
name: build-app
description: "When you want to plan, build, or check an app from idea through launch readiness — web SaaS, macOS/iOS, mobile, or browser extension. Writes the brief, picks the stack (Next.js + TypeScript + Prisma + Better Auth by default, Swift for Apple platforms), designs complete UX states, defines roles and agent access, measures performance before optimizing, and produces a readiness report where missing evidence is never a pass. Three modes: spec (plan v1), check (audit an existing app), fleet (audit a named list of apps). Triggers on \"/build-app,\" \"build me an app,\" \"plan v1,\" \"spec this app,\" \"is this app ready to launch,\" \"launch readiness,\" \"audit my apps,\" \"what's missing before we ship.\" Not for launch marketing or growth (see launch), integration plumbing (see toolify), or CI cost (see ci-audit)."
metadata:
  version: 0.1.0
---

# /build-app — Build coherent apps through launch readiness

Most apps that fail at launch don't fail on the main feature. They fail on what nobody specced: a client who can download another client's files, an invite button that sends twice on a slow network, a backup nobody ever restored, a cache keyed on project ID that leaks internal notes. This skill makes you decide those things up front, and then proves them before calling anything ready.

It ends at **launch-ready**, not launched. Promotion, SEO, launch posts and growth go to the marketing skills.

## Mental model

- **Applicability, not parity.** A local macOS timer doesn't need organizations. A collaborative SaaS does. Choose a platform profile, then check what applies.
- **Evidence, not vibes.** Every requirement ends up as pass, gap, not assessed, or justified N/A. Missing evidence isn't a pass.
- **Measure, then fix.** Broken before slow. Baseline before cache.
- **Complement the model.** Build what gets *more* useful as models improve.

## Step 0 — Pick the mode

| Mode | When | Output |
|---|---|---|
| **spec** | New app or v1 plan | Brief, stack, UX states, access model, test plan |
| **check** | Existing app, "are we ready?" | Readiness report (read-only by default) |
| **fleet** | A named list of apps | One short report per app + a cross-app summary |

Ask which mode if it isn't obvious. In **check** and **fleet**, stay read-only unless the user asks for fixes. Record the exact revision and environment you looked at. When you lack access to something (deploy logs, production data), mark it *not assessed* instead of working around it. In **fleet**, use the list the user gives you. Don't go discovering every repo.

Before any test that could send mail, charge a card, run a migration, flush a cache or hit production, confirm it's sandboxed and get a yes.

## Step 1 — Write the brief

Get these down in a few lines each (ask for anything you can't infer from the repo):

- **Audience** and the **job** they're hiring this for. What's their current workaround?
- **Useful outcome:** what "done" looks like for the user.
- **Critical journeys:** first use, return visit, recovery.
- **v1 in / out**, and acceptance criteria.
- **The better-model test:** if the next model is much better at the intelligence part, does this get more useful or less? Write down what the product contributes.

Then pick a **platform profile** and **stack**. Read `references/standards.md`. Defaults: Next.js + TypeScript + Tailwind + shadcn/ui + Prisma ORM + Prisma Postgres + Better Auth + Stripe for new web apps, and Swift for Apple platforms. Existing apps keep their stack. Note any departure and why.

## Step 2 — Design the experience

Read `references/ux.md`. For each critical journey, name:

- the happy path, and the one primary action at each step
- every state: empty, invalid, denied, sending, timeout, offline, success, recovery
- where contextual help goes: tooltips and helper text for unfamiliar metrics, settings, permissions and unavailable actions. **Errors and essential instructions stay inline, never only in a tooltip.**
- the consequential actions that need preview, confirm or undo

Minimize total effort, not raw clicks. For visual direction, route to **frontend-design**, **web-design-guidelines** or **swiftui-pro** if they're installed. Don't invent a house style. Output a short design record: chosen direction, the states table, and what's still a proposal.

## Step 3 — Define boundaries and trust

Read `references/trust.md`. Check the five outcomes against the profile:

1. **Users, orgs, teams, roles** (if collaborative): access matrix and negative tests.
2. **Feedback:** free text, screenshots, video, with consent and private uploads.
3. **Security that fits the risk:** threat model, least privilege, secrets, sessions, webhooks.
4. **Privacy-aware analytics:** decisions first, minimal payloads, or none at all.
5. **Agent access:** one useful workflow through API/CLI/MCP, using the same policy as the UI.

Mark each applies / justified N/A. Don't add infrastructure just to tick a box. Keep the two "agent-friendly" questions apart: a codebase a coding agent can safely change, and a product an external agent can safely operate.

## Step 4 — Plan the build and its proof

Break accepted requirements into small units, each with an acceptance check and a rollback. Read the testing section of `references/readiness.md`. Map each critical journey and invariant to its cheapest meaningful proof: unit tests for policy, integration tests for tenant boundaries and webhooks, a few e2e tests for real journeys.

If the user wants it built, build it in small commits following the repo's workflow. Route integration plumbing to **toolify** and GitHub Actions cost and timing to **ci-audit**.

## Step 5 — Measure performance, then improve

Read `references/performance.md`. If **front-end-performance-audit**, **back-end-performance-audit** or **database-performance-audit** are installed, use them. Otherwise follow the reference.

Broken before slow → baseline → find the limiter → rank → user picks → apply → remeasure comparably. Fill in the cache contract before recommending any cache. Authorization is still checked on every cache hit. Never claim a speedup you didn't measure.

## Step 6 — Readiness report

Read `references/readiness.md` and fill in its report template. One row per applicable requirement:

- **pass**: verified at a stated revision and environment
- **gap**: verified as unmet; say if it blocks
- **not assessed**: no access, no evidence, or not tested
- **justified N/A**: doesn't apply to this profile, with the reason

End with the verdict for the stated scope, blockers, unknowns, and **one** next step. Keep drafted, checked, merged, deployed and live-verified as separate states. "Ready for review" isn't permission to deploy.

## Composes with

- **toolify**: wire up integrations, APIs and MCP servers during the build.
- **ci-audit**: GitHub Actions timing and cost once CI exists.
- **decide**: when a stack or architecture choice is genuinely close.
- **castmate**: an independent second-model review of the spec or readiness report.
- **skillify**: turn a repeated build lesson into a skill.
- **launch** (marketing skills): everything after launch-ready.
- **frontend-design**, **web-design-guidelines**, **swiftui-pro**, **analytics**, and the **\*-performance-audit** skills: external specialists, used if installed.

## Notes on quality

- **Tooltips supplement, they don't hide.** "Put every error in a tooltip to save space" is wrong. Essentials stay inline, and a tooltip on a native disabled button is unreachable by keyboard.
- **"Make it fast, add Redis everywhere" gets a baseline first.** No TTL or cache layer without measured repeated work and a complete key including the tenant and audience.
- **Revoked access beats cache.** If a revoked user still gets a cached summary, that's a blocking isolation bug, and a TTL won't fix it.
- **Backup ≠ restore.** Restore stays *not assessed* until someone restores to an isolated environment.
- **Fewer tests isn't faster.** Reject speedups that come from dropping work.
- **EXPLAIN ANALYZE runs the query.** Rolling back doesn't undo every side effect. Don't run it against production writes without a yes.
- **An MCP endpoint doesn't make a codebase agent-friendly.** Agent-friendly development and agent operation are separate checks.
- **A local app isn't a failed SaaS.** No orgs, no backend, no telemetry can all be justified N/A.
- **No access means not assessed.** Never "probably fine", and never a credential workaround.
- **Growth isn't a gate.** If asked to add launch posts or SEO to readiness, keep them out and hand off to marketing.
- **Don't promise a moat.** The better-model test is a heuristic, not a guarantee.
