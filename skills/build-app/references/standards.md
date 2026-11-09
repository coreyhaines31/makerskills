# Standards, stack and platform profiles

## The better-model test

Before committing to a v1, ask: **if the next model is much better at the intelligence part, does this product get more useful or less?**

Build things that complement frontier models, like context, permissions, integrations, workflows and reliable actions. Avoid features whose whole value is "our prompt beats the current model." Write down what the product contributes and what would make it obsolete. That's a design heuristic, not a moat claim.

## Stack defaults

Pick the stack as a system. The tools should work well together and be easy for coding agents to set up, type-check, test and debug. Best-in-class doesn't mean newest.

| Medium | Default | Boundary |
|---|---|---|
| New web app | Next.js (App Router), TypeScript, Tailwind, shadcn/ui, Prisma ORM, Prisma Postgres. Add Better Auth when there are accounts and Stripe when there's billing | Check versions and runtime compatibility before scaffolding |
| macOS / iOS | Swift | Follow platform conventions |
| Hot path that needs raw speed | Rust | Only after profiling shows it's needed. No blanket rewrites |
| Extension / host plugin | Whatever the host requires | Read the host's API, permissions and lifecycle first |

The defaults don't cover object storage, transactional email, background jobs or an LLM provider. When the product needs any of those, list it as an open choice in the brief. Route close calls to **decide**.

Existing apps keep their stack. A Rails app isn't a migration target. Record any departure from the defaults and why.

When comparing serious options, compare whole combinations: compatibility, setup reproducibility, type/lint/test feedback, docs quality, an escape path for your data, operating cost. Don't pick a dependency just because an agent recognizes the name.

**Two different "agent-friendly" questions.** *Can a coding agent work on this codebase safely?* (documented invariants, fast checks, legible errors) is separate from *can an external agent operate this product?* (scoped API/CLI/MCP). An MCP endpoint doesn't make a codebase maintainable, and a well-documented repo isn't automatically a safe MCP server.

## The five outcomes

Every app gets checked against these. **Check whether each one applies to the product. Don't chase feature parity.**

| ID | Outcome | When it applies / what proves it |
|---|---|---|
| O1 | Flexible users, orgs, teams, roles | Collaborative products. Membership matrix, server-side policy, cross-tenant negative tests. A single-user local app can justify no orgs. |
| O2 | Easy feedback **to the builder**: free text, screenshots, video | Every product with users other than the builder. This is product feedback, not in-app comments on the user's own content. A native entry point is fine. Verify consent, preview, private upload scope, failure cases. Text-only is a gap, not an equivalent. Justified N/A when the only user is the builder. |
| O3 | Security that fits the risk | Always. Threat model, least privilege, session/input/webhook/secret controls, named residual risks. Start with what the app **ingests** (passwords on the clipboard, screen contents, tokens in prompts), not only what you store on purpose. |
| O4 | Privacy-aware analytics tied to decisions | When there's something to learn. Event purpose, minimal payload, consent, retention. Local-only / no telemetry can be the right answer. |
| O5 | Useful agent access | When the audience would actually automate it: someone has asked, or the job is repetitive across many records. One real workflow through API/CLI/MCP with the same policy as the UI. Not every wrapper. Otherwise justified N/A, with "revisit if asked". |

Supporting checks: complete UX journeys (see `ux.md`), data lifecycle and conditional billing (`trust.md`), measured performance (`performance.md`), reproducible tests and release readiness (`readiness.md`).

**Likely blockers:** authorization or tenant-isolation failures, data loss, exposed secrets, broken core journeys, unsafe billing, a release or rollback path that doesn't work. Accessibility failures on essential journeys need an explicit decision, not a silent deferral.

**Not gates:** launch posts, SEO, landing-page conversion, acquisition, growth. Those are marketing work. Hand them off.

## Platform profiles

Pick a profile so the checks fit the product. Don't force one SaaS checklist onto every app. These examples are made up.

**Personal single-user app** (e.g. a workout log for yourself, on web or iPhone). No accounts, orgs, billing, analytics or agent access, all justified N/A. O2 is N/A if you're the only user. Local data safety, export, and the recovery journey (app killed mid-task) still apply. Keep v1 small. If it ever gets shared, re-profile.

**Collaborative web SaaS** (e.g. agency staff and clients reviewing shared work). O1–O4 apply. O5 applies when the audience automates. Owner/admin/member/client roles, where clients see less than members do. Billing per org. Caches keyed by tenant *and* audience. Restore drills. The first agent interface is "read a summary, draft an update". Publishing needs separate approval.

**Local macOS utility** (e.g. reopen recent work from the menu bar). Swift, no account, no backend. Orgs, cloud billing and backend checks are justified N/A. Local file safety, export/delete (a real purge: SQLite DELETE leaves data in free pages and the WAL), native feedback capture, permission denial (Accessibility, pasteboard privacy prompts), keyboard/menu behavior, startup and hitch time all still apply. Restore means: the backup loads in a fresh user account, and a corrupt data file doesn't crash or silently wipe. Release means: notarization accepted, ticket stapled, and Gatekeeper passes on a second Mac. Don't install analytics just to turn an N/A into a pass.

**Offline-capable mobile app** (e.g. field notes that sync later). Model draft → queued → uploading → synced / conflicted / failed as distinct states. Preserve input across suspension. Test duplicate sync, account switch, and sign-out clearing local data. VoiceOver, Dynamic Type, power and storage matter. Core Web Vitals don't grade this UI.

**Browser extension / host plugin.** No stack is prescribed. Ask for least-privilege host access and don't read every site by default. Treat page content as untrusted. Test permission revocation, restricted pages, suspend/restart and updates. If it talks to a cloud backend, the backend trust checks apply. It doesn't get a pass for being "just a plugin."
