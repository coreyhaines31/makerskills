# Architecture

Mental model for how the plugin is structured, why the personal-config pattern exists, and how skills relate to each other.

## The two-layer split — public repo + private config

`makerskills` is intentionally split into two layers:

```
┌─────────────────────────────────────────────────────────────────┐
│ PUBLIC LAYER (this git repo, github.com/coreyhaines31/makerskills)
│                                                                 │
│   skills/*/SKILL.md         — workflow logic, generic            │
│   skills/*/references/*.md  — schema, methodology, templates     │
│   README, INSTALL, etc.     — documentation                      │
│                                                                 │
│   NO personal data. NO API keys. NO real portfolio names.        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PRIVATE LAYER (~/.config/makerskills/, gitignored)               │
│                                                                 │
│   jab-hook/properties.yaml         — your rotation portfolio     │
│   jab-hook/typefully.yaml          — your Typefully workspace ID │
│   jab-hook/voice.local.md          — your voice rules            │
│   pm/boards.md                     — your kanban board configs   │
│   personal-cfo/scenarios-archive/  — your financial scenarios    │
│   deep-research/archives/          — your past research briefs   │
│                                                                 │
│   YOUR real data. Never leaves your machine.                    │
└─────────────────────────────────────────────────────────────────┘
```

### Why the split matters

- **The repo is safe to share, star, fork, and adopt.** No secrets, no personal portfolio, no client names. Public flip via `git filter-repo` on 2026-06-28 removed all pre-flip personal data from history.
- **Your data stays yours.** `~/.config/makerskills/` is a plain directory with markdown + YAML. Migrate to a new machine by copying it. No cloud sync required.
- **Updating the plugin doesn't break your config.** `git pull` on the repo doesn't touch your personal files.

### The env var contract

Skills locate personal config via `MAKERSKILLS_CONFIG`, defaulting to `$HOME/.config/makerskills`:

```bash
export MAKERSKILLS_CONFIG="$HOME/.config/makerskills"
```

Set additional per-skill vars only for skills that need paths outside the config dir (e.g., `SECOND_BRAIN_VAULT`, `COMPANY_BRAIN_VAULT`, `COMPANY_CFO_ROOT`, `SLIDE_DECK_REPO`).

Full list in [INSTALL.md](./INSTALL.md).

---

## Skill families

The 18 skills group into 6 families by job type:

### Meta — extend Claude Code (the `-ify` trifecta)

Three skills that build MORE skills / tools / loops:

- **`skillify`** — create, adapt, or update a skill
- **`toolify`** — wire up an integration / API / MCP server
- **`loopify`** — set up an agent loop or scheduled task

Vocabulary-moat family: memorable `-ify` rhythm mapping to the 3 primary Claude Code extension surfaces. **Rule of 3: the family stays at three.** Resist Hookify / Configify / Memorify temptations.

### Decision & strategy

Skills for thinking through problems before committing to action:

- **`decide`** — 37signals decision framework
- **`business-brainstorm`** — 9-dimension idea pressure-test
- **`deep-research`** — multi-source research with citations
- **`domain`** — .com domain hunt

Common thread: **structured input → structured output → archived**. Every decision, brief, research result, and domain shortlist gets written to disk with a revisit date.

### Knowledge & content consumption

Skills that ingest external content and turn it into structured knowledge:

- **`second-brain`** — personal-scope Karpathy LLM Wiki over any markdown vault
- **`company-brain`** — team-scope sibling with structured `people/` `companies/` `meetings/` `sops/` `decisions/` dirs
- **`read-book`** — chapter-by-chapter notes / quotes / summaries from PDF/EPUB/MOBI
- **`watch-video`** — transcript / visual / multimodal from any video source

Common thread: **compile raw → wiki → outputs**. Every consumed artifact routes toward a compilable, queryable, evergreen knowledge layer.

### Output & creative

Skills that produce shareable artifacts:

- **`jab-hook`** — social content rotation across X + LinkedIn
- **`slide-deck`** — branded React decks with Playwright export

Common thread: **strong voice + brand-perfect output**. Never generic AI-slop; the output should be indistinguishable from what the operator would produce by hand at their best.

### Operations & utilities

Skills for running the business (or the life):

- **`pm`** — Kanban + Eisenhower across the portfolio
- **`personal-cfo`** — household financial scenarios
- **`company-cfo`** — company monthly CFO cadence
- **`paste`** — clean terminal output for 9 destinations
- **`social-fetch`** — normalized fetcher across 10 platforms

Common thread: **cadence + discipline**. These skills reinforce the routines that keep an operator functional at scale.

### Cross-family patterns

Two patterns show up across families:

