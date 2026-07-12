# Methodology and Technical Review Notes

## Decision frame and data

The unit is one store-week. `Walmart.csv` contains 6,435 observations across 45 stores and 143 weeks. It has sales, a competition-defined holiday flag, temperature, fuel price, CPI, and unemployment. It has no price, markdown amount, unit, SKU, inventory, cost, or margin field. “Holiday lift” therefore means an observed difference in weekly sales, not causal promotion lift or ROI.

The flag covers 10 calendar weeks. Super Bowl and Labor Day appear three times each; Thanksgiving and the post-Christmas December flag appear twice each. The December dates are after Christmas. That labelling issue is preserved explicitly in `sql/05_holiday_type_breakdown.sql`.

## Holiday inference

`analysis/statistical_tests.py` compares flagged and regular weekly sales overall and by store. Shapiro–Wilk tests are used as a diagnostic. When both groups pass at 5%, the script uses a two-sided Welch t-test; otherwise it uses a two-sided Mann–Whitney U test. Because Mann–Whitney tests distributional separation rather than mean difference, the business-scale interval is estimated separately: 5,000 seeded bootstrap resamples produce a percentile 95% interval for percent lift in means.

A result passes the nominal exploratory screen only when unadjusted p<0.05 and the lift interval is entirely above zero. Seven stores meet that display rule. As a QA correction, the 45 per-store p-values are also adjusted using Bonferroni family-wise control and Benjamini-Hochberg false-discovery-rate control; **zero stores survive either correction at 5%**. The dashboard therefore labels the seven as nominal screens, not confirmed discoveries. More importantly, stores observed in the same calendar week share common shocks, so the 450 flagged store-weeks are not equivalent to 450 independent holiday events. The overall result is statistically detectable but still based on only 10 time events.

## Regression

Per store, robust OLS estimates:

`weekly_sales ~ fuel_price + cpi + unemployment + holiday_flag`

HC3 heteroskedasticity-robust standard errors supply p-values and 95% intervals. A pooled version adds store fixed effects (`C(store_id)`) to control for stable level differences between stores. R² is reported and labelled low (<0.20), moderate (0.20–0.49), or strong (≥0.50). Coefficients are conditional associations, not causal effects: omitted seasonality, macro collinearity, serial correlation, shared shocks, and trending CPI can bias inference. A production study would add calendar fixed effects, clustered errors, richer covariates, and a credible treatment/control design.

## Forecast evaluation

`analysis/forecast.py` preserves time order and holds out the final 20 weeks for every store and the all-store aggregate. It compares:

1. Seasonal naive: sales from 52 weeks earlier.
2. Feature OLS: lag-52 sales, holiday flag, fuel price, CPI, unemployment, and a time trend.

Both models are scored on identical dates using MAPE and RMSE. The winner is selected by holdout MAPE per scope. Aggregate OLS wins this holdout (1.87% versus 2.24% MAPE), but seasonal naive wins 22 of 46 scopes, so complexity is not assumed to win. This is a single holdout, not rolling-origin cross-validation. The OLS evaluation also uses observed macro values in the holdout; live use requires forecast or scenario inputs for those variables.

## Engineering controls and reproducibility

`scripts/run_pipeline.py` rebuilds the database, SQL outputs, statistical files, forecasts, dashboard, and tests. `tests/test_pipeline.py` asserts the 6,435-row load, non-null keys, 10 distinct flagged weeks, exact recomputation of SQL lift, expected source types, and presence of analytical artifacts. Load errors report the malformed row and missing columns.

At larger scale, the same contracts could move to BigQuery or Snowflake, dbt models could replace SQLite SQL, and Airflow could schedule tested data and model tasks. That is a proposed scaling path only; this repository does not claim cloud deployment.
