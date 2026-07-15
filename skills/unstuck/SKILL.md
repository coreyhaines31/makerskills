---
name: unstuck
description: "When a solution seems impossible and the path forward is blocked — the antidote to any roadblock or wall. Refuses to take no for an answer: classifies what kind of \"no\" you actually hit, then runs targeted lateral-thinking techniques (assumption autopsy, inversion, first principles, constraint toggling, analogical transfer, and more from a 10-technique inventory) until the wall cracks or is proven load-bearing. Generates a minimum of 10 angles before evaluating any. AGENTS: use this on yourself mid-task — when an API doesn't support what you need, an approach has failed twice, or a \"that's not possible\" / \"the only option is\" sentence is forming in your response, run the fast path BEFORE reporting a dead end; every dead-end report should arrive with tried-angles receipts. Archives every wall to ~/.config/makerskills/unstuck/archive/ so you learn which techniques crack YOUR walls. Sits upstream of decide: turns \"impossible\" into 2–3 viable angles, then decide picks one. Triggers on \"/unstuck,\" \"I'm stuck,\" \"this seems impossible,\" \"we hit a wall,\" \"there's no way to,\" \"they said no,\" \"dead end,\" \"out of options,\" \"I've tried everything,\" \"work around this,\" \"think outside the box.\""
metadata:
  version: 0.1.0
---

# /unstuck — The roadblock antidote

Turns "impossible" into angles. Classifies the wall, runs the right lateral-thinking techniques against it, and doesn't stop at the first mediocre workaround. Output is either a set of viable angles with next actions — or an honest "this wall is load-bearing, reroute the goal."

