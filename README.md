# corey-skills

Personal Claude Code skills for Corey Haines's day-to-day work.

This is a private plugin — a collection of skills (specialized prompts + workflows) that Claude Code can load on demand. Each skill teaches Claude how to do one thing well, in the way I want it done.

## Install

```bash
# In Claude Code
/plugin marketplace add coreyhaines31/corey-skills
/plugin install corey-skills@corey-skills
```

Or for local development, symlink into `~/.claude/plugins/`:

```bash
ln -s ~/code/corey-skills ~/.claude/plugins/corey-skills
```

## Structure

```
corey-skills/
├── .claude-plugin/
│   ├── plugin.json        # plugin manifest
│   └── marketplace.json   # marketplace listing
├── skills/
│   └── <skill-name>/
│       └── SKILL.md       # skill instructions + frontmatter
└── README.md
```

Each skill lives in its own directory under `skills/` with a `SKILL.md` file. Optional `references/` and `evals/` subdirs per skill (see `marketingskills` for reference).

### SKILL.md frontmatter

```yaml
---
name: skill-name
description: When the user wants to [X]. Also use when they mention "[trigger phrase]"...
metadata:
  version: 0.1.0
---
```

The `description` is what Claude uses to decide when to load the skill — be specific about triggers, what it does, and when to use it vs. other skills.

## Cross-referencing other skill collections

Skills can reference each other across plugins by name. In a SKILL.md description or body:

- **Within this plugin:** mention by skill name (`see content-strategy`)
- **From `marketing-skills`:** mention with prefix (`see marketing-skills:cro` or just `cro`)
- **From `cf-skills`:** (`see cf-skills:positioning`)
- **From other plugins (`compound-engineering`, `vercel`, `expo`, etc.):** mention by plugin-prefixed name

Claude resolves these by description match at load time. No manifest linking needed — keep references readable in prose.

## Related skill collections

- [`marketingskills`](https://github.com/coreyhaines31/marketingskills) — 43 marketing skills (CRO, copywriting, SEO, ads, etc.)
- `cf-skills` — Conversion Factory-specific skills (positioning, brand strategy, growth engine, etc.)

## Skills

| Skill | What it does |
|---|---|
| [`add-skill`](./skills/add-skill/SKILL.md) | Bootstrap a new skill in this plugin. Generates SKILL.md frontmatter, creates references/, updates README, commits + pushes. Meta — speeds every other skill we build. |
| [`business-brainstorm`](./skills/business-brainstorm/SKILL.md) | Pressure-test a potential new business or product against Corey's serial-founder filter (9 dimensions). Composes with `deep-research` and `/domain`. Archives every brainstorm so past ideas are searchable + revisit-able. |
| [`deep-research`](./skills/deep-research/SKILL.md) | Multi-source research with citations and archive. Uses WebSearch, WebFetch, agent-browser, `/last30days`, memory, Notion. Outputs structured brief with contradictions and gaps. Compounds — every run adds to the archive. |
| [`my-social`](./skills/my-social/SKILL.md) | Personal portfolio rotation for X + LinkedIn. Ensures each of Corey's 6 properties gets promoted ~1× every 3 weeks, with build-in-public + educational filling the rest. Drafts and syndicates to personal Typefully workspace. |
| [`paste`](./skills/paste/SKILL.md) | Clean terminal output for any destination (Slack, Notion, Twitter, LinkedIn, email, GitHub, plain, HTML). Strips ANSI codes, box-drawing chars, prompts. Reads clipboard, writes back to clipboard + chat preview. Scans for secrets first. |
