---
name: deep-research
description: "When you want multi-source, multi-step research on a topic — competitor research before a sales call, market research for a new business idea, positioning angles, due diligence on a partnership or podcast guest, tech decision research (which DB, which auth), or any \"I need to actually understand X.\" Combines WebSearch, WebFetch, agent-browser, /last30days (Reddit/X/YouTube/HN/web recency), memory, and Notion. Outputs a structured brief with citations, contradictions, gaps, and recommended next steps. Archives every research run to ~/.config/makerskills/deep-research/archive/ so past work is searchable. Triggers on \"/deep-research,\" \"research X,\" \"investigate X,\" \"do a deep dive on X,\" \"look into X,\" \"what's actually happening with X,\" \"due diligence on X,\" \"validate this market.\" Differs from a one-shot WebSearch: this is multi-pass with verification."
metadata:
  version: 0.2.0
---

# /deep-research — Multi-source research with archive

Plans, executes, and synthesizes research from multiple sources. Archives the output so the corpus compounds.

## Step 1 — Frame the question

Restate the research question in one tight sentence. If ambiguous, ask the user:
- What's the decision this research will inform?
- What's the minimum useful answer? (Saves over-researching.)
- Any sources to prioritize or avoid?

Output: `**Research question:** <one sentence>`

## Step 2 — Plan the sources

Pick from this menu based on the question type. Note which sources you'll hit and why.

| Source | When to use | Tool |
|---|---|---|
| Web search (Google) | Authoritative articles, docs, official statements | `WebSearch` |
| `/last30days` | What people are *actually saying* right now — Reddit, X, YouTube, HN, web recency | `Skill({skill: "last30days", args: "<topic>"})` |
| Specific URLs | When the user hands over starting URLs | `WebFetch` |
| Browsable pages (auth-walled, JS-heavy) | Pricing pages, product tours, profiles | `agent-browser` via the `compound-engineering:agent-browser` skill |
| Memory | Prior research / decisions / context the user already captured | grep `~/.claude/memory/` |
| Notion | If the topic touches a known Notion workspace | Direct Notion API (key in `$NOTION_API_KEY`, see `reference_notion_api.md`) |
| Research archive | Prior `/deep-research` runs that touched this topic | grep `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/deep-research/archive/` |

Run discovery passes **in parallel** where possible. Sequential only when one source needs another's output (e.g., agent-browser a URL discovered by WebSearch).

## Step 3 — Execute discovery

Run each chosen source. For each result, capture:
- The source (URL or system)
- 1–3 sentence summary of what was said
- Date / recency
- Confidence in the source (high/medium/low)

Don't synthesize yet — just collect.

## Step 4 — Synthesize

1. **Group findings** by theme or sub-question
2. **Contradiction check** — flag anywhere sources disagree. Don't average them; surface the disagreement.
3. **Confidence**: high (multiple independent sources agree), medium (one strong source or several weak), low (single anecdote or speculation)
4. **Gaps**: what would change the answer? What's NOT in the corpus?

## Step 5 — Output the brief

Use this template:

```markdown
# Research: <question>

**Date:** <YYYY-MM-DD>
**Decision this informs:** <one line>
**Confidence overall:** high / medium / low

## TL;DR
<2–4 sentences with the answer>

## Key findings

### 1. <Finding>
<2–4 sentences>. Sources: [1], [3], [5]

### 2. <Finding>
...

## Contradictions / uncertainty
- <where sources disagree, with each side cited>

## Gaps
- <what's missing from the corpus>
- <what to research next to close the gap>

## Recommended next steps
1. <action>
2. <action>

## Sources
[1] <Title> — <URL or system> (<date>) — <confidence>
[2] ...
```

## Step 6 — Archive

Archives live in `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/deep-research/archive/` (create the directory if missing). Never write archives inside the skill's own folder — skill installs and upgrades re-sync from source and wipe anything saved there. **Migration:** if this skill's folder contains an old `references/research-archive/` with user entries, move those files into the archive directory first.

Write the brief to `<archive dir>/<YYYY-MM-DD>-<slug>.md` so it's grep-able forever. Slug = kebab-case of the topic.

Also append a one-line entry to `<archive dir>/INDEX.md` (create if missing):

```markdown
- 2026-06-15 — [<topic>](./<filename>.md) — <one-line TL;DR>
```

## Step 7 — Surface

After archiving:
- Show the full brief in chat
- Tell the user the archive path
- Offer: *"Push to Notion or save to a project's docs?"*

## Composes with

- `business-brainstorm` — calls this skill during the market validation step
- `/domain` — when research includes "is the .com available"
- `/last30days` — one of the data sources

## Notes on quality

- **Always cite.** Every claim in the brief needs a source pointer.
- **Recency matters** — note dates on each source. For fast-moving topics (AI, startups), de-weight sources >12 months old.
- **Don't trust a single source** for high-stakes claims. Re-search until you have at least 2 independent corroborations or surface the uncertainty.
- **No padding.** If the answer is one paragraph, return one paragraph. The template is a maximum, not a minimum.
