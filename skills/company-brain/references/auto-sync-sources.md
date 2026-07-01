# Auto-sync sources

Company brains benefit from automated capture. Manual capture works for early-stage teams; auto-sync becomes necessary as call volume + team size scale.

**Start manual.** Automate only after 4-6 weeks of manual capture proves the team is actually using the brain.

## Common sources + setup patterns

### Fathom (call notes)

- **What**: AI-generated meeting summaries + full transcripts
- **Sync via**: Zapier / n8n webhook OR Fathom's built-in export → drop into `meetings/`
- **Naming**: `meetings/YYYY-MM-DD-<company-slug>-<slug>.md`
- **Metadata**: attendees list, duration, recording URL
- **Setup**: wire the webhook via `/toolify fathom` when ready

### Gong (sales calls)

- **What**: Enterprise sales call transcripts + coaching notes
- **Sync via**: Gong API (subscription tier dependent) → daily pull
- **Naming**: same as Fathom
- **Metadata**: deal ID, opportunity stage, coaching flags
- **Setup**: `/toolify gong` + schedule daily sync via `/loopify`

### Granola (personal + team meeting notes)

- **What**: Notes-first meeting app (transcript + your own live notes)
- **Sync via**: Granola export (manual or scheduled)
- **Naming**: `meetings/YYYY-MM-DD-<slug>.md`
- **Metadata**: your live-notes tags become wiki hints during compilation

### Slack (team discussions)

- **What**: Preserving discussion threads that resolve decisions or capture context
- **Sync via**: manual per-thread OR scheduled export of specific channels
- **Naming**: `raw/slack-<channel>-<date>.md`
- **Selection**: NOT every message — only threads that resolve a decision, capture a customer quote, or document a process
- **Recommendation**: `#decisions`, `#customer-signals`, `#post-mortems` channels get auto-synced; others stay manual

### Email (Front / Missive / Superhuman)

- **What**: Customer-facing threads worth preserving beyond the inbox
- **Sync via**: forward-to-address (dedicated inbox email address the vault auto-processes)
- **Naming**: append to `people/<person-slug>.md` OR `companies/<company-slug>.md` (thread goes with the person/org, not standalone)
- **Metadata**: thread ID, sender, subject line
- **Setup**: `/toolify <email-provider>` when the team is ready

### CRM (HubSpot / Attio / Pipedrive)

- **What**: Deal state, contact info, opportunity size
- **Sync via**: API pull (nightly or on-change webhook)
- **Naming**: updates `companies/<slug>.md` and `people/<slug>.md` in place (overwrites `status`, `last_touch`, `opportunity_size` fields)
- **Metadata**: opportunity stage, close date, ARR estimate
- **Setup**: `/toolify hubspot` + nightly sync via `/loopify`

### Support tickets (Intercom / Zendesk / Front)

- **What**: Customer questions + support patterns
- **Sync via**: API pull daily
- **Naming**: append repeat-question patterns to `recurring-questions/`; standalone tickets stay in the support tool
- **Selection filter**: only tickets tagged "escalated" or repeated 3+ times

## Cadence recommendations

Wire via `/loopify` with these defaults:

| Source | Cadence | Rationale |
|---|---|---|
| Fathom / Gong / Granola | Daily at 6am (after morning calls settle overnight, before team starts work) | Fresh capture, no overlap with active calls |
| CRM sync | Nightly at 1am | Off-peak, single-source-of-truth reconciliation |
| Slack export | Weekly (Sunday) | Weekly discussion digest fits weekly review cadence |
| Support ticket patterns | Weekly (Monday) | Fresh for support-team standups |
| Email forward-to-address | On-arrival (webhook) | Real-time — sales team wants context immediately |

## Idempotency

All auto-sync jobs must be idempotent. Company-brain has a lint check for this (repeated appends creating duplicate content). Follow the loopify guidance: dedupe by source ID / transcript hash / timestamp before appending.

## When NOT to auto-sync

- **Sensitivity mismatch**: don't auto-sync `confidential` content — manual capture only, with explicit access-list assignment
- **Team hasn't earned it**: if the team isn't capturing manually, auto-sync creates a data-firehose nobody uses. Prove capture demand first.
- **Rate-limited APIs**: some sources (older CRM APIs, Slack free-tier export) rate-limit hard. Manual > broken auto-sync.
- **Compliance-restricted**: for regulated industries (healthcare, legal, finance), auto-sync of client data may violate compliance. Consult legal first.

## Recipe library (populate as team wires them)

- `references/recipes/fathom-webhook-nextjs.md` — Fathom webhook receiver in Next.js
- `references/recipes/gong-daily-sync.md` — Gong API pull loop
- `references/recipes/attio-crm-sync.md` — Attio nightly sync
- `references/recipes/slack-weekly-export.md` — Slack export → structured raw

Each recipe pairs `/toolify <source>` (initial wiring) + `/loopify` (scheduled sync).
