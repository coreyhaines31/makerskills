---
name: toolify
description: When you want to integrate an external tool, API, MCP server, or service into a project — the wizard walks you through auth, config, env vars, client wrapper code, example usage, and (optionally) a smoke-test. Scoped to Next.js and Rails projects (the two primary stacks). Interactive Q&A pattern — starts with the tool name, asks structured questions until the integration is fully specified, then scaffolds files. Examples of tools to toolify — Stripe, Kit, Sanity, Notion, Neon, Supabase, Fathom, Rewardful, SavvyCal, Riverside, ScrapeCreators, Anthropic, OpenAI, Gemini, Twilio, Resend, Postmark, Vercel Blob, custom internal APIs. For MCP servers specifically, also handles the .mcp.json wiring. Triggers on "/toolify," "integrate X," "add X to this project," "wire up X," "set up the X integration," "hook up X," "connect X," "add MCP for X." Part of the -ify trifecta (skillify / toolify / loopify) for extending Claude Code. NOT for adding new SKILL.md files — that's skillify. NOT for cron/agent loops — that's loopify.
metadata:
  version: 0.1.0
---

# /toolify — Wire up an integration or MCP server

Interactive wizard for adding an external tool / API / MCP into a project. Ends with working code + env vars set + a verification path.

## Scope

