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
- `article-` — web article, blog post, news
- `idea-` — your own idea or proposal
- `highlights-` — book/article highlights
- `braindump-` — unstructured thinking
- `note-` — quick reference
- `resource-` — non-text (PDF, video, podcast, image)
- `tweet-` — single X post or thread

First line of each file:
```
source: <URL if applicable>
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

## Rules

- **One page per concept** — not per source
- **Use `[[wikilinks]]`** for all internal references
- **Keep pages focused** — split if >500 words
- **INDEX.md is the root** — keep current
- **Connections section is mandatory** — every page links to ≥1 other page
- **No orphan pages**
- **Summaries are concise**
- **Preserve nuance** — don't flatten contradictions
