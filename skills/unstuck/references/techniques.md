# Technique inventory — the 10 crowbars

Each technique: when it fires (by wall type), the moves, and a worked example. Run 3–4 per session (T1 always runs). Generate 2–3 angles per technique; don't evaluate while generating.

## Triage by wall type

| Wall type | Always | Lead | Backup |
|---|---|---|---|
| Assumption | T1 | T3 | T5 |
| Framing | T1 | T4, T2 | T5 |
| Gatekeeper | T1 | T10 | T6 |
| Tool/tech | T1 | T9, T6 | T3 |
| Resource | T1 | T7 | T8 |
| Physics/math | T1 (confirm it's real) | — honest exit: reroute the goal | T4 (the rerouted goal often hides one altitude up) |
| Unclear / mixed | T1 | T4 | T8 (provocation shakes loose a classification) |

---

## T1 — Assumption autopsy *(always runs)*

**Fires on:** every wall. Most walls die here.

**Moves:**
1. Write the problem statement verbatim.
2. Enumerate every assumption embedded in it — including the invisible ones (the nouns chosen, the actor assumed, the sequence implied, the tool presumed).
3. Mark each: **verified fact** (you checked, recently, yourself) vs **inherited belief** (docs said, someone said, it's always been that way, you assumed).
4. For each belief: what would it cost to test it right now? Test the cheap ones immediately.

**Example:** "The OG-image renderer can't draw the █ cursor — it renders a box glyph." Assumptions: (a) the cursor must be a *text character* — belief; (b) the default font is the only font — belief, the renderer accepts custom fonts; (c) the design needs a cursor at all — belief. Breaking (a) solves it in minutes: draw the cursor as an orange rectangle `<div>`, not a glyph. (Breaking (b) was the fix for the ✓ checkmark next to it — load a font that has one.)

## T2 — Inversion

**Fires on:** framing walls; any wall where forward motion has stalled.

**Moves:** Ask "how would I *guarantee* this stays blocked / fails completely?" List those answers earnestly — then negate each one. The negations are angles. (Jacobi via Munger: "Invert, always invert.")

**Example:** "Can't get replies to cold outreach." Guarantee zero replies: generic opener, ask for 30 minutes, no reason to reply this week, sent to the wrong person. Negations: hyper-specific opener referencing their work this week; ask for nothing (give something); find the person who *owns the pain*, not the title.

## T3 — First principles

**Fires on:** assumption walls, tool walls with deep inherited design.

**Moves:** Strip the problem to what physics/math/economics actually require. Ignore how it's currently done — that's an artifact of someone else's constraints. Rebuild the minimum path from requirements up. Ask: "if nobody had ever solved this before, and I had today's tools, what would I do?"

**Example:** "Shipping costs make this product unviable." First principles: what does the customer actually need to *receive*? If the value is information + a few grams of material, ship the file and license local production — the freight was an artifact of a pre-digital design.

## T4 — Altitude shift

**Fires on:** framing walls. Also the universal Step 2 restatement.

**Moves:** Restate the problem one level UP (what job is this step serving? could that job be done without this step?) and one level DOWN (what *literally* fails — which line, which field, which sentence?). Walls often exist at exactly one altitude.

**Example:** "The vendor's API has no bulk-export endpoint." Up: the job is *getting our data out monthly* — a scheduled per-record crawl also does that job. Down: the export button in their UI works fine — automate the button (browser automation) instead of the API.

## T5 — Work backwards from solved

**Fires on:** framing and assumption walls; anything where the path forward is foggy.

**Moves:** Assume it shipped. Write the one-paragraph changelog entry / press release dated 3 months out. Now ask: what MUST have been true for that to happen? Chain backwards from the solved state to today. The first link backwards from "solved" is often visible even when the first step forward isn't.

**Example:** "No idea how to get our first 100 users." Changelog from the future: "100 users, 60 from the launch partner's newsletter." Must-have-been-true: a launch partner with an audience who wins by sharing this. That's the actual task — find *that partner* — not "do marketing."

## T6 — Analogical transfer

**Fires on:** tool walls, gatekeeper walls, anything that feels unprecedented.

**Moves:** Name the problem's *structure*, stripped of domain ("limited slots, unpredictable demand," "gatekeeper controls distribution," "cargo must survive a hostile channel"). Ask: who has this structure in a totally different domain — restaurants, logistics, biology, military, dating apps? How do they solve it? Port the mechanism, not the surface.

**Example:** "Users abandon our 9-step onboarding." Structure: mandatory sequence with dropout. Who else: airport security (move the wait into parallel/idle time), video games (tutorial disguised as play). Angles: collect steps 4–9 lazily *during* first use; make step 1 deliver the aha before asking for anything.

## T7 — Constraint toggling

**Fires on:** resource walls.

**Moves:** Take the binding constraint and toggle it BOTH ways:
1. **Remove it:** "If money/time/headcount were free, what would I do?" — then ask what a 5% version of that answer costs.
2. **Tighten it 10x:** "If I had one hour / $100 / just myself, what would I do?" — brutal constraint forces the essential move to the surface.
Both directions expose which constraints are real and which are assumed comfort.

**Example:** "Can't afford a rebrand ($40k agency quote)." Free-money version: full agency process → its 5% core is one senior designer's taste applied to logo + type + 3 templates. 10x-tighter version ($4k): hire that one senior designer for a week. The agency was packaging, not the value.

## T8 — Provocation / random entry

**Fires on:** resource walls, staleness, sessions where the first 3 techniques produced variations of the same idea.

**Moves:** (de Bono) State a deliberately wrong/absurd version of the situation ("Po: customers pay us to see ads," "Po: the app has no interface") — then harvest the *movement*: what direction does the absurdity point? Alternative: random entry — pick an unrelated noun (open a book, point), force-connect it to the problem, harvest.

**Example:** "Newsletter growth is flat." Po: *readers write the newsletter.* Movement: reader-submitted teardowns as a recurring section → contributors share their own issue → each issue ships with built-in distribution.

## T9 — SCAMPER

**Fires on:** tool/tech walls — run it against the blocked component specifically.

**Moves:** (Eberle's mnemonic, built on Osborn's brainstorming checklist.) Against the component that "can't": **S**ubstitute (different primitive/library/channel), **C**ombine (merge with an adjacent step), **A**dapt (borrow a mechanism that works elsewhere in the system), **M**agnify/minify (what if this step were 10x bigger or disappeared?), **P**ut to other use (can an existing feature be abused into doing this?), **E**liminate (does this step need to exist?), **R**everse (flip the order/direction/actor).

**Example:** "The metadata route can't re-export another route's component" (Next.js twitter-image, 2026-07). Substitute: literal config exports + delegated default import — same dedupe, analyzable statically. Eliminate was also on the table: delete twitter-image entirely and let og:image serve both.

## T10 — Interrogate the no

**Fires on:** gatekeeper walls — a person or org said no.

**Moves:**
1. **Who exactly said no?** (A person? A policy? A support macro? The intern who answers email?) A "no" from someone without authority to say yes is routing information, not an answer.
2. **To what exactly?** Replay the ask — was it the thing you wanted, or a scary-sounding version of it?
3. **What's their incentive?** What does yes cost them (risk, effort, precedent)? Can you remove that cost?
4. **What would make it a yes?** Smaller ask, different framing, pilot instead of commitment, their win made explicit, a different door entirely (partnerships instead of sales, API instead of contract).
5. **Guardrail:** if they understood the ask and meant the no — that no is real. The move is finding a different door they'd *happily* open, never pushing the closed one.

**Example:** "The conference rejected our sponsorship." Who: the sponsorship coordinator, sold-out tier. To what: a booth. Incentive: floor space is zero-sum. Different door: the speaker dinner needs a host; the lanyard vendor fell through. Same visibility, no booth, cheaper — and the coordinator *wants* to say yes to solving their own problem.

---

## Anti-patterns

- **Costume angles** — 10 angles that are 3 ideas reworded. The quantity gate counts *kinds*.
- **Premature feasibility** — "that won't work because…" during generation kills the wild angle that would have seeded the viable one. Triage is Step 5, not Step 4.
- **Technique tourism** — running all 10 techniques shallowly beats nothing, but 3 techniques run hard beat all 10 run soft. Trust the triage.
- **Skipping the restatement** — techniques applied to a badly-stated problem produce well-organized answers to the wrong question.
