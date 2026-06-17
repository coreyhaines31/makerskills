---
name: slide-deck
description: When Corey wants to draft, update, convert, or export a slide deck for his React/Next.js slide system at corey.co/slides (${COREYCO_REPO:-$HOME/code/coreyco}/src/app/slides/). Writes TypeScript Slide[] arrays using his primitives (Eyebrow, Heading, Accent, Body, BulletList, Divider, TwoCol, GradientText), 12 cycling brand gradients, optional sections for "where am I" context, and speaker notes. Inspired by zarazhangrui/frontend-slides — "show, don't tell" applied to narrative (presents 3 angles, you pick) plus density modes (speaker-led vs reading-first). Four modes — new (draft from brief), update (modify existing, with overflow guards), ppt (convert legacy PPTX → React deck), export (Playwright snapshot existing React deck to standalone HTML, PDF, or Vercel URL — keeps brand). Triggers on "/slide-deck," "/slides new," "/slides export," "/slides update," "/slides ppt," "draft a deck," "deck for [topic]," "talk on [topic]," "keynote on [topic]," "internal deck for [audience]," "convert this pptx," "export this deck."
metadata:
  version: 0.1.0
---

# /slide-deck — Draft, update, convert, and export branded React decks

Authors React/TypeScript decks for `${COREYCO_REPO:-$HOME/code/coreyco}/src/app/slides/<slug>/page.tsx` using Corey's slide system. Branded output (no separate HTML pipeline) — when portable HTML/PDF is needed, export mode snapshots the rendered React deck via Playwright so the output is brand-perfect.

## Modes (pick one before Step 1)

| Mode | Invocation | Goal |
|---|---|---|
| **new** | `/slide-deck new <topic>` (default) | Draft a new deck from a brief |
| **update** | `/slide-deck update <slug>` | Modify an existing deck (with overflow guards) |
| **ppt** | `/slide-deck ppt <path-to-pptx>` | Convert a legacy PPTX into a React deck |
| **export** | `/slide-deck export <slug> [html\|pdf\|vercel]` | Snapshot a deck to HTML, PDF, or Vercel URL |

For `update`, `ppt`, and `export`, skip to the corresponding mode section below. For `new`, continue through Steps 1–8.

---

## Step 1 — Capture the brief (ask all at once)

Ask in one structured message. Don't round-trip on each.

1. **Topic / title** — what's the deck about?
2. **Audience** — who's in the room? (technical / executive / mixed / clients) Push for specificity: "founders" is too broad; "B2B SaaS founders at MicroConf" is workable.
3. **Length** — rough slide count: 5–10 (lightning / short internal) / 10–15 (short keynote, pitch) / 20–25 (keynote) / 30+ (workshop — uncommon for branded decks).
4. **Density** — *speaker-led* (1 idea/slide, big type, lots of breathing room, more slides if needed) or *reading-first* (4–6 bullets/slide, structured grids, self-contained for async review).
5. **CTA** — what should the audience do/think/feel after?
6. **Slug** — kebab-case (e.g., `marketing-like-an-engineer`).
7. **Content state** — all content ready / rough notes / topic only.

Remember density — it affects slide count, copy length per slide, and which primitives to favor. See `references/narrative-and-voice.md` for the density-specific rules.

## Step 2 — Three narrative angles

Riff on `zarazhangrui/frontend-slides`' "show, don't tell" — but applied to *story*, not visuals (your visual system is fixed).

Pitch 3 angles in 1–2 sentences each:

- **Safe** — most likely to land. Conventional structure for the audience.
- **Bold** — contrarian or counterintuitive frame. Higher upside, slight risk.
- **Wildcard** — unexpected structure (story-first, single-question deck, anti-thesis, etc.).

Corey picks one. If he rejects all three, propose three more — don't force a path.

## Step 3 — Outline

For the chosen angle:

1. **Sections** — propose 3–7 named sections (e.g., `Title`, `Hook`, `Problem`, `Framework`, `Examples`, `Close`). The default 3-act structure is OPTIONAL; only use it if Corey wants it or the deck is a keynote-length talk that benefits from one.
2. **Slide titles** within each section
3. **One-line takeaway** per slide

Total slide count should match the duration estimate from Step 1.

Show the outline as a table. Corey edits / approves before expand.

## Step 4 — Expand to slide content

For each slide, write the full content using his primitives. Reference `references/system.md` for the primitive vocabulary and `references/narrative-and-voice.md` for hook patterns and voice rules.

Slide types and which primitives fit:

