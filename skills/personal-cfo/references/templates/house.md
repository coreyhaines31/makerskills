# House template — full input questionnaire

For `/personal-cfo house` mode. Walk Corey through this in a structured batch (one message, numbered questions). Don't proceed with placeholder numbers — bad inputs → dangerous output.

## Property fundamentals

1. **Property nickname** (for filing — e.g., "Elm Street," "the white one")
2. **Address** (for the record — optional)
3. **Purchase price** ($)
4. **Estimated closing costs** (% of purchase, typical: 2–5%. If unknown, use 3% as a placeholder + flag for verification)
5. **Down payment** (% or $ — confirm which)

## Financing

6. **Mortgage rate** (interest rate, %, fixed or ARM — note which)
7. **Mortgage term** (years — typical: 30, sometimes 15)
8. **PMI** (does down payment trigger PMI? typically yes if <20%. Estimate $50–$200/mo if applicable.)
9. **Loan type** (conventional / FHA / VA / jumbo — affects insurance + qualification)

## Holding costs

10. **Property taxes** (annual $ — usually 1–2% of value but varies wildly by state/county. Get exact from listing or assessor.)
11. **Homeowner's insurance** (annual $ — typical: $1,200–$3,000)
12. **HOA fees** (monthly $, if any)
13. **Utilities estimate** (monthly $ — electric + water + gas + sewer + trash, owner portion if renting rooms)
14. **Lawn / pest / pool / other recurring** (monthly $)

## Renovations (one-time, day 1)

15. **List of planned renovations** with line items. Common categories:
    - Kitchen: $X
    - Bathroom(s): $X each
    - Flooring: $X
    - Paint: $X
    - ADU buildout / refresh: $X
    - Roof / HVAC if needed: $X
    - Landscaping: $X
    - Permits / contractor markup buffer: add 15–25% on top of line-item subtotal
16. **Timeline** (months to complete — affects whether Year 1 income includes ADU)

## Ongoing maintenance

17. **Year-1 expected repairs** ($ — inspection report informs this; older properties higher)
18. **Annual maintenance budget** ($ — rule of thumb: 1% of purchase price per year)

## Rental scenarios

For each potential rental unit:

### ADU
19. **ADU monthly rent estimate** ($ — verify against local comps)
20. **ADU ready when?** (immediately / after X months of renovation)
21. **ADU utilities** (owner pays / tenant pays / split — affects net cash flow)
22. **ADU vacancy assumption** (typical: 5–10% — higher for short-term)
23. **Short-term vs long-term**? (STR has higher gross but higher costs + management overhead)

### Bedroom 1 (house-hack)
24. **Bedroom 1 monthly rent** ($)
25. **Vacancy assumption** (higher than ADU usually — typical 10–15% for room rentals)
26. **Includes utilities?** (usually yes for room rentals)

### Bedroom 2 (if applicable)
27–29. Same as Bedroom 1

### Property management
30. **Self-manage or property manager?** PM typically 8–12% of rent collected. STR can be 20–30%.

## Tax

31. **Combined household marginal tax bracket** (federal % — affects mortgage interest deduction value)
32. **State** (for state income tax + property tax deduction cap awareness)
33. **Filing status** (married joint / single — affects SALT cap, standard deduction)

## Personal context (for comparison)

34. **Current monthly housing cost** (rent or mortgage on existing place — this is the baseline)
35. **Combined household income** (for affordability + ratio sanity checks)
36. **Cash on hand for down + closing + reserves** ($ — should have 6 months reserves after closing)
37. **Time horizon** for the analysis (default: 10 years; also model 5 and 30)

## Lifestyle (qualitative — not in the math, but in the report)

38. **Comfort level with roommates** (fiancée especially — this is a real variable)
39. **Distance / commute from this property** (vs. current)
40. **Schools / future kids planning** (affects neighborhood weighting)
41. **Exit plan** (how long do you plan to live here? sell when? rent out fully later?)

---

## After gathering

Output an `inputs.yaml` so the analysis is rerunnable:

```yaml
property:
  nickname: "Elm Street"
  purchase_price: 850000
  down_payment_pct: 20
  closing_costs_pct: 3
financing:
  rate_pct: 6.5
  term_years: 30
  pmi_monthly: 0
holding:
  property_tax_annual: 12000
  insurance_annual: 1800
  hoa_monthly: 0
  utilities_owner_monthly: 250
renovations:
  - { item: "Kitchen refresh", cost: 25000 }
  - { item: "ADU buildout", cost: 65000 }
  - { item: "Buffer (20%)", cost: 18000 }
  timeline_months: 4
maintenance:
  year_1_repairs: 8000
  annual_pct_of_price: 1.0
rental:
  adu:
    monthly_rent: 2200
    ready_month: 5   # available starting month 5
    utilities: "tenant pays"
    vacancy_pct: 6
  bedroom_1:
    monthly_rent: 1100
    vacancy_pct: 12
    includes_utilities: true
  bedroom_2:
    monthly_rent: 1100
    vacancy_pct: 12
    includes_utilities: true
  property_management_pct: 0   # self-manage
tax:
  federal_marginal_pct: 32
  state: "CA"
  filing: "married_joint"
personal:
  current_housing_monthly: 3500
  household_income: 350000
  cash_for_close: 220000
  time_horizon_years: 10
lifestyle:
  roommate_comfort: "open to ADU; not comfortable with bedroom rentals year 1"
  commute_minutes: 25
  exit_plan: "live in 5–10 yr, then full STR rental"
```

This file lives in the workdir and is the source of truth. The `report.md` and `comparison.md` are generated from it.

## When inputs are incomplete

Don't fake numbers. Mark missing as `null` and flag at the top of the report:

```markdown
> ⚠️ Inputs incomplete. The following used placeholders or estimates — verify before acting:
> - `closing_costs_pct`: 3% (typical, not verified for this property)
> - `adu.monthly_rent`: $2,200 (estimate, verify via Zillow/Craigslist comps via /deep-research)
> - `tax.federal_marginal_pct`: 32% (estimated from income; verify with last year's return)
```
