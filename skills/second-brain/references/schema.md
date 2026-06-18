# Schema (fallback)

**Authoritative source: `<vault>/CLAUDE.md`.** This file is a fallback used only when the vault's CLAUDE.md is missing.

The schema below mirrors Corey's vault as of 2026-06-17. Update this file only if you're seeding a new vault from scratch.

---

## Folder structure

```
raw/          → Unprocessed source material (articles, highlights, ideas, notes, images)
wiki/         → AI-compiled knowledge base (topic pages, interlinked, with INDEX.md)
  INDEX.md    → Master index of all wiki pages with brief descriptions
outputs/      → Saved Q&A results, analyses, slide decks, research summaries
Projects/     → Project-specific notes (DO NOT modify)
Daily/        → Daily notes (DO NOT modify)
Templates/    → Note templates (DO NOT modify)
Inbox/        → Quick capture (DO NOT modify — see Inbox/Quick Capture.md)
```

## raw/ — file naming

Type prefixes:

**Personal / intellectual**
- `article-` — web article, blog post, news
- `idea-` — your own idea or proposal
- `highlights-` — book/article highlights
- `braindump-` — unstructured thinking
- `note-` — quick reference
- `resource-` — non-text (PDF, video, podcast, image)
- `tweet-` — single X post or thread
- `bookmark-` — URL + a one-line "why I saved this"

**Business / operational** (CF, fCMO, client work)
- `call-` — call/meeting transcript (Riverside, Zoom, Otter)
- `meeting-` — meeting notes (your own, not auto-transcripts)
- `screenshot-` — image capture with context (UI, dashboard, competitor)
- `sop-` — standard operating procedure
- `email-` — customer / sales / prospect email worth preserving
- `objection-` — sales objection heard from a prospect (with context)
- `ticket-` — support ticket pattern worth remembering
- `person-` — contact / profile note (think CRM-lite, like Gbrain's people entity)

First line of each file:
```
source: <URL if applicable, or "call with X on YYYY-MM-DD", "email from X", etc.>
captured: YYYY-MM-DD
```

## wiki/ — page format

```markdown
# Topic Name

Brief summary (2–3 sentences).

## Key Concepts
- Concept with explanation

## Details
Main content organized by subtopic.

## Connections
- [[Related Topic]] — how it connects
- [[Another Topic]] — how it connects

## Sources
- `raw/article-example.md` — what was drawn from this source
```

## wiki/INDEX.md — format

```markdown
# Wiki Index

## <Category>
- [[Page Name]] — brief one-line description

## <Another Category>
- [[Page Name]] — brief one-line description
```

Standard categories (extend as needed):
- Creative
- Health & Longevity
- Faith & Personal Growth
- Business
- Personal Growth
- Tech
- Hobbies
- Sci-Fi
- Pets
- Personal Reference

### Suggested wiki pages that compose with other makerskills

Pages whose existence makes other skills sharper:

| Wiki page | Composes with | Why |
|---|---|---|
| **Decision Log** | `decide` | Narrative version of decisions made — the `decide` skill archives one-off decisions; the wiki page is the story of how decisions stacked over time on a topic |
| **Content Ideas** | `jab-hook`, `cf-blog` | Centralized hopper of hooks, frameworks, stories — drafted posts pull from here |
| **Customer Language** | CF positioning + sales | Verbatim phrases from prospects/customers — used for copy, headlines, objections |
| **Offer Notes** | CF positioning | What's been tried, what landed, what didn't |
| **Recurring Questions** | CF sales, client onboarding | Questions asked >3 times across calls; pre-answered for SOP / FAQ / scripts |
| **Workflow Docs** | `pm` | Documented operational patterns — what gets done, by whom, on what cadence |
| **People** | CF, fundraising, partnerships | Contacts with context — a CRM-lite. Inspired by Gbrain's people entity. |
| **Companies** | CF clients, prospects | Org profiles with last touchpoint, opportunity, status |
| **Sales Objections** | CF sales scripts | Library of objections + best responses |
| **Sales Scripts** | CF sales | Templates assembled from Customer Language + Objections |

### Outputs categories

The `outputs/` folder hosts generated artifacts. Common kinds:
- Posts (social drafts, blog drafts)
- Reports
- Proposals (especially CF)
- SOPs (your own + client deliverables)
- Audits (CF deliverable)
- Research briefs (composes with `deep-research`)
- Sales scripts
- Client summaries
- Slide deck content (handed off to `slide-deck`)

## Rules

- **One page per concept** — not per source
- **Use `[[wikilinks]]`** for all internal references
- **Keep pages focused** — split if >500 words
- **INDEX.md is the root** — keep current
- **Connections section is mandatory** — every page links to ≥1 other page
- **No orphan pages**
- **Summaries are concise**
- **Preserve nuance** — don't flatten contradictions
