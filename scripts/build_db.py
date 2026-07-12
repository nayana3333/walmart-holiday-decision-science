import sqlite3, csv, os, logging
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(SCRIPT_DIR, "..")
DATA_DIR = os.path.join(ROOT, "data")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
 conn = sqlite3.connect(os.path.join(DATA_DIR, "walmart_project.db"))
 cur = conn.cursor()
 cur.executescript("""
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    store_id INTEGER,
    date TEXT,
    week_of_year INTEGER,
    year INTEGER,
    weekly_sales REAL,
    holiday_flag INTEGER,
    temperature REAL,
    fuel_price REAL,
    cpi REAL,
    unemployment REAL
);
""")

 rows = []
 source = os.path.join(DATA_DIR, "Walmart.csv")
 with open(source, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    required = {"Store","Date","Weekly_Sales","Holiday_Flag","Temperature","Fuel_Price","CPI","Unemployment"}
    missing = required - set(reader.fieldnames or [])
    if missing: raise ValueError(f"Walmart.csv is missing columns: {sorted(missing)}")
    for line, r in enumerate(reader, start=2):
      try:
       d = datetime.strptime(r["Date"], "%d-%m-%Y")
       rows.append((
            int(r["Store"]), d.strftime("%Y-%m-%d"), d.isocalendar()[1], d.year,
            float(r["Weekly_Sales"]), int(r["Holiday_Flag"]),
            float(r["Temperature"]), float(r["Fuel_Price"]),
            float(r["CPI"]), float(r["Unemployment"])
       ))
      except (KeyError, ValueError) as exc:
       raise ValueError(f"Malformed Walmart.csv row {line}: {exc}") from exc

 cur.executemany("INSERT INTO sales VALUES (?,?,?,?,?,?,?,?,?,?)", rows)
 cur.execute("CREATE INDEX idx_store ON sales(store_id)")
 cur.execute("CREATE INDEX idx_date ON sales(date)")
 conn.commit(); conn.close()
 logging.info("Loaded %d rows -> walmart_project.db", len(rows))

if __name__ == "__main__":
 try: main()
 except Exception as exc:
  logging.error("Database build failed: %s", exc); raise SystemExit(1) from exc
