---
name: company-cfo
description: Monthly CFO workflow for a company or agency — pull raw data from bank + payment processor + payroll + expense management, categorize and reconcile, compute end-of-month cash via transaction-sum method, update a scenario projector for forward forecasting, write the monthly snapshot report, surface decisions to leadership. Modes — monthly (default; the standing report), weekly (thin cash pulse), scenario (ad-hoc modeling in the projector), pickup (resume where the prior run left off). Anonymized team-scope sibling to personal-cfo (which handles personal household finances). Composes with company-brain (report gets stored + wiki-indexed there), toolify (wire company-specific data sources), loopify (schedule the monthly + weekly runs). Triggers on "/company-cfo," "/cfo," "monthly cash report," "do the CFO snapshot," "CFO monthly," "let's run CFO," "cash projection," "runway forecast," "monthly financials," "cash pulse."
metadata:
  version: 0.1.0
---

# /company-cfo — Monthly company CFO workflow

The standing analysis leadership uses to make distribution / cuts / hiring / runway decisions. Primary cadence is **monthly** (run on the 1st for the closed prior month). Weekly and scenario modes cover the in-between.

Anonymized team-scope sibling to `personal-cfo` (households). Same discipline (transaction-sum EOM, categorization traps, scenario modeling) applied to company books.

## Step 0 — Load company config + prior run

Before starting work, read these in order:

1. **`${COMPANY_CFO_ROOT:-$HOME/code/company-cfo}/CLAUDE.md`** — your company's specific methodology, data source map, categorization rules, distribution mechanics. **This is the source of truth for HOW your company computes things.** Don't invent your own methodology.
2. **The most recent report** in `${COMPANY_CFO_ROOT}/reports/monthly/` — last month's snapshot. Tells you what leadership decided + what was open.
3. **The most recent `*-followup.md`** in that folder (if one exists) — supplementary decisions, scenario analysis.
4. **Any relevant memory notes** in `~/.claude/memory/` — running context: known anomalies, leadership constraints, current churn state.
5. **`git log --oneline -10`** in `${COMPANY_CFO_ROOT}` — what's shipped since the last run.

If the `COMPANY_CFO_ROOT` dir doesn't exist yet: first-run walkthrough asks the user to `mkdir` it, seed a `CLAUDE.md` from `references/company-config-template.md`, and set the env var.

## Step 1 — Parse mode

| Invocation | Mode | Cadence |
|---|---|---|
| `/company-cfo monthly` (default) | **monthly** | Once per month on the 1st for the closed prior month |
| `/company-cfo weekly` | **weekly** | Thin cash pulse — current cash + next 2 weeks of expected flows |
| `/company-cfo scenario <question>` | **scenario** | Ad-hoc modeling in the projector |
| `/company-cfo pickup` | **pickup** | Resume where the prior run left off (checks git log + last report + open items) |

Below sections walk through **monthly** in detail. Weekly + scenario are summarized at the end.

---

## Monthly workflow

Ask the user: **Which month are we reporting on?** (Default: prior calendar month.)

Then walk through these phases. Pause and confirm before moving to the next.

### Phase 1 — Pull raw data

