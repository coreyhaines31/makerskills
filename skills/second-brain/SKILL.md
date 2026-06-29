---
name: second-brain
description: When you want to capture into, compile, query, lint, or connect his personal Second Brain. Wraps the Karpathy LLM Wiki schema he runs in Obsidian — raw/ (unprocessed sources), wiki/ (AI-compiled interlinked topic pages), outputs/ (generated artifacts). Tool-agnostic in design but defaults to his vault at ${SECOND_BRAIN_VAULT:-$HOME/Documents/SecondBrain}/. Six modes — capture (drop something into raw/), compile (process unprocessed raw files into wiki pages, update INDEX.md), query (answer a question from the wiki, save to outputs/), lint (orphans / contradictions / stale / unprocessed raw / topic gaps), connect (suggest new wikilinks between pages), search (quick lookup). Triggers on "/second-brain," "/sb," "capture this," "save this to my brain," "compile the wiki," "process raw notes," "query my wiki," "ask my brain," "lint the wiki," "find connections," "search my notes." Complements deep-research (external corpus) — this is the internal corpus.
metadata:
  version: 0.1.0
---

# /second-brain — Karpathy LLM Wiki workflow

Wraps an existing Second Brain in Obsidian (or any markdown-based vault). The wiki vault's CLAUDE.md is the authoritative schema — the skill orchestrates the operations he's been doing manually.

## Mental model

Three layers, each with a clear role:

```
raw/      →  wiki/         →  outputs/
sources      compiled         generated
                              artifacts
```

