# Six-Page Report Layout

Use a 16:9 canvas, 24 px outer margins, 16 px visual gaps, white cards on `#EEF1F4`, and one navy header band. Keep titles left-aligned. Use teal for supported/positive evidence, amber for caution, red only for negative or review signals, and grey for inconclusive results.

## 1. Executive Overview

Top cards: Total Sales, Stores (45), Weeks (143), Holiday Weeks (10), Overall Lift (7.84%).

- Left 2/3: line chart, `WeeklyKPI[date]` vs `WeeklyKPI[total_sales]`
- Right 1/3: recommendation mix donut
- Bottom: three-line decision summary and limitation callout

Required callout: **Observed holiday association, not causal markdown ROI.**

## 2. Holiday Impact

- Store slicer across the top
- Ranked column chart: `store_id` vs `holiday_lift_pct`
- Clustered bars: regular vs holiday average sales
- Table: store, lift, CI lower, CI upper, nominal p-value, FDR p-value, Evidence Label
- Cards: nominal screen stores (7), FDR-confirmed stores (0)

Conditional formatting: teal only for nominal screens; grey for other stores. Add an amber caption that none survives multiplicity correction.

## 3. Holiday Type Breakdown

- Four-bar chart ordered by `lift_vs_regular_pct`
- Supporting table with occurrence count and average store sales
- Large amber data-quality callout about the post-Christmas flag

Do not add significance icons: each type occurs only 2-3 times.

## 4. Economic Sensitivity

- Store slicer
- Coefficient bar chart by term
- Error-range/custom interval visual using `ci_lower` and `ci_upper`
- Detail table: coefficient, p-value, R-squared, fit quality, observations
- Pooled fixed-effects row shown separately from store results

Required subtitle: **Conditional associations; not causal effects.**

## 5. Forecast & Model Evaluation

- Scope slicer defaulted to Aggregate
- Actual vs predicted line chart by date and model
- Model table: MAPE, RMSE, train weeks, test weeks, winner
- Winning Model card
- Aggregate comparison cards: OLS 1.87%, seasonal naive 2.24%

Keep both models visible. Do not hide the baseline when OLS wins.

## 6. Store Recommendations

- Recommendation and store slicers
- Matrix: store, average sales, coefficient of variation, lift, Evidence Label, Recommendation Evidence
- Scatter plot: average sales vs holiday lift, sized by consistency or fixed size
- Amber controlled-pilot callout for Store 7

Never display “statistically confirmed expansion.” Use “nominal screen” or “directional” language.
