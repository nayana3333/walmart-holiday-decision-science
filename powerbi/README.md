# Power BI Report Package

This folder is the build specification for `Walmart_Holiday_Decision_Dashboard.pbix`. Power BI is a presentation layer only: all statistical and forecast outputs are produced and tested by the Python/SQL pipeline.

## Before opening Power BI

From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
```

## Build the report

1. Open Power BI Desktop and create a blank report.
2. Import [Walmart_Theme.json](Walmart_Theme.json) using **View > Themes > Browse for themes**.
3. Create a text parameter named `ProjectRoot` containing the absolute path to this repository.
4. Add the queries from [POWER_QUERY.md](POWER_QUERY.md). Apply changes.
5. Create the relationships documented in [DATA_MODEL.md](DATA_MODEL.md).
6. Add the measures from [measures.dax](measures.dax).
7. Build the six pages using [REPORT_LAYOUT.md](REPORT_LAYOUT.md).
8. Run every check in [VALIDATION_CHECKLIST.md](VALIDATION_CHECKLIST.md).
9. Save the finished file here as `Walmart_Holiday_Decision_Dashboard.pbix`.

## Required pages

1. Executive Overview
2. Holiday Impact
3. Holiday Type Breakdown
4. Economic Sensitivity
5. Forecast & Model Evaluation
6. Store Recommendations

## Evidence language

Use these phrases consistently:

- Overall flagged-week association: **7.84%** (95% CI: **2.08% to 13.67%**)
- Seven stores pass the **nominal exploratory screen**
- **Zero** stores survive Bonferroni or FDR correction
- Store 7 is a **controlled-pilot candidate**, not an automatic rollout
- Results do not estimate causal markdown ROI because price, markdown, margin and SKU fields are absent

## Sharing

Commit the `.pbix` only if it is comfortably within the repository host's file-size limit. Always include exported PDF/screenshots because reviewers may not have Power BI Desktop.
