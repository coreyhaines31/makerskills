# makerskills

[![Stars](https://img.shields.io/github/stars/coreyhaines31/makerskills?style=flat-square&label=stars&color=000)](https://github.com/coreyhaines31/makerskills/stargazers) [![Release](https://img.shields.io/github/v/release/coreyhaines31/makerskills?style=flat-square&color=000)](https://github.com/coreyhaines31/makerskills/releases) [![License](https://img.shields.io/badge/license-MIT-000?style=flat-square)](./LICENSE)

**AI agent skills for the personal operator's craft.** Decisions, research, second-brain workflows, content rotation, scenario modeling, and the meta-skills to author more.

Built for founders and indie operators. Works with [Claude Code](https://claude.ai/code), Codex, Cursor, and other Agent Skills hosts.

**Site:** [maker-skills.com](https://maker-skills.com)

---

## Install

```bash
# In Claude Code
/plugin marketplace add coreyhaines31/makerskills
/plugin install makerskills@makerskills
```

Or symlink for local dev:

```bash
git clone https://github.com/coreyhaines31/makerskills ~/code/makerskills
ln -s ~/code/makerskills ~/.claude/plugins/makerskills
```

See [INSTALL.md](./INSTALL.md) for env vars, personal-config setup, and runtime dependencies.

---

## The 15 skills

### Meta — manage skills themselves
| Skill | What |
|---|---|
| [`create-skill`](./skills/create-skill/SKILL.md) | Turn a workflow, brief, or chat into a new skill. `from-chat`, `from-video`, `from-dump`, `from-scratch` modes. |
| [`adapt-skill`](./skills/adapt-skill/SKILL.md) | Port an external skill into your namespace. Three-bucket classification (keep / adapt / add), license check, attribution file. |
| [`update-skill`](./skills/update-skill/SKILL.md) | Improve existing skills from learnings. Cross-skill propagation, memory-vs-skill triage, semver discipline. |

### Decision & strategy
| Skill | What |
|---|---|
| [`decide`](./skills/decide/SKILL.md) | 37signals decision framework (38 questions triaged to 6–8 per decision). Archives with revisit dates. |
| [`business-brainstorm`](./skills/business-brainstorm/SKILL.md) | Pressure-test a new business or product on 9 dimensions. Composes with `deep-research` + `/domain`. |
| [`deep-research`](./skills/deep-research/SKILL.md) | Multi-source research with citations + archive. WebSearch, WebFetch, `agent-browser`, `/last30days`, memory. |

### Knowledge & content consumption
| Skill | What |
|---|---|
| [`second-brain`](./skills/second-brain/SKILL.md) | Karpathy LLM Wiki workflow over any markdown vault. Capture / compile / query / lint / connect / search. |
| [`read-book`](./skills/read-book/SKILL.md) | PDFs, EPUBs, MOBI, markdown — chapter-by-chapter notes, quotes, summaries, or spaced-rep study mode. |
| [`watch-video`](./skills/watch-video/SKILL.md) | YouTube, Loom, Vimeo, Riverside, Zoom, MP4. Transcript / visual / multimodal (Gemini-native) modes. |

### Output & creative
| Skill | What |
|---|---|
| [`jab-hook`](./skills/jab-hook/SKILL.md) | Gary Vee's jab-jab-jab-right-hook rhythm applied to your portfolio rotation on X + LinkedIn via Typefully. |
| [`slide-deck`](./skills/slide-deck/SKILL.md) | Branded React decks (Next.js). "Show, don't tell" narrative pitching, density modes, PPT conversion, Playwright export. |

### Operations & utilities
| Skill | What |
|---|---|
| [`pm`](./skills/pm/SKILL.md) | Kanban (5-column) + Eisenhower across your portfolio. Tool-agnostic adapters (Notion, GitHub, Plane, Linear, Obsidian, manual). |
| [`personal-cfo`](./skills/personal-cfo/SKILL.md) | Personal financial scenarios — house purchase + rental forecasting, monthly cash flow, big-purchase decisions. |
| [`paste`](./skills/paste/SKILL.md) | Clean terminal output for 9 destinations (Slack, Notion, Twitter, LinkedIn, email, GitHub, plain, HTML). Secret-detection first. |
| [`social-fetch`](./skills/social-fetch/SKILL.md) | Pull any social post by URL across 10 platforms (X, LinkedIn, IG, TikTok, Bluesky, Reddit, Mastodon, Threads, HN). Strategy chain with free + paid fallbacks. |

---

## Architecture

The repo is **public + generic**. Your personal data (Typefully workspace IDs, portfolio properties, voice overlays, archives) lives separately in `~/.config/makerskills/` (gitignored, on disk only).

Skills read from `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/<skill>/` paths. Set env vars in `~/.zshenv` to point at your locations:

```bash
export MAKERSKILLS_CONFIG="$HOME/.config/makerskills"
export SECOND_BRAIN_VAULT="$HOME/Documents/SecondBrain"
export COREYCO_REPO="$HOME/code/your-site-repo"            # for slide-deck
```

Full setup in [INSTALL.md](./INSTALL.md).

## SKILL.md format

```yaml
---
name: skill-name
description: When the user wants to [X]. Triggers on "[trigger phrase]"...
metadata:
  version: 0.1.0
---
```

The `description` is what Claude uses to decide when to load the skill — be specific about triggers and disambiguation from sibling skills.

## Cross-referencing other skill packs

Skills can reference each other across plugins. In a SKILL.md description or body:

- **Within this plugin**: mention by name (`see decide`)
- **Cross-plugin**: prefix with the plugin (`see marketing-skills:cro`)

Claude resolves references by description match at load time — no manifest linking needed.

## Related skill packs

- [`marketingskills`](https://github.com/coreyhaines31/marketingskills) — 44 marketing skills (CRO, copywriting, SEO, ads, etc.)
- [`anthropics/skills`](https://github.com/anthropics/skills) — official Anthropic Agent Skills examples
- [`garrytan/gstack`](https://github.com/garrytan/gstack) — engineering-focused skill stack

## License

MIT — see [LICENSE](./LICENSE).

## Built by

[Corey Haines](https://corey.co) — founder, [Conversion Factory](https://conversionfactory.co) + [Magister](https://magistermarketing.com).
