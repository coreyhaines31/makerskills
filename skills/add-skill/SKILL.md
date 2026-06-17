---
name: add-skill
description: When Corey wants to bootstrap a new skill in the makerskills plugin. Generates the SKILL.md with proper frontmatter, creates a references/ subdirectory, updates the README.md skill table, commits, and pushes. Saves the ~5 min of manual scaffolding every time. Triggers on "add a skill," "new skill," "/add-skill," "create skill called," "bootstrap skill," "scaffold skill." This skill only works inside the makerskills repo at ~/code/makerskills.
metadata:
  version: 0.1.0
---

# /add-skill — Bootstrap a new makerskills skill

Scaffolds a new skill in `~/code/makerskills/skills/<name>/` with the right structure, updates the README, and commits.

## Step 1 — Gather inputs

Ask (or infer from the trigger):

1. **Name** — kebab-case (e.g., `weekly-review`). Confirm it doesn't collide with existing skills:
   - Run: `ls ~/code/makerskills/skills/` to check this plugin
   - Also flag if name matches a skill in `marketing-skills` or `cf-skills` (Claude resolves by namespace, but reduces ambiguity)
2. **One-line purpose** — what the skill does, in plain language
3. **Trigger phrases** — what Corey will say to invoke it (the description's job). Examples: `/<name>`, `"<verb> <noun>"`, `"<keyword>"`. If not given, draft from purpose.
4. **Initial reference files?** — default yes, create empty `references/` dir. Ask if specific files should be seeded (e.g., `voice.md`, `framework.md`, `archive/`).
5. **Composes with?** — does this skill call other skills (e.g., `/last30days`, `cf-skills:x-li`, `marketing-skills:copywriting`)? List them so the description and body reference them.

## Step 2 — Generate frontmatter

Build the YAML frontmatter:

```yaml
---
name: <kebab-case-name>
description: <rich, trigger-rich, ~2-4 sentences. Lead with "When Corey wants to..." Include explicit trigger phrases in quotes. Differentiate from adjacent skills in marketing-skills / cf-skills if relevant.>
metadata:
  version: 0.1.0
---
```

**Description-writing rules** (load-bearing — Claude routes by description match):
- Lead with the use case ("When Corey wants to X...")
- Include 4–8 explicit trigger phrases the user might say
- Differentiate from sibling skills if there's overlap
- Mention key references the skill loads
- Keep under ~500 characters

## Step 3 — Scaffold the directory

Create:
```
skills/<name>/
├── SKILL.md            # generated below
└── references/         # empty unless seeded
    └── <seeded files>  # only if specified
```

The SKILL.md body should follow the pattern of existing skills (`my-social`, `paste`):
- `# /<name> — <one-line purpose>`
- `## Step 1 — <first phase>` … etc.
- Sections for: inputs, processing, outputs, cross-references
- Cross-reference any composed skills explicitly

If seeded reference files are requested, create them with frontmatter-less markdown stubs and `# Iterate me` markers.

## Step 4 — Update README.md

Append a row to the Skills table in `~/code/makerskills/README.md`:

```markdown
| [`<name>`](./skills/<name>/SKILL.md) | <one-line purpose> |
```

Insert in alphabetical order if the table is sorted, otherwise append.

## Step 5 — Commit and push

```bash
cd ~/code/makerskills && git add -A && git commit -m "Add <name> skill: <one-line purpose>" && git push
```

Report:
- New skill path
- Commit hash
- Reminder: `/plugin install` or symlink may need a refresh to pick up the new skill

## Step 6 — Offer follow-ups

After scaffolding, ask: *"Want to flesh out the SKILL.md body now, or come back to it?"*

If yes, work through it interactively — the scaffold is intentionally minimal; the real work is filling in the steps per the skill's specific logic.

## Cross-references

- The existing skills (`my-social`, `paste`, `deep-research`, `business-brainstorm`) are the best style references — match their structure (numbered steps, references/ subdir, voice).
- For description-writing patterns, look at how `marketing-skills` skills describe themselves — heavy on trigger phrases.
