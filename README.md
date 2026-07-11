# makerskills

[![Stars](https://img.shields.io/github/stars/coreyhaines31/makerskills?style=flat-square&label=stars&color=000)](https://github.com/coreyhaines31/makerskills/stargazers) [![Release](https://img.shields.io/github/v/release/coreyhaines31/makerskills?style=flat-square&color=000)](https://github.com/coreyhaines31/makerskills/releases) [![License](https://img.shields.io/badge/license-MIT-000?style=flat-square)](./LICENSE)

**AI agent skills for the personal operator's craft.** Decisions, research, second-brain workflows, content rotation, scenario modeling, CFO cadence, domain hunts, and the meta-skills to author more.

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

## Getting started — 5-minute path

New to the plugin? Do these in order. Everything else can wait until you need it.

**1. Install the plugin** (above), then set the base env var in `~/.zshenv`:

```bash
export MAKERSKILLS_CONFIG="$HOME/.config/makerskills"
```

Reload your shell.

**2. Run your first skill — start with `decide`.** No config required:

```
/decide
```

It'll ask what decision you're facing, pick the right questions from the 37signals framework, and archive the result with a revisit date. **That's the first-touch experience**: any skill in this plugin. Structured input → structured output → written to disk.

**3. Read one SKILL.md** to see the pattern:

```bash
open ~/code/makerskills/skills/decide/SKILL.md
```

Each skill is a workflow doc — you can invoke via `/decide` OR read the SKILL.md and run the steps by hand. The plugin is documentation-first; the automation is a side effect.

**4. Try one more skill** that involves personal config, so you understand the pattern:

```
/paste twitter
```

It'll read your clipboard, strip formatting, warn if over 280 chars, and copy back the cleaned output. First invocation may prompt you to install `pbcopy`-adjacent deps if missing. No config file needed — this is a pure utility.

**5. Now branch out.** Skim [The 19 skills](#the-19-skills) below and pick one that maps to a workflow you're already doing manually. That's the highest-leverage adoption path.

---

## Which skill do I invoke when?

Routing table for common operator jobs. Match your intent → skill.

| I want to... | Skill |
|---|---|
| Think through a decision with a real fork | [`decide`](./skills/decide/SKILL.md) |
| Pressure-test a new business or product idea | [`business-brainstorm`](./skills/business-brainstorm/SKILL.md) |
| Research a topic with citations | [`deep-research`](./skills/deep-research/SKILL.md) |
| Find an available `.com` for a new project | [`domain`](./skills/domain/SKILL.md) |
| Capture / query / lint my personal knowledge base | [`second-brain`](./skills/second-brain/SKILL.md) |
| Same but for a team-shared knowledge base | [`company-brain`](./skills/company-brain/SKILL.md) |
| Extract notes / highlights / summaries from a book | [`read-book`](./skills/read-book/SKILL.md) |
| Extract a transcript or key moments from a video | [`watch-video`](./skills/watch-video/SKILL.md) |
| Fetch any social post by URL as structured data | [`social-fetch`](./skills/social-fetch/SKILL.md) |
| Plan / draft social content rotation across a portfolio | [`jab-hook`](./skills/jab-hook/SKILL.md) |
| Draft, update, convert, or export a slide deck | [`slide-deck`](./skills/slide-deck/SKILL.md) |
| Design a physical object (furniture, parts) by describing it | [`vibecad`](./skills/vibecad/SKILL.md) |
| Clean terminal output for Slack / LinkedIn / X / Notion etc. | [`paste`](./skills/paste/SKILL.md) |
| Manage projects across businesses (kanban) | [`pm`](./skills/pm/SKILL.md) |
| Model personal financial scenarios (house, cash flow, etc.) | [`personal-cfo`](./skills/personal-cfo/SKILL.md) |
| Run monthly / weekly CFO for a company or agency | [`company-cfo`](./skills/company-cfo/SKILL.md) |
| Create, adapt, or update a skill | [`skillify`](./skills/skillify/SKILL.md) |
| Wire up an integration / API / MCP into a project | [`toolify`](./skills/toolify/SKILL.md) |
| Set up an agent loop or scheduled task | [`loopify`](./skills/loopify/SKILL.md) |

Not sure between two? The **skill's SKILL.md description** always includes trigger phrases and disambiguation from adjacent skills.

---

## The 19 skills

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
| [`company-brain`](./skills/company-brain/SKILL.md) | Team-scope sibling to second-brain. Structured raw dirs (people / companies / meetings / sops / decisions / customer-language / recurring-questions / sales-objections), multi-author attribution, sensitivity tagging, trust levels + a `/cb review` culling pass so unreviewed or deprecated info never poisons answers, optional auto-sync from Fathom / Gong / Granola / CRM. Backbone for a Company Brain Setup productized service. |
| [`read-book`](./skills/read-book/SKILL.md) | PDFs, EPUBs, MOBI, markdown — chapter-by-chapter notes, quotes, summaries, or spaced-rep study mode. |
| [`watch-video`](./skills/watch-video/SKILL.md) | YouTube, Loom, Vimeo, Riverside, Zoom, MP4. Transcript / visual / multimodal (Gemini-native) modes. |

### Output & creative
| Skill | What |
|---|---|
| [`jab-hook`](./skills/jab-hook/SKILL.md) | Gary Vee's jab-jab-jab-right-hook rhythm applied to your portfolio rotation on X + LinkedIn via Typefully. |
| [`slide-deck`](./skills/slide-deck/SKILL.md) | Branded React decks (Next.js). "Show, don't tell" narrative pitching, density modes, PPT conversion, Playwright export. |
| [`vibecad`](./skills/vibecad/SKILL.md) | Conversational parametric CAD via OpenSCAD — describe an object in plain English, get rendered multi-view previews, iterate; no CAD UI. Woodworking-first (cut lists, nominal-vs-actual lumber, board feet, kerf-aware stock layout) plus STL export for 3D printing and DXF for laser/CNC. |

### Operations & utilities
| Skill | What |
|---|---|
| [`pm`](./skills/pm/SKILL.md) | Kanban (5-column) + Eisenhower across your portfolio. Tool-agnostic adapters (Notion, GitHub, Plane, Linear, Obsidian, manual). |
| [`personal-cfo`](./skills/personal-cfo/SKILL.md) | Personal financial scenarios — house purchase + rental forecasting, monthly cash flow, big-purchase decisions. Household scope. |
| [`company-cfo`](./skills/company-cfo/SKILL.md) | Company / agency CFO workflow — monthly snapshots, weekly cash pulse, scenario projector. Transaction-sum EOM methodology, categorization discipline, forward forecasting. Pulls from bank + payment processor + payroll + expense-mgmt via `toolify`-wired integrations. Team scope. |
| [`paste`](./skills/paste/SKILL.md) | Clean terminal output for 9 destinations (Slack, Notion, Twitter, LinkedIn, email, GitHub, plain, HTML). Secret-detection first. |
| [`social-fetch`](./skills/social-fetch/SKILL.md) | Pull any social post by URL across 10 platforms (X, LinkedIn, IG, TikTok, Bluesky, Reddit, Mastodon, Threads, HN). Strategy chain with free + paid fallbacks. |

---

## Skills compose

Skills call each other by name. When a skill's job hits an adjacent job, it routes there rather than reimplementing. The most-referenced skills are the "central" ones — expect to touch these first as you adopt:

| Most referenced by siblings | Composes with... |
|---|---|
| **`watch-video`** (54 refs) | `second-brain` (capture summary), `skillify from-video`, `social-fetch` (X/IG/TikTok metadata), `pm` (action items), `decide` (flagged decisions) |
| **`skillify`** (51 refs) | `watch-video` (record → skill), `second-brain` (capture source), `compound-engineering:*` (Anthropic-official skill authoring) |
| **`second-brain`** (48 refs) | `deep-research` (external gaps), `read-book` (highlights → wiki), `watch-video` (summaries → raw), `paste` (clean captures) |
| **`slide-deck`** (38 refs) | `business-brainstorm` (pitch decks), `watch-video` (talk-recording → outline), `second-brain` (wiki as content) |
| **`company-brain`** (33 refs) | `toolify` (wire auto-sync), `loopify` (schedule sync), `deep-research` (external gaps), `decide` (structured archive) |
| **`domain`** (32 refs) | `business-brainstorm` (name after idea passes filter), `toolify` (wire Domainr + Namecheap), `decide` (candidate fork) |

See each skill's `## Composes with` section for the full dependency list.

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

Full setup in [INSTALL.md](./INSTALL.md). Full mental model in [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## Versioning

Two levels of semver:

- **Plugin release tag** (e.g. `v0.5.0`) — this repo's overall version. Bumped on each meaningful addition to the collection. See [CHANGELOG.md](./CHANGELOG.md).
- **Per-skill `metadata.version`** in each SKILL.md frontmatter — that skill's individual version. Evolves independently.

A plugin release at `v0.5.0` may contain skills at `0.1.0`, `0.1.1`, `0.2.0`, `0.3.1` simultaneously. That's expected — each skill has its own iteration cadence.

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
- **Cross-plugin**: prefix with the plugin (`see marketingskills:cro`)

Claude resolves references by description match at load time — no manifest linking needed.

## Related skill packs

- [`marketingskills`](https://github.com/coreyhaines31/marketingskills) — 46 marketing skills (CRO, copywriting, SEO, ads, etc.)

## Docs

- [`INSTALL.md`](./INSTALL.md) — env vars, personal config setup, runtime dependencies
- [`EXAMPLES.md`](./EXAMPLES.md) — one worked example per skill: what you say → what the skill produces
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — mental model, families, personal-config pattern, sibling-repo ecosystem
- [`CHANGELOG.md`](./CHANGELOG.md) — release history with per-version details
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — how to add a skill, testing, PR conventions
- [`FAQ.md`](./FAQ.md) — common questions and gotchas
- [`BACKLOG.md`](./BACKLOG.md) — planned skills + brainstorm candidates

## License

MIT — see [LICENSE](./LICENSE).

## Built by

[Corey Haines](https://corey.co) — founder, [Conversion Factory](https://conversionfactory.co) + [Magister](https://magistermarketing.com).
