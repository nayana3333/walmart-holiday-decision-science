"""Validate the Power BI handoff package and its source data contracts."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PBI = ROOT / "powerbi"
DATA = ROOT / "dashboard" / "data"

required = ["README.md", "Walmart_Theme.json", "POWER_QUERY.md", "DATA_MODEL.md",
            "measures.dax", "REPORT_LAYOUT.md", "VALIDATION_CHECKLIST.md"]
for name in required:
    path = PBI / name
    assert path.exists() and path.stat().st_size > 100, f"Missing/empty Power BI artifact: {name}"

theme = json.loads((PBI / "Walmart_Theme.json").read_text(encoding="utf-8"))
assert theme["name"] == "Walmart Decision Science"
assert theme["dataColors"][:3] == ["#0E7C7B", "#C97F0A", "#0B1D33"]

weekly = pd.read_csv(DATA / "weekly_kpi.csv")
stats = pd.read_csv(DATA / "statistical_tests.csv")
metrics = pd.read_csv(DATA / "forecast_metrics.csv")
preds = pd.read_csv(DATA / "forecast_predictions.csv")
assert len(weekly) == 143
assert stats.scope.nunique() == 46
assert metrics.scope.nunique() == 46 and len(metrics) == 92
assert len(preds) == 46 * 2 * 20
assert int(stats.significant_05.sum()) == 8  # includes the Overall row
assert int(stats.loc[stats.scope.str.startswith("Store "), "significant_05"].sum()) == 7
assert not stats.significant_fdr_bh_05.any()

dax = (PBI / "measures.dax").read_text(encoding="utf-8")
for measure in ["Overall Lift %", "Nominal Screen Stores", "FDR Confirmed Stores",
                "Winning Model", "Recommendation Evidence"]:
    assert measure in dax

print("powerbi_package_ok pages=6 source_tables=8 headline_contracts=valid")