- **raw/** — unprocessed source material. Articles, highlights, ideas, braindumps, tweets. Type-prefixed (`article-`, `idea-`, `highlights-`, `braindump-`, `note-`, `resource-`, `tweet-`). Never deleted — source of truth.
- **wiki/** — AI-compiled topic pages. One page per concept, not per source. Interlinked via `[[wikilinks]]`. `INDEX.md` at root.
- **outputs/** — generated artifacts from queries: research summaries, analyses, slide decks. Named descriptively.

Folders to leave alone during wiki ops: `Projects/`, `Daily/`, `Templates/`, `Inbox/`, `Notes/`, `Tasks.md`, `Kanban.md`, `Home.md`.

## Step 1 — Load vault config + schema

1. Read `references/vault-config.md` for the vault path (default: `${SECOND_BRAIN_VAULT:-$HOME/Documents/SecondBrain}/`)
2. Read `<vault>/CLAUDE.md` for the authoritative schema. If present, trust it over `references/schema.md` — the user's vault is the source of truth.
3. If no `<vault>/CLAUDE.md`, fall back to `references/schema.md`.

## Step 2 — Parse mode

| Invocation | Mode |
|---|---|
| `/sb capture` / `/second-brain capture` / "capture this" / "save this to my brain" | **capture** |
| `/sb compile` / "compile the wiki" / "process raw notes" | **compile** |
| `/sb query <question>` / "ask my brain X" / "what does my brain say about Y" | **query** |
| `/sb lint` / "lint the wiki" / "health check my brain" | **lint** |
| `/sb connect` / "find connections" / "suggest wikilinks" | **connect** |
| `/sb search <term>` / "search my notes for X" | **search** |

## Step 3 — Run the mode

### capture

Inputs: URL, pasted text, file path, or screenshot.

1. **Detect type** from content:
   - URL → `article-`
   - Pasted text with quoted highlights → `highlights-`
   - User's own thoughts / brainstorm → `braindump-` or `idea-`
   - Single tweet / X post → `tweet-`
   - PDF, video, podcast → `resource-`
   - Quick reference (recipe, command, fact) → `note-`
   - If ambiguous, ask.
2. **Generate a descriptive filename**: `<type>-<kebab-case-topic>.md` (e.g., `article-andrew-wilkinson-tiny-manual.md`). Use the source title or topic — not the URL slug.
3. **Add metadata to the top:**
   ```markdown
   source: <URL if applicable>
   captured: YYYY-MM-DD
   ```
4. **Save to `<vault>/raw/`**.
5. If the source is a URL, fetch the article content (via WebFetch or agent-browser for auth-walled) and save the readable text — not just the URL.
6. **Report** path + a one-line summary of what was saved.

Don't compile into the wiki here — capture is fast intake. Compilation is a separate, deliberate pass.

### compile

The expensive but valuable operation. Process unprocessed raw files into wiki pages.

1. **Find unprocessed raw files**: grep `wiki/*.md` for `Sources` sections; the raw files NOT listed are unprocessed.
2. **Read each unprocessed raw file** + the existing `wiki/INDEX.md`.
3. **For each raw file**:
   - Extract key concepts, facts, insights
   - **Default: merge into an existing wiki page** if the topic overlaps. Only create a new page if the concept doesn't fit anywhere.
   - **One page per concept, not per source.**
   - Use `[[wikilinks]]` for every related concept
   - Add the raw file under the wiki page's `## Sources` section with a one-line note on what was drawn from it
4. **Update `wiki/INDEX.md`**:
   - Add new pages under their category (Creative / Health & Longevity / Faith & Personal Growth / Business / Personal Growth / Tech / Hobbies / Sci-Fi / Pets — or new category if needed)
   - One line per entry: `- [[Page Name]] — brief description`
5. **Connections section is mandatory** on every wiki page. If a new page has no connections, find one before saving.
6. **Quality > quantity.** If a page would be <100 words, hold the raw file for now and ask Corey if it should be merged into an adjacent page.

Output: list of pages created/updated, what merged where, anything held for clarification.

### query

Answer a question using ONLY the wiki/raw corpus. Different from `deep-research` (which goes external).

1. **Read `wiki/INDEX.md`** to identify potentially relevant pages
2. **Read those pages** + traverse `[[wikilinks]]` 1–2 hops
3. **Compose the answer**:
   - Cite wiki pages by name: *"Per [[Microplastics Detox]]..."*
   - If the wiki contradicts itself, surface both sides
   - If the wiki doesn't contain the answer, say so and offer to run `/deep-research` to expand
4. **Save to `outputs/<YYYY-MM-DD>-<question-slug>.md`** with:
   - The original question
   - The answer
   - List of wiki pages consulted
5. **Show the answer in chat** + path to the saved output
6. **Optional render**: if `--render pdf` or `--render html` was passed, pipe the output through pandoc using the shared stylesheet. See `references/schema.md` → "Publishing alternatives" for the commands.

### lint

Health check the wiki.

Check:
1. **Orphan pages** — wiki/*.md that aren't in INDEX.md
2. **Connection orphans** — pages with no `[[wikilinks]]` to other pages
3. **Unprocessed raw** — raw files not listed under any wiki page's Sources
4. **Stale pages** — most recent source >6 months old AND topic is volatile (AI, marketing, finance, health protocols)
5. **Topic gaps** — concepts mentioned in 3+ pages without their own dedicated page
6. **Contradictions** — wiki pages making opposing claims without flagging it
7. **Missing connections** — pages on clearly related topics with no `[[wikilink]]` between them (suggest `/sb connect`)

Output: prioritized list. Most important first (broken structure beats stale content).

### connect

Find pages that should be linked but aren't.

1. Build a topic map from INDEX.md + page summaries
2. For each page, find 2–5 other pages with thematic overlap
3. Check whether each candidate is already linked
4. Suggest the missing links — and if Corey approves, edit the pages to add them to their `## Connections` sections

### search

Quick grep across `wiki/` + `raw/` for a term. Return matching files with a 2-line excerpt around the match. Faster than `query` when Corey knows what page he's looking for.

## Composes with

- `deep-research` — when `query` finds gaps in the wiki, route to deep-research to expand from external sources. Deep-research output can be captured back into `raw/` for future compilation.
- `paste` — capture content cleanly into `raw/` (especially for terminal/CLI captures).
- `business-brainstorm` — checks `Portfolio of Businesses` and `Entrepreneurship & Startups` wiki pages for relevant context before brainstorming.
- `decide` — pull from `Personal Philosophy` / `Productivity & Systems` wiki for principles when scoring Q34 ("what principles are we bending"). New: a `Decision Log` wiki page accumulates the narrative form of decisions over time (the `decide` archive is the structured form; the wiki page is the story).
- `jab-hook` — a `Content Ideas` wiki page hoppers hooks, frameworks, and stories. `/jab-hook` drafts pull candidates from there.
- `slide-deck` — content drafted in `outputs/` becomes deck source; speaker notes can reference relevant wiki pages.
- `pm` — Projects/ folder in the vault is off-limits to second-brain; pm owns it. But a `Workflow Docs` wiki page captures operational patterns that show up across multiple projects.
- `cf-blog` (in `cf-skills`) — pulls from `Content Ideas` and `Customer Language` wiki pages for blog drafts.

## Sibling implementations (reference)

Two other systems following the same raw → wiki → outputs pattern. Both are worth watching as upgrade paths.

- **[Hermes' `llm-wiki` skill](https://hermes.team)** — off-the-shelf implementation of the 3-folder pattern. Pre-built workflows for compile / query / lint. Useful for comparing schema decisions.
- **[Gbrain](https://github.com/garrytan/gbrain)** by Garry Tan — much more sophisticated. Treats the brain as a database (Postgres or PGLite) with synthesis, graph traversal, gap analysis, scheduled cron maintenance, and MCP integration. Powers a 146K-page deployment with 24K people entities. If Corey's vault outgrows the markdown-only pattern, Gbrain is the upgrade direction. Borrows worth adopting today even without migrating: **people-as-entities** (the `person-` raw type + `People` wiki page) and **scheduled maintenance** (wire `compile` and `lint` to fire on a recurring schedule via the `loop` or `compound-engineering:schedule` skill).

## Notes on quality

## Notes on quality

- **Quality over quantity.** Fewer well-connected wiki pages beat many thin ones. Hold raw files for clarification if compilation would produce a thin page.
- **Don't flatten nuance.** If two raw sources contradict, the wiki page should note the disagreement, not pick a side silently.
- **Connections section is mandatory** — every wiki page must link to at least one other page.
- **Never delete raw files** after compilation. They're the source of truth.
- **Never modify** files in `Projects/`, `Daily/`, `Templates/`, `Notes/`, `Tasks.md`, `Kanban.md`, `Home.md`, or `Inbox/` during second-brain operations. Those belong to other workflows.
