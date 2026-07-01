---
name: company-brain
description: Your team's shared, AI-ready knowledge base — people, companies, meetings, SOPs, and decisions structured so Claude can answer questions on your team's behalf. Team-scope sibling to second-brain (which is personal-scope). Six modes — capture (drop something into the right structured dir), compile (process into wiki pages, update INDEX.md), query (answer from the corpus, save to outputs/), lint (orphans / stale / contradictions / gaps), connect (suggest new wikilinks), search (quick lookup). Structured raw dirs (people/, companies/, meetings/, sops/, decisions/, customer-language/, recurring-questions/, sales-objections/) instead of second-brain's flat type-prefixed raw/. Multi-author aware — every capture stamps author + timestamp. Optional auto-sync from Fathom/Gong/Granola call transcripts, Slack/email exports, CRM. Defaults to a vault at ${COMPANY_BRAIN_VAULT:-$HOME/Documents/CompanyBrain}/. Triggers on "/company-brain," "/cb," "capture this into the team brain," "log this meeting," "add this person to the team brain," "save this SOP," "compile the company wiki," "query the team brain," "what does the team know about X," "lint the company brain," "who's the internal expert on X."
metadata:
  version: 0.1.0
---

# /company-brain — Team-shared AI-ready knowledge base

**Company Brain** *(n.)*: Your team's shared, AI-ready knowledge base — people, companies, meetings, SOPs, and decisions structured so Claude can answer questions on your team's behalf.

Team-scope sibling to `second-brain` (personal-scope). Same core compile → wiki → outputs pattern; different raw schema optimized for multi-author, sales-heavy, ops-heavy team use.

Also the operational backbone for the **Company Brain Setup** productized service (CF offering — was previously called "Second Brain as a Service"; renamed to match the skill).

## Mental model

Three layers, same as second-brain — but the raw/ layer is *structured*, not flat:

```
raw/          →  wiki/         →  outputs/
(structured      (compiled        (generated
 by category)     interlinked)     artifacts)
```

**Structured raw/ dirs** (each is its own top-level folder in the vault):

