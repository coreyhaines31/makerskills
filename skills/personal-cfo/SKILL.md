---
name: personal-cfo
description: "When you want to model personal financial scenarios — house purchase + rental income (ADU, bedroom rentals, house-hacking), renovation budgets, monthly cash flow forecasts, big-purchase decisions, savings/investment what-ifs. For personal life: a household (you + partner), household budgets, real-estate decisions. v0.1 ships with the house scenario template (purchase + rental scenarios) as the first use case. Architected so other personal-finance scenarios (refi, car, education, retirement, side income) slot in as additional templates. Outputs scenario comparison tables in markdown. Saves every scenario to references/scenarios-archive/ for revisit + comparison. Composes with decide (formalize the call after modeling), deep-research (rental comps, mortgage rates, market data), business-brainstorm (when the scenario is a small business / side hustle), second-brain (capture the analysis to outputs/). Triggers on \"/personal-cfo,\" \"model this scenario,\" \"house math,\" \"rental forecast,\" \"monthly cash flow,\" \"what if I rent out the ADU,\" \"compare these housing scenarios,\" \"should we buy this house,\" \"house-hack math,\" \"renovation budget.\""
metadata:
  version: 0.1.0
---

# /personal-cfo — Personal financial scenario modeling

This skill is for a household (you + partner): housing decisions, monthly cash flow, big purchases, scenario what-ifs. Pair it with a business-books CFO skill if you also run one for a company — the DNA is the same, the domain is different.

## Step 1 — Pick the scenario type

| Invocation | Type | What it models |
|---|---|---|
| `/personal-cfo house` (default for now) | **house** | Buy a house + rental income scenarios (ADU / bedrooms / combinations) + renovations + monthly cash flow |
| `/personal-cfo refi` | **refi** | Refinancing scenarios |
| `/personal-cfo cash-flow` | **cash-flow** | Generic monthly cash flow (income, expenses, savings rate) |
| `/personal-cfo big-purchase` | **big-purchase** | Should we buy X (car, education, equipment) — cash vs finance vs lease comparisons |
| `/personal-cfo side-income` | **side-income** | Adding a side income stream — break-even, tax implications |
| `/personal-cfo savings-what-if` | **savings-what-if** | What if we put $X into Y for N years — index funds, real estate, etc. |

For v0.1, only the **house** template is fleshed out. Others are sketched in `references/templates/` as stubs.

## Step 2 — Gather inputs

Ask in a structured batch. For house mode, see `references/templates/house.md` for the full input questionnaire. Core fields:

**Property**
- Purchase price
- Down payment (% or $)
- Mortgage rate + term (years)
- Property taxes (annual)
- HOA (monthly, if any)
- Homeowner's insurance (monthly)
- Closing costs (estimate)

**Renovations / repairs**
- Day-1 renovations (line items with estimates — kitchen, bath, ADU buildout, etc.)
- Year-1 expected repairs
- Annual maintenance budget (rule of thumb: 1% of purchase price)

**Rental scenarios** (for the house mode)
- ADU monthly rent estimate + vacancy assumption (typical: 5–8%)
- Bedroom 1 monthly rent + vacancy
- Bedroom 2 monthly rent + vacancy
- Utilities split assumption (who pays what)
- Property management cost (if not self-managing)

**Personal**
- Current monthly housing cost (rent or current mortgage)
- Combined household income
- Marginal tax bracket (for mortgage interest + rental income calcs)
- Time horizon for the analysis (typical: 5 yr, 10 yr, 30 yr)

If anything's fuzzy, ask. Don't proceed with placeholder numbers — financial models with wrong inputs are dangerous.

## Step 3 — Build the scenarios

For the house mode, default scenarios to compare:

| Scenario | Description |
|---|---|
| **Baseline** | Own + live in, no rental income |
| **A: ADU only** | Rent the ADU, live in main house |
| **B: 1 bedroom only** | House-hack 1 bedroom, keep ADU empty (or for guests) |
| **C: 2 bedrooms only** | House-hack 2 bedrooms, ADU empty |
| **D: ADU + 1 bedroom** | Both ADU and 1 bedroom rented |
| **E: ADU + 2 bedrooms** | Maximum rental |
| **F: ADU + bedrooms (year 2+)** | Year 1: just ADU while renovating. Year 2+: add bedrooms after partner's comfort |

Let the user customize the scenario list — every house is different.

## Step 4 — Run the math

For each scenario, calculate:

**Monthly**
- Mortgage payment (P&I) — see `references/calculators.md` for the formula
- + Property tax / 12
- + HOA + Insurance + Utilities (owner-paid portion)
- − Gross rental income (rooms + ADU)
- × (1 − vacancy rate) for effective rental income
- − Property management fee (if applicable)
- = **Net monthly housing cost** (negative = positive cash flow)

