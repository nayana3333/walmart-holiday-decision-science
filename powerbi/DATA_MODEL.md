# Data Model

Use a small star-style model. Avoid bidirectional filtering.

## Dimension

Create this DAX table:

```DAX
DimStore = GENERATESERIES(1, 45, 1)
```

Rename `Value` to `store_id` and set it to Whole Number.

## Relationships

| From | To | Cardinality | Direction |
|---|---|---|---|
| DimStore[store_id] | HolidayImpact[store_id] | 1:* | Single |
| DimStore[store_id] | StoreSegmentation[store_id] | 1:* | Single |
| DimStore[store_id] | StatisticalTests[store_id] | 1:* | Single |
| DimStore[store_id] | RegressionResults[store_id] | 1:* | Single |
| DimStore[store_id] | ForecastPredictions[store_id] | 1:* | Single |
| DimStore[store_id] | ForecastMetrics[store_id] | 1:* | Single |

`WeeklyKPI` and `HolidayTypes` remain disconnected reporting tables. Aggregate forecast rows have a blank `store_id` and are selected using `scope = "Aggregate"`.

## Types

- `date`: Date
- Store IDs, ranks, sample counts and weeks: Whole Number
- Sales, coefficients, confidence bounds, p-values, R-squared, MAPE and RMSE: Decimal Number
- Winner and significance flags: True/False
- Scope, model, test, recommendation and interpretation: Text

Hide technical columns not needed by report users, including Shapiro p-values, test statistics, and raw caveat duplication. Keep them in the model for auditability.
