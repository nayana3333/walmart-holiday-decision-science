# Power Query Imports

Create a text parameter named `ProjectRoot`, for example:

```text
C:\Pricing\Walmart_Holiday_Pricing_Project\walmart_project
```

Create a blank query named `CsvFromProject` and paste:

```powerquery
(FileName as text) as table =>
let
    Path = ProjectRoot & "\\dashboard\\data\\" & FileName,
    Source = Csv.Document(File.Contents(Path), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    Headers
```

Create the following queries. After each source step, use **Detect Data Type**, then verify against `DATA_MODEL.md`.

```powerquery
WeeklyKPI = CsvFromProject("weekly_kpi.csv")
HolidayImpact = CsvFromProject("holiday_impact.csv")
HolidayTypes = CsvFromProject("holiday_type_breakdown.csv")
StatisticalTests = CsvFromProject("statistical_tests.csv")
RegressionResults = CsvFromProject("regression_results.csv")
ForecastPredictions = CsvFromProject("forecast_predictions.csv")
ForecastMetrics = CsvFromProject("forecast_metrics.csv")
StoreSegmentation = CsvFromProject("store_segmentation.csv")
```

Add calculated store keys in Power Query:

```powerquery
// StatisticalTests
= Table.AddColumn(PreviousStep, "store_id", each if Text.StartsWith([scope], "Store ") then Number.FromText(Text.AfterDelimiter([scope], "Store ")) else null, Int64.Type)
```

```powerquery
// ForecastPredictions and ForecastMetrics
= Table.AddColumn(PreviousStep, "store_id", each if Text.StartsWith([scope], "Store ") then Number.FromText(Text.AfterDelimiter([scope], "Store ")) else null, Int64.Type)
```

For boolean CSV columns, replace text `True`/`False` with logical values in Power Query before loading.
