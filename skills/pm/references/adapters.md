# Adapters

How `pm` reads from / writes to each PM tool. Add new adapters here as needed.

Each business board has a `tool` value in `boards.md` that selects one of these adapters.

---

## notion

**Auth:** `$NOTION_API_KEY` (in `~/.zshenv`). No MCP — call API directly. See `reference_notion_api.md` in memory.

**Pattern:** Each business board is a Notion database with these properties:
- `Name` (title)
- `Status` (select: Backlog / Ready / In Progress / Review/Blocked / Done) — defaults; override in `boards.md`
- `Priority` (select: Q1 / Q2 / Q3 / Q4) — Eisenhower quadrant
- `Owner` (people or text)
- `Size` (select: XS / S / M / L)

**Operations:**

```bash
# List cards by column
curl -X POST "https://api.notion.com/v1/databases/<db-id>/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter":{"property":"Status","select":{"equals":"In Progress"}}}'

# Read one card (page)
curl -X GET "https://api.notion.com/v1/pages/<page-id>" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"

# Move a card to another column
curl -X PATCH "https://api.notion.com/v1/pages/<page-id>" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"Status":{"select":{"name":"Ready"}}}}'

# Create a new card
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"parent":{"database_id":"<db-id>"},"properties":{"Name":{"title":[{"text":{"content":"<title>"}}]},"Status":{"select":{"name":"Backlog"}}}}'
```

---

## github

**Auth:** `gh` CLI (already authed). Works for both GitHub Issues and GitHub Projects (v2).

**Pattern A — Issues on a single repo:**

The "board" is the repo's issues filtered by label (e.g., `column:ready`, `column:in-progress`). Or by Project (v2) status field.

```bash
# List issues in a column (label-based)
gh issue list --repo <owner>/<repo> --label "column:ready" --json number,title,labels

# Move (change label)
gh issue edit <num> --repo <owner>/<repo> --remove-label "column:ready" --add-label "column:in-progress"

# Create
gh issue create --repo <owner>/<repo> --title "<title>" --label "column:backlog"
```

**Pattern B — GitHub Projects (v2):**

```bash
# List items in a column (Status field)
gh project item-list <project-number> --owner <owner> --format json

# Move item (set Status field)
gh project item-edit --id <item-id> --field-id <status-field-id> --single-select-option-id <option-id> --project-id <project-id>
```

For Projects v2, the skill needs to discover field IDs once via `gh project field-list` and cache them in `boards.md`.

---

## plane

**Auth:** Plane API key (set as `$PLANE_API_KEY` in `~/.zshenv` if not yet — prompt the user if missing). Workspace slug from `boards.md`.

**Pattern:** Plane has Projects → Modules/Cycles → Issues. The "board" maps to a Plane Project; columns map to Plane "State" values.

```bash
# List issues in a state
curl -X GET "https://api.plane.so/api/v1/workspaces/<workspace>/projects/<project-id>/issues/?state__name=Ready" \
  -H "X-API-Key: $PLANE_API_KEY"

# Move issue (change state)
curl -X PATCH "https://api.plane.so/api/v1/workspaces/<workspace>/projects/<project-id>/issues/<issue-id>/" \
  -H "X-API-Key: $PLANE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "<state-id-for-In Progress>"}'
```

Note: Plane uses state IDs, not names — discover and cache once per workspace.

---

## linear

**Auth:** Linear MCP if installed, else `$LINEAR_API_KEY`. Prefer MCP when available.

**Pattern:** Each Linear Team or Project maps to a board. Columns map to workflow states.

If using the Linear MCP, the skill calls those tools directly. If using the API:

```bash
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ issues(filter: {team: {key: {eq: \"<team-key>\"}}, state: {name: {eq: \"In Progress\"}}}) { nodes { id title } } }"}'
```

---

## obsidian

**Auth:** none — local files.

**Pattern:** Obsidian Kanban plugin stores boards as markdown files with `## Column Name` headings. Each card is a `- [ ] Card title` bullet under its column.

```
## Backlog
- [ ] Card A
- [ ] Card B

## Ready
- [ ] Card C

## In Progress
- [ ] Card D

## Review/Blocked
- [ ] Card E — blocked on <person>

## Done/Archived
- [x] Card F
```

**Operations:**
- **Read**: `Read` the markdown file at the path in `boards.md`
- **Move**: edit the file — remove card from old column, add under new column
- **Create**: append a bullet under the right column
- **Done**: change `[ ]` to `[x]` and move to Done section

Watch out: Obsidian Kanban supports embedded YAML metadata blocks per card (priority, due, assignee). Preserve them when moving cards.

---

## manual

**Auth:** none.

When no tool is connected (or the user doesn't want one for a particular business), `pm` works in conversation:

1. Ask the user to paste the current board state (or describe verbally)
2. Run the requested mode against that snapshot
3. Output recommended moves as plain text
4. Optionally: persist a snapshot to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/pm/boards-cache/<business>.md` so subsequent runs don't require re-pasting (with a clear warning that the cache is stale until next paste) — never inside the skill folder; upgrades wipe it

The cache file uses the same Obsidian-style markdown format above so it's portable.

---

## Adding a new adapter

When the user starts using a new tool (Trello, Jira, Asana, ClickUp, etc.):

1. Add a new section above with: auth method, board structure, list/read/move/create operations
2. Add the tool as a valid value in `boards.md`
3. Test once with a real board before relying on it
