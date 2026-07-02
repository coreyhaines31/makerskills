# Boards — per-business config (TEMPLATE)

This is the template. Your real board mappings live in `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/pm/boards.md` — not in this repo. Copy the schema below and populate it there.

One row per business. Populated by `/pm setup [business]` and edited freely.

When the skill targets a business not listed in your local config, it falls back to `manual` mode and prompts setup.

| business | tool | board_id / URL / path | columns (if custom) | WIP override |
|---|---|---|---|---|
| _example_project_a_ | _notion_ | _<db-id>_ | _default_ | _default_ |

_No boards configured yet. Run `/pm setup <business>` to start._

---

## Default columns

If a row doesn't list custom columns, the skill uses:

```
Backlog → Ready → In Progress → Review/Blocked → Done/Archived
```

## Default WIP

```
In Progress: 3
Review/Blocked: no cap (flag at 5+)
Ready: soft cap 10
```

## Cross-portfolio WIP

Max **5 In Progress** across all boards combined. Above that, `/pm next` (cross-board) recommends finishing something before pulling new work.
