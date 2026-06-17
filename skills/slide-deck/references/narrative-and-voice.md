# Narrative and voice for branded decks

## Voice (load-bearing)

Corey's slide voice is the same as his social and copy voice:

1. **Conviction-coded** — make the audience feel the take, not the hedging
2. **Reader-perspective** — "you'll know X" not "I'll teach you X"
3. **Specific nouns, short sentences, verbs that do work**
4. **Lead with a take, not a question**

Voice anti-patterns to avoid:
- "Today I want to talk about…" / "Let me start by…"
- "I'm excited to be here" (save it for notes, not the slide)
- "Has anyone ever…?" (engagement bait)
- Emojis as decoration
- Generic AI aesthetics in copy ("dive deep," "leverage synergies")

## Anti-AI-slop discipline

LLMs converge toward generic copy. Hold a higher bar by avoiding these specific patterns:

**Banned words/phrases on slides** (use anything else):
- *Dive deep, dive in, deep-dive*
- *Leverage, unlock, supercharge, turbocharge*
- *Game-changing, paradigm shift, next-level*
- *Synergies, ecosystems, holistic*
- *Robust, scalable, future-proof*
- *Empowering, enabling, transforming*
- *Journey* (as a metaphor — "their journey," "your journey")
- *Solutions* (as a noun standalone — "marketing solutions")
- *Best-in-class, world-class, cutting-edge*
- "*In today's fast-paced world…*" / "*Now more than ever…*" / "*In an era of…*"

**Banned slide patterns:**
- Definitions on slide 1 ("Marketing is…")
- Three bullets that are just three rephrasings of the same idea
- A heading that doesn't survive being read aloud ("Optimizing Customer Engagement Through Strategic Initiatives")
- Stat with no source ("76% of CMOs say…") — either name the source or drop the stat
- Trailing question to invite engagement ("So what do you think?")

**Test:** if a slide's heading could appear unchanged in a generic SaaS pitch deck, rewrite it. Specific > vague every time.

The voice should be unmistakably Corey's. If you can imagine three other marketers reading the same slide and it landing, it's not voiced enough.

Voice exceptions in **speaker notes**: notes are SPOKEN Corey — slightly more conversational, can include "you know," asides, callbacks. The slide text is written Corey — tighter.

## Narrative patterns (pick one, don't force any)

### Take-first
1. Open with the take as the title slide (e.g., *"Marketing Like an Engineer"*)
2. Brief moment of surreal/unexpected stat or image (slide 2)
3. Frame the problem the take solves
4. Walk through the system / framework
5. Show it working with examples
6. Close with the action the audience takes Monday

Best for: keynotes, conference talks, opinionated frameworks.

### Story-first
1. Open inside a specific moment (a client conversation, a screenshot, a number)
2. Pull back: this isn't unusual — it's common
3. Why it happens
4. The reframe / framework
5. Concrete next step

Best for: persuasion talks, sales decks, fundraising pitches.

### Problem → Reframe → System → Close
1. Show the broken thing the audience knows
2. The reframe (why their current model misses)
3. The system that fixes it
4. The path forward

Best for: pitches, internal updates that change direction.

### Anti-thesis
1. Show the conventional wisdom
2. Take it apart
3. What's actually true
4. What to do with that

Best for: contrarian talks, hot-take keynotes.

### Single-question deck
The whole deck answers ONE question, building up the answer slide by slide.

Best for: short decks (5–10 slides), lightning talks.

## Slide-level patterns

### Hooks that work (slide 2 / right after title)
- A specific number that's bigger or smaller than expected ("$120k saved by removing one button")
- A counterintuitive observation ("the more we asked customers, the less they bought")
- A short story with a named person and place ("Last week, a founder asked me…")
- A surreal moment / image that earns "wait, what?"

### Hooks that don't work
- Definitions ("Marketing is…")
- Generic stats from a McKinsey report
- Questions
- "Today I want to share…"

## Speaker notes discipline

Notes should be **spoken Corey**, not written Corey. Slightly more conversational, more callbacks, more "you know" allowed.

Structure per slide (3–5 lines):

1. **Opener** — what you say when the slide appears
2. **Point** — the one idea this slide makes
3. **Support** — example, data, color
4. **Transition** — segue into the next slide
5. *(Optional)* **Aside** — quip, callback, audience read

Notes are the *full talk*. If a presenter could read just the notes (not the slides) and deliver the talk, the notes are doing their job.

Title slides and section dividers get 2–3 notes lines, not 5.

## Length calibration

| Slide count | Format | Use case |
|---|---|---|
| 5–10 | Lightning / single-question | Internal update, 5-min talk, demo intro |
| 10–15 | Short keynote / pitch | 15-min conference slot, sales pitch, board update |
| 20–25 | Keynote | 20–30 min headliner talk |
| 30+ | Workshop / training | Deep teaching, less appropriate for branded decks |

For pitch decks specifically: 10–15 slides is the sweet spot. 20+ becomes a doc, not a deck.

## Density modes

Borrowed from `frontend-slides`. Ask Corey up front — affects slide count, copy length per slide, and which primitives to favor.

### speaker-led (low density)

Best for: public talks, keynotes, conference slots, live explanation.

Rules:
- **One idea per slide.** If two ideas are fighting, split.
- **Large type, lots of negative space.** Let the slide breathe.
- **Max 3 bullets per `BulletList`** — and consider whether bullets are even right (vs. one strong line).
- **`<Body>` paragraphs: ≤2 sentences** on a single slide. Beyond that, split.
- **More slides, not denser slides.** A 20-min talk might be 30 speaker-led slides — that's fine, each slide is short.
- **Favor: title slide, hook slides, single-quote slides, section dividers, framework slide with 3-bullet list, close with one CTA line.**
- **Avoid: dense tables, multi-column comparisons with long content, big numbered lists.**

### reading-first (high density)

Best for: reports, async handouts, async review, detailed internal docs, post-meeting recap.

Rules:
- **Self-contained slides.** The audience reads alone — no presenter to fill in gaps.
- **4–6 bullets per `BulletList` allowed.** Up to 6 cards in a grid.
- **Structured layouts**: TwoCol comparisons, tables, annotated lists, captions.
- **Strong hierarchy** — `Eyebrow → Heading → Body → BulletList` so the reader can scan.
- **Fewer slides, denser slides.** A 10-page reading-first deck conveys what a 25-page speaker-led deck would.
- **Speaker notes optional** (no one's reading them; audience reads the slide).
- **Favor: TwoCol, BulletList with longer items, framework slides with explanations under each bullet, tables.**

### When stated needs are mixed

Pick the closer mode rather than inventing a middle. Live audience persuasion → speaker-led. Async circulation or detailed review → reading-first. Never let high density become visual clutter — if a slide starts to overflow, split it.

## Section discipline

When using sections (`SectionRange[]`):
- 3–7 sections per deck (more than 7 = sprawl)
- Each section is named with a noun phrase, not a question
- The first section is always `Title` (single slide)
- The last section is always `Close` or `CTA`
- Section names appear in the presenter view "where am I" header
