# Walmart Holiday Sales Decision Science

Decision-science portfolio project built on the Kaggle Walmart Store Sales Forecasting data: 6,435 store-weeks, 45 stores, and 143 calendar weeks from 2010–2012.

## Run it yourself

```bash
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
```

The second command rebuilds every database, analysis export, dashboard, PDF, and test artifact.

## Executive summary

The data contains store-level weekly sales and macro variables, but **no SKU, price, discount, cost, margin, or markdown amount**. Accordingly, this project does not claim price elasticity or promotion ROI. It evaluates the association between competition-defined holiday weeks and sales, tests uncertainty, measures conditional macro associations, and evaluates two forecasting methods on a time-ordered holdout.

The headline data-quality finding is unchanged: the two December `Holiday_Flag` dates are the **week after Christmas**, not Christmas week. Those weeks average 7.7% below regular weeks, so using the flag as “Christmas lift” understates the Christmas selling period.

## Validated findings

- Overall flagged-week sales are 7.84% above regular weeks (bootstrap 95% CI: 2.08% to 13.67%; Mann–Whitney p=0.0259). This is statistically detectable at the row level, but still based on only 10 calendar weeks repeated across stores and is not a causal markdown estimate.
- Seven of 45 stores pass the project's **nominal exploratory screen** (unadjusted p<0.05 plus a positive bootstrap interval). None survives either Bonferroni or Benjamini-Hochberg FDR correction across 45 tests. Store 7 still leads the descriptive ranking at 19.44% lift (95% CI: 4.20% to 36.46%; nominal p=0.0166), making it a controlled-pilot candidate rather than a rollout decision.
- Thanksgiving is the strongest directional holiday type (+41.3% versus regular weeks), but it has only two occurrences. Super Bowl has three (+3.6%), Labor Day three (+0.1%), and the post-Christmas flag two (-7.7%). These are descriptive, not causal.
- On the final 20-week aggregate holdout, feature OLS achieves 1.87% MAPE and $1.11M RMSE versus seasonal naive at 2.24% and $1.31M. Across 46 evaluated scopes, OLS wins 24 and seasonal naive wins 22—evidence that the more complex model is not universally better.
- The pooled store-fixed-effects OLS has R²=0.920 and a positive holiday coefficient of $77,786 (HC3 95% CI: $55,229 to $100,342; p<0.001). This is a conditional association; correlated time trends and omitted variables prevent causal interpretation.

## What is implemented

- SQLite load and governed SQL reporting views
- Descriptive SQL using CTEs, windows, segmentation, and holiday-type labelling
- Normality checks, Welch/Mann–Whitney selection, bootstrap lift intervals
- Per-store robust OLS and pooled store fixed-effects OLS
- Time-based 20-week holdout with seasonal-naive and feature-OLS forecasts
- Automated data/schema/regression tests
- Six-tab offline Chart.js dashboard with confidence and model-evaluation views
- Power BI build package with theme, Power Query imports, DAX measures, six-page layout and validation checklist

## Run from a clean checkout

```bash
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
```

On macOS/Linux, the wrapper is also available:

```bash
sh scripts/run_pipeline.sh
```

The command rebuilds the database, SQL exports, statistical tests, forecasts, consolidated dashboard, one-page PDF, and test suite. Then open `dashboard/Walmart_Dashboard.html`.

## Repository map

```text
analysis/                 statistical_tests.py, forecast.py
data/                     source CSV and generated SQLite database
dashboard/                generated HTML and data CSVs
docs/                     methodology and hiring-reader one-pager
powerbi/                  Power BI theme, model, DAX and report build specification
scripts/                  loader, SQL runner, dashboard builder, pipeline
sql/                      descriptive analysis and reporting views
tests/                    pipeline regression tests
```

## Limitations

There are only 10 flagged calendar weeks; each holiday type occurs 2–3 times. Rows across stores in the same week share shocks and are not fully independent. Macro variables are observational and collinear with time. Forecast evaluation is one 20-week historical holdout, not repeated backtesting. The feature model uses observed holdout macro values, so operational deployment would require macro forecasts or scenarios. See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for assumptions and failure modes.

For true markdown ROI or price elasticity, add product-level price, markdown exposure, units, margin, inventory, and control-group data.
