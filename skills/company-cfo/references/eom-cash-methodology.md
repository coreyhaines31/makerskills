# End-of-month cash methodology

The single most important discipline in the CFO workflow. Getting this wrong once has propagated errors into every downstream chart, forecast, and partner decision.

## The rule

**Compute EOM cash by summing raw transactions, not by walking back from a current balance snapshot.**

## Why walkback fails

A bank API balance snapshot at pull time reflects a specific instant. That instant might include:

- Transactions in-flight but not yet posted (ACH holds, wire receipts pending)
- API-cache staleness (some banks serve a 5-15 minute cached value)
- Pending-vs-posted delta (Stripe payouts marked available but not yet in the checking account)

If your snapshot is off by $X and you walk backward through transactions to reconstruct historical EOMs, every historical EOM is off by exactly $X — silently — and no downstream chart can catch it. This has happened multiple times in production CFO workflows; one incident carried a ~$42K error for weeks before the reconciliation caught it.

## The correct method

```python
# 1. Pull ALL transactions for each cash-holding account:
#    (Checking + Savings + any other bank account that actually holds cash)
transactions = fetch_all_transactions(account_id, limit=100000)

# 2. Sum the signed amount field across all transactions:
transaction_sum = sum(t["amount"] for t in transactions)

# 3. Sanity check: transaction_sum should equal the account's CURRENT available_balance
#    to the cent. If not, one of:
#      - Missing transactions (paging error, API timeout, filter mistake)
#      - Pre-history baseline deposit (opening deposit that predates the transaction history)
#      - Data-source bug (rare but real — file an issue)
current_balance = fetch_current_balance(account_id)
assert abs(transaction_sum - current_balance) < 0.01, \
    f"Transaction sum {transaction_sum} != current balance {current_balance}"

# 4. For any past date T:
#    balance_at_T = sum of all transactions with posted_date <= T
#                   + any pre-history baseline (should be ~$0 if step 3 passes)
def balance_at(date, transactions):
    return sum(t["amount"] for t in transactions if t["posted_date"] <= date)
```

## Cross-checks

Every monthly run:

1. **Sanity check per account** — transaction sum == current balance (to the cent)
2. **Month-over-month reconciliation** — last month's EOM + this month's net cash change == this month's EOM (to the dollar)
3. **Cash accounts only** — filter out credit card / debt accounts. Including a credit card account double-counts autopay flows (charges on the card show, AND the autopay debit from checking shows).
4. **Internal transfers excluded** — Checking ↔ Savings transfers net to zero within the company. Exclude via `kind=internal_transfer` filter or account-pair matching.

## What to do when reconciliation fails

**Stop.** Do not proceed with walkback as a fallback. Investigate:

1. **Re-pull transactions with a larger `--max-items`** — pagination silently truncated at a lower limit?
2. **Check for accounts you didn't know about** — a treasury account, a savings bucket, an escrow account?
3. **Look for a pre-history baseline** — the transaction history may not go back to account opening. If the oldest transaction is a $50K "initial deposit," that's your baseline.
4. **Timeout during pull?** — API returned partial data. Retry with a longer timeout or smaller date range.

Never silently ship a report with an unreconciled gap. The gap will grow.

## Intramonth cycle low

The EOM cash is often the *high* point of the month, not what you have most of the month. Payment processors on monthly payout cadences deposit the entire month's revenue at end-of-month, so mid-month your cash is at the low.

Formula depends on payout cadence:

- **Monthly payouts (legacy)**: `intramonth_low ≈ EOM − month_revenue` — whole month's inflow lands at EOM, so trough is everything except that lump
- **Weekly payouts**: `intramonth_low ≈ EOM − (month_revenue / 4)` — only one week of inflow is "lumpy," rest is smoothed across the month
- **Daily payouts** (rare): `intramonth_low ≈ EOM − (month_revenue / 30)` — negligible dip

**Switching from monthly to weekly payouts** is one of the highest-leverage cash-management moves available. It cuts the intramonth dip by ~75% and dramatically reduces cash-floor pressure. If your payment processor supports it (Stripe does), the switch takes ~5 minutes in the dashboard.

## The $50K floor (or whatever your floor is)

Every company should have a documented cash floor — the minimum cash balance below which leadership takes action (defer distributions, cut expenses, accelerate collections).

**The floor applies to the intramonth LOW, not the EOM HIGH.** A company that says "we'll never go below $50K" and only checks EOM is guaranteed to breach mid-month at some point.

Weekly cash pulse mode (see main SKILL.md) is designed to catch floor risk before it becomes a floor breach.

## Historical incidents (add yours here)

- **The $42K walkback error** — snapshot-based reconstruction was silently off by ~$42K for weeks. Now all EOM computation uses transaction-sum only. Discovered via a month-over-month reconciliation failure.
- (Add your own incidents as they happen — the log is the discipline.)
