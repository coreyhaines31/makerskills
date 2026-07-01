# Skill backlog

Skills queued for future sessions. Use `/skillify` to scaffold when ready.

---

## Shipped

- **v0.2.0** — The `-ify` trifecta: `skillify` (consolidated create/adapt/update), `toolify` (integration wizard), `loopify` (agent-loop setup). Vocabulary-moat family — memorable `-ify` rhythm mapping to the 3 primary Claude Code extension surfaces (skills, tools, loops). Ship notes: rule of 3 — do NOT extend the family further (no Hookify / Configify / Memorify). See `~/Corey's Projects/wiki/Founding Marketing Frameworks.md` for the broader vocabulary strategy.

---

## v0.3 — `company-brain` (team-scope sibling to second-brain)

### One-sentence definition (ships with the skill everywhere)

> **Company Brain** *(n.)*: Your team's shared, AI-ready knowledge base — people, companies, meetings, SOPs, and decisions structured so Claude can answer questions on your team's behalf.

### Why a separate skill, not a mode on `second-brain`

Different audience, different file conventions, different sales motion. `second-brain` stays solo-operator (Zettelkasten / Commonplace Book lineage). `company-brain` is multi-author with structured org schema. Crucially: `company-brain` is the skill *behind* the "Second Brain as a Service" productized CF service (see brainstorm candidate below). Splitting into two skills lets the skill + the service ship aligned with one coined phrase.

### Naming rationale

Chose `company-brain` over `company-os` because:
1. Extends the "Brain" family Corey already half-owns (Second Brain → Company Brain → potentially Client Brain / Project Brain)
2. Vocabulary moat — coined, attributable, quotable. "Company OS" rides Notion's category term.
3. Distribution doesn't depend on SEO — makerskills repo is the funnel, audience hears the term from Corey directly
4. Semantic family rhyme: *"Second Brain made YOU a knowledge worker. Company Brain makes your TEAM one."*

### Schema (different from second-brain's free-form raw/wiki/outputs)

Adds structured top-level dirs to the standard compilation pattern:

- `people/` — contacts with context (CRM-lite; inspired by Garry Tan's Gbrain people entity)
- `companies/` — org profiles with last touchpoint + status
- `meetings/` — call transcripts, meeting notes (auto-loaded from Fathom/Gong/Granola when integrated)
- `sops/` — documented operational patterns
- `decisions/` — decision log (narrative form; `decide` skill archives the structured form)
- `customer-language/` — verbatim phrases from prospects/customers
- `recurring-questions/` — questions asked 3+ times → pre-answered as SOP/FAQ/sales scripts
- `sales-objections/` — library of objections + best responses
- Plus standard `raw/` `wiki/` `outputs/` for compilation pattern

(Note: most of these already exist as conventions in Corey's personal vault per his `~/Corey's Projects/CLAUDE.md` "Business / operational wiki pages worth maintaining" section. company-brain formalizes them as multi-author defaults.)

### Shared compilation logic — extract to references/

Don't copy-paste between `second-brain` and `company-brain`. Extract the shared compilation rules (raw → wiki → outputs flow, INDEX.md maintenance, Connections section requirements, source citations) into a shared reference doc that both skills read. Same pattern other makerskills use for shared style guides.

### Ordering (after v0.2 trifecta ships)

1. Sketch the schema (top-level dirs, multi-author conventions, sensitivity tagging if any)
2. Extract shared compilation pattern from `second-brain` into `references/compilation-pattern.md`
3. Build `company-brain` SKILL.md against the shared reference
4. Wire optional auto-sync sources (Fathom/Gong/Granola transcripts, Front/Slack emails, CRM data)
5. Add the 1-sentence definition to README + skill description verbatim
6. Tag `v0.3.0`
7. Update the "Second Brain as a Service" brainstorm note to point at this skill as the operational backbone

### Constraints

- **Skill name + service name should match.** If the service stays "Second Brain as a Service," there's a mismatch with the `company-brain` skill name. Rename one to align — either rename the service to "Company Brain Setup" or rename the skill. Recommended: rename the service so the vocabulary is consistent.
- **Don't bundle with v0.2.** Trifecta ships separately. `company-brain` is its own coordinated release.

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

- **Second Brain as a Service** *(rename pending — see company-brain note above)* — productized service: build an AI-ready knowledge base for a company. ~$2–5K setup, monthly retention for ongoing maintenance. Loads existing assets (call transcripts, emails, SOPs, customer language) into raw/wiki/outputs pattern. Slots into CF's existing positioning + content + agency surface. Sourced from [@coreyganim's 2026-06-17 thread](https://x.com/coreyganim/status/2067289417803538931). **Operational backbone: `company-brain` skill (v0.3 — see above).** Rename candidate: "Company Brain Setup" to align vocabulary with the skill name.
