# Skill backlog

Skills queued for future sessions. Use `/create-skill` to scaffold when ready (will become `/skillify` in v0.2 — see below).

---

## v0.2 — The `-ify` trifecta (priority next release)

Coined-phrase trifecta for the 3 ways to extend Claude Code. Memorable family (`-ify` rhythm), each maps to a real extension surface, no equivalent canonical naming exists in the ecosystem yet.

### Scope (ship together, not piecemeal)

1. **`skillify`** — create / adapt / update a Claude Code skill. Replaces and consolidates the three current skills (`create-skill`, `adapt-skill`, `update-skill`) into one with internal mode routing (detects intent from input: existing SKILL.md present → adapt/update; net new → create).
2. **`toolify`** — wizard for adding an integration / MCP server / API wrapper into a project. Reference Matt Pocock's `/wizard` skill (github.com/mattpocock/skills) for the interactive Q&A pattern before designing. Scope tightly — "integrate an MCP or API into a Next.js project" beats "integrate anything."
3. **`loopify`** — wizard for setting up an agent loop (cron-based or dynamic). Judgment layer on top of `ScheduleWakeup`/`CronCreate`: when to loop vs re-prompt, delay tuning (avoiding 5-min cache-miss territory), idempotent loop body design, bail-out conditions.

### Ordering (single coordinated PR)

1. Pull Matt Pocock's `/wizard` from github.com/mattpocock/skills — study the pattern
2. Sketch the 3 SKILL.md descriptions in one sitting so the family voice is consistent
3. Rename `create-skill`/`adapt-skill`/`update-skill` → `skillify` with mode routing
4. Build `toolify` + `loopify`
5. Update README + INSTALL + cross-references in other SKILL.md files (anywhere `makerskills:create-skill` etc. is cited)
6. Tag `v0.2.0` with the trifecta as headline feature
7. Add `skillify`/`toolify`/`loopify` to `~/.config/youtubeskills/` vocabulary-moat list so YT scripts know to use the terms

### Constraints

- **Don't extend the `-ify` family beyond three.** Magic of three is canonical (HIVES rule of 3). Resist Hookify / Configify / Memorify temptations.
- **No backward-compatibility shims** for the rename. makerskills only flipped public 2026-06-28; small enough audience for clean rename per CLAUDE.md guidance ("Don't use feature flags or backwards-compatibility shims when you can just change the code").
- **Vocabulary moat is the strategic goal**, not just code reorganization. This trifecta + Marketing Engineer + Bottom-Up Growth + ORB Framework + Engineering as Marketing forms Corey's coined-phrase IP stack for the YT channel. See `~/Corey's Projects/wiki/Founding Marketing Frameworks.md` for the broader vocabulary strategy.

---

## Skill candidates (on the shortlist)

- `weekly-review` — Friday pulse across all properties
- `intro-broker` — double opt-in intros
- `thanks-no` — polite declines for speaker/podcast/partnership asks
- `daily-startup` — morning brief (priorities + overnight + calendar + top 3)
- `swipe-save` — marketing inspiration capture (may merge with `second-brain`)
- `new-project` — Next.js + Drizzle + Neon scaffold with Corey's patterns
- `gh-triage` — cross-repo issue/PR summary
- `bjj-log` — training log

## Brainstorm candidates (for `/business-brainstorm`)

Not skills — business / product ideas worth pressure-testing through the `business-brainstorm` skill.

- **Second Brain as a Service** — productized service: build an AI-ready knowledge base for a company. ~$2–5K setup, monthly retention for ongoing maintenance. Loads existing assets (call transcripts, emails, SOPs, customer language) into raw/wiki/outputs pattern. Slots into CF's existing positioning + content + agency surface. Sourced from [@coreyganim's 2026-06-17 thread](https://x.com/coreyganim/status/2067289417803538931). Tangentially: validates `second-brain` skill design.