1. **Personal ↔ team siblings**: `second-brain` ↔ `company-brain`, `personal-cfo` ↔ `company-cfo`. Same methodology, different scope. Team-scope skills add multi-author attribution + structured schema. Positioning: *"[Personal thing] made YOU a knowledge worker / financially literate. [Company thing] makes your TEAM one / your BUSINESS one."*
2. **The `-ify` extension trifecta**: `skillify` / `toolify` / `loopify` cover the 3 ways to extend Claude Code. Naming coined for vocabulary consistency.

---

## Composition patterns

Skills call each other by name. The most-referenced skills are the "central" ones:

```
                          watch-video (54 refs)
                              ↓
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
         skillify (51)   second-brain (48)   slide-deck (38)
              ↓               ↓
         (record → skill)  company-brain (33)
                              ↓
                          domain (32)
```

**Reading the composition map**: `watch-video` is invoked by 54 other skill contexts (including `skillify from-video`, `slide-deck` for talk-recordings, and any blog/publish skills you compose with). `second-brain` is invoked by 48 (for captures + queries). The central skills carry more downstream load.

Practical implication: **when adopting the plugin, install and set up the central skills first**. `watch-video` needs yt-dlp + ffmpeg + MLX-Whisper; `second-brain` needs a vault path. Get those working, and the rest of the plugin becomes progressively more useful.

---

## SKILL.md as executable documentation

The core insight of this plugin: **a SKILL.md IS the skill**. Not "code that implements the skill" — the markdown itself is the workflow logic. Claude reads the markdown at invocation time and executes the steps.

Consequences:

- **Every SKILL.md is human-readable.** Anyone can read it, learn the methodology, and run the steps by hand without Claude Code.
- **Iterating a skill is markdown editing.** No build step, no test harness, no compilation. Edit the SKILL.md, invoke, observe, edit again.
- **Debugging is reading.** If a skill behaves unexpectedly, read its SKILL.md. The behavior IS the documentation.
- **Voice matters.** Because Claude routes to a skill by matching the description against a user's phrasing, the description's precision matters more than any other line in the file.

This is why the collection is intentionally documentation-first. The plugin is a library of workflow docs; the automation is a side effect of Claude Code being able to execute those docs.

---

## Sibling repo ecosystem

`makerskills` is designed to sit alongside your other skill plugins. Public siblings you can install today:

| Repo | Scope |
|---|---|
| **[`makerskills`](https://github.com/coreyhaines31/makerskills)** | Personal operator's craft — this repo |
| **[`marketingskills`](https://github.com/coreyhaines31/marketingskills)** | 44 marketing skills (CRO, copywriting, SEO, ads) |

Skills can cross-reference each other (`makerskills:paste` from a `marketingskills` skill, for example). Cross-plugin references resolve at invocation time — no manifest linking needed.

If you maintain private domain-specific plugins of your own (agency, book, video, client work), `skillify` reads a list from `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/skillify/repos.yaml` so you can propagate learnings across all of them.

---

## Versioning policy

Two levels of semver:

1. **Plugin release tag** — the collection's overall version. Bumped on each meaningful addition. See [CHANGELOG.md](./CHANGELOG.md).
2. **Per-skill `metadata.version`** in each SKILL.md frontmatter. Evolves independently.

A plugin release at `v0.5.0` may contain skills at `0.1.0`, `0.1.1`, `0.2.0`, `0.3.1` simultaneously. That's expected.

**When to bump a skill's individual version:**

- **PATCH** (0.1.0 → 0.1.1): docs clarification, added `## Notes on quality` section, typo fixes, non-behavioral improvements
- **MINOR** (0.1.0 → 0.2.0): new mode, new sub-workflow, new composition, new references file
- **MAJOR** (0.1.0 → 1.0.0): breaking change to invocation contract, mode rename, output-schema change

**When to bump the plugin release tag:**

- **MINOR** (v0.4.0 → v0.5.0): net-new skill added, or a significant coordinated update across skills
- **PATCH** (v0.5.0 → v0.5.1): docs / infrastructure polish, no new user-visible skill capabilities
- **MAJOR** (v0.5.0 → v1.0.0): reserved for the eventual "we consider this stable" milestone. Not yet reached.

---

## Design principles

The principles that shape every skill in the collection:

1. **Documentation-first, automation-second.** The SKILL.md is the primary artifact.
2. **Composability over completeness.** Better to have small skills that compose than one mega-skill that tries to do everything.
3. **Structured input, structured output, archived to disk.** Every meaningful invocation leaves a trace on disk for future revisitation.
4. **Voice matters.** Every skill's description + body should sound like the operator's own voice, not generic AI.
5. **Graceful degradation.** Optional dependencies (API keys, external tools) should be optional — the skill should degrade cleanly, not fail hard.
6. **Personal data stays private.** Public repo + private config layer. Never mix.
7. **Cite everything.** Sources, references, memory files — traceability makes future revisions possible.
8. **Cadence + rituals over one-off invocations.** The daily/weekly/monthly rhythm is what compounds. Skills should reinforce rituals, not fight them.
