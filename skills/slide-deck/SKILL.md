---
name: slide-deck
description: When Corey wants to draft a slide deck — keynote, talk, internal update, pitch — for his React/Next.js slide system at corey.co/slides (${COREYCO_REPO:-$HOME/code/coreyco}/src/app/slides/). Writes TypeScript Slide[] arrays using his primitives (Eyebrow, Heading, Accent, Body, BulletList, Divider, TwoCol, GradientText), 12 cycling brand gradients, optional sections for "where am I" context, and speaker notes. Inspired by zarazhangrui/frontend-slides — "show, don't tell" applied to narrative (presents 3 angles, you pick). Triggers on "/slide-deck," "/slides new," "draft a deck," "deck for [topic]," "talk on [topic]," "keynote on [topic]," "internal deck for [audience]." For portable HTML/PDF decks without coreyco branding, use frontend-slides instead. This skill is for Corey's branded React decks.
metadata:
  version: 0.1.0
---

# /slide-deck — Draft branded React decks for corey.co/slides

Generates TypeScript `Slide[]` for `${COREYCO_REPO:-$HOME/code/coreyco}/src/app/slides/<deck-name>/page.tsx` using Corey's slide system.

## Step 1 — Capture the brief

Get these from Corey (ask only what's missing):

- **Topic / title** — what's the deck about?
- **Audience** — who's in the room? technical / executive / mixed / clients?
- **Duration** — number of slides (rough). 20 slides ≈ 20 min keynote, 10 slides ≈ 10 min internal update, 5 slides ≈ lightning.
- **CTA** — what should the audience do/think/feel after?
- **Slug** — kebab-case deck name (e.g., `marketing-like-an-engineer`). Used for the route + filename.

If audience or CTA is fuzzy, push for specificity. "Founders" is too broad; "B2B SaaS founders at MicroConf" is workable.

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

## Step 8 — Archive (optional)

Append a one-liner to `references/decks-archive.md` (create if missing):

```markdown
- 2026-06-17 — [<title>](${COREYCO_REPO:-$HOME/code/coreyco}/src/app/slides/<slug>/page.tsx) — <audience> — <one-line angle>
```

This compounds — future decks can grep "what talks have I done about X" to avoid repetition and find reusable patterns.

## Modes (quick invocations)

| Invocation | Behavior |
|---|---|
| `/slide-deck new <topic>` | Full pipeline (Steps 1–8) |
| `/slide-deck outline <topic>` | Stop at Step 3 (outline only) |
| `/slide-deck angles <topic>` | Stop at Step 2 (just the 3 angles) |
| `/slide-deck expand <slug>` | Skip to Step 4 from an existing outline |
| `/slide-deck notes <slug>` | Rewrite speaker notes for an existing deck |
| `/slide-deck rewrite <slug> <slide-id>` | Edit one slide |
| `/slide-deck preview <slug>` | Just check the deck URL |

## Composes with

- `business-brainstorm` — if a pitch deck, brainstorm the offer first; deck draws from the brief
- `decide` — for talks that hinge on a decision (e.g., "should I take VC money?"), `/decide` first
- `deep-research` — for talks needing data the deck doesn't have yet
- `second-brain` — pull relevant `[[wiki]]` pages as content sources; the deck can cite them
- `youtube-transcript` — turn a Factory Floor episode or talk recording into a deck outline
- `my-social` — once delivered, the talk becomes promo angles for the BIP rotation
- `frontend-skills` (external) — for non-branded HTML decks where coreyco isn't the home
