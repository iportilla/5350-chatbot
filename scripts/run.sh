#!/usr/bin/env bash
# Run a lab without activating anything.
# Usage:  bash scripts/run.sh lab2      (bash scripts/run.sh  -> list of labs)
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -x .venv/bin/python ]; then
  echo "The course environment isn't set up yet. Run:  bash scripts/setup.sh"
  exit 1
fi
exec .venv/bin/python run.py "$@"
