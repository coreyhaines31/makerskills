---
name: business-brainstorm
description: When you want to pressure-test a potential new business, product, or side project against his serial-founder filter. Not "marketing ideas for a product" (that's marketing-skills:marketing-ideas) — this is "should this business exist + can you win it." Runs the idea through a structured framework (problem, audience, wedge, monetization, moat, portfolio fit, distribution, energy fit, opportunity cost), checks domain availability via /domain, optionally triggers /deep-research for market validation, and outputs a viability brief: build / sleep on it / pass. Archives every idea to references/ideas-archive/ so past work is searchable. Triggers on "/business-brainstorm," "/brainstorm," "new business idea," "should I build X," "pressure test this idea," "validate this idea," "is X a good business," "what about a [type] for [audience]."
metadata:
  version: 0.1.0
---

# /business-brainstorm — Pressure-test a business idea

Takes a vague idea, runs it through Corey's filter, and outputs a structured viability brief. Composes with `deep-research` (for market) and `/domain` (for naming).

## Step 1 — Capture the idea

Get from Corey:
- The idea in 1–2 sentences (the *what*)
- The reason it's on his mind (the *why now*)
- Any starting context (a chat where this came up, a tweet that inspired it, a problem he's hit)

If he points at a past chat / doc, load it first. Memory has `project_*.md` files for in-flight projects (workhouse, peptidepatterns, etc.) — check there before assuming the idea is brand-new.

If the idea is too vague to score, ask 1–2 clarifying questions and stop. Don't pad the brief with assumptions.

## Step 2 — Load the framework

Read `references/framework.md` — Corey's filter. Apply each dimension in order.

## Step 3 — Score each dimension

For each of the 9 dimensions in `framework.md`, give a 1-line take + a verdict (✅ strong / 🟡 OK / ❌ weak / ❓ unknown — needs research).

Don't BS the unknowns. Mark them ❓ and route to deep-research in Step 4.

## Step 4 — Trigger research where needed (optional)

If 2+ dimensions are ❓ unknown, offer Corey: *"Want me to run `/deep-research` on [topic] before scoring?"*

Useful research targets:
- Market size / who pays signal → `/last30days <space>` + `WebSearch`
- Competitive landscape → search for "alternatives to X", "X vs Y" pages
- ICP signal → forums / Reddit / X where the audience hangs out
- Pricing benchmarks → look at competitor pricing pages

If Corey says yes, run `Skill({skill: "deep-research", args: "<topic>"})` and incorporate the brief.

## Step 5 — Check the .com

Always run `/domain` on the working name(s). A perfect idea with a $50k domain is a worse idea than a B+ idea with a free .com.

If naming is wide open, brainstorm 5–10 candidate names through `/domain` and report which are available.

## Step 6 — Output the brief

Use this template:

```markdown
# Business brainstorm: <name or idea slug>

**Date:** <YYYY-MM-DD>
**Idea:** <1–2 sentences>
**Why now:** <1 sentence>

## Verdict
**Build** / **Sleep on it** / **Pass** / **Steal an angle for [existing property]**

<2–3 sentence rationale>

## Score

| Dimension | Take | Verdict |
|---|---|---|
| 1. Problem | … | ✅ |
| 2. Audience | … | 🟡 |
| 3. Wedge | … | ❓ |
| 4. Monetization | … | ✅ |
| 5. Moat | … | ❌ |
| 6. Portfolio fit | … | ✅ |
| 7. Distribution | … | ✅ |
| 8. Energy fit | … | 🟡 |
| 9. Opportunity cost | … | ❌ |

## Domain
- <name>.com — available / taken / aftermarket $<price>
- (other candidates if relevant)

## Research applied
- <link to deep-research brief in ../deep-research/references/research-archive/, if run>

## Open questions
- <what would change the verdict>

## If you build it (sketch)
- **First 100 customers:** <how>
- **Wedge offer:** <what>
- **Price:** <range>
- **MVP scope:** <1–3 features>

## If you don't build it
- **Angle to steal for existing properties:**
  - CF: …
  - Swipe Files: …
  - Magister: …
  - (etc., only where relevant)
```

## Step 7 — Archive

Write to `references/ideas-archive/<YYYY-MM-DD>-<slug>.md`. Append to `references/ideas-archive/INDEX.md`:

```markdown
- 2026-06-16 — [<idea>](./<filename>.md) — **<verdict>** — <one-line rationale>
```

## Step 8 — Surface

Show the brief in chat. Tell Corey the archive path. Offer:
- *"Want to push to Notion as a positioning canvas?"*
- *"Want me to scaffold a project repo / landing page?"* (if verdict = Build)
- *"Want me to revisit in 30 days?"* (if verdict = Sleep on it)

## Composes with

- `deep-research` — for market validation when dimensions are ❓
- `/domain` — for .com availability and naming brainstorm
- `/last30days` — for audience/market recency signal (via deep-research)
- Memory (`project_*.md`) — for portfolio context (don't pitch an idea that already exists)
