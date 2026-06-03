#!/usr/bin/env bash
set -euo pipefail

echo "[run_all] start"

python3 scripts/bench.py --mode vector --n 2000000 --steps 3

if command -v hipcc >/dev/null 2>&1; then
  echo "[run_all] hipcc found, building HIP example"
  hipcc examples/vector_add_hip.cpp -o vector_add_hip
  ./vector_add_hip
else
  echo "[run_all] hipcc not found, skipping HIP example"
fi

echo "[run_all] done"
