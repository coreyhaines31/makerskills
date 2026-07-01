# Scenario projector — reference implementation

An interactive forecast that projects EOM cash forward N months under adjustable assumptions (revenue growth, expense scenarios, hiring plans, distribution changes). Updated monthly during Phase 4 of the standing workflow.

Most CFO workflows benefit from having a projector — leadership decisions (hire, distribute, cut) get made against projected scenarios, not just the current month's snapshot.

## Structure

Standard chart layout (adopt as-is or adapt to your team's preferences):

- **HISTORICAL** — trailing 3 closed months. Provides context before TODAY.
- **TODAY** — today's actual cash balance, calendar-positioned within the current month.
- **Mo 1** — current calendar month EOM (partial — only remaining-month activity, dominated by the upcoming payment-processor payout).
- **Mo 2–7** — next 6 full calendar month EOMs. Scenario settings apply from Mo 2 onward.

Rationale: 3 months of history is enough to see trend + spot anomalies; more than 3 crowds the chart. 6-7 months forward is the right forecast horizon for most operational decisions — long enough to catch cliffs, short enough to be reliable.

## Per-month computation

For each future month:

```
starting + revenue − expenses = profit ± → ending
```

Where:
- `starting` for Mo 1 = TODAY's actual cash (Mo 1's projection starts from today, not from the prior closed-month EOM)
- `starting` for Mo 2+ = prior month's EOM (chained forward)
- `revenue` = `baselineMrr` * (growth multiplier if applicable) + one-times
- `expenses` = sum of per-category baselines under the active scenario

## Intramonth cycle low

The EOM cash is often the *high* of the month (payment processor payout just landed). Cash floor checks apply to the LOW, not the HIGH.

Formulas by payout cadence (see `eom-cash-methodology.md` for the full derivation):

- **Monthly payouts** (legacy): `low ≈ EOM − month_revenue` (whole month's inflow lands at EOM, trough is everything except that lump)
- **Weekly payouts**: `low ≈ EOM − (month_revenue / 4)` (one week of inflow is lumpy, rest smoothed)
- **Daily payouts** (rare): `low ≈ EOM − (month_revenue / 30)` (negligible dip)

Weekly payouts smooth the cycle dramatically. If your processor supports it (Stripe does), switching from monthly to weekly is one of the highest-leverage cash-management moves available.

**Mo 1 (current month, partial)** uses a different formula since most outflows may already have fired MTD:

```
mo1_low = starting_cash − mo1_outflow
```

Where `mo1_outflow` is calibrated by run-date:
- **Late-month run** (25th+): `mo1_outflow ≈ small drip` — today's cash IS approximately the low
- **Early-month run** (1st-3rd): `mo1_outflow ≈ full month's expenses` — significant drop coming
- **Mid-month run**: `mo1_outflow ≈ remaining outflows` — pro-rata estimate

## Chart implementation options

Three common approaches:

### Option A: Static HTML with hardcoded arrays

Simplest. Serve via a lightweight `serve.sh` script (`python3 -m http.server 8765` or similar). Each monthly run edits the `HISTORICAL` array + `startingCash` HTML input default. Scenario adjustments happen via HTML input fields that trigger JS recomputation.

Pros: no build step, no framework, no dependencies. Anyone can open the file and tweak numbers in the browser.
Cons: no version control on scenario state (you're editing HTML), can drift.

### Option B: React app (Next.js / Vite)

More sophisticated. Scenario state in URL params, share links for specific what-if analyses.

Pros: version-controllable scenarios, shareable URLs, easier to add features.
Cons: build step + deps.

### Option C: Google Sheet

For teams that live in spreadsheets already. Sheets → CSV export → chart in the report.

Pros: familiar tool, easy for non-technical leadership to interact with.
Cons: sync friction, chart quality is lower than custom HTML/React.

Most companies land on Option A first + graduate to Option B once the projector becomes a decision-making tool used weekly.

## Monthly projector updates (Phase 4 checklist)

1. **Append the just-closed month** to `HISTORICAL` with ALL category fields: `label`, `cash`, `revenue`, `distributions`, `team`, `software`, `reimbursements`, `benefits`, `other`, `total_out`, `net`. Use `"MMM 'YY EOM"` label format (e.g., `"Jun '26 EOM"`).
2. **Drop the oldest** so `HISTORICAL` stays at 3 entries.
3. **Update `startingCash`** default to today's actual bank balance (cash accounts only, excluding credit card debt).
4. **Update `mo1Inflow`** based on run date:
   - **Late-month run**: current processor balance + pending (upcoming EOM payout). Divide by 100 if the API returns cents.
   - **Early-month run**: estimate based on full month's expected MRR + alt revenue.
   - **Mid-month run**: what's in processor now + pro-rata for remaining days.
5. **Update `mo1Outflow`** based on run date (see intramonth cycle low above).
6. **Update `OPEX_DEFAULTS`** AND matching HTML `value=` attributes for any category that materially shifted from the trailing baseline.
7. **Update `baselineMrr`** — current MRR NET of processing fees (typically ~3%).
8. **Verify presets still make sense**. If comp structure or hiring plans changed, the scenario descriptions and `apply()` handlers may need updating.

## Scenarios worth having

Common presets to seed the projector with:

- **Status quo** — trailing 3-month averages carry forward. Baseline.
- **Aggressive hire** — add a $X/mo team cost starting Mo N. See what runway looks like.
- **Distribution cut** — reduce partner distributions by X% for M months.
- **Revenue optimism** — MRR grows Y% m/m.
- **Revenue pessimism** — Z% churn spike concentrated in Mo 2-3.
- **Big client win** — one-time $X inflow in Mo N.
- **Big client loss** — MRR drops $X starting Mo N.

Every preset should call `resetBaseline()` (or equivalent) first to clear prior state cleanly.

## Tooltip framing per EOM point

Use the explicit equation format, not raw "net":

```
starting $X + revenue $Y − expenses $Z = profit ±$P → ending $E
```

For historical months (already happened), drop `starting` (just `revenue − expenses = profit → ending`) since we're showing what landed in the bank that month, not chaining from a prior position.

For future months, show the full equation — including which month's ending balance feeds this month's starting.

## Rebuilding after data changes

When a monthly close changes (e.g., a late-arriving corrective transaction), the whole HISTORICAL chain needs updating downstream. Rerun Phase 3 (transaction-sum EOM) for the affected months, update HISTORICAL, re-verify month-over-month reconciliation.

**Don't patch a single EOM value manually.** Always rerun the transaction sum. Manual patches introduce reconciliation gaps that will silently propagate.
