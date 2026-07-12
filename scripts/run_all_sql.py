import sqlite3, csv, os, json, logging

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(SCRIPT_DIR, "..")
DB = os.path.join(ROOT, "data", "walmart_project.db")
SQL_DIR = os.path.join(ROOT, "sql")
EXPORT_DIR = os.path.join(ROOT, "dashboard", "data")
os.makedirs(EXPORT_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
conn = sqlite3.connect(DB)
cur = conn.cursor()

def run(path, label, export_name=None, script=False):
    with open(path, encoding="utf-8") as source: sql = source.read()
    if script:
        cur.executescript(sql); conn.commit()
        print(f"--- {label} --- executed")
        return
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    print(f"--- {label} --- ({len(rows)} rows)")
    print(" | ".join(cols))
    for r in rows[:3]: print(" | ".join(str(v) for v in r))
    if export_name:
        with open(os.path.join(EXPORT_DIR, export_name), "w", newline="") as f:
            w = csv.writer(f); w.writerow(cols); w.writerows(rows)
    return cols, rows

run(f"{SQL_DIR}/01_holiday_impact.sql", "Holiday Impact", "holiday_impact.csv")
run(f"{SQL_DIR}/02_economic_sensitivity.sql", "Economic Sensitivity", "economic_sensitivity.csv")
run(f"{SQL_DIR}/03_store_segmentation.sql", "Store Segmentation", "store_segmentation.csv")
run(f"{SQL_DIR}/04_views.sql", "Views", script=True)
run(f"{SQL_DIR}/05_holiday_type_breakdown.sql", "Holiday Type Breakdown", "holiday_type_breakdown.csv")

cols, rows = run("/dev/null", "skip") if False else (None, None)
for view, name in [("vw_weekly_kpi","weekly_kpi.csv"), ("vw_store_segmentation","store_segmentation_view.csv")]:
    cur.execute(f"SELECT * FROM {view}")
    rows = cur.fetchall(); cols = [d[0] for d in cur.description]
    with open(os.path.join(EXPORT_DIR, name), "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols); w.writerows(rows)
    print(f"Exported {view} -> {name}")

conn.close()

# Consolidate for dashboard
def load_csv(fn):
    with open(os.path.join(EXPORT_DIR, fn)) as f:
        return list(csv.DictReader(f))

data = {
    "holiday_impact": load_csv("holiday_impact.csv"),
    "economic_sensitivity": load_csv("economic_sensitivity.csv"),
    "store_segmentation": load_csv("store_segmentation.csv"),
    "weekly_kpi": load_csv("weekly_kpi.csv"),
    "holiday_type_breakdown": load_csv("holiday_type_breakdown.csv"),
}
for key, filename in [("statistical_tests", "statistical_tests.csv"),
                      ("regression_results", "regression_results.csv"),
                      ("forecast_predictions", "forecast_predictions.csv"),
                      ("forecast_metrics", "forecast_metrics.csv")]:
    path = os.path.join(EXPORT_DIR, filename)
    data[key] = load_csv(filename) if os.path.exists(path) else []
with open(os.path.join(SCRIPT_DIR, "dashboard_data.json"), "w") as f:
    json.dump(data, f)
print("Dashboard data consolidated.")
