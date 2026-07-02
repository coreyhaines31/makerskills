---
name: pm
description: When you want to manage projects across your businesses using a kanban + Eisenhower methodology. One kanban per business (whatever portfolio of businesses, projects, or initiatives you run). Tool-agnostic — connects via API/MCP to whatever PM tool each business uses (Notion, GitHub Projects, Plane, Linear, Obsidian file-based, or manual mode). Async-first output. Six modes — setup (scaffold a new board for a business), triage (Eisenhower-sort the backlog), next (pick the next thing to work on, single board or across all), status (paste-ready async snapshot), unblock (diagnose Review/Blocked column), weekly (Friday pulse + week planning). Triggers on "/pm," "/pm setup," "/pm triage," "/pm next," "/pm status," "/pm unblock," "/pm weekly," "what should I work on next," "kanban status," "Eisenhower this," "triage my backlog," "what's blocked."
metadata:
  version: 0.1.1
---

# /pm — Project management across the portfolio

Methodology-first project management. Kanban + Eisenhower + async. One board per business. Tool-agnostic via adapters.

## Mental model

Each business gets its own kanban with 5 columns:

```
Backlog  →  Ready  →  In Progress  →  Review/Blocked  →  Done/Archived
```

- **Backlog**: everything that *might* matter — not yet committed
- **Ready**: triaged, well-defined, can be picked up
- **In Progress**: actively being worked
- **Review/Blocked**: waiting on someone else, review, or external dependency
- **Done/Archived**: shipped or killed

**Eisenhower** sits on top of the board — used to triage Backlog → Ready (which items make the cut) and to pick next from Ready (which Ready item to pull).

```
                Urgent          Not Urgent
Important       Q1: Do          Q2: Schedule    ← Q2 is the high-leverage zone
Not Important   Q3: Delegate    Q4: Delete
```

**Async-first**: every status snapshot should read like a Loom you didn't have to record. Make work visible without requiring a meeting.

## Step 1 — Detect mode and target

Parse the invocation:

| Invocation | Mode | Target |
|---|---|---|
| `/pm setup [business]` | setup | the named business |
| `/pm triage [business]` | triage | the named business (or ask) |
| `/pm next [business]` | next | the named business |
| `/pm next` | next | **across all boards** (cross-portfolio) |
| `/pm status [business]` | status | the named business (or ask) |
| `/pm unblock [business]` | unblock | the named business (or ask) |
| `/pm weekly` | weekly | all boards (Friday pulse) |
| `/pm weekly [business]` | weekly | the named business |

## Step 2 — Load board config + personal overlay

Read `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/pm/boards.md` (personal — real business list + tool mapping per business). Falls back to `references/boards.md` in the repo if the local file doesn't exist yet — that's a template.

Also try to load `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/pm/team.local.md` if present — this is where the user lists partners, active clients, and typical blocker phrasings. Use it to make status output specific ("Waiting on <partner>'s review") instead of generic.

| Field | Example |
|---|---|
| business | `<slug>` |
| tool | `notion` / `github` / `plane` / `linear` / `obsidian` / `manual` |
| board_id or URL | tool-specific |
| column overrides | only if this board doesn't use the default 5 columns |

If the business has no mapping yet, jump to **setup** automatically — ask which tool, save the mapping, return to the requested mode.

## Step 3 — Load the adapter

Read the relevant section of `references/adapters.md` for the tool. Each adapter section explains how to:
- List cards / issues / pages by column
- Read a single card's full content
- Create a card
- Move a card between columns
- Add a comment / note

Adapters use:
- **Notion** → `$NOTION_API_KEY` (already in zshenv). Database with `Status` select property.
- **GitHub Projects** → `gh` CLI (already authed). `gh project item-list`, `gh project item-edit`.
- **Plane** → Plane API (needs `$PLANE_API_KEY` and workspace slug).
- **Linear** → Linear MCP or API key.
- **Obsidian** → local kanban markdown files in the vault. Read/write directly.
- **Manual** → ask the user to paste the current board state; offer to write back to a local markdown file.

## Step 4 — Run the mode

