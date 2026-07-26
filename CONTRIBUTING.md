# Contributing to makerskills

Thanks for considering a contribution. This plugin is intentionally opinionated (built around one operator's craft), but useful additions from the community are welcome — especially skill improvements, bug fixes, and additions that generalize an existing pattern.

## Ways to contribute

- **Fix a bug** in an existing SKILL.md or references file
- **Improve documentation** — better trigger phrases, clearer step ordering, a missing "Notes on quality" observation
- **Port a workflow** you've built into a new skill (see [Add a new skill](#add-a-new-skill) below)
- **Cross-pollinate** — if you have a public skill in another plugin that would compose well with makerskills, open an issue proposing the cross-reference
- **Report an issue** — something didn't behave as documented? File it

## Setup for local dev

```bash
git clone https://github.com/coreyhaines31/makerskills ~/code/makerskills
cd ~/code/makerskills
ln -s ~/code/makerskills ~/.claude/plugins/makerskills
```

Then set `MAKERSKILLS_CONFIG` in `~/.zshenv` per [INSTALL.md](./INSTALL.md).

The symlink approach means edits to any SKILL.md are picked up on the next Claude Code invocation — no rebuild step.

## Branch + PR conventions

- **Never push directly to `main`.** Open a PR.
- **Branch names**: `feature/<short-slug>` for additions, `fix/<short-slug>` for bug fixes, `docs/<short-slug>` for docs-only changes
- **Commit messages**: focus on the "why," not the "what." One-line summary + optional body. Keep it under 72 chars on the summary line.
- **PR title = the eventual squash-merge commit title**. Same conventions.
- **PR body** should explain: what changed, why, any tradeoffs, how to test manually. Screenshots for anything that produces visual output (e.g., slide-deck primitive changes).

## Add a new skill

### 1. Scaffold via `skillify` (recommended)

The easiest path is invoking `/skillify from-scratch <name>` — the skill will interactively ask for name, one-line purpose, trigger phrases, initial reference files, and composition relationships. It writes the SKILL.md skeleton for you.

### 2. Manual scaffold

```
skills/<name>/
├── SKILL.md
└── references/
    └── <topic>.md    # add as needed; some skills have zero references files
```

### 3. Required SKILL.md frontmatter

```yaml
---
name: <kebab-case>
description: <2-4 sentences. Lead with "When you want to..." Include 4-8 trigger phrases in quotes. Differentiate from adjacent skills.>
metadata:
  version: 0.1.0
---
```

The `description` is load-bearing — Claude routes to your skill by description match. Be specific about triggers. See existing skills for examples of description length + tone.

### 4. Body structure conventions

Not strict rules, but the pattern most skills follow:

- `# /<name> — <one-line purpose>` (H1)
- Optional intro paragraph explaining scope
- `## Mental model` (optional but useful for complex skills)
- `## Step 0 — Load config / detect mode` (if applicable)
- `## Step 1 — <phase>` through `## Step N`
- `## Composes with` — bulleted list of sibling skills the new skill invokes or is invoked by
- `## Notes on quality` — non-negotiable rules that separate good invocations from bad. Learned lessons, guardrails, subtle gotchas.

### 5. References directory

- Keep it under 5 files unless the skill is genuinely huge (`skillify` has 5, `company-brain` has 3)
- One file per concern (schema, templates, methodology, config)
- Example / seed files use `.example.md` or `.example.yaml` extension
- User-specific overrides live in `~/.config/makerskills/<skill>/*.local.md` (never in this repo — gitignored globally)

### 6. Add to the catalog

- Append your skill's row to the appropriate section in `README.md`'s [The 19 skills](./README.md#the-19-skills) table (update the count in the section heading)
- If new env vars are introduced, add them to `INSTALL.md`
- If it's a significant addition, add a `CHANGELOG.md` entry under a new unreleased version heading

### 7. Test

- Invoke via `/<skill-name>` in Claude Code
- Verify the description triggers on your natural language variants
- Try the failure cases documented in `## Notes on quality`
- Check that `## Composes with` cross-references actually route correctly

### 8. PR

Open the PR. Include a description of what problem the skill solves, an example invocation + expected output, and any dependencies (env vars, brew installs, MCP servers).

## Testing pattern

There's no automated test harness — SKILL.md files are executable documentation, not code. Testing is:

1. **Live invocation** — run the skill via Claude Code, verify it behaves as documented
2. **Description match** — try 3-5 natural language phrasings that should trigger the skill. All should route correctly.
3. **Composition** — if the skill composes with siblings, verify those cross-references still work after any refactor
4. **Graceful degradation** — if the skill has optional dependencies (Domainr API key, Namecheap API, `~/.config/makerskills/<skill>/*.local.md`), verify the skill still works when they're missing

## Style guide (voice)

- **Direct, conviction-coded.** Not "you might want to consider" — say what to do.
- **Listener perspective.** "You'll know X" not "we'll teach you X."
- **No filler.** Skip "In this skill, we'll be..." — open with the take.
- **Contractions everywhere.** *don't, won't, you're, I'd.*
- **Specific over abstract.** "Add `SLIDE_DECK_REPO` to `~/.zshenv`" beats "configure the env var."
- **No AI-slop tells.** No "no fluff, no BS," "here's the kicker," "let's dive right in."

If it doesn't sound like something a real operator would say to another real operator across a coffee table, rewrite.

## Governance

`makerskills` is maintained by [Corey Haines](https://corey.co). Substantive contributions (new skills, significant refactors) are subject to review + may be reshaped for consistency with the collection's overall voice + architecture. Small fixes (typos, bug fixes, doc improvements) generally merge fast.

Not every good idea belongs in makerskills. If a skill is too niche or too personal, the reviewer may suggest publishing it as a standalone plugin instead, referenced from makerskills' README `## Related skill packs` section.

## Code of conduct

Be kind. Be direct. Assume good intent. Push back on ideas, not people. If a review feels harsh, ask for clarification — usually it's just conviction, not criticism.

## Questions

Open a [Discussion](https://github.com/coreyhaines31/makerskills/discussions) — questions about how to use existing skills, ideas for new ones, or clarifying the architecture. Open an [Issue](https://github.com/coreyhaines31/makerskills/issues) for bugs or specific behavior that doesn't match documentation.
