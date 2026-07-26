---
name: decide
description: When you have a decision to make and want a structured workflow that picks the load-bearing questions, walks through them, reaches a call (or "wait"), and archives the rationale for future reference. Based on the 37signals Guide to Making Decisions (38 questions) plus house additions like Q39 opportunity cost ("what does saying yes displace?"). Triages to 6–8 relevant questions per decision instead of forcing the full set. Archives every decision to ~/.config/makerskills/decide/archive/ with a revisit date so you can check later whether the call was right. Triggers on "/decide," "help me decide," "should I [X]," "I need to make a decision about," "stuck on a decision," "deciding between," "go/no-go on," "what should I do about." This is both the decision-making workflow AND the decision log — making the decision is the act of logging it.
metadata:
  version: 0.3.0
---

# /decide — Structured decision workflow + archive

Picks load-bearing questions from the 37signals guide, walks through them, reaches a call, archives the rationale with a revisit date.

## Step 1 — Capture the decision

Get from the user:
- **The decision** in one sentence (what are we deciding between?)
- **Stakes**: low / medium / high (how much does this matter?)
- **Reversibility**: easy / hard / one-way door
- **Deadline**: when does this need to be decided? Or "open"?
- **Context** (optional, 1–3 sentences)

If any are missing, ask. Don't proceed with vague framing.

## Step 2 — Triage the question set

Read `references/questions.md` for the full set (the 37signals 38 + house additions, e.g. Q39 opportunity cost) and category mapping. Pick 6–8 based on the decision's characteristics:

**Default 5 (always ask):**
- Q1 — Does this decision actually need to be made?
- Q2 — Is the right person making this decision?
- Q8 — How easily can we reverse it?
- Q9 — First instinct? (capture before "thinking" muddies it)
- Q3 — A year from now, how will we feel about this?

**Add based on type:**

| If… | Add |
|---|---|
| Reversibility = hard / one-way door | Q14 (is there a wrong decision?), Q17 (knock-on effects), Q34 (principles bent) |
| Time pressure | Q5 (why hesitating?), Q15 (different tomorrow?), Q22 (when do we have to decide?) |
| Multiple people involved | Q21 (someone else's practice rep?), Q27 (would another opinion help?), Q35 (multiple people deciding what one should?) |
| Lots of data / analysis | Q19 (what missing info would change it?), Q26 (data vs gut?), Q9 deepened |
| Recurring decision | Q11 (last time?), Q23 (one-and-done or repeating?) |
| Customer-facing | Q24 (anyone outside depending?), Q25 (customer vs us impact?) |
| Money decision | Q38 (in the end, is this about money?), Q36 (return on effort?), Q39 (what does yes displace?) |
| Big time / focus commitment | Q39 (opportunity cost), Q36 (return on effort?), Q20 (creates or eliminates work?) |
| Stuck / not deciding | Q4 (why hasn't it been made already?), Q10 (what if we don't decide?), Q31 (do you even care?) |

Cap at ~8 questions. More than that turns into analysis paralysis (which is itself one of the things this skill exists to prevent).

Tell the user which questions you picked and why, then proceed.

## Step 3 — Walk through

Ask the questions one at a time, or in a tight cluster if the user wants to write fast. Capture their answers verbatim — don't paraphrase into corporate-speak.

For Q9 (first instinct), get the answer BEFORE diving into analysis. The point is to surface the gut call so we can later check if "analysis" was just rationalization.

## Step 4 — Reach a call

Synthesize the answers into a decision. Options:

- **Decide now** — answers point to a clear call
- **Decide smaller** — break into 2–3 smaller decisions (Q7)
- **Wait** — flag what info / time would change the answer (Q19, Q15)
- **Don't decide** — the decision doesn't need to be made (Q1, Q10)
- **Wrong person** — kick to the right decider (Q2, Q35)

State the call clearly. No hedging.

## Step 5 — Set the revisit

Pick a revisit date based on when consequences would show up:
- Decisions about tools/processes: 30 days
- Decisions about strategy/positioning: 90 days
- Decisions about hires/partnerships: 90–180 days
- Decisions about products/launches: 30–60 days post-launch

Write what to look for on the revisit ("did MRR move? did the partner ship? do clients still ask for X?").

## Step 6 — Archive

Archives live in `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/decide/archive/` (create the directory if missing). Never write archives inside the skill's own folder — skill installs and upgrades re-sync from source and wipe anything saved there.

**Migration:** if this skill's folder contains an old `references/decisions-archive/` with user entries, move those files into the archive directory before writing anything new.

Write to `<archive dir>/<YYYY-MM-DD>-<slug>.md`:

```markdown
# Decision: <one-line>

**Date:** YYYY-MM-DD
**Decide by:** <date or "open">
**Reversibility:** easy / hard / one-way door
**Stakes:** low / medium / high

## Context
<1–3 sentences>

## Questions

### <Q3 phrasing>
<answer>

### <Q8 phrasing>
<answer>

(only questions actually applied — heading is the question text, not "Q3")

## Decision
**<the call, stated clearly>**

## Rationale
<2–3 sentences synthesizing the answers>

## Expected outcome
<what should be true if this was right, by <date>>

## Revisit
**<YYYY-MM-DD>** — <what to look for>

## Source
Questions adapted from [The 37signals Guide to Making Decisions](https://37signals.com/how-we-make-decisions)
```

Append to `<archive dir>/INDEX.md` (create if missing):

```markdown
- 2026-06-16 — [<decision>](./<filename>.md) — **<call>** — <one-line rationale> — revisit 2026-09-16
```

## Step 7 — Surface

Show the archive entry in chat. Tell the user the archive path. Offer:

- *"Want me to schedule a /loop reminder for the revisit date?"* (would use the `loop` skill to fire at the right time)
- *"Push to Notion as a decision card?"*
- *"Need a follow-up decision after this one?"*

## Future enhancements

- Auto-create a calendar event or cron reminder for the revisit (via `compound-engineering:schedule`)
- Composable with `business-brainstorm` — brainstorm scores the idea on 9 dimensions; `decide` formalizes the go/no-go after
- Grep past decisions for patterns ("show me decisions I made that were marked 'easy reverse' but didn't reverse")

## Composes with

- `business-brainstorm` — brainstorm → decide is a natural pipeline for "should I build X"
- `deep-research` — when a decision is waiting on info (Q19), trigger research first
- Memory — load `feedback_*.md` for principles that might be at play (Q34)
- `loop` / `compound-engineering:schedule` — for revisit reminders

## Notes on quality

- **Don't ask all 38.** The point of triage is to skip questions that don't apply. Eight relevant questions > thirty-eight padded ones.
- **Don't soften the call.** "Probably yes, lean toward, maybe should" wastes the skill. Pick.
- **The first instinct (Q9) is sacred.** Always capture it before analysis. If the final call differs from the first instinct, the rationale needs to explain why — that's the whole point of the question.
- **Archive every decision, even small ones.** The compounding value comes from being able to grep "what did I decide about pricing last year" — and that requires writing them down even when they feel obvious in the moment.