- **Primary stacks**: Next.js (App Router + TypeScript) and Rails. Reason: those are the two stacks the user actually ships in; supporting every stack bloats the wizard.
- **What toolify handles**: auth pattern (API key, OAuth, JWT, session cookie), env var setup, official SDK vs raw fetch, client wrapper location, example usage, webhook handling (if applicable), MCP `.mcp.json` wiring (if MCP server).
- **What toolify does NOT handle**: writing business logic on top of the integration (that's for the human). It scaffolds the *plumbing*, not the *feature*.

## Step 0 — Get the tool name

Ask if not provided: *"Which tool are we integrating?"*

Detect category from name:

| Category | Examples | Extra steps |
|---|---|---|
| **Payments** | Stripe, LemonSqueezy, Paddle | Webhook signature verification, customer model, event handlers |
| **Auth** | NextAuth/Auth.js, Clerk, Supabase Auth, Devise | Session management, protected routes, callbacks |
| **Email** | Resend, Postmark, SendGrid, Kit | From address, template setup, unsubscribe handling |
| **CMS/DB** | Sanity, Prisma, Drizzle, Neon, Supabase | Schema location, migration path, client singleton pattern |
| **AI/LLM** | Anthropic, OpenAI, Gemini, Vercel AI SDK | Model choice, streaming vs non-streaming, rate limits |
| **Analytics** | Fathom, PostHog, Plausible | Script placement, event tracking API |
| **Scheduling/Comms** | SavvyCal, Cal.com, Twilio, Riverside | Webhook events, embed patterns |
| **Scraping** | ScrapeCreators, Apify, Playwright | Rate limits, response caching, retry policy |
| **Affiliate/Referral** | Rewardful, PartnerStack | Cookie handling, webhook events, dashboard access |
| **Storage** | Vercel Blob, S3, R2 | Bucket setup, signed URL pattern, presigned upload |
| **MCP server** | Any MCP — Sanity, Stripe, GitHub, Kit, etc. | `.mcp.json` entry + env vars, no client wrapper |
| **Custom / other** | Internal API, unknown tool | Ask more questions |

If category detection fails, ask 2 questions to place it: *"Is it an API you call, a webhook receiver, or both?"* / *"Does it have an official SDK?"*

## Step 1 — Structural interview

Ask the following in order (skip questions that don't apply based on category):

1. **Which project?** (path — infer from cwd; ask if ambiguous)
2. **Which stack?** (Next.js / Rails — infer from `package.json` vs `Gemfile`; ask if both)
3. **Auth pattern?** (API key / OAuth / JWT / session cookie / signed webhooks — usually knowable from official docs)
4. **Official SDK exists?** (check the docs; prefer SDK when good; fall back to raw fetch when SDK is bloated/abandoned)
5. **Env var name convention?** (default: `SCREAMING_SNAKE_CASE` matching official convention — e.g., `STRIPE_SECRET_KEY`, `RESEND_API_KEY`)
6. **Environments?** (dev / preview / prod — different keys?)
7. **Webhook receiver needed?** (YES for Stripe/Rewardful/most payment+auth+CMS; NO for pure client-side or read-only APIs)
8. **Rate limits to respect?** (grep official docs)
9. **Where does the client wrapper live?** (default: `src/lib/<tool>.ts` for Next.js; `app/services/<tool>_client.rb` for Rails)

Show the user the answers as a summary before scaffolding — one chance to correct before writing files.

## Step 2 — Fetch official setup docs

Use `WebFetch` or `context7:query-docs` to pull the *current* official quickstart:

```bash
# Prefer context7 if available (fresher docs than training data)
Skill({skill: "compound-engineering:context7", ...})

# Fallback to WebFetch
WebFetch <official-quickstart-url>
```

Read *once*, then work from cached content. Don't re-fetch mid-scaffold. Note the SDK version cited so `package.json` gets the right pin.

## Step 3 — Scaffold files

For a **standard Next.js integration**, generate:

```
src/lib/<tool>.ts                    # client singleton + typed wrappers
src/app/api/webhooks/<tool>/route.ts # webhook handler (if applicable)
src/app/api/<tool>/example/route.ts  # one working example route
.env.local.example                    # env var template with placeholder values
```

For **Rails**:

```
config/initializers/<tool>.rb        # SDK config
app/services/<tool>_client.rb        # client wrapper
app/controllers/webhooks/<tool>_controller.rb  # webhook handler if applicable
config/routes.rb                      # webhook route
.env.example                          # env vars
```

For an **MCP server**, only:

```
.mcp.json                             # add or update with the new server entry
.env.local                            # add the env vars the MCP needs
```

Every scaffolded file should have a comment at the top like:

```typescript
// Scaffolded by /toolify on 2026-06-30. Official docs: <url>. SDK version: <version>.
// The client wrapper is scoped to plumbing only — business logic lives elsewhere.
```

## Step 4 — Auth pattern implementation

Apply the right auth pattern per tool category. Never invent — use the pattern the official docs specify. Common patterns:

- **API key in header**: `Authorization: Bearer <key>` or `X-<Vendor>-Key: <key>` — check vendor's exact spelling
- **Webhook signature**: use the vendor's crypto method (Stripe uses HMAC-SHA256; Rewardful uses similar). NEVER skip signature verification on webhooks — it's the #1 security bug in scaffolded integrations.
- **OAuth**: redirect URL setup, token storage, refresh handling. Prefer Auth.js/NextAuth for Next.js; Devise + omniauth for Rails.
- **Signed URL / presigned**: for uploads / temp access — set expiration explicitly, never use unbounded.

## Step 5 — Env var setup

Add to the appropriate file:

- **Local dev**: `.env.local` (Next.js) / `.env` (Rails) — NEVER committed
- **Vercel**: `vercel env add <VAR> production --value "<value>" --no-sensitive --yes` (use `--no-sensitive` for any `NEXT_PUBLIC_*` var per user's global CLAUDE.md — see `references/vercel-env-vars.md`)
- **Heroku**: `heroku config:set <VAR>=<value> -a <app-name>`

Also update `.env.example` / `.env.local.example` with the placeholder so teammates know the var is needed.

## Step 6 — Smoke test

Generate a one-line verification the user can run:

```bash
# Example for a REST API:
curl -H "Authorization: Bearer $STRIPE_SECRET_KEY" https://api.stripe.com/v1/customers?limit=1

# Example for an SDK:
node -e "const s = require('./src/lib/stripe.ts').default; s.customers.list({limit:1}).then(console.log)"

# For MCP: restart Claude Code, run any command that touches the MCP server
```

Show the expected output shape. If the call fails, the wizard should be first to catch it, not the user in prod.

## Step 7 — Report + follow-ups

Report:
- Files created (paths)
- Env vars added (names only — never values in the report)
- SDK/dependency added to `package.json` / `Gemfile`
- Smoke-test command run + result
- Any TODOs the user needs to complete manually (e.g., "add webhook URL to <vendor> dashboard")

Offer:
- *"Set up a `loopify` cron to check the webhook is still receiving events daily?"*
- *"Save this integration recipe as a skill via `skillify from-chat`?"*
- *"Commit these changes now?"*

## Reference — integration recipes

Full recipes for common tools live in `references/` (populate as they're used):

- `references/stripe-nextjs.md` — payment integration + webhook + customer portal
- `references/kit-nextjs.md` — Kit (ConvertKit) MCP + subscriber API
- `references/sanity-nextjs.md` — Sanity CMS + MCP + Studio embed
- `references/anthropic-nextjs.md` — Claude API + streaming + rate limits
- `references/scrapecreators-nextjs.md` — social scraping API + retry policy
- `references/rewardful-nextjs.md` — referral tracking + webhook events

If a recipe doesn't exist yet, the wizard fetches the official docs, scaffolds fresh, and offers to save the recipe as `references/<tool>-<stack>.md` for reuse.

## Composes with

- **`skillify`** — sibling in `-ify` trifecta. Use `skillify` when the goal is a new SKILL.md, not an integration.
- **`loopify`** — sibling. Use `loopify` for setting up cron/agent-loop patterns on top of the toolified integration (e.g., poll a webhook, sync data daily).
- **`compound-engineering:context7`** — fetch current SDK docs (fresher than training data).
- **`makerskills:watch-video`** — if the user has a Loom of an integration walkthrough, feed it in to synthesize the recipe.

## Notes on quality

- **Never skip webhook signature verification.** Even for internal-only endpoints. The vendor provides the crypto pattern for a reason.
- **Never commit secrets.** `.env.local` and `.env` are gitignored — verify before finishing.
- **Never invent auth patterns.** Use the vendor's official pattern verbatim. If docs are unclear, fetch again.
- **SDK version matters.** Pin the SDK version in `package.json` / `Gemfile.lock`. Note the version in the file header comment.
- **One tool per invocation.** Don't scaffold Stripe + Kit + Sanity in one run. Wizard is designed for depth per tool, not breadth.
- **Prefer official SDKs** unless they're bloated/abandoned. Raw fetch is fine when the SDK adds no value.
- **Recipe-first for repeat tools.** If integrating a tool the user has done before, load the recipe from `references/` and adapt, don't re-derive.
