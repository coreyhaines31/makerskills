# Skill backlog

Skills queued for future sessions. Use `/skillify` to scaffold when ready.

---

## Shipped

- **v0.5.0** — `domain` — 11-step .com domain-hunt workflow on Laura Roeder's "availability-first" methodology. Multi-tool ensemble (Vercel CLI + whois per-TLD + Domainr API + Namecheap API + rdap.org for modern TLDs + agent-browser for USPTO trademark screening). Handles bare-word + prefix/suffix brainstorming, budget filtering, aftermarket click-throughs (HugeDomains/Afternic/Sedo/Dan), negotiation guidance, social handle checks. Ported from a personal slash command; generic for adopters.
- **v0.4.0** — `company-cfo` — anonymized team-scope sibling to `personal-cfo`. Monthly snapshots + weekly cash pulse + scenario projector. Universal methodology (transaction-sum EOM, categorization discipline, cycle-low tracking) applied to company books. Data sources wired via `toolify` (bank + payment processor + payroll + expense mgmt); scheduled via `loopify`. First-run walkthrough seeds a per-company `CLAUDE.md` from `references/company-config-template.md`.
- **v0.3.0** — `company-brain` — team-scope sibling to `second-brain`. Structured raw dirs (people / companies / meetings / sops / decisions / customer-language / recurring-questions / sales-objections), multi-author attribution, sensitivity tagging, optional auto-sync from Fathom / Gong / Granola / CRM. Operational backbone for the **Company Brain Setup** productized CF service (renamed from "Second Brain as a Service" for vocabulary consistency with the skill name).
- **v0.2.0** — The `-ify` trifecta: `skillify` (consolidated create/adapt/update), `toolify` (integration wizard), `loopify` (agent-loop setup). Vocabulary-moat family — memorable `-ify` rhythm mapping to the 3 primary Claude Code extension surfaces (skills, tools, loops). Ship notes: rule of 3 — do NOT extend the family further (no Hookify / Configify / Memorify).

---

## Skill candidates (on the shortlist)

- `weekly-review` — Friday pulse across all properties
- `intro-broker` — double opt-in intros
- `thanks-no` — polite declines for speaker/podcast/partnership asks
- `daily-startup` — morning brief (priorities + overnight + calendar + top 3)
- `swipe-save` — marketing inspiration capture (may merge with `second-brain`)
- `new-project` — Next.js + Drizzle + Neon scaffold with the user's patterns
- `gh-triage` — cross-repo issue/PR summary
- `bjj-log` — training log

## Brainstorm candidates (for `/business-brainstorm`)

Not skills — business / product ideas worth pressure-testing through the `business-brainstorm` skill.

- **Company Brain Setup** *(renamed from "Second Brain as a Service" 2026-06-30 for vocabulary consistency with the shipped `company-brain` skill)* — productized service: build a team's AI-ready knowledge base. ~$2–5K setup, monthly retention for ongoing maintenance. Loads existing assets (call transcripts, emails, SOPs, customer language) into `company-brain`'s structured raw dirs, then compiles + maintains the wiki. Slots into CF's existing positioning + content + agency surface. Sourced from [@coreyganim's 2026-06-17 thread](https://x.com/coreyganim/status/2067289417803538931). **Operational backbone: `company-brain` skill (shipped v0.3.0).**