**Annual**
- Sum of 12 months
- + One-time renovation costs (amortized over time horizon)
- − Tax savings (mortgage interest deduction + depreciation on rented portion)

**Long-term**
- Equity build-up (mortgage paydown + appreciation assumption — default 3%/yr)
- Total cost of ownership at year 5 / 10 / 30
- Return on cash invested vs. alternative (e.g., S&P 500 at 7% real return)

## Step 5 — Output the comparison table

Output to `~/Documents/personal-cfo/<scenario-slug>-<YYYY-MM-DD>/`:
- `inputs.yaml` — all the input numbers (so the analysis is rerunnable + auditable)
- `report.md` — the full analysis with assumptions called out
- `comparison.md` — side-by-side scenario table (the headline output)

### `comparison.md` template

```markdown
# <Property nickname> — scenario comparison

**Date:** YYYY-MM-DD
**Property:** <address or nickname>
**Time horizon:** 10 years
**Key assumptions:** 3%/yr appreciation, 7% S&P alt return, 6% vacancy

| Scenario | Net monthly cost | Annual cost | 10-yr total | Equity @ 10yr | Notes |
|---|---:|---:|---:|---:|---|
| Baseline | $X,XXX | $XX,XXX | $XXX,XXX | $XXX,XXX | No rental income |
| A: ADU | $X,XXX | $XX,XXX | $XXX,XXX | $XXX,XXX | $X,XXX/mo ADU rent |
| B: 1 BR | … | … | … | … | … |
| C: 2 BR | … | … | … | … | … |
| D: ADU + 1 BR | … | … | … | … | … |
| E: ADU + 2 BR | … | … | … | … | … |

## Headline takeaway
<1–2 sentences: which scenario wins on cash flow, which wins on lifestyle, where the inflection points are>

## Sensitivity analysis
- If rates rise 1%: <impact>
- If ADU rent comes in 20% lower: <impact>
- If renovations overrun 30%: <impact>
- If vacancy doubles to 12%: <impact>

## Open questions
- <what would change the recommendation>
- <what to research next — composes with /deep-research>
```

## Step 6 — Archive

Save the scenario folder so future revisits work. Append a one-liner to `references/scenarios-archive/INDEX.md`:

```markdown
- 2026-06-26 — [<property nickname>](./<slug>-2026-06-26/) — <type> — <headline takeaway>
```

This compounds — when you're considering Property #2 a year later, you can reuse the model and grep past analyses for patterns.

## Step 7 — Surface + offer follow-ups

- Show the comparison table in chat
- Tell the user the workdir path
- Offer:
  - *"Want to run `/deep-research` on rental comps for the area to firm up the ADU and bedroom rent assumptions?"*
  - *"Want to formalize the buy/don't-buy decision through `/decide` once the scenarios land?"*
  - *"Want to capture this analysis to `second-brain raw/` as `note-house-<slug>.md`?"*
  - *"Want me to revisit in 30 days as more info comes in (loan rate locked, inspection done, etc.)?"*

## Composes with

- **`decide`** — once scenarios are modeled, the buy / don't / negotiate decision goes through `/decide`. Cash flow analysis is input, not the decision itself.
- **`deep-research`** — for inputs that need market data: rental comps, mortgage rate trends, neighborhood trajectory, school ratings, comparable sales.
- **`business-brainstorm`** — if the scenario tips into "this is a business" (e.g., short-term rental, multi-unit purchase, scaling to N properties), route there to pressure-test the business angle.
- **`second-brain`** — capture analyses to `raw/note-house-<slug>.md` so they live in the personal wiki and can be referenced later.

## Notes on quality

- **Conservative assumptions by default.** Default to higher vacancy (8% not 5%), lower appreciation (3% not 6%), 20% buffer on renovation estimates. Real estate optimism is the most reliable way to lose money.
- **Surface the sensitivity, not just the point estimate.** A scenario that's positive only if everything goes right isn't actually positive.
- **Lifestyle is a real variable.** "Living with 2 roommates" can be financially optimal AND a quality-of-life disaster. Note these tradeoffs in the report, even if they aren't quantified.
- **Tax calcs are starting points, not authoritative.** This skill estimates; an accountant verifies. Flag this in the report.
- **The decision isn't here — the inputs to the decision are.** This skill produces the model. `/decide` makes the call.

## Future templates (sketched in references/templates/)

- `refi.md` — refinance scenarios
- `cash-flow.md` — generic monthly budget
- `big-purchase.md` — cash vs finance vs lease for big-ticket items
- `side-income.md` — adding a side income stream
- `savings-what-if.md` — investment what-ifs

v0.1 ships only `house.md` fleshed out. Add others when the use case is real.
