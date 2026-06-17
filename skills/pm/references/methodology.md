# Methodology — kanban + Eisenhower + async

## Kanban core

### Why kanban

- **Make work visible.** Cards on columns. Nothing hidden in someone's head.
- **Pull, don't push.** Only start new work when capacity opens — finishing > starting.
- **Limit WIP.** Multitasking is the most reliable way to ship nothing. Cap In Progress.
- **Flow over batch.** Small cards moving steadily beats heroic sprints.
- **Inspect and adapt.** Look at flow weekly. If cards pile up in one column, that's the constraint.

### The 5-column flow (Corey's default)

```
Backlog  →  Ready  →  In Progress  →  Review/Blocked  →  Done/Archived
```

- **Backlog**: everything that *might* matter. Wide net. No commitment yet.
- **Ready**: triaged. Well-defined enough that anyone could pick it up. Has acceptance criteria.
- **In Progress**: actively being worked. Strict WIP limit.
- **Review/Blocked**: waiting on someone or something external. Should be the shortest-lived state — if a card lives here >5 days, escalate or kill.
- **Done/Archived**: shipped or explicitly killed. Archived weekly.

### Card hygiene

A good card has:
- **Title** — verb-first ("Ship Magister waitlist email" not "Magister email")
- **Acceptance criteria** — what does "done" look like? 1–3 bullets.
- **Owner** — even for solo projects: which "hat" is wearing this?
- **Size** — XS / S / M / L (XS = <2 hrs, S = <1 day, M = 2–3 days, L = >1 week — break it down)

Cards that don't meet hygiene live in Backlog, not Ready.

## Eisenhower matrix — the prioritization overlay

```
                    Urgent          Not Urgent
Important           Q1: Do          Q2: Schedule
Not Important       Q3: Delegate    Q4: Delete
```

### Quadrant rules

- **Q1 — Urgent + Important.** Do it. Move to Ready (or In Progress if capacity). These earn priority within Ready.
- **Q2 — Important, Not Urgent.** *This is where leverage lives.* Schedule it. Most Q2 items become Q1 emergencies if neglected — proactively pulling Q2 is the difference between operators who compound and ones who firefight.
- **Q3 — Urgent, Not Important.** Delegate. If there's nobody to delegate to (solo project), ask: is this actually important and I'm mislabeling it, or is it actually noise I'm letting trick me?
- **Q4 — Not Urgent, Not Important.** Archive. The hardest skill in PM is closing tabs.

### When to apply Eisenhower

1. **During Backlog triage** — sort Backlog into Q1/Q2/Q3/Q4; Q1+Q2 candidates move to Ready, Q3 gets delegated or noted, Q4 gets archived.
2. **When picking next from Ready** — within Ready, Q1 > Q2 > Q3.
3. **During weekly planning** — bias next week's pull toward Q2 (preventative + high-leverage).

### Common Eisenhower mistakes

- **Mislabeling Q3 as Q1.** "Urgent" feels urgent because someone else made it urgent. Test: would this matter if you didn't do it for a week?
- **Q4 sneaking into Ready as "easy wins."** If it's not important, the only thing easy about it is the time it takes from Q2 work.
- **Endless Q2.** Q2 is great in moderation. Too many Q2 cards in Ready = the board is wishful thinking, not a commitment. Cap Q2 cards in Ready at ~5 per board.

## Async-first

You're running multiple businesses with partners (CF: Zach, Nick) and async clients (Olo fCMO). Async-first PM means:

1. **Status visible without you.** Anyone should be able to look at the board and know where things stand. No "let me catch you up" calls.
2. **Decisions documented.** When a card moves between columns, the why is in the card or a comment. Compose with `/decide` for big calls.
3. **Cards read like messages.** Title = headline. Body = what a colleague would need to pick this up cold. No "see Slack thread" — link the thread *and* summarize.
4. **Status updates are written, not spoken.** Use the `/pm status` output format. Send a Slack message. Don't call.
5. **Reduce back-and-forth.** Every card has owner + acceptance criteria so reviewers don't ping you to ask "what should I check for."

## Cross-portfolio prioritization

When you have N businesses each with their own kanban, the meta-decision is "which board should I work in today?"

Heuristics, in order:

1. **Q1 across all boards first.** Even a Q2 on a hot business loses to a Q1 on a quieter one.
2. **Then: revenue or strategic lever.** Among Q2 items across boards, pull from the business with the most leverage right now.
3. **Then: momentum tax.** If a business has gone 14+ days without progress, prioritize ANY card there. Drift kills compound businesses faster than slow execution.
4. **Then: energy fit.** If two cards are tied, pick the one that matches your current state. Morning analytical brain ≠ end-of-day creative brain.

## WIP limits — recommended defaults

Per business board (override per business in `boards.md`):

| Column | Default WIP |
|---|---|
| In Progress | **3** (max) |
| Review/Blocked | no cap, but flag at 5+ |
| Ready | soft cap at 10 — more than that means you're hoarding, not committing |

Cross-portfolio: across all businesses, **don't exceed 5 In-Progress total**. Each business burns context-switch tax; more than 5 means you're not really In Progress anywhere.
