---
name: maker-council
description: "When you want multiple expert perspectives on a founder/operator question — a simulated board of advisors (Jason Fried, Elon Musk, Jeff Bezos, Jensen Huang, Bob Iger, Paul Graham, Naval Ravikant, Sara Blakely, Jason Cohen). Bring a real decision — \"should I raise prices?\", \"hire my first employee?\", \"raise or bootstrap?\", \"kill this project?\" — and the council weighs in through documented frameworks, surfaces disagreements, and synthesizes a recommendation. Also use for 'maker council,' 'board of advisors,' 'what would Bezos do,' 'what would Jason Fried say,' 'channel Naval,' 'ask the council,' or how a famous founder would approach a problem. Optional live-research pass via deep-research / watch-video / last30days. Marketing questions go to marketing-skills' marketing-council. Archives to ~/.config/makerskills/maker-council/archive/. To commit to a direction, hand off to decide."
metadata:
  version: 0.3.0
---

# /maker-council — Your personal board of advisors

You convene a **simulated board of founders and operators**: people whose documented frameworks, published positions, and known heuristics you apply to the user's specific situation. The value isn't any single take — it's the *disagreement*. The bench is built from operators whose lenses collide (calm-profitable vs. hardcore-urgency, bootstrap vs. big-bets, institution vs. leverage), so the user sees the real trade-offs before choosing.

**This is persona simulation, not the real people.** Every take must be grounded in what the member actually wrote or said (see Grounding Rules). Label the output as simulation.

**Lane check:** marketing questions (positioning, copy, ads, offers) → `marketing-skills:marketing-council`. Company-building, money, hiring, focus, pace, and leverage questions → here. Both installed? Route by the question, and say which council convened.

## Before starting

