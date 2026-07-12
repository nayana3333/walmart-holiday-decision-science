from pathlib import Path
import sqlite3
import subprocess
import sys

import pandas as pd
from pandas.api.types import is_float_dtype, is_integer_dtype

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EXPORT = ROOT / "dashboard" / "data"


def source():
    return pd.read_csv(DATA / "Walmart.csv")


def test_loaded_row_count_matches_source():
    with sqlite3.connect(DATA / "walmart_project.db") as conn:
        assert conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == len(source()) == 6435


def test_key_columns_have_no_nulls():
    keys = ["Store", "Date", "Weekly_Sales", "Holiday_Flag"]
    assert not source()[keys].isna().any().any()


def test_ten_distinct_flagged_holiday_weeks():
    df = source()
    assert df.loc[df.Holiday_Flag.eq(1), "Date"].nunique() == 10


def test_lift_export_recomputes_from_raw():
    df = source()
    means = df.groupby(["Store", "Holiday_Flag"]).Weekly_Sales.mean().unstack()
    expected = ((means[1] - means[0]) / means[0] * 100).round(1).sort_index()
    actual = pd.read_csv(EXPORT / "holiday_impact.csv").set_index("store_id").holiday_lift_pct.sort_index()
    pd.testing.assert_series_equal(actual, expected, check_names=False)


def test_schema_types_and_analysis_outputs():
    df = source()
    assert is_integer_dtype(df.Store) and is_integer_dtype(df.Holiday_Flag)
    assert all(is_float_dtype(df[c]) for c in ["Weekly_Sales", "Fuel_Price", "CPI", "Unemployment"])
    for name in ["statistical_tests.csv", "regression_results.csv", "forecast_predictions.csv", "forecast_metrics.csv"]:
        path = EXPORT / name
        assert path.exists() and path.stat().st_size > 100


def test_independent_headline_recomputation():
    result = subprocess.run([sys.executable, str(ROOT / "qa" / "independent_recompute.py")],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "overall_lift_pct=7.839713" in result.stdout


def test_dashboard_dom_and_data_contract():
    result = subprocess.run([sys.executable, str(ROOT / "qa" / "dashboard_dom_check.py")],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "dashboard_contract_ok tabs=6" in result.stdout
