# Company config template

Copy this to `${COMPANY_CFO_ROOT}/CLAUDE.md` when seeding a new company's CFO workflow. Fill in placeholders with your actuals.

The file becomes the source of truth for HOW your company computes its financials. The `company-cfo` skill reads this first before every run.

---

```markdown
# <Company Name> CFO — methodology + config

## Structure

- **Legal form**: <LLC / C-Corp / S-Corp / other>
- **Fiscal year**: <calendar / July-June / other>
- **Owners / partners / leadership**: <names + roles>
- **Number of monthly distributions expected**: <N>
- **Cash floor**: $<X>K (below this, defer distributions + review expenses)

## Data sources

| Source | Tool | Access | Notes |
|---|---|---|---|
| Bank / cash | <e.g. Mercury CLI> | `<install> ; <auth>` | Cash accounts to include: <list account labels> |
| Payment processor | <e.g. Stripe> | `<key location>` | MRR source of truth |
| Alt revenue | <e.g. Paddle, direct invoicing> | <access> | Note: not visible in payment processor |
| Payroll (contractors) | <e.g. Plane, Deel> | `<key location>` | Currency: use `source_amount` for base-currency cost |
| Payroll (W-2) | <e.g. Gusto, Rippling> | <access> | Includes employer taxes + benefits |
| Expense management | <e.g. Ramp, Brex> | `<CLI or API>` | Cash-out timing lives in bank (RMPR / equivalent debits) |

## Cash accounts

Filter transactions to these accounts only (exclude credit card / debt / escrow):

- Checking ••<last 4> (primary operating)
- Savings ••<last 4> (reserves)
- <any other cash-holding accounts>

Exclude: internal transfers (Checking ↔ Savings), credit card account (debt-side, double-counts autopay flows).

## Categorization

| Category | What counts here |
|---|---|
| **distributions** | ACHs to partner accounts <account digits or names> |
| **team** | All payroll debits + payroll platform fees |
| **software** | Corporate card autopay (dominated by SaaS) |
| **reimbursements** | Expense-management outflows paid to team |
| **benefits** | Healthcare, retirement, dental, vision |
| **other** | Rent, CPA, insurance, professional services, one-times |

Add categories only at fiscal year-end (see `references/categorization.md`).

## Distribution mechanics

- **Frequency**: <monthly / quarterly / ad-hoc>
- **Formula**: <fixed amount / % of profit / other>
- **Recipients**: <named partners + account digits>
- **Constraints**: <cash floor, retention buffer, deferrals>

## MRR + revenue

- **Primary source**: <Stripe / other>
- **Secondary sources**: <alt billing platforms — always include, they're invisible in the primary>
- **Processing fee assumption**: ~<X>% (default 3% for Stripe). Report MRR NET of fees, not gross.
- **Churn tracking**: <how you track — Stripe events, manual log, other>

## Payroll notes

- **Contractor tool**: <tool>. Currency: use `source_amount` for base-currency cost. `destination_amount` is in worker's payout currency (e.g. JPY, EUR, GBP).
- **W-2 tool**: <tool>. Includes employer taxes + benefits in the total.
- **Held deductions**: expect ~$<X> residual between bank total and payroll tool total.

## Traps documented for this company

Add as they're discovered — this list is company-specific muscle memory:

- <e.g. "The IO autopay double-counts if we include the credit card account. Cash accounts only.">
- <e.g. "Contractor <Name>'s payments come through in JPY. Use source_amount.">
- <e.g. "Vendor <Name> revenue is invisible in Stripe. Add from bank inflows manually.">

## Reports

- **Monthly**: `reports/monthly/YYYY-MM.md`
- **Weekly cash pulse**: `reports/weekly/YYYY-WW.md`
- **Scenarios**: `reports/scenarios/YYYY-MM-DD-<question>.md`

## Scenario projector

- **Location**: `scenarios/index.html` (served via `scenarios/serve.sh` on port <port>)
- **Structure**: 3 historical months + TODAY + 7 forward months
- **Update cadence**: end of each monthly run

## Git workflow

- Branch pattern: `feature/YYYY-MM-snapshot`
- Review: <auto / manual / codex review / other>
- Merge: `gh pr merge --squash --delete-branch`

## Memory note

Running context lives at `~/.claude/memory/company_cfo_<slug>.md`. Update if:
- Distribution/comp structure changes
- Active sub count or MRR shifts materially
- New revenue stream or new payroll tool
- Cash floor changes
```
