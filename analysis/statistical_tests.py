"""Statistical validation for holiday lift and macroeconomic sensitivity."""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "Walmart.csv"
OUTPUT = ROOT / "dashboard" / "data"
RNG = np.random.default_rng(42)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def bootstrap_lift_ci(holiday: np.ndarray, regular: np.ndarray, draws: int = 5000) -> tuple[float, float]:
    """Percentile CI for percent lift; retains the business metric's scale."""
    h = RNG.choice(holiday, (draws, len(holiday)), replace=True).mean(axis=1)
    r = RNG.choice(regular, (draws, len(regular)), replace=True).mean(axis=1)
    lift = (h - r) / r * 100
    return tuple(np.percentile(lift, [2.5, 97.5]))


def test_group(label: str, group: pd.DataFrame) -> dict:
    holiday = group.loc[group.holiday_flag.eq(1), "weekly_sales"].to_numpy()
    regular = group.loc[group.holiday_flag.eq(0), "weekly_sales"].to_numpy()
    # Shapiro is sensitive and only defined up to 5,000 observations in SciPy.
    hp = stats.shapiro(holiday[:5000]).pvalue
    rp = stats.shapiro(regular[:5000]).pvalue
    normal = hp >= 0.05 and rp >= 0.05
    if normal:
        result = stats.ttest_ind(holiday, regular, equal_var=False)
        method = "Welch two-sample t-test"
        statistic, p_value = result.statistic, result.pvalue
    else:
        result = stats.mannwhitneyu(holiday, regular, alternative="two-sided")
        method = "Mann-Whitney U"
        statistic, p_value = result.statistic, result.pvalue
    lift = (holiday.mean() - regular.mean()) / regular.mean() * 100
    lo, hi = bootstrap_lift_ci(holiday, regular)
    return {
        "scope": label, "n_holiday": len(holiday), "n_regular": len(regular),
        "avg_holiday_sales": holiday.mean(), "avg_regular_sales": regular.mean(),
        "lift_pct": lift, "ci_lower_pct": lo, "ci_upper_pct": hi,
        "normality_p_holiday": hp, "normality_p_regular": rp,
        "test_method": method, "statistic": statistic, "p_value": p_value,
        "significant_05": bool(p_value < 0.05 and lo > 0),
        "caveat": "Only 10 flagged weeks overall; individual holiday types occur 2-3 times.",
    }


def regression_rows(df: pd.DataFrame) -> list[dict]:
    rows: list[dict] = []
    formula = "weekly_sales ~ fuel_price + cpi + unemployment + holiday_flag"
    for store_id, group in df.groupby("store_id"):
        model = smf.ols(formula, data=group).fit(cov_type="HC3")
        fit_quality = "low" if model.rsquared < 0.20 else "moderate" if model.rsquared < 0.50 else "strong"
        for term in ["fuel_price", "cpi", "unemployment", "holiday_flag"]:
            rows.append({"scope": f"Store {store_id}", "store_id": store_id, "term": term,
                         "coefficient": model.params[term], "p_value": model.pvalues[term],
                         "ci_lower": model.conf_int().loc[term, 0], "ci_upper": model.conf_int().loc[term, 1],
                         "r_squared": model.rsquared, "n_obs": int(model.nobs), "fit_quality": fit_quality})
    pooled = smf.ols(formula + " + C(store_id)", data=df).fit(cov_type="HC3")
    for term in ["fuel_price", "cpi", "unemployment", "holiday_flag"]:
        rows.append({"scope": "Pooled store fixed effects", "store_id": "ALL", "term": term,
                     "coefficient": pooled.params[term], "p_value": pooled.pvalues[term],
                     "ci_lower": pooled.conf_int().loc[term, 0], "ci_upper": pooled.conf_int().loc[term, 1],
                     "r_squared": pooled.rsquared, "n_obs": int(pooled.nobs),
                     "fit_quality": "low" if pooled.rsquared < .2 else "moderate" if pooled.rsquared < .5 else "strong"})
    return rows


def main() -> None:
    try:
        df = pd.read_csv(INPUT).rename(columns={
            "Store": "store_id", "Weekly_Sales": "weekly_sales", "Holiday_Flag": "holiday_flag",
            "Fuel_Price": "fuel_price", "CPI": "cpi", "Unemployment": "unemployment"})
        OUTPUT.mkdir(parents=True, exist_ok=True)
        tests = [test_group("Overall", df)]
        tests.extend(test_group(f"Store {sid}", group) for sid, group in df.groupby("store_id"))
        test_frame = pd.DataFrame(tests)
        store_mask = test_frame.scope.str.startswith("Store ")
        pvals = test_frame.loc[store_mask, "p_value"].to_numpy()
        test_frame["p_bonferroni"] = np.nan
        test_frame["p_fdr_bh"] = np.nan
        test_frame["significant_bonferroni_05"] = False
        test_frame["significant_fdr_bh_05"] = False
        bonf_reject, bonf_p, _, _ = multipletests(pvals, alpha=.05, method="bonferroni")
        fdr_reject, fdr_p, _, _ = multipletests(pvals, alpha=.05, method="fdr_bh")
        test_frame.loc[store_mask, "p_bonferroni"] = bonf_p
        test_frame.loc[store_mask, "p_fdr_bh"] = fdr_p
        test_frame.loc[store_mask, "significant_bonferroni_05"] = bonf_reject
        test_frame.loc[store_mask, "significant_fdr_bh_05"] = fdr_reject
        test_frame.to_csv(OUTPUT / "statistical_tests.csv", index=False, float_format="%.6f")
        pd.DataFrame(regression_rows(df)).to_csv(OUTPUT / "regression_results.csv", index=False, float_format="%.6f")
        logging.info("Exported statistical tests (%d scopes) and regression results.", len(tests))
    except Exception as exc:
        logging.error("Statistical analysis failed: %s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
