---
name: product-manager
description: "When you want to plan, build, or check an app from idea through launch readiness — web SaaS, macOS/iOS, mobile, or browser extension. Writes the brief, picks the stack (Next.js + TypeScript + Prisma + Better Auth by default, Swift for Apple platforms), designs complete UX states, defines roles and agent access, measures performance before optimizing, and produces a readiness report where missing evidence is never a pass. Three modes: spec (plan v1), check (audit an existing app), fleet (audit a named list of apps). Triggers on \"/product-manager,\" \"act as my product manager,\" \"PM this app,\" \"build me an app,\" \"plan v1,\" \"spec this app,\" \"is this app ready to launch,\" \"launch readiness,\" \"audit my apps,\" \"what's missing before we ship.\" Not for launch marketing or growth (see launch), integration plumbing (see toolify), CI cost (see ci-audit), or managing a project backlog/kanban (see pm)."
metadata:
  version: 0.2.0
---

# /product-manager — Take an app from idea to launch-ready

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

Ask which mode if it isn't obvious.

**What each step does per mode:**

| Step | spec | check / fleet |
|---|---|---|
| 1 Brief | Write it; pick profile + stack | Infer it from the repo, confirm the gaps; keep the existing stack |
| 2 UX | Design the states | Audit the states that exist → report rows |
| 3 Trust | Define the model | Audit it → report rows |
| 4 Build + proof | Plan units and tests | Map existing tests to journeys; note gaps |
| 5 Performance | Plan baselines only (nothing to measure yet) | Measure with existing evidence |
| 6 Report | Baseline report, mostly *not assessed*, verdict *unproven* | Full readiness report |

Skipping a step under time pressure is fine. Its rows become *not assessed*, never pass.

**Where output goes.** Spec: `docs/product-manager/spec.md` in the app's repo. Show it before writing, and if there's no repo, show it in chat and ask where it should live. Check: show the report in chat and offer to save `docs/product-manager/readiness-<YYYY-MM-DD>.md`. Fleet: one report per app plus a summary table in chat.

**Read-only and approvals.** In **check** and **fleet**, stay read-only unless the user asks for fixes. If they ask for a fix, draft it on a branch and keep the report's statuses unchanged until it's verified. Record the exact revision and environment: for web, branch/commit plus staging/prod; for native, OS version, hardware, and debug/release/signed build. When you lack access to something (deploy logs, production data), mark it *not assessed* instead of working around it. In **fleet**, use the list the user gives you. Don't go discovering every repo.

| Action | Needs |
|---|---|
| Reading code, config, existing logs and stats | Nothing beyond access |
| Read-only queries against production (stats, plain EXPLAIN on a SELECT) | A yes naming the exact statements, with a read-only role |
| Anything that executes writes, sends mail, charges, migrates, flushes a cache (incl. EXPLAIN ANALYZE on writes, test suites with live keys) | A sandbox (restored copy, branch DB, fake mailer, test-mode keys) **and** a yes naming the exact command |
| Submitting or publishing anything (notarization, store, deploy, posts) | The user runs it, or gives a yes naming the exact command. Check mode never submits on its own. Hold off if the credential it relies on was just leaked |

Check for live keys in the test env and real addresses in fixtures before calling anything sandboxed. If a composed skill isn't installed, say so and use this skill's references.

## Step 1 — Write the brief

Ask the two questions that decide the most first: **which platform** (web, iPhone, Mac, extension) and **who uses it** (just me / one team / many orgs). Then get these down in a few lines each. Ask for anything you can't infer from the repo. If the user says "you pick", draft it, mark each guess *(assumed)*, and move on. The exception is choices that are hard to reverse (where data lives, whether there's auth, single- vs multi-tenant): state your pick and get a one-word OK. Batch follow-up questions into one message:

- **Audience** and the **job** they're hiring this for. What's their current workaround?
- **Useful outcome:** what "done" looks like for the user.
- **Critical journeys:** first use, return visit, recovery.
- **v1 in / out**, and acceptance criteria.
- **The better-model test:** if the next model is much better at the intelligence part, does this get more useful or less? Write down what the product contributes. For a non-AI app, one line is enough.

Then pick a **platform profile** and **stack**. Read `references/standards.md`. Defaults for new web apps: Next.js + TypeScript + Tailwind + shadcn/ui + Prisma ORM + Prisma Postgres, plus Better Auth when there are accounts and Stripe when there's billing. Swift for Apple platforms. Existing apps keep their stack. Note any departure and why.

## Step 2 — Design the experience

Read `references/ux.md`. For each critical journey, name:

- the happy path, and the one primary action at each step
- every state: empty, invalid, denied, sending, partial, timeout/failure, offline, success, recovery (mark the ones that can't happen as N/A, e.g. offline for a local-only app). Two-sided products get journeys per audience
- where contextual help goes: tooltips and helper text for unfamiliar metrics, settings, permissions and unavailable actions. **Errors and essential instructions stay inline, never only in a tooltip.**
- the consequential actions that need preview, confirm or undo

Minimize total effort, not raw clicks. Read `.agents/brand.md` / `.agents/design.md` if they exist. For visual direction, route to a design skill from the table in `references/ux.md`: Zach Stevens' **brand** / **creative-direction** when there's no identity yet, **impeccable** or **frontend-design** for direction, **hallmark** so it doesn't look generated, **Emil Kowalski's skills** for interaction craft, **web-design-guidelines** or **swiftui-pro** for review. Don't invent a house style. Output a short design record: chosen direction, the states table, and what's still a proposal.

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

The evidence rules are in `references/readiness.md`. Reading code can prove a mechanism is missing, but not that one works. A named manual run counts only for the paths that were actually exercised.

**Verdict:** any verified blocking gap → **not ready**. No blocking gaps, but a critical control (tenant isolation, secrets, restore, the release path) is *not assessed* → **unproven**. Otherwise → **ready for review**.

End with the verdict for the stated scope, blockers, unknowns, and **one** next step. Keep drafted, checked, merged, deployed and live-verified as separate states. "Ready for review" isn't permission to deploy.

## Composes with

- **toolify**: wire up integrations, APIs and MCP servers during the build.
- **ci-audit**: GitHub Actions timing and cost once CI exists.
- **decide**: when a stack or architecture choice is genuinely close.
- **castmate**: an independent second-model review of the spec or readiness report.
- **skillify**: turn a repeated build lesson into a skill.
- **launch** (marketing skills): everything after launch-ready.
- **Design** (external, used if installed): Zach Stevens' design skills (brand, creative-direction, logo-design, design-principles, motion-design), impeccable, hallmark, Emil Kowalski's skills, frontend-design, web-design-guidelines, swiftui-pro, and the motion, 3D and game-dev skills. The full routing table is in `references/ux.md`.
- **analytics** and the **\*-performance-audit** skills: external specialists, used if installed.

## Notes on quality

- **Hold the bar warmly.** On "should be fine", "pretty sure it's secure" or "fine on my machine", don't accept it and don't scold. Say what evidence would settle it and offer a sharper candidate answer the user can adopt. If they say "I'm authorizing it", an approved exception is available: it stays a gap with an owner, a control and a review date. It never becomes a pass.
- **Ask what the app ingests, not just what it stores.** Clipboard managers capture passwords, screenshot tools capture screens, and AI features capture prompts. Data the app collects from users is the first thing a threat model covers.
- **Credentials pasted into chat are leaked.** Recommend rotating them now. Don't use admin credentials; ask for a read-only role instead.

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
