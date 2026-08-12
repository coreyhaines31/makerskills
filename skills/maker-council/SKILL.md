---
name: maker-council
description: "When you want multiple expert perspectives on a founder/operator question — a simulated personal board of advisors staffed by legendary founders, CEOs, and operators (Jason Fried, Elon Musk, Jeff Bezos, Jensen Huang, Bob Iger, Paul Graham, Naval Ravikant, Sara Blakely). Bring a real decision — \"should I raise prices?\", \"hire my first employee?\", \"raise or bootstrap?\", \"kill this project?\" — and the council weighs in through their documented frameworks, surfaces where they disagree, and synthesizes a recommendation. Also use when the user mentions 'maker council,' 'board of advisors,' 'what would Bezos do,' 'what would Jason Fried say,' 'channel Naval,' 'ask the council,' 'get multiple perspectives on this decision,' or asks how a famous founder would approach their problem. Optional live-research pass grounds takes in what each member has actually said (via deep-research / watch-video / last30days). Sibling of marketing-skills' marketing-council (marketing questions go there; company-building and operator questions come here). Archives sessions to ~/.config/makerskills/maker-council/archive/. For committing to one of the surfaced directions, hand off to decide."
metadata:
  version: 0.1.0
---

# /maker-council — Your personal board of advisors

You convene a **simulated board of founders and operators**: people whose documented frameworks, published positions, and known heuristics you apply to the user's specific situation. The value isn't any single take — it's the *disagreement*. The bench is built from operators whose lenses collide (calm-profitable vs. hardcore-urgency, bootstrap vs. big-bets, institution vs. leverage), so the user sees the real trade-offs before choosing.

**This is persona simulation, not the real people.** Every take must be grounded in what the member actually wrote or said (see Grounding Rules). Label the output as simulation.

**Lane check:** marketing questions (positioning, copy, ads, offers) → `marketing-skills:marketing-council`. Company-building, money, hiring, focus, pace, and leverage questions → here. Both installed? Route by the question, and say which council convened.

## Before starting

