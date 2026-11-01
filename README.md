# Pension Scheme Valuation

A valuation of a small illustrative defined benefit pension scheme (100 made-up members), built in R, Python and Excel.

## What it does
- Fits a Gompertz mortality model to ONS life table data (R)
- Projects pension cash flows and calculates the liability (Python)
- Validates the Python output against a manual Excel rebuild
- Tests sensitivity to the discount rate, mortality and salary growth
- Runs a 1,000-simulation Monte Carlo of random deaths

## Key results
- Liability: £9.27m against assets of £9.5m (102.5% funded)
- A 1% fall in the discount rate raises the liability by 21.2%
- 26.7% chance of a deficit from longevity risk alone

## Files
- `Pension_Scheme_Valuation_Report.pdf`: full report
- `members.xlsx`: member data and assumptions
- `projection.R`: mortality model and valuation in R
- `projection.py`: valuation in Python
- `sensitivities.py`: sensitivity tests
- `montecarlo.py`: Monte Carlo simulation

## Note
The member data is made up for illustration and is not a real scheme.
