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

## The 18 skills

### Meta — extend Claude Code (the `-ify` trifecta)
| Skill | What |
|---|---|
| [`skillify`](./skills/skillify/SKILL.md) | Create, adapt, or update a skill in any sibling repo. Three modes: CREATE (from-chat / from-video / from-dump / from-scratch), ADAPT (port external skill with license check + attribution), UPDATE (improve existing skills with cross-skill propagation + semver discipline). |
| [`toolify`](./skills/toolify/SKILL.md) | Wire up an integration, API, MCP server, or third-party service into a Next.js or Rails project. Interactive wizard for auth, env vars, client wrapper, webhook handling, and smoke-test. |
| [`loopify`](./skills/loopify/SKILL.md) | Set up an agent loop, cron-scheduled task, or recurring workflow. Judgment layer on top of `ScheduleWakeup` / `CronCreate` / `/loop` — picks pattern (dynamic / cron / one-shot), tunes delay for cache windows, enforces idempotency + bail-out conditions. |

### Decision & strategy
| Skill | What |
|---|---|
| [`decide`](./skills/decide/SKILL.md) | 37signals decision framework (38 questions triaged to 6–8 per decision). Archives with revisit dates. |
| [`business-brainstorm`](./skills/business-brainstorm/SKILL.md) | Pressure-test a new business or product on 9 dimensions. Composes with `deep-research` + `domain`. |
| [`domain`](./skills/domain/SKILL.md) | 11-step .com domain hunt on Laura Roeder's "availability-first, never fall in love with a name" methodology. Multi-tool ensemble: Vercel CLI + whois (per-TLD) + Domainr API + Namecheap API + `rdap.org` (modern TLDs) + `agent-browser` for USPTO trademark screening + aftermarket click-throughs (HugeDomains / Afternic / Sedo / Dan). Handles bare-word + prefix/suffix brainstorming, budget filtering, negotiation guidance, and social handle checks. |
| [`deep-research`](./skills/deep-research/SKILL.md) | Multi-source research with citations + archive. WebSearch, WebFetch, `agent-browser`, `/last30days`, memory. |

### Knowledge & content consumption
| Skill | What |
|---|---|
| [`second-brain`](./skills/second-brain/SKILL.md) | Karpathy LLM Wiki workflow over any markdown vault. Capture / compile / query / lint / connect / search. Personal-scope. |
| [`company-brain`](./skills/company-brain/SKILL.md) | Team-scope sibling to second-brain. Structured raw dirs (people / companies / meetings / sops / decisions / customer-language / recurring-questions / sales-objections), multi-author attribution, sensitivity tagging, optional auto-sync from Fathom / Gong / Granola / CRM. Backbone for the Company Brain Setup CF service. |
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
| [`personal-cfo`](./skills/personal-cfo/SKILL.md) | Personal financial scenarios — house purchase + rental forecasting, monthly cash flow, big-purchase decisions. Household scope. |
| [`company-cfo`](./skills/company-cfo/SKILL.md) | Company / agency CFO workflow — monthly snapshots, weekly cash pulse, scenario projector. Transaction-sum EOM methodology, categorization discipline, forward forecasting. Pulls from bank + payment processor + payroll + expense-mgmt via `toolify`-wired integrations. Team scope. |
| [`paste`](./skills/paste/SKILL.md) | Clean terminal output for 9 destinations (Slack, Notion, Twitter, LinkedIn, email, GitHub, plain, HTML). Secret-detection first. |
| [`social-fetch`](./skills/social-fetch/SKILL.md) | Pull any social post by URL across 10 platforms (X, LinkedIn, IG, TikTok, Bluesky, Reddit, Mastodon, Threads, HN). Strategy chain with free + paid fallbacks. |

---

## Architecture

The repo is **public + generic**. Your personal data (Typefully workspace IDs, portfolio properties, voice overlays, archives) lives separately in `~/.config/makerskills/` (gitignored, on disk only).

Skills read from `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/<skill>/` paths. Set env vars in `~/.zshenv` to point at your locations:

```bash
export MAKERSKILLS_CONFIG="$HOME/.config/makerskills"
export SECOND_BRAIN_VAULT="$HOME/Documents/SecondBrain"    # for second-brain (personal-scope vault)
export COMPANY_BRAIN_VAULT="$HOME/Documents/CompanyBrain"  # for company-brain (team-scope vault)
export COMPANY_CFO_ROOT="$HOME/code/company-cfo"           # for company-cfo (reports, projector, config)
export SLIDE_DECK_REPO="$HOME/code/your-site-repo"         # for slide-deck
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

## License

MIT — see [LICENSE](./LICENSE).

## Built by

[Corey Haines](https://corey.co) — founder, [Conversion Factory](https://conversionfactory.co) + [Magister](https://magistermarketing.com).
