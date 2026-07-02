# Changelog

All notable changes to `makerskills` are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

**Versioning note**: the plugin tag (e.g. `v0.5.0`) reflects the meta-collection version. Each skill has its own `metadata.version` in its SKILL.md frontmatter that evolves independently — a plugin release may contain skills at different internal versions.

---

## [v0.5.4] — 2026-07-01

### Fixed
Three follow-up issues surfaced by `codex review` on v0.5.3:

- **Missed brand mentions** — `skills/pm/references/boards.md` example row said `_example_magister_`, `skills/social-fetch/SKILL.md` + `references/output-schema.md` still cited `@coreyganim`, and `skills/watch-video/SKILL.md` + `skills/slide-deck/SKILL.md` still mentioned "Factory Floor." Genericized all four to placeholders.
- **`/pm setup` re-introduced personal data** — the setup mode instructed the agent to save new board mappings back to `references/boards.md` in the tracked repo, which would leak real business names + board IDs. Changed to write to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/pm/boards.md`. Repo's `references/boards.md` is now clearly marked TEMPLATE only.
- **skillify cross-repo loop had two bugs** — (a) `yq` output includes a literal `~` in paths like `~/code/makerskills`, but the shell doesn't expand `~` inside a quoted variable, so `grep` looked under a directory called `~` and found nothing. Fixed by explicit `${raw/#\~/$HOME}` expansion. (b) The config path hardcoded `~/.config/makerskills`, ignoring users with `MAKERSKILLS_CONFIG` set to a different location. Both loops (`SKILL.md` + `references/update-propagation.md`) now honor the env var.

---

## [v0.5.3] — 2026-07-01

### Changed
- **Public-launch polish**: swept remaining personal brand names, partner names, and private-sibling references out of `EXAMPLES.md` and 8 skills (`business-brainstorm`, `pm`, `jab-hook`, `second-brain`, `company-brain`, `deep-research`, `personal-cfo`, `skillify`, `social-fetch`, `watch-video`) plus `ARCHITECTURE.md` and `README.md`. Placeholders (`<owner>`, `Property A`, `<person>`, etc.) replace anything user-specific.
- **`skillify`**: sibling repo list moved out of hardcoded prose into `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/skillify/repos.yaml`. `--cross-repo` propagation now iterates over the user's declared repos instead of a fixed list.
- **`business-brainstorm`**: portfolio-fit + distribution + opportunity-cost dimensions now load user-specific context from `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/business-brainstorm/portfolio.local.md` if present, instead of hardcoding one operator's businesses.
- **`pm`**: board config and team/partner overlay load from `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/pm/{boards.md, team.local.md}` — repo's `references/boards.md` is now just a template.

### Removed
- Dropped inline cross-references to `cf-skills` (a private companion plugin external users can't install) from `personal-cfo`, `jab-hook`, `company-brain`, `social-fetch`, `watch-video`, and `second-brain`. Fresh users no longer see "sibling for CF agency books" style references to something they can't get.
- Dropped `~/.claude/memory/feedback_cf_*.md` references from `jab-hook` — those are personal memory files, not portable.

---

## [v0.5.0] — 2026-07-01

### Added
- **`domain`** — 11-step `.com` domain-hunt workflow on Laura Roeder's "availability-first, never fall in love with a name" methodology. Multi-tool ensemble: Vercel CLI + `whois` (per-TLD server) + `rdap.org` (modern TLDs) + Domainr API + Namecheap API + `agent-browser` for USPTO trademark screening + click-through URLs for aftermarket marketplaces (HugeDomains / Afternic / Sedo / Dan). Handles bare-word + prefix/suffix brainstorming (`try/use/with/join/get/go/hey/the` + word, `word +ly/+ify/+labs`), budget filtering, negotiation guidance, social handle checks, and (on confirmation) purchase via Vercel or Namecheap. Ported from a personal slash command; generic for adopters.

### Changed
- `README.md` skill catalog now reflects 18 skills.
- `INSTALL.md` documents 4 new optional env vars: `DOMAINR_API_KEY`, `NAMECHEAP_API_USER`, `NAMECHEAP_API_KEY`, `NAMECHEAP_CLIENT_IP`.
- `makerskills-website` skills.ts updated to include `domain` (skill count 17 → 18).

---

## [v0.4.0] — 2026-07-01

### Added
- **`company-cfo`** — anonymized team-scope sibling to `personal-cfo`. Monthly snapshots + weekly cash pulse + scenario projector, applied to company books. Universal methodology preserved (transaction-sum EOM computation, categorization discipline, intramonth cycle-low tracking, cash floor discipline) — company-specific data stripped so any team can adopt.
  - Four modes: `monthly` (default, 7-phase workflow) / `weekly` (thin cash pulse) / `scenario` (ad-hoc projector modeling) / `pickup` (resume from prior run)
  - Data source pattern generalized across bank / payment processor / payroll / expense management. Wire via `/toolify`; schedule via `/loopify`.
  - First-run walkthrough seeds a per-company `CLAUDE.md` from `references/company-config-template.md`.
  - Ships with 3 references: `eom-cash-methodology.md` (the transaction-sum method + why walkback fails), `categorization.md` (lock categories for the fiscal year), `company-config-template.md` (seed for the per-company config).

### Changed
- New env var `COMPANY_CFO_ROOT` documented in `README.md` + `INSTALL.md`.
- `makerskills-website` skills.ts updated (16 → 17).
- Vocabulary file (`~/.config/youtubeskills/vocabulary.local.md`) extended with the "CFO family" — *"Personal CFO for your household. Company CFO for your business."*

---

## [v0.3.0] — 2026-06-30

### Added
- **`company-brain`** — team-scope sibling to `second-brain`. Structured raw dirs (`people/`, `companies/`, `meetings/`, `sops/`, `decisions/`, `customer-language/`, `recurring-questions/`, `sales-objections/`) instead of flat type-prefixed `raw/`. Multi-author attribution (`author:` stamp on every capture, cited in wiki `## Sources` sections). Sensitivity tagging (`internal` / `leadership` / `confidential`) respected in query mode. Optional auto-sync source recipes for Fathom / Gong / Granola / Slack / email / CRM (wired via `/toolify`, scheduled via `/loopify`).
  - Positioning line: *"Second Brain made YOU a knowledge worker. Company Brain makes your TEAM one."*
  - Operational backbone for the **Company Brain Setup** productized CF service (renamed from "Second Brain as a Service" for vocabulary consistency with the skill name).

### Changed
- New env var `COMPANY_BRAIN_VAULT` documented in `README.md` + `INSTALL.md`.
- `makerskills-website` skills.ts updated (15 → 16).

---

## [v0.2.0] — 2026-06-30

### Added
- **`skillify`** — consolidates the prior `create-skill`, `adapt-skill`, and `update-skill` into a single skill with mode routing. **CREATE** mode covers from-chat / from-video / from-dump / from-scratch input paths. **ADAPT** mode ports an external skill with three-bucket classification (keep verbatim / adapt / add), license check, and attribution file. **UPDATE** mode improves existing skills from learnings with cross-skill propagation, memory-vs-skill triage, and semver discipline. All original reference files preserved under `skills/skillify/references/` with mode prefixes.
- **`toolify`** — wizard for wiring up an integration, API, MCP server, or third-party service into a Next.js or Rails project. Handles auth, env vars, client wrapper, webhook signature verification, and smoke-test. Scoped tightly (Next.js + Rails) — supporting every stack would bloat the wizard.
- **`loopify`** — wizard for setting up an agent loop, cron-scheduled task, or recurring workflow. Judgment layer on top of `ScheduleWakeup` / `CronCreate` / built-in `/loop` — picks pattern (dynamic / cron / one-shot), tunes delay for cache windows (avoids the 5-minute cache-miss cliff), enforces idempotency, requires bail-out conditions.

### Removed
- `create-skill`, `adapt-skill`, `update-skill` — replaced by `skillify` (mode-routed).

### Changed
- `README.md` catalog reorganized: Meta section renamed to *"Meta — extend Claude Code (the -ify trifecta)"*. All cross-references in other SKILL.md files updated (e.g., `watch-video` now references `skillify from-video` instead of `create-skill from-video`).
- Vocabulary moat strategy: the trifecta names (`skillify` / `toolify` / `loopify`) added to `~/.config/youtubeskills/vocabulary.local.md` for consistent use in YT scripts + descriptions. See `~/Corey's Projects/wiki/Founding Marketing Frameworks.md` for the broader vocabulary strategy.

### Constraints (documented, self-imposed)
- **Rule of 3**: the `-ify` family stays at exactly three. Resist Hookify / Configify / Memorify temptations.
- **No backward-compatibility shims** on the rename. Clean cutover per repo's public flip date (2026-06-28) — audience small enough that no shim is needed.

---

## [v0.1.0] — 2026-06-28

Initial public release. 15 skills across 5 families:

- **Meta — manage skills themselves**: `create-skill`, `adapt-skill`, `update-skill` (consolidated to `skillify` in v0.2.0)
- **Decision & strategy**: `decide` (37signals framework), `business-brainstorm` (9-dimension pressure-test), `deep-research` (multi-source with citations)
- **Knowledge & content consumption**: `second-brain` (Karpathy LLM Wiki over markdown vault), `read-book` (PDF/EPUB/MOBI notes), `watch-video` (transcript/visual/multimodal)
- **Output & creative**: `jab-hook` (Gary Vee's rotation on X + LinkedIn via Typefully), `slide-deck` (branded React decks with Playwright export)
- **Operations & utilities**: `pm` (Kanban + Eisenhower, tool-agnostic adapters), `personal-cfo` (household financial scenarios), `paste` (clean terminal output for 9 destinations), `social-fetch` (normalized fetcher across 10 social platforms)

Public flip on 2026-06-28 via `git filter-repo` history scrub — personal data (Typefully IDs, portfolio properties, voice overlays, archives) migrated to `~/.config/makerskills/` (gitignored, on-disk only). Repo pattern locked: **public + generic code + private personal-config layer**.

Documentation established: `README.md` skill catalog + architecture, `INSTALL.md` env vars + runtime dependencies, `LICENSE` (MIT), `BACKLOG.md` skill shortlist + brainstorm candidates.

---

## Unreleased

Tracked in [`BACKLOG.md`](./BACKLOG.md). No confirmed next release yet — candidates include `weekly-review`, `daily-startup`, `release-notes`, `model-select`.
