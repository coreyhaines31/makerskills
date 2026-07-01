# Categorization discipline

Same categories every month = trend-readable. Changing categories mid-year = trends become noise. This file documents a starter category set + the discipline of maintaining it.

## Starter categories for a services or SaaS company

Bucket all cash outflows into these categories (adjust once per year, not mid-year):

| Category | What counts |
|---|---|
| **distributions** | ACHs to founder/partner accounts (owner draws, member distributions, W-2 salary if paid through payroll instead of ACH) |
| **team** | Payroll debits (contractor + W-2) + payroll platform fees |
| **software** | Corporate card autopay (usually dominated by SaaS subscriptions — CRM, dev tools, comms, hosting, analytics) |
| **reimbursements** | Expense-management-tool outflows actually paid to team members |
| **benefits** | Healthcare, retirement (401k custodian, Vestwell / Guideline / Human Interest), dental, vision, HSA |
| **other** | Everything else: rent, professional services (CPA, lawyer, contractor accountant), insurance, events, one-times |

Companies with distinct revenue models may need additional categories:

| Category (add if relevant) | What counts |
|---|---|
| **cogs** | Cost of goods sold — for physical or fulfilled products |
| **advertising** | Paid channel spend (Meta, Google, LinkedIn, etc.) — separate line item because it varies wildly |
| **inventory** | Inventory purchases (physical goods) |
| **client-pass-through** | Money that flows through to third parties on client's behalf (freelancer platforms, ad spend billed to client) |

## The discipline

**Lock categories for the fiscal year.** Every month uses the same categories, in the same order, with the same definitions. Deviations get flagged in the report's "why" paragraph, not silently moved into a different bucket.

**When a new expense type appears**, ask: does it fit an existing category? If yes, bucket it. If no, add a new category — but only at the start of a new fiscal year, or with a documented rationale in the memory note.

**Don't over-split.** More categories = more moving lines = harder to read the trend. 6-8 categories is the sweet spot; >12 becomes noise.

**Don't over-lump.** If two very different expense types share a bucket, the trend hides real signal. Advertising bucketed into "other" is the classic mistake — ad spend can swing $20-100K month-to-month; hiding it in "other" makes "other" unreadable.

## Cross-checking categorization each month

At Phase 2 (categorize and reconcile), run these cross-checks:

1. **Payroll cross-check**: Total payroll debits in bank ≈ payroll-tool API total + platform fees. Should be within ~$1K residual (held deductions, timing lags).
2. **Distribution count**: N partners → N distributions. If N-1, flag the missing partner. Common cause: one partner deferring their draw to preserve cash.
3. **Software vs actuals**: Corporate card autopay total should roughly match your subscribed SaaS bills (from receipts or the card statement). Big deltas mean either a new subscription or a canceled one worth noting.
4. **Category vs prior 3 months**: Is any category materially different from the trailing average? If yes, is there a documented reason? If no, investigate before writing the report.

## The "why" paragraph

Every monthly report includes a "why" paragraph explaining what happened this month vs last:

> Team costs were up $12K m/m because we onboarded [Role] on the 15th (prorated payroll). Software was flat. Advertising was down $8K because [Campaign] wrapped end of month. Other was up $4K due to Q3 CPA fees hitting.

This paragraph is the trend-narrative. Without it, category numbers are just numbers.

## Category evolution

Once per year (at fiscal year-end), review:

- Are all categories still meaningful? (Merge any that consistently run <$1K/mo into "other")
- Are any hidden categories worth surfacing? (Grep "other" for line items >$5K/mo — those may deserve their own category)
- Does the ordering still match how leadership reads the report? (Reorder if needed for readability)

Document the changes in the memory note + call them out in the first monthly report of the new fiscal year.
