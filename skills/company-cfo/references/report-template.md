# Monthly snapshot report template

Copy this template and fill in placeholders. Adapt sections as needed — this is a starting point, not a rigid form.

Save to `${COMPANY_CFO_ROOT}/reports/monthly/YYYY-MM.md`. Commit only this file (not the raw data used to generate it).

---

```markdown
# <YYYY-MM> Monthly Snapshot

**Report date**: <YYYY-MM-DD>
**Prepared by**: <who ran the workflow>
**Data through**: last day of <MMMM YYYY>

---

## TL;DR

| Metric | Value | vs prior month | Status |
|---|---|---|---|
| Net cash change | ±$X | ±$Y m/m | 🟢 / 🟡 / 🔴 |
| Ending balance | $X | ±$Y m/m | (vs floor) |
| Current MRR | $X | ±$Y m/m | 🟢 / 🟡 / 🔴 |
| Trailing 3-mo avg | $X | | |
| Runway (at current burn) | N months | | |

**Recommendation**: <1-2 sentences — what leadership should do next month>

---

## Cash In

### By source

| Source | Amount | Notes |
|---|---|---|
| <Payment processor> | $X | <N transactions, avg $Y> |
| <Alt revenue source> | $X | <notes> |
| One-time inflows | $X | <describe> |
| Refunds / chargebacks | -$X | <notes> |
| **Total in** | $X | |

### Notable inflows
- <one-line item + $X + why it matters>
- <another item>

---

## Cash Out

### By category

Match the categories defined in your `CLAUDE.md`:

| Category | Amount | vs prior month | Notes |
|---|---|---|---|
| Distributions | $X | ±$Y | <N of N expected partners> |
| Team (payroll) | $X | ±$Y | <contractor + W-2 split> |
| Software | $X | ±$Y | <corporate card autopay> |
| Reimbursements | $X | ±$Y | <expense-mgmt outflows actually paid> |
| Benefits | $X | ±$Y | <healthcare + retirement + custodian> |
| Other | $X | ±$Y | <rent + CPA + insurance + one-times> |
| **Total out** | $X | ±$Y | |

### Notable outflows
- <one-line item + $X + why it matters>

---

## Payroll breakdown

**Verified against `<payroll tool>` API totals + bank debits.**

| Line | Bank total | Payroll API total | Residual |
|---|---|---|---|
| Contractors (Plane / Deel / etc.) | $X | $X | $X (held deductions) |
| W-2 payroll (Gusto / Rippling / etc.) | $X | $X | $X (employer taxes + benefits) |
| Payroll platform fees | $X | | |
| **Combined** | $X | $X | $X |

Currency notes: <e.g., contractor N is JPY, converted at ~150 JPY/USD>

---

## Distributions

Expected: <N> partners × 1 distribution each

| Partner | Amount | Sent | Received | Notes |
|---|---|---|---|---|
| <Name> | $X | ✅ | ✅ | |
| <Name> | $X | ✅ | ✅ | |
| <Name> | $0 | ⏸ | | Deferred to preserve cash (see notes) |

Flag anomalies: <e.g., partner N deferred, or partner M received a larger draw as catch-up>

---

## Revenue metrics

### MRR
- Current: $X (net of processing fees)
- Prior month: $Y
- Delta: ±$Z (±W%)

### Active subscriptions
- Count: N
- Delta: ±M m/m
- Avg revenue per customer: $X

### Churn (recent cancels)

| Customer | MRR lost | Reason (if known) | Cancel date |
|---|---|---|---|
| <Name> | $X | <reason> | <YYYY-MM-DD> |
| <Name> | $X | | |

Churn rate this month: X% (lost / start-of-month active)

### New subs

| Customer | MRR added | Sign-up date | Source |
|---|---|---|---|
| <Name> | $X | <YYYY-MM-DD> | <channel> |

---

## Forward projection

Scenarios from `${COMPANY_CFO_ROOT}/scenarios/index.html`:

### Scenario A: Status quo
- Mo 3 EOM: $X, low: $Y
- Mo 6 EOM: $X, low: $Y
- Runway assumption: N months

### Scenario B: <name — e.g., aggressive hire>
- Mo 3 EOM: $X, low: $Y
- Mo 6 EOM: $X, low: $Y
- Trigger: <when to commit to this>

### Scenario C: <name — e.g., churn pessimism>
- Mo 3 EOM: $X, low: $Y
- Mo 6 EOM: $X, low: $Y
- Trigger: <when to worry>

---

## Recommended actions

Concrete, tactical, decidable by leadership:

1. <action + owner + deadline>
2. <action + owner + deadline>
3. <action + owner + deadline>

---

## Open items

- [ ] <question to resolve next month>
- [ ] <data to verify — e.g., reconcile alt revenue source X>
- [ ] <categorization to revisit — e.g., how to bucket new AI subscriptions>

---

## Why paragraph (plain English)

Explain what happened this month vs last, in continuous prose. Reference prior months when there's continuity ("The <Vendor X> churn from last month finished hitting <this month>'s payouts; hence the MRR dip"). Note anomalies + the story behind them.

2-4 paragraphs is the sweet spot. This is the section leadership actually reads first.
```

---

## Section adaptations

Trim / expand based on your business shape:

- **Services company (agency)**: expand "Distributions" — often the largest cash outflow. Add sub-categories for retainer vs one-off vs pass-through.
- **SaaS**: expand "Revenue metrics" with cohort retention, LTV, CAC payback if you track those.
- **Ecommerce**: add COGS + inventory + advertising as top-level categories (they'll dominate).
- **Marketplace**: separate GMV (through your platform) from your take-rate revenue.

## What NOT to include

- **Raw bank transaction dumps.** Sensitive. Belongs in `data/` (gitignored), not the report.
- **Customer names for churn if the report will be shared broadly.** Anonymize as needed.
- **Employee comp specifics.** If the report is shared with a broader team, aggregate to category level; keep individual comp in leadership-sensitivity-tagged sections.
- **Forward-looking guarantees.** Projections are estimates, not commitments. Frame accordingly.
