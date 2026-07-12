# Quality Assurance Notes

## Independent headline recomputation

`qa/independent_recompute.py` reads `data/Walmart.csv` directly and does not import any existing analysis function. It independently recomputes:

- Holiday rows: 450; regular rows: 5,985
- Mean-sales lift: 7.839713%
- Seeded 5,000-draw bootstrap 95% interval: 2.079147% to 13.666078%

These match the committed headline values of 7.84% and 2.08%-13.67%. A pipeline test fails if they diverge.

## Why only 7 of 45 pass the nominal screen

Every store has 10 holiday observations and 133 regular observations. The holiday group is therefore small and noisy: across stores, its median standard deviation is $209,974, versus $118,498 for regular weeks. Holiday-week standard deviations range from $28,308 to $484,339. Store 7, for example, has standard deviations of $149,504 on holiday weeks and $106,151 on regular weeks. Wide uncertainty intervals are expected with only 10 high-variance holiday observations.

Eight stores have an unadjusted two-sided p-value below 0.05. The dashboard's original screen also requires a positive bootstrap interval, leaving 7 of 45. That is a **nominal exploratory result**, not a family-wise significance claim.

The original analysis did not adjust the 45 store tests for multiple comparisons. QA now applies both Bonferroni correction (controls the chance of any false positive) and Benjamini-Hochberg FDR correction (controls the expected false-discovery share). At alpha=0.05:

- Nominal p<0.05: 8 stores
- Nominal p<0.05 plus positive lift interval: 7 stores
- Bonferroni significant: 0 stores
- Benjamini-Hochberg FDR significant: 0 stores

The statistical export now contains both adjusted p-values and rejection flags. README, methodology, dashboard labels, and the one-pager were corrected to describe Store 7 as an exploratory controlled-pilot candidate, not a confirmed discovery.

## Forecast split and metric checks

The final 20 dates, 2012-06-15 through 2012-10-26, are held out. Training uses earlier dates only; lag-52 points in the holdout refer to the prior year, so target dates do not overlap training targets.

| Scope | Model | MAPE | RMSE |
|---|---|---:|---:|
| Aggregate | Seasonal naive | 2.2447% | $1,307,252 |
| Aggregate | Feature OLS | 1.8728% | $1,105,185 |
| Store 7 | Seasonal naive | 3.6808% | $29,038 |
| Store 7 | Feature OLS | 10.0307% | $66,533 |

No value is implausibly close to zero. Aggregate error is lower than many store errors because positive and negative store-level errors partially offset when summed. Store 7 also demonstrates that the feature model is not mechanically favored. One limitation remains: OLS uses observed holdout macro values, which is documented and would require scenario/forecast inputs in production.

## Dashboard checks

The Browser tool rejected direct automation of the local `file://` URL under its security policy, so no claim of a headless visual render is made. Instead, `qa/dashboard_dom_check.py` performs the allowed manual/static DOM and data-contract check and is part of pytest. It verifies:

- Exactly six tabs and six matching page sections
- Seven chart canvases and five populated table targets
- Non-empty real datasets for KPIs, holiday lift/type, statistics, regression, forecasts, and recommendations
- Every canvas/table DOM ID is referenced by population code
- No literal `undefined` or `NaN` table cell in the generated HTML

The generated HTML was also rebuilt successfully. This verifies DOM/data wiring, but it is not pixel-level browser rendering; that limitation is explicit.

## PDF checks

`docs/ONE_PAGER.pdf` was generated from `scripts/build_one_pager.py`, inspected with Poppler, and rendered to PNG for visual review. It is one A4 page with no clipping, overlap, or unreadably small text. Its navy/teal/amber design remains distinguishable through hierarchy and borders when printed without color.

## Clean-environment packaging check

The exact pinned `requirements.txt` installed successfully into a new Python 3.13 virtual environment. A disposable local clone contained no SQLite database; `python scripts/run_pipeline.py` regenerated it from `data/Walmart.csv`, rebuilt all outputs and the PDF, and passed all 7 tests with no manual fixes. README heading levels, fenced commands, relative links, and Markdown table syntax were checked for GitHub-compatible rendering.