| Slide type | Primitives | Pattern |
|---|---|---|
| Title | `Eyebrow` + `<h1>` with `<Accent>` keyword | First slide, sets brand and topic |
| Hook | `Heading` + `Body` | A take, story open, contrarian frame, or specific stat |
| Section divider | `Eyebrow` + `Heading` (centered, large) | Clean break between sections |
| Framework | `Heading` + `BulletList` or custom layout | The thing Corey's teaching |
| Two-column | `TwoCol` | Comparison, before/after, problem/solution |
| Quote / pull-quote | `Body` (large) | Authority or audience-recognition moment |
| Resource / link | `Body` + URL on its own line | Outbound (rare — Corey's voice says minimize) |
| Close / CTA | `Heading` + `Body` + `BulletList` for next steps | What the audience should do |

**Voice anchors** (see `narrative-and-voice.md`):
- Direct, conviction-coded, reader-perspective ("you'll know X" not "I'll teach you X")
- Specific nouns, short sentences, verbs that do work
- No filler ("Today I want to talk about…") — open with a take

## Step 5 — Speaker notes

Every slide gets 3–5 notes lines. Each line is a complete thought a speaker would say. Notes are spoken Corey, not written Corey — a bit more conversational than the slide body.

Notes structure:
1. **The opener** — what you say when the slide comes up
2. **The point** — the one idea this slide is making
3. **The supporting beat** — example, data, or color
4. **The transition** — how this connects to the next slide
5. **(Optional) The aside** — a quip or callback

For title slides and section dividers, 2–3 notes is fine.

## Step 6 — Generate files

Write to `${COREYCO_REPO:-$HOME/code/coreyco}/src/app/slides/<slug>/`:

1. `layout.tsx` — Next.js layout with `<title>` metadata (use the deck title)
2. `page.tsx` — the slide deck

Use the templates in `references/template.md` as the skeleton.

`page.tsx` must:
- Have `"use client"` at the top
- Import `SlideDeck` and `Slide` type from `@/components/slides/slide-deck`
- Import `SectionRange` from `@/components/slides/sections` (only if using sections)
- Import the primitives Corey uses from `@/components/slides/slide-primitives`
- Declare `const slides: Slide[] = [...]`
- (Optional) Declare `const sections: SectionRange[] = [...]` with 0-indexed `from`/`to`
- Export default a component that returns `<SlideDeck slides={slides} sections={sections} />`

## Step 7 — Preview

After writing the files, check if Corey's coreyco dev server is running.

```bash
lsof -i :3000-3099 2>/dev/null | grep -E "LISTEN" | head
```

If a port is in use for coreyco (he uses portless — check `package.json` for the dev script naming):

```bash
# Suggested URL pattern (he uses portless)
echo "Preview at: http://${COREYCO_DEV_HOST:-localhost:3000}/slides/<slug>"
```

If no dev server is running, tell Corey:

```bash
cd ${COREYCO_REPO:-$HOME/code/coreyco} && npm run dev
# then visit http://${COREYCO_DEV_HOST:-localhost:3000}/slides/<slug>
```

Don't auto-start the dev server (might disrupt other work).

## Step 8 — Archive

Append a one-liner to `references/decks-archive.md` (create if missing):

```markdown
- 2026-06-17 — [<title>](${COREYCO_REPO:-$HOME/code/coreyco}/src/app/slides/<slug>/page.tsx) — <audience> — <one-line angle>
```

This compounds — future decks can grep "what talks have I done about X" to avoid repetition and find reusable patterns.

---

## Mode: update

Modify an existing deck without breaking it. Risks: overflowing slides, exceeding density limits, breaking the section ranges.

**Before modifying, check:**

1. Read the existing `page.tsx`
2. Count slides + identify the section ranges
3. For each modification, apply the right guard:

| Change | Guard |
|---|---|
| **Adding bullets** | Max 6 per `BulletList` in reading-first; 3 in speaker-led. If exceeded → split into two slides. |
| **Adding text** | If `<Body>` paragraph >2 sentences in speaker-led → split. >5 sentences in reading-first → split. |
| **Adding images** | Images must fit in the 1920×1080 stage. If the slide already has heavy content, move image to its own slide. |
| **Adding slides** | Update `sections` array — increment `from`/`to` for all sections after the insertion point. |
| **Removing slides** | Decrement `from`/`to` for sections after the removal. Watch for orphaned `id` references. |
| **Rewriting a slide** | Preserve the `id` (used for anchors). Only change `content` and `notes`. |

**After modifying:**
- Re-count slides and verify section ranges sum correctly
- Spot-check the visual in the dev server before committing

---

## Mode: ppt

Convert a legacy PPTX (client deck, conference template) into Corey's React system.

1. **Extract content** via `python3` and `python-pptx`:
   ```bash
   pip install python-pptx 2>/dev/null
   python3 -c "
   from pptx import Presentation
   import json, sys
   p = Presentation(sys.argv[1])
   out = []
   for i, s in enumerate(p.slides):
       title = next((sh.text for sh in s.shapes if sh.has_text_frame and sh.shapes_element.tag.endswith('}sp') == False), '')
       texts = [sh.text for sh in s.shapes if sh.has_text_frame]
       notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ''
       out.append({'i': i, 'texts': texts, 'notes': notes})
   print(json.dumps(out, indent=2))
   " "<path-to-pptx>"
   ```
   See `references/ppt-conversion.md` for the full extraction + mapping recipe.

2. **Show Corey the extracted summary** — slide titles, content excerpts, image count. Confirm before proceeding.

3. **Map to React primitives**:
   - First slide → title pattern (Eyebrow + h1 + Accent)
   - Content slides with bullets → `Heading + BulletList`
   - Comparison slides → `TwoCol`
   - Section breaks (title-only slides in PPTX) → section divider pattern
   - Speaker notes from PPTX → `notes` array on each slide

4. **Images** — copy referenced images from PPTX assets to `${COREYCO_REPO:-$HOME/code/coreyco}/public/slide-assets/<slug>/`, reference them in slides via `<img src="/slide-assets/<slug>/<filename>" />` inside the `content`.

5. **Write `page.tsx` + `layout.tsx`** per the new-deck flow (Step 6).

6. **Preserve the original PPTX** — never modify in place. Save under `~/Documents/slide-conversions/<slug>-from-pptx/` with the original file + extracted JSON for audit.

---

## Mode: export

Snapshot a deck rendered in the corey.co dev server to portable HTML / PDF / Vercel URL. Output is brand-perfect because it's screenshots of your actual rendered React deck.

**Output options:**
- `html` — standalone HTML file with snapshots as inline `<img>`, keyboard nav (arrow keys) baked in
- `pdf` — combined slide snapshots
- `vercel` — push standalone HTML to a Vercel project for a shareable URL

**Flow** (full details in `references/export.md`):

1. **Verify dev server**: confirm `${COREYCO_DEV_HOST:-localhost:3000}/slides/<slug>` loads. If not, prompt Corey to `cd ${COREYCO_REPO:-$HOME/code/coreyco} && npm run dev`.
2. **Count slides**: read `page.tsx`, count entries in the `slides` array.
3. **Run Playwright snapshot**:
   ```bash
   bash references/export.md script: snapshot-deck <slug> <count>
   ```
   - Launches headless Chromium at 1920×1080
   - Loads `http://${COREYCO_DEV_HOST:-localhost:3000}/slides/<slug>?present=1` (presenter mode hides chrome)
   - Sets `localStorage["slides:/slides/<slug>"] = "0"` to start at slide 0
   - Loops: screenshot → keyboard ArrowRight → wait — for N slides
   - Saves PNGs to `~/Documents/slide-exports/<slug>-<YYYY-MM-DD>/slide-<n>.png`
4. **Combine** per output type:
   - `html` → wrap snapshots in a minimal HTML shell with arrow-key navigation
   - `pdf` → use `magick` (ImageMagick) or `img2pdf` to combine PNGs
   - `vercel` → `vercel deploy ~/Documents/slide-exports/<slug>-<date>/`
5. **Report** path / URL.

**Caveats** (mention to Corey):
- Animations and presenter view are not preserved — exports are static snapshots.
- For interactive demo, present the React version live; for sharing/PDF/portable, use exports.
- Snapshots are 1920×1080 — high-quality on any device, but file size scales with slide count.

---

## Modes (quick invocations)

| Invocation | Mode | Behavior |
|---|---|---|
| `/slide-deck new <topic>` | new | Full pipeline (Steps 1–8) |
| `/slide-deck angles <topic>` | new | Stop at Step 2 (just the 3 angles) |
| `/slide-deck outline <topic>` | new | Stop at Step 3 (outline only) |
| `/slide-deck expand <slug>` | new | Skip to Step 4 from an existing outline |
| `/slide-deck notes <slug>` | update | Rewrite speaker notes for an existing deck |
| `/slide-deck rewrite <slug> <slide-id>` | update | Edit one slide |
| `/slide-deck update <slug>` | update | General modification with overflow guards |
| `/slide-deck ppt <pptx-path>` | ppt | Convert legacy PPTX → React deck |
| `/slide-deck export <slug> html` | export | Snapshot to standalone HTML |
| `/slide-deck export <slug> pdf` | export | Snapshot to PDF |
| `/slide-deck export <slug> vercel` | export | Snapshot + Vercel deploy → shareable URL |
| `/slide-deck preview <slug>` | — | Just check the deck URL |

## Composes with

- `business-brainstorm` — if a pitch deck, brainstorm the offer first; deck draws from the brief
- `decide` — for talks that hinge on a decision (e.g., "should I take VC money?"), `/decide` first
- `deep-research` — for talks needing data the deck doesn't have yet
- `second-brain` — pull relevant `[[wiki]]` pages as content sources; the deck can cite them
- `video-watch` — turn a Factory Floor episode, Loom, or talk recording into a deck outline (run in `visual` mode to also capture key moments + slides shown)
- `my-social` — once delivered, the talk becomes promo angles for the BIP rotation
- `frontend-skills` (external) — for non-branded HTML decks where coreyco isn't the home