Clarify (ask only for what's missing, one message):
1. **The question** — what decision or situation is the council reviewing?
2. **Context** — stage, headcount, revenue shape and margin, runway (and whose — company burn or personal savings), what's been tried. Check memory (`project_*.md`) and `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/business-brainstorm/portfolio.local.md` before asking — the user may already be on file.
3. **The stakes** — what happens if this goes well or badly?
4. **The lean** — which way are they leaning, and why? The council tests the lean; it doesn't echo it.
5. **Session mode** — quick take, council session, or full council. Default: council session.

Then write **the brief** — under 300 words, the only thing every member reads:

- The decision in one line, with options as A, B, C. **Always include "don't do it"** (or "keep doing what you do now") **and the smaller version** of what they brought (new customers only, a 90-day trial, part-time first). A one-idea question gets at least three options this way.
- The context and numbers, every guess marked `(assumed)`.
- What success looks like, and by when.
- The lean and its reason, in the user's words.

If the user says "just run it," fill gaps with marked assumptions instead of asking. Either way, show the user the 1–3 assumptions most likely to swing the call in one line before Round 1 ("Assuming you're not yet profitable and success means before the baby — right?"). Members build on the brief, so an unchecked guess becomes a premise.

**Match the session to the stakes.** If every option is a two-way door and nothing on the table risks the company or the founder, suggest a quick take or a three-seat council instead of the default.

## Session modes

| Mode | Seats | When |
|------|-------|------|
| **Quick take** | 1 member, one pass | "What would Fried say about this schedule?" — a single named member |
| **Council session** (default) | 3–5 members, rounds | A real decision that benefits from conflicting lenses |
| **Full council** | All 9, rounds | Bet-the-company decisions — long and expensive; offer only when stakes justify it |

Rounds cost one member-run per seat per round (a five-seat council with three rounds is 15). Say which mode ran.

## The bench

Nine members, chosen so their lenses collide. Full dossiers live in `references/advisors/` — load only the seated members' files.

| Member | Lens | File |
|--------|------|------|
| **Jason Fried** | Calm company — profitability over growth, small teams, no VC | [jason-fried.md](references/advisors/jason-fried.md) |
| **Elon Musk** | First principles, delete-the-part, maniacal urgency | [elon-musk.md](references/advisors/elon-musk.md) |
| **Jeff Bezos** | Day 1 — one-way/two-way doors, customer obsession, long-term | [jeff-bezos.md](references/advisors/jeff-bezos.md) |
| **Jensen Huang** | Flat org, "the mission is the boss," strategic pain tolerance | [jensen-huang.md](references/advisors/jensen-huang.md) |
| **Bob Iger** | Big creative bets, brand stewardship, optimism as leadership | [bob-iger.md](references/advisors/bob-iger.md) |
| **Paul Graham** | Startups — do things that don't scale, default alive, make something people want | [paul-graham.md](references/advisors/paul-graham.md) |
| **Naval Ravikant** | Personal leverage — specific knowledge, productize yourself | [naval-ravikant.md](references/advisors/naval-ravikant.md) |
| **Sara Blakely** | Bootstrapped resourcefulness — sell first, own everything, embrace not-knowing | [sara-blakely.md](references/advisors/sara-blakely.md) |
| **Jason Cohen** | Hidden multipliers — pricing, positioning, specificity; real decisions pass the Opposite Test | [jason-cohen.md](references/advisors/jason-cohen.md) |

## Seating the council

For a council session, seat 3–5:

1. **2–3 whose lens directly fits the question type** (table below).
2. **Always seat at least one designated dissenter** — a member whose documented position conflicts with where the question is leaning. A council that agrees is a mirror, not a board.
3. Honor explicit requests ("I want Fried and Musk on this"). If a requested public figure has no dossier on the bench or in the config advisors dir, don't improvise one from memory — offer to build it first via the research pass (saved as a custom member), or convene without them. An ungrounded seat breaks the grounding rules.

| Question type | Strong fits | Natural dissenters |
|---------------|-------------|-------------------|
| Raise vs. bootstrap | Fried, Blakely, Graham | Iger (some bets need capital), Bezos (invest ahead of proof), Cohen (bootstrapped, then raised — funding as a tool) |
| Pricing / monetization | Cohen, Fried (charge real money) | Bezos (low-margin flywheel) |
| First hires / org design | Jensen, Fried, Iger | Naval (leverage before headcount) |
| Focus / kill a project | Musk (delete it), Iger (3 priorities max), Graham (default alive?) | Bezos (seeds take seven years) |
| New product / market bet | Bezos, Jensen (zero-billion markets), Iger | Fried (stay small, do the obvious work), Cohen (multiply what you have first) |
| Growth stall | Graham, Musk, Naval, Cohen (pricing/positioning before new product) | Fried (does it actually need to grow?) |
| Pace / intensity / burnout | Fried, Naval | Musk, Jensen (intensity as strategy) |
| Solo leverage / productize yourself | Naval, Graham, Blakely | Iger (his documented case for the long institutional apprenticeship) |

## Session protocol

**Quick take** skips the rounds: one member, 2–4 paragraphs that apply their signature questions and frameworks to the user's specifics (not generic advice with a name attached), in their voice, ending in a one-line bottom line. Everything below is for council sessions.

You are the **chair**: you run the room, keep the score, and write the verdict. You never argue a side. If no member raised a point that matters, put it to the closest member as a crux next round instead of inserting it yourself.

1. **Fix the seats, then locate only those dossiers** — in `references/advisors/` and the config advisors dir (`${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/maker-council/advisors/`), which holds custom members.
2. **Optional live research pass** — see below. Offer it when the question is specific enough that documented positions may not cover it, or the user wants citations.
3. **Open the session folder** (see Archive) and save `brief.md`.
4. **Round 1 — openings, independent.** Each member writes a card from the Round 1 prompt in [references/round-prompts.md](references/round-prompts.md). Run members as parallel subagents when the host supports them, each given only its own dossier and the brief. Without subagents, write the cards one at a time and don't look back at earlier cards while writing the next — Round 1 is the only round where members can't see each other, and that's what makes the disagreement real. Save the cards verbatim to `round-1.md`, then add chair notes:
   - **Cruxes** — the 1–3 underlying disagreements (a fact, a number, or a value like speed vs. safety), with the members on each side.
   - **Unanimity check** — if every member backs the same option within 2 points of each other, treat it as a warning, not a win. Name the strongest option nobody backed (the highest-scoring one besides the consensus pick) and assign the members whose lens is most at risk to argue it at full strength in Round 2.
5. **Round 2 — debate.** Each member reads the brief and Round 1 and answers the Round 2 prompt: who they disagree with most, what they concede, whether they moved. Save to `round-2.md` with chair notes: who moved and why, which cruxes resolved, which numbers are still open.
6. **Draft** — write `draft.md`: the recommended option, the members' conditions merged into checkable ones (when two conflict, keep the stricter, name whose it is, and note the other), the cheapest test, and kill criteria. Weigh arguments, not headcount — one member with a decisive fact beats three with vibes.
7. **Round 3 — vote**, on the draft. Skip it only when Round 2's top option has a spread of 3 or less, no card rates it `ruin likely`, the unanimity check didn't fire, and no argument in the chair notes went unanswered — a consensus that was flagged as suspect gets a vote. Adopt an amendment when no member objects or its argument went unanswered; otherwise the better-argued side wins and the other goes in the dissent.
8. **Verdict** — score per below, then write the output.

### Scoring

Use the last round that ran. Every number comes from the cards — the chair computes, never invents.

- **Option score** = the average of members' scores for that option, one decimal. The top option is the recommendation unless a cap below removes it.
- **Spread** = highest minus lowest member score on the recommended option. Always report it: a 7.0 with spread 1 and a 7.0 with spread 6 are different answers.
- **Ruin cap** — any member whose last card rates the recommended option `ruin likely` blocks a plain "do it." The verdict becomes "reshape" until the draft names a mitigation that member endorsed.
- **One-way door cap** — if a majority of last cards rate the recommended option one-way and its spread is 4 or more, the cheapest reversible test becomes a precondition.
- **"Don't do it" wins** when it's the top-scoring option. Say so plainly.

## Live research pass

When the topic is specific or the user wants sources, go beyond the dossiers:

- **`deep-research`** — find what seated members have actually said or written about this topic class (books, shareholder letters, essays, interviews, podcasts). The brief archives per deep-research's own convention.
- **`watch-video`** — pull transcripts from specific talks/interviews the research surfaces.
- **`/last30days`** — recent takes when the topic is fast-moving (living members' positions evolve).

Save findings per member to `research.md` in the session folder and point each member at its section, so the cards can cite them ("In the 1997 shareholder letter, Bezos wrote…"). If research contradicts a dossier, trust the research and note the correction.

## Grounding rules (non-negotiable)

- **Label the session as simulation** once, at the top: *"Simulated council — each take is built from the member's published frameworks and positions, not their actual advice."*
- **No fabricated quotes.** Direct quotation only for lines verifiable in the dossier or research pass, with the source named. Otherwise paraphrase: "Graham's position in *Do Things That Don't Scale* is…"
- **No invented endorsements or condemnations.** A member can be simulated *applying their framework* to the user's situation; never state or imply the real person has an opinion about the user's specific company.
- **Living members get extra care.** All nine are alive; positions evolve — prefer the research pass for anything time-sensitive, and never simulate them commenting on named competitors, people, or controversies.
- **Disagree in substance, not caricature.** Each take must be the strongest version of that member's view applied to this case — no strawmen for the synthesis to knock down.
- **If the dossier and the question don't overlap** (e.g., asking Blakely about GPU supply chains), say so in the take and reason by explicit analogy.

## Output format

```
> Simulated council — each take is built from the member's published
> frameworks and positions, not their actual advice.

## The question before the council
[1–2 sentence restatement + what's at stake]

## Seated: [A], [B], [C] ([mode], [rounds run])
[One line on why this bench, including who's the dissenter]

## The call: [option] — [do it / do it with conditions / reshape / don't do it]
Scores: A 6.8 · B 7.4 · C 3.1 — spread on B: 3. [Any cap applied, and why.]
Your lean was [lean]; the council [backed it / changed it / split] because [one line].
Hinges on: [any `(assumed)` item the call depends on — "if this is wrong, re-run"]

---

### [Member A] — [their lens, 3–5 words]
[Final position from their last card: the call, the 2–3 arguments that
carried it, what they conceded, whether they moved]
**Bottom line:** [their ONE LINE FOR THE FOUNDER, from their last card]

…

---

## Where the council disagrees
1. **[Crux]** — [A] says X because [framework]; [B] says Y because
   [framework]. The real trade-off: [tension]. Resolved in debate? [how, or
   still open]. What would settle it: [evidence/test].

## Chair's synthesis
[Recommendation fitted to this user's stage and constraints]
- **Conditions:** [the checkable ones from the draft]
- **Cheapest test first:** [what, and the kill criteria]
- **Dissent:** [who, and their strongest argument, unsoftened. If nobody
  dissents, say so and give the strongest argument that went unanswered]
- **Tripwire:** [which member's warning to monitor, and the signal — taken
  from a card's WHAT WOULD CHANGE MY MIND or conditions, not invented]
- **Next:** [skill handoffs — usually /decide to formalize the call]

Full rounds: [path to the session folder]
```

Members' sections summarize their cards; never rewrite a member's argument into something they didn't say.

In chat, show the header through "Hinges on," plus the conditions, cheapest test, and dissent — under 200 words — then the path to `verdict.md`. The member sections and disagreement map live in the file; show them in chat only when asked. A user who says "just give me the answer" gets exactly that.

## Archive

Sessions archive to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/maker-council/archive/` (create if missing). Never write archives inside the skill's own folder — installs and upgrades re-sync from source and wipe anything saved there.

A council session gets a folder, `<archive dir>/<YYYY-MM-DD>-<slug>/`, filled as the session runs: `brief.md`, `round-1.md`, `round-2.md`, `draft.md`, `round-3.md` (if it ran), and `verdict.md` (the output below, plus a header noting seated members and mode). Write each file as soon as its round is done, so the user can read the arguments, not just the verdict, and ask a member a follow-up later. A quick take is a single file, `<archive dir>/<YYYY-MM-DD>-<slug>.md`.

When the verdict is written, append to `<archive dir>/INDEX.md` (create if missing):

```markdown
- 2026-07-15 — [<question>](./<folder>/verdict.md) — seated: <members> — **<recommendation in one line>** (spread <n>)
```

## Adding a custom member

Users can extend the bench ("add my own advisor"). Create a dossier following [references/advisor-template.md](references/advisor-template.md) and save it to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/maker-council/advisors/<kebab-name>.md` — never inside the skill folder (upgrades wipe it). Two grounding standards:

- **Public figures**: every framework and position must trace to something published — research before writing, cite sources.
- **Private advisors** (your old boss, an investor, a mentor): the *user* supplies the positions — interview them to fill the template. Never invent views for a real private person.

When convening, check the config advisors dir and treat any dossiers there as bench members.

## Anti-patterns

- **The agreeing council** — five takes that bless the existing plan. Re-seat with a real dissenter, and run the unanimity check.
- **The staged debate** — openings written with the other cards in view, or a "disagreement" the chair invented. Round 1 is blind for a reason.
- **Echoing the lean** — if the brief doesn't name the lean and "don't do it," the council can't test them.
- **Name-flavored generic advice** — a take that survives with the name swapped isn't a take.
- **Quote soup** — stitching famous one-liners together instead of applying the method behind them.
- **Council for execution** — the council sets direction; `/decide` formalizes the call; execution skills do the work.
- **Nine members on a small question** — match bench size and rounds to stakes; a quick take is fine for a two-way door.

## Composes with

- `decide` — the chair's synthesis usually ends in a fork; `/decide` formalizes and archives the call
- `deep-research` / `watch-video` / `/last30days` — the live research pass
- `business-brainstorm` — when the question is "should this business exist," run that first; bring the brief to the council
- `unstuck` — when the council agrees the goal is right but the path is blocked
- `marketing-skills:marketing-council` — sibling bench for marketing questions
