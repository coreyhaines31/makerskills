# Calculators — formulas this skill uses

All formulas are documented inline so the math is auditable. Round to whole dollars in output; carry full precision internally.

## Mortgage monthly payment (P&I)

Standard amortization formula:

```
M = P × [r(1+r)^n] / [(1+r)^n − 1]
```

Where:
- `M` = monthly P&I payment
- `P` = principal (loan amount = purchase price − down payment)
- `r` = monthly interest rate (annual rate / 12, as decimal)
- `n` = total number of payments (years × 12)

**Example** — $680K loan at 6.5% for 30 years:
- `P = 680000`
- `r = 0.065 / 12 = 0.005417`
- `n = 360`
- `M = 680000 × (0.005417 × 1.005417^360) / (1.005417^360 − 1) ≈ $4,298/mo`

Add property tax (annual / 12), insurance (annual / 12), and HOA on top for **PITI** (Principal + Interest + Tax + Insurance).

## Effective rental income (vacancy-adjusted)

```
Effective monthly rent = Gross monthly rent × (1 − vacancy_rate)
```

If property management:
```
Net monthly rent = Effective × (1 − pm_fee_pct)
```

## Net monthly housing cost (per scenario)

```
Net monthly = PITI
            + utilities (owner-paid portion)
            + HOA
            + monthly_maintenance_reserve  (annual maintenance / 12)
            − net_monthly_rent (all units, summed)
```

Negative result = positive cash flow.

## Renovation amortization

For comparison purposes, amortize one-time renovation costs over the time horizon:

```
Monthly renovation amortization = total_renovation_cost / (time_horizon_years × 12)
```

This converts a $108K upfront cost into a comparable monthly figure (over 10 years, that's $900/mo of "renovation rent").

Don't conflate with mortgage — renovations are paid in cash (or via a renovation loan, which adds a separate payment).

## Mortgage interest deduction value

```
Annual interest paid year 1 ≈ P × r  (rough — actually slightly less due to amortization)
                              ≈ $680K × 6.5% = $44,200 first-year interest

Deduction value = annual_interest × marginal_federal_tax_rate
                ≈ $44,200 × 0.32 = $14,144/year of tax savings
```

**Caveats:**
- Only valid if itemizing exceeds standard deduction
- 2017 TCJA capped mortgage interest deduction to first $750K of debt
- SALT cap ($10K) limits property tax deduction
- These rules expire 2025 — verify current law before acting

## Depreciation (for rented portion of the property)

If renting part of the property (ADU, bedrooms), the rented square footage's portion of the building basis depreciates over 27.5 years.

```
Building basis = purchase_price − land_value  (land doesn't depreciate)
Rented fraction = sq_ft_rented / total_sq_ft
Annual depreciation = (building_basis × rented_fraction) / 27.5
```

This depreciation is deducted against rental income — can produce paper losses that offset other income (up to $25K for active management, phased out above $100K AGI).

**Caveat**: depreciation recapture at sale at 25% — not free money, just deferred.

This is the messiest part of the math. Default to surfacing it as an estimate and flagging "verify with accountant."

## Cap rate (return on investment, simplified)

```
Cap rate = (Net annual operating income) / (Purchase price + closing + renovations)
```

Where NOI = rent collected − all operating expenses (not including mortgage P&I).

**Rule of thumb**: ≥8% cap rate is good for residential. <4% means you're betting on appreciation, not income.

## Cash-on-cash return

```
Cash-on-cash = (Annual pre-tax cash flow) / (Total cash invested)
```

Where cash invested = down payment + closing + renovations + reserves.

A house-hack where you live in a unit + rent others: cash-on-cash often higher than pure investment property because you also save on rent you'd otherwise pay.

## Equity build-up (over time horizon)

Two components:

```
Equity year N = Mortgage paydown by year N + Appreciation by year N
              = (P − remaining_balance_year_N) + P × (1 + appreciation_rate)^N − P
```

Default appreciation: 3%/yr (conservative; long-run US average is closer to 3.5–4% nominal).

## Opportunity cost (vs S&P alternative)

```
Alternative wealth at year N = cash_invested × (1 + 0.07)^N
                              (using 7% real return — long-run S&P average)
```

Compare to equity build-up + cash flow to see net financial benefit of the property.

This is the most important number for "should we buy at all" decisions. If the property barely beats S&P + 7%, the lifestyle benefits matter more than the financial ones.

## Sensitivity analysis variables

For each scenario, surface what happens if:

| Variable | Stress |
|---|---|
| Mortgage rate | +1%, +2% (refi-from-current implications) |
| ADU rent | −10%, −20% (market softens) |
| Vacancy | 2× baseline (long vacancy after tenant leaves) |
| Renovation cost | +30% (overruns are the norm) |
| Appreciation | 0%, −2% (flat or declining market) |
| Maintenance | 2% of price/yr (older property) |

Surface the 3 variables the scenario is most sensitive to — these are the ones that flip the decision.