### setup
- Ask which tool the business uses
- Walk through column setup (default 5 columns; offer custom)
- Save mapping to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/pm/boards.md` (NOT to `references/boards.md` in the repo — that's a template only). Create the parent directory if it doesn't exist yet.
- Optionally seed the board with starter cards from a conversation about what's on the user's mind for that business

### triage
- Pull the Backlog column
- Apply Eisenhower (Q1/Q2/Q3/Q4) — show the user the matrix view
- Recommend moves:
  - Q1 (urgent + important) → move to Ready or In Progress now
  - Q2 (important, not urgent) → move to Ready, schedule when
  - Q3 (urgent, not important) → delegate (to whom?) or move to Ready if no one
  - Q4 (neither) → archive
- Apply moves via the adapter (or output text the user applies manually)

### next
- **Single board**: pull Ready, then In Progress. If WIP exceeded, surface what to finish first. If WIP available, recommend top Ready item by Eisenhower priority.
- **Cross-portfolio** (`/pm next` with no business): pull Ready from every board, Eisenhower-rank, recommend top 1–3 across all businesses. Bias toward Q1 then Q2.

### status
Generate an async-shareable snapshot:

```markdown
# [Business] — Status as of YYYY-MM-DD

**Shipped this week:** N cards
- <card title>
- <card title>

**In progress:** N cards
- <card title> — <who/what>

**Review/Blocked:** N cards
- <card title> — blocked on <reason>

**Up next:** top 2–3 from Ready
- <card title>
- <card title>

**Open question:** <one thing that would unblock progress if answered>
```

Output is paste-ready for Slack, Notion, email, partner DM.

### unblock
- Read everything in Review/Blocked
- For each card: surface the blocker, suggest an action (nudge X, escalate to Y, descope, kill, move back to In Progress if blocker is gone)
- Output a short list of moves

### weekly
**Friday pulse + planning**:
1. For each board: shipped this week, in progress, blocked
2. Cross-portfolio: where's momentum? where's drift?
3. Plan next week: 3–5 Q2 items to pull from Ready into In Progress on Monday
4. Output the combined snapshot — pasteable into Notion weekly log, partner update, or personal journal

## WIP limits

Default WIP per column (override in your local `boards.md` per business):

| Column | Default WIP |
|---|---|
| In Progress | 3 |
| Review/Blocked | (no limit — but flag if >5) |

If WIP exceeded in `next` mode, **don't pull more** — recommend finishing or moving something to Review/Blocked first.

## Async-first writing rules

When generating status / weekly outputs:

- **Lead with the headline** — what shipped this week, or what's at risk
- **Be specific** — "shipped X" not "made progress on Y"
- **No verbs without subjects** — write so the reader can pick up cold
- **Blockers name the blocker** — "waiting on designer's review" not "blocked"
- **Open questions are explicit** — one bolded line per status that asks for what would unblock momentum

## Composes with

- `decide` — when a project hits a real decision, route to `/decide`
- `deep-research` — when a card needs research before it's actionable
- `business-brainstorm` — when an idea on the Backlog deserves pressure-testing before triage
- `jab-hook` — when status / shipped items become BIP-post material
- Memory (`project_*.md`) — for portfolio context per business

## Notes on quality

- **Limit WIP.** Multitasking is the most reliable way to ship nothing. Cap In Progress at 3 (override in your local `boards.md` per business if truly needed). If the cap is hit, don't pull more — recommend finishing or moving something to Review/Blocked.
- **Lead with the headline** in every status output — what shipped this week, or what's at risk. Not "made progress on X" — that's noise.
- **Be specific.** "Shipped the primary logo variant" beats "made progress on branding." Specificity signals real motion; vagueness signals none.
- **No verbs without subjects.** Write status so the reader can pick up cold — 3 weeks later or forwarded to a partner who missed the last update.
- **Blockers name the blocker.** "Waiting on designer's review of the homepage draft" — not "blocked." Blockers without names create no urgency.
- **Open questions are explicit** — one bolded line per status that asks for what would unblock momentum. Async momentum lives or dies on how well open questions are surfaced.
- **Tool-agnostic by design.** pm speaks Kanban + Eisenhower; the adapters (Notion / GitHub / Plane / Linear / Obsidian / manual) translate. Adding a new tool = one adapter file, not a rewrite.