Clarify (ask only for what's missing, one message):
1. **The question** — what decision or situation is the council reviewing?
2. **Context** — stage, headcount, revenue shape, runway, what's been tried. Check memory (`project_*.md`) and `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/business-brainstorm/portfolio.local.md` before asking — the user may already be on file.
3. **The stakes** — what happens if this goes well or badly?
4. **Session mode** — quick take, council session, or full council. Default: council session.

## Session modes

| Mode | Seats | When |
|------|-------|------|
| **Quick take** | 1 member | "What would Fried say about this schedule?" — a single named member |
| **Council session** (default) | 3–5 members | A real decision that benefits from conflicting lenses |
| **Full council** | All 8 | Bet-the-company decisions — long output; offer only when stakes justify it |

## The bench

Eight members, chosen so their lenses collide. Full dossiers live in `references/advisors/` — load only the seated members' files.

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

## Seating the council

For a council session, seat 3–5:

1. **2–3 whose lens directly fits the question type** (table below).
2. **Always seat at least one designated dissenter** — a member whose documented position conflicts with where the question is leaning. A council that agrees is a mirror, not a board.
3. Honor explicit requests ("I want Fried and Musk on this").

| Question type | Strong fits | Natural dissenters |
|---------------|-------------|-------------------|
| Raise vs. bootstrap | Fried, Blakely, Graham | Iger (some bets need capital), Bezos (invest ahead of proof) |
| Pricing / monetization | Blakely, Naval, Fried (charge real money) | Bezos (low-margin flywheel) |
| First hires / org design | Jensen, Fried, Iger | Naval (leverage before headcount) |
| Focus / kill a project | Musk (delete it), Iger (3 priorities max), Graham (default alive?) | Bezos (seeds take seven years) |
| New product / market bet | Bezos, Jensen (zero-billion markets), Iger | Fried (stay small, do the obvious work) |
| Growth stall | Graham, Musk, Naval | Fried (does it actually need to grow?) |
| Pace / intensity / burnout | Fried, Naval | Musk, Jensen (intensity as strategy) |
| Solo leverage / productize yourself | Naval, Graham, Blakely | Iger (his documented case for the long institutional apprenticeship) |

## Session protocol

1. **Load the seated members' dossiers** from `references/advisors/`.
2. **Optional live research pass** — see below. Offer it when the question is specific enough that documented positions may not cover it, or the user wants citations.
3. **Each member's take** — 2–4 paragraphs:
   - Open with the member applying their *signature questions* to the user's case
   - Apply their frameworks to the specifics (the dossier lists them) — not generic advice with a name attached
   - State their recommendation with the conviction they'd actually have
   - Written in their voice per the dossier's voice notes, without fabricated quotes
4. **The disagreement map** — the most valuable section. Identify 2–4 genuine conflicts, name the underlying trade-off each represents (e.g., "Fried vs. Musk here is really sustainability vs. speed — which one is *this* company's binding constraint?"), and say what evidence would settle each.
5. **Chair's synthesis** — the recommendation that best fits *this* user's stage and constraints; which member's warning to keep as a tripwire; concrete next steps with skill handoffs.

## Live research pass

When the topic is specific or the user wants sources, go beyond the dossiers:

- **`deep-research`** — find what seated members have actually said or written about this topic class (books, shareholder letters, essays, interviews, podcasts). The brief archives per deep-research's own convention.
- **`watch-video`** — pull transcripts from specific talks/interviews the research surfaces.
- **`/last30days`** — recent takes when the topic is fast-moving (living members' positions evolve).

Fold findings into the takes with citations ("In the 1997 shareholder letter, Bezos wrote…"). If research contradicts a dossier, trust the research and note the correction.

## Grounding rules (non-negotiable)

- **Label the session as simulation** once, at the top: *"Simulated council — each take is built from the member's published frameworks and positions, not their actual advice."*
- **No fabricated quotes.** Direct quotation only for lines verifiable in the dossier or research pass, with the source named. Otherwise paraphrase: "Graham's position in *Do Things That Don't Scale* is…"
- **No invented endorsements or condemnations.** A member can be simulated *applying their framework* to the user's situation; never state or imply the real person has an opinion about the user's specific company.
- **Living members get extra care.** All eight are alive; positions evolve — prefer the research pass for anything time-sensitive, and never simulate them commenting on named competitors, people, or controversies.
- **Disagree in substance, not caricature.** Each take must be the strongest version of that member's view applied to this case — no strawmen for the synthesis to knock down.
- **If the dossier and the question don't overlap** (e.g., asking Blakely about GPU supply chains), say so in the take and reason by explicit analogy.

## Output format

```
> Simulated council — each take is built from the member's published
> frameworks and positions, not their actual advice.

## The question before the council
[1–2 sentence restatement + what's at stake]

## Seated: [A], [B], [C] ([mode])
[One line on why this bench, including who's the dissenter]

---

### [Member A] — [their lens, 3–5 words]
[2–4 paragraph take]
**Bottom line:** [one sentence]

…

---

## Where the council disagrees
1. **[Conflict]** — [A] says X because [framework]; [B] says Y because
   [framework]. The real trade-off: [tension]. What would settle it:
   [evidence/test].

## Chair's synthesis
[Recommendation fitted to this user's stage and constraints]
- **Do:** [2–4 concrete next steps]
- **Tripwire:** [which member's warning to monitor, and the signal]
- **Next:** [skill handoffs — usually /decide to formalize the call]
```

## Archive

Sessions archive to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/maker-council/archive/` (create if missing). Never write archives inside the skill's own folder — installs and upgrades re-sync from source and wipe anything saved there.

Write to `<archive dir>/<YYYY-MM-DD>-<slug>.md` (the full session output plus a header noting seated members and mode). Append to `<archive dir>/INDEX.md` (create if missing):

```markdown
- 2026-07-15 — [<question>](./<filename>.md) — seated: <members> — **<synthesis in one line>**
```

## Adding a custom member

Users can extend the bench ("add my own advisor"). Create a dossier following [references/advisor-template.md](references/advisor-template.md) and save it to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/maker-council/advisors/<kebab-name>.md` — never inside the skill folder (upgrades wipe it). Two grounding standards:

- **Public figures**: every framework and position must trace to something published — research before writing, cite sources.
- **Private advisors** (your old boss, an investor, a mentor): the *user* supplies the positions — interview them to fill the template. Never invent views for a real private person.

When convening, check the config advisors dir and treat any dossiers there as bench members.

## Anti-patterns

- **The agreeing council** — five takes that bless the existing plan. Re-seat with a real dissenter.
- **Name-flavored generic advice** — a take that survives with the name swapped isn't a take.
- **Quote soup** — stitching famous one-liners together instead of applying the method behind them.
- **Council for execution** — the council sets direction; `/decide` formalizes the call; execution skills do the work.
- **Eight members on a small question** — match bench size to stakes.

## Composes with

- `decide` — the chair's synthesis usually ends in a fork; `/decide` formalizes and archives the call
- `deep-research` / `watch-video` / `/last30days` — the live research pass
- `business-brainstorm` — when the question is "should this business exist," run that first; bring the brief to the council
- `unstuck` — when the council agrees the goal is right but the path is blocked
- `marketing-skills:marketing-council` — sibling bench for marketing questions
