"""Time-based holdout evaluation: seasonal naive versus feature regression."""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dashboard" / "data"
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def metrics(actual: pd.Series, predicted: pd.Series) -> tuple[float, float]:
    err = actual.to_numpy() - predicted.to_numpy()
    return float(np.mean(np.abs(err / actual.to_numpy())) * 100), float(np.sqrt(np.mean(err ** 2)))


def evaluate(scope: str, frame: pd.DataFrame, holdout: int = 20) -> tuple[list[dict], list[dict]]:
    frame = frame.sort_values("date").copy()
    frame["lag_52"] = frame.weekly_sales.shift(52)
    frame["trend"] = np.arange(len(frame))
    usable = frame.dropna(subset=["lag_52"]).copy()
    cutoff = frame.date.iloc[-holdout]
    train, test = usable[usable.date < cutoff], usable[usable.date >= cutoff]
    features = ["lag_52", "holiday_flag", "fuel_price", "cpi", "unemployment", "trend"]
    model = sm.OLS(train.weekly_sales, sm.add_constant(train[features], has_constant="add")).fit()
    predictions = {
        "Seasonal naive (52-week)": test.lag_52,
        "OLS lag + holiday + macro": model.predict(sm.add_constant(test[features], has_constant="add")),
    }
    pred_rows, metric_rows = [], []
    for name, pred in predictions.items():
        mape, rmse = metrics(test.weekly_sales, pred)
        metric_rows.append({"scope": scope, "model": name, "mape_pct": mape, "rmse": rmse,
                            "test_weeks": len(test), "train_weeks": len(train)})
        pred_rows.extend({"scope": scope, "date": d.strftime("%Y-%m-%d"), "actual": a,
                          "predicted": p, "model": name}
                         for d, a, p in zip(test.date, test.weekly_sales, pred))
    winner = min(metric_rows, key=lambda r: r["mape_pct"])["model"]
    for row in metric_rows:
        row["winner"] = row["model"] == winner
        row["interpretation"] = ("Lowest holdout MAPE for this scope." if row["winner"] else
                                  "Challenger retained for comparison.")
    return pred_rows, metric_rows


def main() -> None:
    try:
        df = pd.read_csv(ROOT / "data" / "Walmart.csv", parse_dates=["Date"], dayfirst=True).rename(columns={
            "Store": "store_id", "Date": "date", "Weekly_Sales": "weekly_sales",
            "Holiday_Flag": "holiday_flag", "Fuel_Price": "fuel_price", "CPI": "cpi",
            "Unemployment": "unemployment"})
        scopes = [("Aggregate", df.groupby("date", as_index=False).agg(
            weekly_sales=("weekly_sales", "sum"), holiday_flag=("holiday_flag", "max"),
            fuel_price=("fuel_price", "mean"), cpi=("cpi", "mean"), unemployment=("unemployment", "mean")))]
        scopes += [(f"Store {sid}", group) for sid, group in df.groupby("store_id")]
        predictions, metric_rows = [], []
        for name, group in scopes:
            p, m = evaluate(name, group)
            predictions.extend(p); metric_rows.extend(m)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(predictions).to_csv(OUTPUT / "forecast_predictions.csv", index=False, float_format="%.4f")
        pd.DataFrame(metric_rows).to_csv(OUTPUT / "forecast_metrics.csv", index=False, float_format="%.4f")
        logging.info("Evaluated two models across %d scopes using a 20-week holdout.", len(scopes))
    except Exception as exc:
        logging.error("Forecast evaluation failed: %s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
