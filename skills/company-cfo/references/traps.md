# CFO workflow traps

Universal categorization + reconciliation traps that recur across CFO workflows. Check each every monthly run.

## Cash-vs-credit double-count

If your bank shows a monthly "credit card autopay" outflow AND the credit card account shows individual charges, counting both double-counts every SaaS bill.

**Fix**: Filter to cash accounts only when computing outflows. Treat the credit card as a debt account (individual charges are visible on the CC statement, but the CC autopay from checking is what actually leaves cash).

Alternative: treat the CC individual charges as your source of truth and exclude the autopay from cash outflow analysis. Both work — pick one and lock it.

## Internal transfers

Transfers between your own accounts (Checking ↔ Savings, brokerage ↔ checking, subsidiary ↔ parent) net to zero within the company but appear as separate transactions.

**Fix**: Filter out `kind=internalTransfer` (or equivalent) OR match by account-pair-and-timestamp OR sum only OUTGOING transactions to accounts you don't own.

Common gotcha: sweep accounts (auto-move idle cash to savings for yield) generate internal transfers daily. Include them in the exclusion filter.

## Currency mismatches

Contractor payment tools often return `destination_amount` in the worker's payout currency (JPY, EUR, GBP, INR, etc.) — not USD.

**Fix**: Always use `source_amount` (or equivalent — different tools name it differently) for base-currency cost analysis.

Common tools + right field:
- **Plane**: `funding.amount` (USD funding) vs `destination_amount` (worker's local currency) → use `funding.amount`
- **Deel**: `source_amount` vs `destination_amount` → use `source_amount`
- **Gusto** (US-only): USD everywhere, no ambiguity
- **Wise Business**: check the API docs — the naming varies by endpoint

## Distribution count mismatch

If N partners should get a monthly distribution and only N-1 appear in the bank data, flag the missing partner.

**Common causes**:
- One partner is deferring their draw to preserve cash
- One partner's ACH bounced or was rejected (rare, but worth catching)
- Distribution was routed to a different account than usual (e.g., moving from personal checking to an LLC-owned brokerage)
- The payroll platform processed the distribution as a W-2 payment instead of an owner draw (common when there's a comp-structure change mid-month)

**Fix**: Ask leadership to confirm — don't guess. The report should note which N-1 distributions occurred + flag the missing one.

## Held deductions residual

Total payroll debits in the bank rarely EXACTLY match payroll-tool API totals — there's usually a small residual ($100-$2K) from held deductions:
- Retirement contributions held for the 401k custodian
- Benefits held for insurance carriers
- Tax withholdings held for quarterly payment
- Garnishments (rare but real)
- Corrections + adjustments applied later

**Fix**: Allow ~$1K-$2K residual as normal. Flag anything bigger — that's usually a missed transaction or a categorization bug.

## Cash-basis vs accrual lag (expense management)

Expense management tools (Ramp / Brex / Divvy) show WHEN expenses were submitted / approved. Bank shows WHEN reimbursement was PAID OUT.

These can lag 1-4 weeks. Reconciliation between expense-mgmt total and bank total will always show a delta.

**Fix**: Use **bank** as the source of truth for cash-basis reporting (matches what actually left the account). Use expense-mgmt for spend-by-category reporting (matches spend by category). Note the two in the report — they're different lenses on different questions.

## Payment processor lag

Payment processors (Stripe, etc.) charge customers on day X but payout to your bank on day X+2 or later. Monthly Stripe payout cadence lands the whole month's revenue at EOM.

**Fix**: For MRR + revenue reporting, use processor API (charges) as source of truth. For cash-in-bank reporting, use bank inflows. They will not match — that's expected — but they should be reconcilable via known payout schedules.

## Missing revenue sources (invisible in primary processor)

If you bill through multiple platforms (Stripe + Paddle, Stripe + direct invoicing, Stripe + a marketplace's payment intermediary), the primary processor's MRR is an undercount.

**Fix**: Add all revenue sources to your `CLAUDE.md` methodology. Query each independently. Reconcile against bank inflows.

Common example: SaaS with a primary Stripe subscription AND a "Mallow-style" secondary invoicing platform. Stripe MRR shows $80K; total revenue from all sources is $95K. Reporting Stripe MRR only understates cash generation.

## Software baseline drift

The monthly SaaS bill (dominated by autopay from corporate cards) shifts as tools are added / removed. Model the current baseline, not last year's — a stale baseline creates optimistic cash projections.

**Fix**: Every quarter, review the actual last-3-month software autopay average. Update `baselineMrr` and `OPEX_DEFAULTS` in the projector to match. Don't project with a lower software baseline "to be conservative" — the projection is inaccurate.

## Categorization drift mid-year

Changing how a category is defined mid-year makes trends unreadable. If June's "software" category includes AI subscriptions but May's didn't, month-over-month software growth is noise.

**Fix**: Lock categories at the start of the fiscal year. If a new expense type appears that doesn't fit, add a new category at year-end + document in the memory note. See `categorization.md`.

## Partner comp-structure changes

If a partner's W-2 salary decreases by $X and their monthly distribution increases by $X, total comp is unchanged. But the "team" (payroll) line drops and the "distributions" line rises — this WILL show up as a trend break in your monthly charts.

**Fix**: Note comp-structure changes in the "why" paragraph. Don't read the team-line drop as a real cost decrease.

## The cash floor applies to the LOW, not the EOM HIGH

EOM cash is the cycle HIGH (Stripe payout just landed). Most of the month you're at the intramonth LOW.

**Fix**: Weekly cash pulse (weekly mode of this skill) monitors the low. Cash floor checks apply to the low. See `eom-cash-methodology.md` for the intramonth-low formulas by payout cadence.

## Add your own

Every CFO workflow discovers company-specific traps over time. Document them in your `${COMPANY_CFO_ROOT}/CLAUDE.md` under a "Traps documented for this company" section. This file is the universal starter; your company's `CLAUDE.md` is where the specific muscle memory lives.