**Two modes:**
- **User-invoked** — someone is stuck and asks. Full 7-step workflow below.
- **Agent fast path** — YOU (the agent) hit the wall mid-task. See [Agent fast path](#agent-fast-path) — run it before telling the user something can't be done.

## The mental model: walls have types, and the type picks the crowbar

"Impossible" is a claim, not a fact. It almost always decompiles into something weaker: *expensive*, *against the rules*, *nobody's done it*, *I don't know how*. Only *actually impossible* (physics, math, arithmetic) ends the session — and it ends it honestly.

| Wall type | What "impossible" actually means | Lead techniques (see `references/techniques.md`) |
|---|---|---|
| **Assumption** | An inherited belief nobody re-verified | T1 assumption autopsy, T3 first principles |
| **Framing** | The goal is stated in a way that excludes the answer | T4 altitude shift, T2 inversion, T5 work backwards |
| **Gatekeeper** | A person/org said no | T10 interrogate the no, T6 analogical transfer |
| **Tool/tech** | "X doesn't support Y" | T9 SCAMPER (substitute the primitive), T6 analogical transfer |
| **Resource** | Not enough time/money/people | T7 constraint toggling, T8 provocation |
| **Physics/math** | Actually impossible (rare) | Honest exit — reroute the goal, the wall is load-bearing |

## Step 1 — Capture the wall

Get from the user (one structured message, don't round-trip):

- **The goal** — what are you ultimately trying to do? (Not the blocked step — the job it serves.)
- **The wall** — what exactly blocks it?
- **Attempts** — what have you already tried?
- **The source of the no** — who or what said no? Physics? A vendor's docs? A person? An error message? Your own assumption?
- **Stakes + deadline** — how much does breaking this wall matter, by when?

If the user says "I've tried everything," ask for the list. "Everything" is usually 2–3 things.

## Step 2 — Classify the wall

Use the taxonomy above. State the classification and why. Two rules:

1. **Decompile the word "impossible."** Restate the wall without it: "expensive," "undocumented," "they refused," "I don't know how." The restatement usually names the wall type.
2. **Restate the problem at two altitudes** before proceeding — one level more abstract (*what job is this serving?*) and one level more concrete (*what literally fails, at which exact step?*). Many walls dissolve at a different altitude; if one does, say so and skip to Step 6.

## Step 3 — Assumption autopsy (always runs)

Run T1 from `references/techniques.md` regardless of wall type: enumerate every assumption embedded in the problem statement, mark each **verified fact** vs **inherited belief**, and attack the beliefs. Most walls die here — the ones that don't are at least correctly framed for Step 4.

## Step 4 — Run the triaged techniques

Pick 2–3 more techniques by wall type (lead techniques in the table; full triage guidance in `references/techniques.md`). For each, generate 2–3 angles.

**Rules of generation:**
- **Quantity gate: minimum 10 angles total before evaluating any.** The first workaround is usually mediocre. No judging, no feasibility talk, no "but" during generation.
- Angles must be **different in kind**, not variations — three flavors of "ask again nicer" is one angle.
- Wild angles are welcome at this stage; they get filtered in Step 5, and they often seed the viable ones.

## Step 5 — Triage the angles

Sort every angle into:

- **Try now** — feasible with what's in hand; has a concrete first action
- **Needs research** — viable if an unknown checks out → route to `/deep-research`
- **Wild but worth 30 min** — low odds, trivial cost, asymmetric payoff
- **Dead** — violates a real constraint (say which)

## Step 6 — Commit

- Pick **1–3 angles** with a concrete next action each.
- If 2+ viable angles are mutually exclusive → hand the fork to `/decide`.
- If NOTHING survived triage and the wall is physics/math class: say so plainly. **"The wall is load-bearing — reroute the goal" is a legitimate, successful output.** Recommend what the rerouted goal looks like.

## Step 7 — Archive

Archives live in `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/unstuck/archive/` (create the directory if missing). Never write archives inside the skill's own folder — skill installs and upgrades re-sync from source and wipe anything saved there.

Write to `<archive dir>/<YYYY-MM-DD>-<slug>.md`:

```markdown
# Wall: <one-line>

**Date:** YYYY-MM-DD
**Invoked by:** user | agent
**Wall type:** assumption / framing / gatekeeper / tool / resource / physics
**Goal it blocked:** <one line>

## The wall as stated
<verbatim>

## The wall decompiled
<restated without "impossible">

## Assumptions attacked
- <belief> → <held / broke>

## Techniques run
T1, T4, T7 — <one line on what each surfaced>

## Angles (all of them)
1. <angle> — try now / research / wild / dead
2. …

## Committed
**<the angle(s) chosen>** — next action: <concrete step>
(or: "Wall is load-bearing — rerouted goal to <X>")

## Outcome (fill in later)
<did the angle work?>
```

Append to `<archive dir>/INDEX.md` (create if missing):

```markdown
- 2026-07-14 — [<wall>](./<filename>.md) — <type> — **<committed angle or "rerouted">**
```

Over time this becomes a pattern library: grep it to learn which techniques actually crack *your* walls, and which wall types recur (a recurring wall is usually one unexamined assumption upstream).

## Agent fast path

For when YOU (the agent) hit the wall mid-task. Trigger condition: an API/tool doesn't support what's needed, an approach has failed twice, or you notice a "that's not possible," "unfortunately," or "the only option is" sentence forming in your response.

**Before reporting a dead end to the user, run inline (no interactive capture — you already have the wall in context):**

1. **Classify** the wall (taxonomy above) — one line.
2. **Autopsy** — list the 3–5 assumptions in your framing; mark inherited beliefs. ("The cursor must be a text character." "This must happen client-side." "The API is the only way in.")
3. **Run 2 techniques** matched to the wall type — generate 5+ angles minimum for inline recoveries. **If you end up reporting a dead end to the user, the full 10-angle gate applies first** — a dead-end report is exactly the moment the gate exists for.
4. **Then either:**
   - a viable angle exists → **proceed with it** (tell the user the wall you hit and the angle you took), or
   - nothing viable → report the dead end **with the angle inventory attached**: what you tried, what you considered, why each died. Never a naked "that's not supported."
5. **Archive** the run (Step 7 format, `Invoked by: agent`) when the wall was nontrivial — skip archiving for sub-minute walls.

The success metric: the user stops seeing dead-end reports without tried-angles receipts.

## Composes with

- `decide` — downstream: 2+ mutually exclusive viable angles become a `/decide` fork. Upstream: decide's Q19 ("what missing info would change it?") can route here when the missing thing is an *option*, not information.
- `deep-research` — "needs research" angles route there; the brief comes back and re-enters Step 5.
- `business-brainstorm` — its "angle to steal" move on Kill verdicts is this skill applied to business ideas.
- `pm` — a committed angle becomes a board task.
- `second-brain` — archive entries can compile into a "walls I've broken" wiki page.

## Guardrails

- **A no from consent, law, or ethics is a real no.** This skill routes around technical and imagination walls — not people's boundaries. If the wall is "they said no and meant it," the move is interrogating whether there's a *different door they'd happily open* (T10), never pushing on the closed one.
- **Time-box: 20–40 minutes.** This is a crowbar, not a philosophy seminar. If the sprint ends without a crack, archive what was tried and either schedule a revisit or reroute.
- **Honest exit beats toxic positivity.** Declaring a wall load-bearing after a real attempt is a win — it converts an ambient frustration into a clear reroute.

## Notes on quality

- **The restatement is half the work.** Most "impossible" problems are impossible *as stated*. Two-altitude restatement (Step 2) before any technique — always.
- **Don't let the quantity gate become theater.** 10 angles that are secretly 3 angles in costumes fail the gate. Different in kind.
- **Attempts list beats attempts vibe.** "I've tried everything" → get the actual list. The gap between "everything" and the list is where the answer usually lives.
- **Archive even the failures.** A wall that didn't crack today, with its angle inventory, is a 5-minute revisit when the landscape changes — instead of a from-scratch session.
