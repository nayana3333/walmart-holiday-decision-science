#!/usr/bin/env sh
set -eu
PYTHON="${PYTHON:-python3}"
"$PYTHON" scripts/run_pipeline.py
