"""Cross-platform, one-command project pipeline."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STEPS = [
    [sys.executable, "scripts/build_db.py"],
    [sys.executable, "scripts/run_all_sql.py"],
    [sys.executable, "analysis/statistical_tests.py"],
    [sys.executable, "analysis/forecast.py"],
    # Consolidate again now that statistical/forecast files exist.
    [sys.executable, "scripts/run_all_sql.py"],
    [sys.executable, "scripts/build_dashboard.py"],
    [sys.executable, "scripts/build_one_pager.py"],
    [sys.executable, "-m", "pytest", "-q"],
]

for command in STEPS:
    print(f"\n>>> {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)

print("\nPipeline completed successfully.")
