# Vault config

The Second Brain vault location and tool.

| Field | Value |
|---|---|
| **Path** | `${SECOND_BRAIN_VAULT:-$HOME/Documents/SecondBrain}/` |
| **Tool** | Obsidian (markdown-based) |
| **Schema source** | `<path>/CLAUDE.md` (authoritative — always read first) |
| **Backup** | _not configured here — assumes vault is in iCloud/Dropbox/git_ |

## Folders

| Folder | Purpose | Modifiable by `second-brain`? |
|---|---|---|
| `raw/` | Unprocessed source material | ✅ create files |
| `wiki/` | Compiled topic pages | ✅ create + update files |
| `wiki/INDEX.md` | Master index | ✅ update |
| `outputs/` | Generated artifacts (queries, slide decks, briefs) | ✅ create files |
| `Inbox/` | Quick-capture inbox | ❌ off-limits — `Quick Capture.md` is for raw thoughts before they hit `raw/` |
| `Projects/` | Project-specific notes | ❌ off-limits — `pm` skill territory |
| `Daily/` | Daily notes | ❌ off-limits |
| `Templates/` | Note templates | ❌ off-limits |
| `Notes/` | Misc | ❌ off-limits |
| `Tasks.md` | Task list | ❌ off-limits |
| `Kanban.md` | Personal kanban | ❌ off-limits — `pm` skill territory |
| `Home.md` | Vault home | ❌ off-limits |

## Switching vaults

If Corey moves the vault or wants to use a different setup (Logseq, plain markdown dir, Notion):

1. Update **Path** above
2. If the tool changes, note any structural differences (e.g., Logseq uses `journals/` and `pages/`)
3. Ensure the new vault has a CLAUDE.md or schema doc the skill can read at Step 1

## Note

The skill always reads `<vault>/CLAUDE.md` at start. If Corey updates his schema there, the skill picks it up automatically — no need to keep this skill's `schema.md` in sync.