| Dir | What lives here |
|---|---|
| `people/` | Contacts with context — CRM-lite. One markdown file per person. |
| `companies/` | Org profiles — last touchpoint, opportunity size, status. One file per company. |
| `meetings/` | Call/meeting transcripts + notes. Naming: `YYYY-MM-DD-<company-or-topic>.md`. Auto-sync source. |
| `sops/` | Standard operating procedures. Named: `<team>-<process>.md` (e.g., `sales-outbound-cadence.md`). |
| `decisions/` | Decision records (narrative form; `decide` skill's structured form is different). |
| `customer-language/` | Verbatim phrases from prospects/customers/users. Fuels copy, headlines, objections. |
| `recurring-questions/` | Questions asked 3+ times across calls. Each becomes a pre-answered SOP/FAQ/script. |
| `sales-objections/` | Library of objections + best responses. Assembled into sales scripts. |
| `raw/` | Legacy / uncategorized captures (fallback bucket, minimize use). |

`wiki/`, `outputs/`, and `INDEX.md` work the same as second-brain.

**Reserved dirs** (never modified by company-brain): `Projects/`, `Team/`, `Templates/`, `Drafts/`.

## Multi-author discipline

Every capture stamps:

```markdown
source: <URL / call / email / manual entry>
author: <who added this — email or handle>
captured: YYYY-MM-DD
```

Wiki pages track cumulative contributions in the `## Sources` section (per source file, per author). No overwriting — always append + attribute.

**Sensitivity tagging** (optional but recommended):

```markdown
sensitivity: internal        # any team member can read
sensitivity: leadership      # exec team only
sensitivity: confidential    # named list only (list access in the file)
```

Default: `internal`. Query mode respects sensitivity — refuses to include `confidential` content unless the invoker is on the access list.

## Step 1 — Load vault config + schema

1. Read `references/vault-config.md` for the vault path (default: `${COMPANY_BRAIN_VAULT:-$HOME/Documents/CompanyBrain}/`)
2. Read `<vault>/CLAUDE.md` for the authoritative team schema. If present, trust it over `references/schema.md` — the team's vault is the source of truth.
3. If no `<vault>/CLAUDE.md`, fall back to `references/schema.md` — the team schema starter kit.

## Step 2 — Parse mode

| Invocation | Mode |
|---|---|
| `/cb capture` / `/company-brain capture` / "capture this into the team brain" | **capture** |
| `/cb compile` / "compile the company wiki" | **compile** |
| `/cb query <q>` / "what does the team know about X" | **query** |
| `/cb lint` / "lint the company brain" | **lint** |
| `/cb connect` / "find cross-team connections" | **connect** |
| `/cb search <term>` / "search the company brain" | **search** |

## Step 3 — Run the mode

### capture

**Same intake mechanics as second-brain, but the routing is different — pick the structured dir based on content type.**

1. **Detect content type + route to the right dir**:
   - Call/meeting transcript → `meetings/YYYY-MM-DD-<slug>.md`
   - Person's LinkedIn / bio / contact context → `people/<name-slug>.md`
   - Company profile / prospect / client → `companies/<company-slug>.md`
   - Documented process / how-we-do-X → `sops/<team>-<process>.md`
   - Decision made by leadership / team → `decisions/YYYY-MM-DD-<decision-slug>.md`
   - Verbatim customer quote → `customer-language/<theme-slug>.md` (append to existing themed file if one exists)
   - Question asked in a call → `recurring-questions/<question-slug>.md` (append counter if repeat)
   - Sales objection heard → `sales-objections/<objection-slug>.md` (append variant if repeat)
   - If ambiguous, ask.

2. **Add multi-author metadata** (top of file):
   ```markdown
   source: <URL / call with X on YYYY-MM-DD / email from Y / etc.>
   author: <who captured this>
   captured: YYYY-MM-DD
   sensitivity: internal  # or leadership / confidential
   ```

3. **Save + report** file path + one-line summary.

Don't compile into the wiki here — capture is fast intake.

### compile

Same core pattern as `second-brain`'s compile mode — process unprocessed structured-raw files into wiki pages, update INDEX.md, add Sources sections.

**Differences from second-brain:**

- **Multi-author attribution**: Sources section includes author, not just filename
  ```markdown
  ## Sources
  - `people/jane-doe.md` (added by @alex, 2026-06-30) — CTO of Acme, evaluated us Q2
  ```
- **Cross-category compilation**: a wiki page on "Acme Corp deal" might pull from `companies/acme.md`, `meetings/2026-06-15-acme-discovery.md`, `sales-objections/acme-pricing.md`, and `people/jane-doe.md` — all into one wiki page.
- **Sensitivity inheritance**: wiki pages inherit the highest sensitivity of any source. If any source is `confidential`, the wiki page is `confidential`.
- **INDEX.md categories** for teams: `Sales`, `Customers`, `Ops`, `Product`, `Team & People`, `Decisions`, `Playbooks`. Extend as needed.

Everything else (one-page-per-concept, `[[wikilinks]]`, Connections mandatory, quality > quantity) is identical.

### query

Same as second-brain query, plus:

- **Sensitivity check first**: identify the invoker; refuse to include content above their sensitivity level.
- **Author-aware answers**: when citing, include who contributed the info: *"Per [[Acme Deal]] (source: `meetings/2026-06-15-acme-discovery.md` by @alex)..."*
- **Route external gaps to `deep-research`**, same as second-brain.

Save to `outputs/<YYYY-MM-DD>-<question-slug>.md` with the answer + wiki pages consulted + sensitivity level of the output.

### lint

Same six checks as second-brain PLUS:

7. **Stale people/companies** — `person-` or `companies/` file with no update in >6 months for active accounts
8. **Recurring-questions above threshold** — questions asked 5+ times without a wiki page or SOP
9. **Objections without responses** — `sales-objections/` files with no linked response in `sops/` or `wiki/`
10. **SOP freshness** — SOPs not touched in >12 months (may be stale as the business evolves)
11. **Author load imbalance** — one contributor doing >80% of captures (usually signals the vault is one-person-dependent — bad for team continuity)

### connect

Same as second-brain plus **cross-category link suggestions** — e.g., `sales-objections/pricing-too-high.md` should link to `customer-language/willingness-to-pay.md` and `sops/discovery-call-cadence.md` if they exist.

### search

Same. Grep across all structured-raw dirs + `wiki/`.

## Optional: auto-sync sources

Team vaults benefit from automated capture. See `references/auto-sync-sources.md` for the setup patterns:

| Source | What it captures | Setup |
|---|---|---|
| **Fathom / Gong / Granola** | Call/meeting transcripts | Webhook → append to `meetings/` |
| **Slack export** | Team discussions worth preserving | Manual or scheduled export → `raw/slack-<channel>-<date>.md` |
| **Email (Front / Missive / Superhuman)** | Customer-facing threads worth preserving | Forward-to-address → append to `people/` or `companies/` |
| **CRM (HubSpot / Attio / Pipedrive)** | Deal state, contact info | Periodic sync → `companies/` + `people/` |

Auto-sync is optional — most teams start with manual capture and add automation as the vault matures. Pair with `loopify` to schedule periodic sync jobs.

## Composes with

- **`second-brain`** — sibling. Use `second-brain` for your personal wiki; `company-brain` for the team's. A person can maintain both simultaneously with separate vault paths.
- **`skillify`** — use to author new skills that read from the company brain (e.g., a `weekly-team-brief` skill that queries `company-brain` every Monday).
- **`loopify`** — schedule auto-sync jobs (Fathom pull daily, Slack export weekly, INDEX lint monthly).
- **`toolify`** — wire up integrations that feed the company brain (Fathom webhook receiver, Attio API, etc.).
- **`deep-research`** — when `query` finds gaps, route external. Save deep-research results into `raw/` for future compilation.
- **`decide`** — `decisions/` folder complements `decide`'s structured archive. `decide` records the *evaluation*; `decisions/` records the *narrative + outcome + review notes*.
- **`pm`** — team task management sits in `Projects/` (reserved from company-brain). `pm` owns Projects/; company-brain reads it for context but doesn't modify.
- **`jab-hook`** — `customer-language/` fuels social copy that resonates with actual prospect language.
- **`cf-blog`** (in `cf-skills`) — pulls from `customer-language/`, `recurring-questions/`, and `sops/` for authoritative blog drafts.

## Sibling implementations (reference)

Same lineage as `second-brain`:

- **[Gbrain](https://github.com/garrytan/gbrain)** — Garry Tan's team-scale brain (146K pages, 24K people entities). Postgres/PGLite backed with graph traversal + scheduled maintenance. When a team's company-brain outgrows markdown-only, Gbrain is the upgrade path.
- **[Hermes' `llm-wiki`](https://hermes.team)** — reference for the 3-folder pattern.
- **Notion AI / Glean / Mem** — commercial "Company OS" tools. Company-brain is the Claude-native, markdown-first alternative — cheaper, more portable, better for teams that already live in Obsidian / Git-backed docs.

## Notes on quality

- **Structured raw > flat raw at team scale.** Second-brain's type-prefix works for one person; teams need dedicated dirs for people/companies/meetings/etc. so multi-author search stays fast.
- **Multi-author attribution is non-negotiable.** Every file stamps `author:` and `captured:`. Wiki pages cite by source + author.
- **Sensitivity is respected end-to-end.** Query mode refuses to include content above the invoker's level. Wiki pages inherit the highest sensitivity of any source.
- **Never delete raw files.** Same rule as second-brain — the structured dirs are the source of truth.
- **Never modify** `Projects/`, `Team/`, `Templates/`, `Drafts/` during company-brain operations.
- **Auto-sync is optional.** Start manual; automate as the vault matures. Don't burn cycles on Fathom webhooks before the team is capturing meetings regularly by hand.
- **One person shouldn't be the whole vault.** If lint flags author-load imbalance >80%, the team is one bus-factor away from losing the brain. Broaden contribution.
