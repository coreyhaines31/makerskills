# Vault config

## Location

Company brain lives at `${COMPANY_BRAIN_VAULT:-$HOME/Documents/CompanyBrain}/`.

Override in `~/.zshenv`:

```bash
export COMPANY_BRAIN_VAULT="$HOME/code/acme-company-brain"    # per-team path
```

For multi-team users (e.g., a consultant maintaining vaults for multiple clients):

```bash
export COMPANY_BRAIN_VAULT="$HOME/code/current-client-brain"

# Switch by aliasing:
alias cb-acme="export COMPANY_BRAIN_VAULT=$HOME/code/acme-brain"
alias cb-beta="export COMPANY_BRAIN_VAULT=$HOME/code/beta-brain"
```

The skill respects whatever `$COMPANY_BRAIN_VAULT` points to at invocation time.

## Storage backends

Company brains live in one of three places, in order of team-scale readiness:

| Backend | When to use | Trade-offs |
|---|---|---|
| **Obsidian vault (local, git-synced)** | 1-10 person teams | Simplest, portable, git handles history + attribution. Requires everyone to install Obsidian. |
| **Shared git repo** (no Obsidian) | 5-50 person teams, engineering-heavy | Everyone reads markdown in their editor of choice. Git is the sync layer. Requires markdown literacy. |
| **Notion / Coda backed by markdown export** | 20+ person teams, non-technical majority | Team edits in Notion; nightly export → git-backed markdown for company-brain. Extra sync layer, but non-engineers can contribute. |

Company-brain skill treats all three the same — reads/writes markdown. The backend choice is a team decision, not a skill decision.

## Initial setup for a new team

```bash
# 1. Pick a path
export COMPANY_BRAIN_VAULT="$HOME/code/mycompany-brain"

# 2. Create the vault
mkdir -p "$COMPANY_BRAIN_VAULT"
cd "$COMPANY_BRAIN_VAULT"

# 3. Init git (if not already)
git init
git remote add origin git@github.com:mycompany/company-brain.git

# 4. Create the base dirs, plus ONLY the pilot workflow's dirs (see "Start narrow" below)
mkdir -p raw wiki outputs Projects Team Templates Drafts
mkdir -p meetings sales-objections customer-language   # e.g. a Sales pilot

# 5. Seed the schema doc from this skill's references/schema.md (path depends on where your agent installed the skill)
#    AGENTS.md is read by Codex, Cursor, and most hosts; the symlink covers Claude Code
cp <skill-dir>/references/schema.md AGENTS.md
ln -s AGENTS.md CLAUDE.md

# 6. Seed INDEX.md
echo "# Wiki Index\n\n## Sales\n\n## Customers\n\n## Ops\n\n## Product\n\n## Team & People\n\n## Decisions\n\n## Playbooks" > wiki/INDEX.md

# 7. Seed .gitignore
cat > .gitignore <<EOF
.DS_Store
.obsidian/workspace*
.obsidian/cache
.trash/
Drafts/*.private.md
EOF

# 8. First commit
git add . && git commit -m "Seed company brain schema"
git push -u origin main
```

### Start narrow

Don't seed all eight structured dirs on day one. Pick the **one workflow closest to revenue** and seed only its dirs:

| Pilot workflow | Dirs to seed |
|---|---|
| Sales | `meetings/` + `sales-objections/` + `customer-language/` |
| Content / marketing | `customer-language/` + `recurring-questions/` + `sops/` |
| Ops / delivery | `sops/` + `decisions/` + `meetings/` |
| Reporting | `decisions/` + `companies/` + `meetings/` |

Other dirs get created by the first capture that needs one. Fewer dirs means a smaller review queue, so the review habit sticks before volume arrives. The brain earns the right to touch more. See [rollout.md](rollout.md) for widening it beyond the pilot group.

## Sensitivity access lists (optional)

If using sensitivity tagging, maintain two access lists in `Team/`:

```
Team/leadership.md         # emails/handles that can read `leadership` content
Team/confidential-access.md # per-topic access lists for confidential wiki pages
```

Company-brain skill reads these when respecting sensitivity in `query` mode.

## Backup

Same as any git repo. Push to a hosted remote (GitHub / GitLab / Bitbucket). Recover by cloning.

For sensitive content in the vault, treat it like any git repo with secrets — encrypted at rest via `git-crypt` if the remote isn't fully trusted.
