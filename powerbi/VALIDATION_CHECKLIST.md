# Validation Checklist

Complete before sharing the PBIX or exporting screenshots/PDF.

## Data

- [ ] Pipeline was run immediately before refresh
- [ ] 143 rows in WeeklyKPI
- [ ] 45 rows in HolidayImpact and StoreSegmentation
- [ ] 46 scopes in StatisticalTests and 46 distinct scopes / 92 model rows in ForecastMetrics
- [ ] 20 holdout dates per scope/model in ForecastPredictions
- [ ] No Power BI query errors

## Headline reconciliation

- [ ] Overall lift = 7.84%
- [ ] Overall CI = 2.08% to 13.67%
- [ ] Nominal screen count = 7 under the project rule
- [ ] Bonferroni count = 0
- [ ] FDR count = 0
- [ ] Store 7 lift = 19.44%
- [ ] Aggregate OLS MAPE = 1.87%
- [ ] Aggregate seasonal-naive MAPE = 2.24%

## Presentation

- [ ] All six pages have data
- [ ] No blank, `(Blank)`, NaN or Infinity in user-facing visuals
- [ ] Currency and percentages have consistent formatting
- [ ] Store and scope slicers work across intended visuals
- [ ] Titles state the decision question, not only the metric name
- [ ] Every page has a concise limitation/evidence note
- [ ] Report remains readable at 100% zoom and in exported PDF
- [ ] Three screenshots exported to `powerbi/screenshots/`

## Submission

- [ ] Save as `powerbi/Walmart_Holiday_Decision_Dashboard.pbix`
- [ ] Refresh and save once more
- [ ] Export report to PDF
- [ ] Confirm PBIX size is accepted by the Git host
- [ ] Add a dashboard screenshot to the main README