For the target month, pull raw data from each source. Standard source categories (each company's actual tools live in their `CLAUDE.md`):

| Source category | What it gives | Common tools |
|---|---|---|
| **Bank / cash accounts** | Cash truth, internal vs external transfers, distribution recipients | Mercury CLI, Plaid, direct bank export |
| **Payment processor** | Revenue, subscriptions, churn, payout timing | Stripe API, Paddle, LemonSqueezy |
| **Payroll / contractors** | W-2 payroll, contractor pay | Plane, Deel, Gusto, Rippling |
| **Expense management** | Reimbursements, corporate cards | Ramp, Brex, Divvy |
| **Alternative revenue** | Non-primary billing sources | Direct invoice tools, alternative payment platforms |

Save all pulls to `${COMPANY_CFO_ROOT}/data/YYYY-MM/<source>-*.json[l]` (gitignored — raw data doesn't get committed).

Also pull the **current cash balance** from the bank source for the "today" starting-cash figure.

**If a source isn't wired yet:** use `/toolify <source>` to wire it up before running the CFO workflow. First-time integration is a one-time cost.

### Phase 2 — Categorize and reconcile

Bucket all cash-account outflows into the categories your company uses. See `references/categorization.md` for a starter category set and the discipline of maintaining categorization.

**Universal traps to check** (see `references/traps.md` for full list):

- **Cash-vs-credit double-count** — if the bank shows a "credit card autopay" outflow AND the credit card account shows individual charges, don't count both. Filter to cash accounts only OR treat the CC as a debt account.
- **Internal transfers** — Checking ↔ Savings transfers net to zero. Exclude them (usually via a `kind=internalTransfer` filter or account-pair match).
- **Currency mismatches** — contractor payment tools often return `destination_amount` in the worker's payout currency. Always use `source_amount` (or equivalent) for USD/base-currency cost analysis.
- **Distribution counting** — if leadership has N partners who should get a monthly distribution, verify N distributions exist. If N-1, flag the missing partner — often one is deferring their draw to balance cash.

Cross-checks before writing the report:
- Total payroll debits in bank ≈ payroll-tool API total + fees (within a small residual for held deductions)
- Payment processor payouts arriving in the month ≈ bank inflows from that processor (within timing lag)
- Expense-management outflows in bank ≈ approved expenses in expense-mgmt tool (with cash-basis lag)

### Phase 3 — Compute EOM cash (the transaction-sum method)

**Use transaction sums, not the walkback-from-current-balance method.** Walkback has bitten CFO workflows repeatedly — a bank API balance snapshot at pull time can be off by tens of thousands, and that error propagates into every historical EOM value.

Correct method (see `references/eom-cash-methodology.md` for the full recipe):

```python
# 1. Pull ALL transactions for each cash account (Checking + Savings + any other cash-holding):
#    <bank-tool> transactions list --account-id <id> --format jsonl --max-items 100000
# 2. Sum the amount field across all transactions in each account.
# 3. The sum should equal that account's CURRENT available_balance exactly.
#    (Sanity check — if not, missing data or a pre-history baseline deposit exists.)
# 4. For any past date T: balance_at_T = sum of all transactions posted on or before T
#    (plus any pre-history baseline, which should be ~$0 if the sanity check passes).
```

Cross-check EOM: last month's EOM + this month's net cash change should equal this month's EOM, to the dollar.

If transaction sums don't reconcile with current balance, **do not proceed** with walkback as fallback. Investigate the gap first — missing pulls (timeout, paging), an unknown account, or a legitimate pre-history baseline.

### Phase 4 — Update the scenario projector

Most CFO workflows benefit from a scenario projector — an interactive forecast that projects EOM cash forward N months under adjustable assumptions (revenue growth, expense scenarios, hiring plans, distribution changes).

Common structure (see `references/scenario-projector.md` for the reference implementation):

- **HISTORICAL** (trailing 3 closed months) — provides context before TODAY
- **TODAY** — actual current cash balance (calendar-positioned within current month)
- **Mo 1** — current calendar month EOM (partial — remaining-month activity)
- **Mo 2-7** — next 6 full calendar month EOMs (scenario settings apply from here)

Each month: `starting + revenue − expenses = profit → ending`

**Intramonth cycle low** (for weekly cash pulse relevance): most CFO systems care about the *low* point of the month (when you might hit a cash floor), not just the high (EOM). Formula depends on payout cadence — see `references/scenario-projector.md`.

**Update the projector each monthly run:**
1. Append the just-closed month to HISTORICAL with all category fields; drop the oldest.
2. Update `startingCash` to today's actual bank balance.
3. Update expense baselines for any category that materially shifted.
4. Update `baselineMrr` (net of processing fees).
5. Verify presets still make sense (scenarios may need updating if comp structure or hiring plans changed).

### Phase 5 — Write the snapshot report

Create `${COMPANY_CFO_ROOT}/reports/monthly/YYYY-MM.md` following the template in `references/report-template.md`. Sections (adapt as needed):

1. **TL;DR** — headline + status table (net cash, ending balance, current MRR, trailing-N-month, recommendation)
2. **Cash In** — by source (payment processor, alt revenue, one-times)
3. **Cash Out** — by category (matches the projector's category structure)
4. **Payroll breakdown** — verified contractor + W-2 split
5. **Distributions** — who got paid, who didn't (flag anomalies)
6. **Revenue metrics** — active subs, MRR delta, recent cancels with $ and customer
7. **Forward projection** — 1-3 scenarios from the projector (link the projector state)
8. **Recommended actions** — concrete for leadership to decide on
9. **Open items** — questions to resolve next month

Write the why-paragraph in plain English: what happened and why. Reference the previous month if there's continuity ("Vendor X churn from last month finished hitting June payouts").

### Phase 6 — Update memory

Update `~/.claude/memory/company_cfo_<company-slug>.md` (or wherever your memory system lives) if any of:

- Distribution/comp structure changed
- Active sub count or MRR shifted materially
- New revenue stream (new billing platform)
- New partner / contractor decision
- New cash floor or distribution constraint

Don't bloat the note. Replace stale facts; don't append indefinitely.

### Phase 7 — Review and ship

Follow your company's git workflow:

```bash
cd ${COMPANY_CFO_ROOT}
git checkout -b feature/YYYY-MM-snapshot
git add -A
git commit -m "YYYY-MM monthly snapshot"
git push -u origin feature/YYYY-MM-snapshot
gh pr create --base main --title "YYYY-MM monthly snapshot"
```

Before merging: run a code review (if applicable) or manually review the diff. Then merge + delete branch.

---

## Weekly cash pulse mode

Thin — designed to fit into a 15-minute weekly sync.

1. Pull current cash balance (bank API `accounts list`)
2. Pull last 7 days of transactions + next 7 days of scheduled outflows (payroll, known bills)
3. Compute: current cash, next-payroll date + amount, next-Stripe-payout date + amount
4. Flag if cash < next 2 weeks of outflows (below cash floor)
5. One-line status: `Cash $X | Next payroll $Y on <date> | Next inflow $Z on <date> | Floor status: OK|WATCH|BREACH`

Save to `${COMPANY_CFO_ROOT}/reports/weekly/YYYY-WW.md`.

Pair with `/loopify` to schedule the weekly run (typically Monday 9am).

## Scenario mode

Ad-hoc — for "what if we hire a $150K/yr engineer in September" or "what if churn ticks up 2%".

Open the scenario projector, adjust the relevant knobs, screenshot or export the resulting cash projection. Save the analysis to `${COMPANY_CFO_ROOT}/reports/scenarios/YYYY-MM-DD-<question-slug>.md`.

If the scenario decision is material (new hire, distribution change, big expense), also run `/decide` to formalize.

## Pickup mode

Resume from the prior run. Surface:

1. Most recent monthly report (`ls -t ${COMPANY_CFO_ROOT}/reports/monthly/*.md | head -1`)
2. Most recent weekly pulse
3. Latest `git log` on `${COMPANY_CFO_ROOT}` (what's shipped since last snapshot)
4. Memory note for current narrative
5. Open items from the last report's §9

**Don't assume continuity from training data.** Always check the reports + memory + git log first.

## Composes with

- **`personal-cfo`** — sibling. Personal-cfo handles household finances (house math, monthly cash flow, big purchases). Same discipline (transaction-sum method, scenario modeling) applied to different scope.
- **`company-brain`** — the CFO reports get stored + wiki-indexed there. `outputs/` in the company brain accumulates monthly reports; wiki pages compile trends across months.
- **`toolify`** — wire company-specific data sources (Mercury API, Stripe, Plane, Ramp, or equivalents). First-run integration setup.
- **`loopify`** — schedule the monthly run (1st of month) + weekly cash pulse (Monday 9am).
- **`decide`** — for material decisions surfaced by the report (distribution changes, hiring, cash floor breach response). Formalize with the 37signals framework.
- **`deep-research`** — for benchmark questions ("what's a typical SaaS marketing budget as % of ARR?") that inform scenario inputs.

## Notes on quality

- **Never invent methodology.** Every company computes cash differently — trust the company's `CLAUDE.md` in `${COMPANY_CFO_ROOT}`. If it's not documented, ask; don't guess.
- **Transaction-sum method is non-negotiable.** Walkback from a balance snapshot has burned CFO workflows repeatedly. Use raw transaction sums, verify against current balance.
- **Categorization discipline matters more than accuracy.** Same categories every month = trend-readable. Changing categories mid-year = trends become noise.
- **Baseline expenses to actuals, not to "safe" estimates.** A software line modeled at $8K when actuals run $12K creates optimistic projections that break the model.
- **Revenue is net of processing fees, not gross.** ~3% Stripe/similar processor fees materially change monthly cash inflow.
- **The intramonth cycle low matters more than EOM.** With monthly payout cadences, cash dips deep mid-month. Cash floor applies to the LOW, not the EOM HIGH.
- **Weekly payouts smooth the cycle dramatically** — if your payment processor supports it, switching from monthly to weekly payouts is one of the highest-leverage cash-management moves available. See `references/eom-cash-methodology.md`.
- **When numbers don't reconcile, stop.** Don't ship a report with unexplained gaps. Investigate first — a $42K reconciliation gap once propagated silently for weeks before being caught.

## When NOT to use this skill

- **Ad-hoc single-number lookups** ("what's our current cash?") — just query the bank source directly, don't run the full workflow.
- **Tax / accounting questions** — out of scope; refer to your CPA.
- **Personal finance** — use `personal-cfo` instead.
- **Investor pitch financials** — different discipline (multi-year projections, unit economics deep dives). This skill covers operational CFO cadence, not fundraising narrative.
