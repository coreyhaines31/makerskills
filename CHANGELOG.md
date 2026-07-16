# Changelog

All notable changes to `makerskills` are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

**Versioning note**: the plugin tag (e.g. `v0.5.0`) reflects the meta-collection version. Each skill has its own `metadata.version` in its SKILL.md frontmatter that evolves independently — a plugin release may contain skills at different internal versions.

---

## [v1.5.0] — unreleased

### Added
- **New skill: `maker-council`** (v0.1.0, closes #1) — your personal board of advisors, simulated. Eight founders/operators whose lenses collide on purpose: Jason Fried (calm/profitable), Elon Musk (first principles/urgency), Jeff Bezos (decision doors/long-term), Jensen Huang (flat org/strategic pain), Bob Iger (big bets/creative respect), Paul Graham (default alive/unscalable things), Naval Ravikant (leverage/productize yourself), Sara Blakely (bootstrap/sell first). Seats 3–5 by question type with a **designated dissenter** (an agreeing council is a mirror, not a board), grounds every take in documented frameworks via per-member dossiers, optional live-research pass through `deep-research`/`watch-video`/`last30days`, maps the disagreements, and synthesizes a chair's call that usually hands off to `/decide`. Strict grounding rules: labeled as simulation, no fabricated quotes, no invented endorsements, extra care for living members. Custom bench members + session archive live in `$MAKERSKILLS_CONFIG/maker-council/`. Adapted from the shipped `marketing-skills:marketing-council` (same author) with an operator bench and makerskills conventions. 19 → 20 skills.

---

## [v1.4.0] — 2026-07-15

### Added
- **`decide` Q39 — opportunity cost** (skill v0.3.0, closes #11) — a reader on X pointed out the 37signals 38 never directly ask "if we say yes to this, what are we saying no to?" (nearest: Q36 return-on-effort, Q37 easier/harder). Added as a clearly-labeled **house addition** so the original 38 stay faithful to the source, and wired into triage: money decisions and big time/focus commitments now pull Q39.

---

## [v1.3.0] — 2026-07-14

### Added
- **New skill: `unstuck`** (v0.1.0, closes #9) — the roadblock antidote. When a solution seems impossible, it refuses to take no for an answer: classifies what kind of "no" you hit (assumption / framing / gatekeeper / tool / resource / physics), triages 3–4 lateral-thinking techniques from a 10-technique inventory (`references/techniques.md` — assumption autopsy, inversion, first principles, altitude shift, work-backwards, analogical transfer, constraint toggling, provocation, SCAMPER, interrogate-the-no), and enforces a 10-angle minimum before evaluating anything. **Agent-proactive by design**: agents run the fast path on themselves before reporting any dead end, so "that's not supported" always arrives with tried-angles receipts. Honest-exit guardrail: "the wall is load-bearing, reroute the goal" is a legitimate output, and a no from consent/law/ethics is a real no. Archives to `$MAKERSKILLS_CONFIG/unstuck/archive/` — a growing pattern library of which techniques crack *your* walls. Sits upstream of `decide` (generates options when there appear to be none; `decide` picks among them). 18 → 19 skills.

---

## [v1.2.0] — 2026-07-10

### Fixed
- **Archives moved out of the install tree** (closes #5; `decide`, `business-brainstorm`, `deep-research`, `personal-cfo`, `slide-deck` all → v0.2.0) — skills previously archived user state inside their own skill folder (`references/*-archive/`). Installers that re-sync skills from source (e.g. `npx skills add`) wiped the folder on upgrade, destroying the user's whole archive. Archives now live in `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/<skill>/archive/` (matching the public/private split ARCHITECTURE.md already documented), with a best-effort migration step: each skill moves old in-repo archive entries to the new location if they still exist (plugin/symlink installs keep them; an npx re-sync that already ran may have deleted them — that loss is exactly the bug this fixes going forward). Repo no longer ships INDEX.md seeds; `.gitignore` guards against old-style in-repo archives.
- **Gender-neutral prose** — skill bodies referred to the user as "he/his/him" in 16 places across 9 files ("capture his answers," etc.). All rewritten to they/their/the user.
- **`slide-deck` no longer hardcodes the author's identity** — the close-slide footer (`@coreyhaines · corey.co`) is now `<AUTHOR_HANDLE> · <AUTHOR_SITE>` tokens sourced from `$MAKERSKILLS_CONFIG/slide-deck/identity.yaml` (or asked once and saved); decks never ship with someone else's handle. Stray corey.co mentions genericized.

*Thanks to a user bug report for all three.* 🙏

---

## [v1.1.0] — 2026-07-06

### Added
- **`company-brain` trust levels + review mode** (skill v0.2.0, closes #3) — answers "what stops dumped-in info from poisoning context?":
  - `trust:` field on every structured-raw capture: `unreviewed` (default) / `verified` / `deprecated` / `superseded`. Named `trust`, not `status`, to avoid colliding with the lifecycle `status:` fields on `companies/` and `decisions/`. Files with no `trust:` field are treated as `unreviewed`.
  - **Query trust rules** — prefer `verified` + recent; never use `deprecated`/`superseded` as context; surface conflicts; flag low-confidence answers built mostly on `unreviewed` sources.
  - **New `/cb review` mode** — human triage queue (unreviewed captures + lint flags + lapsed review dates) with verify / deprecate / supersede / skip dispositions. Respects sensitivity levels; every non-skip disposition stamps `reviewed` + `reviewed_by`; saves a review summary to `outputs/` for an audit trail. Pair with `loopify` for a weekly cadence.
  - **Compile trust filtering** — deprecated/superseded sources excluded from wiki pages; pages built mostly on unreviewed sources get a warning callout.
  - **Lint check 13** — review backlog (>20 unreviewed files or no review pass in >1 month).
  - Deprecation replaces deletion — the "never delete raw files" rule stays intact.

### Fixed
- `company-brain` lint said "same six checks as second-brain" but second-brain has seven; company-brain additions renumbered 8–13.
- Meeting filename pattern and a `person-`/`people/` reference aligned between SKILL.md and schema.md.

---

## [v1.0.0] — 2026-07-06

Public launch. 🚀

18 skills for founders and indie operators, organized in five groups: meta (`skillify` / `toolify` / `loopify`), decision + strategy (`decide` / `business-brainstorm` / `deep-research` / `domain`), knowledge (`second-brain` / `company-brain` / `read-book` / `watch-video`), output (`jab-hook` / `slide-deck`), and operations (`pm` / `personal-cfo` / `company-cfo` / `paste` / `social-fetch`).

### Changed
- Genericized remaining brand mentions in `BACKLOG.md`, `ARCHITECTURE.md`, and `README.md` (follow-ups since v0.5.4).
- Version bumped to 1.0.0 — no breaking changes from v0.5.4; this marks launch stability.

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
