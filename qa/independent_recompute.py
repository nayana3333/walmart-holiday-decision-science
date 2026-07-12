"""Independent QA recomputation; intentionally does not import project analysis code."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "Walmart.csv")
holiday = df.loc[df.Holiday_Flag.eq(1), "Weekly_Sales"].to_numpy()
regular = df.loc[df.Holiday_Flag.eq(0), "Weekly_Sales"].to_numpy()
lift = (holiday.mean() - regular.mean()) / regular.mean() * 100
rng = np.random.default_rng(42)
h_draws = rng.choice(holiday, (5000, len(holiday)), replace=True).mean(axis=1)
r_draws = rng.choice(regular, (5000, len(regular)), replace=True).mean(axis=1)
ci = np.percentile((h_draws - r_draws) / r_draws * 100, [2.5, 97.5])

print(f"overall_lift_pct={lift:.6f}")
print(f"bootstrap_ci_95_pct={ci[0]:.6f},{ci[1]:.6f}")

if not (np.isclose(lift, 7.839713, atol=5e-6) and
        np.allclose(ci, [2.079147, 13.666078], atol=5e-6)):
    raise SystemExit("Independent QA result does not match the committed headline result.")
