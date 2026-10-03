#!/usr/bin/env bash
# One-time setup for macOS and Linux.
# Usage (from the repo folder):   bash scripts/setup.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== 5350 Chatbot Labs setup (macOS / Linux) =="

# 1. Find a Python 3.10+
PY=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && \
     "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    PY="$candidate"; break
  fi
done
if [ -z "$PY" ]; then
  echo "ERROR: Python 3.10 or newer was not found."
  echo "  macOS:  install from https://www.python.org/downloads/  (or: brew install python)"
  echo "  Ubuntu: sudo apt install python3 python3-venv python3-pip"
  exit 1
fi
echo "Using $($PY --version)"

# 2. Create the virtual environment
if [ ! -d .venv ]; then
  echo "Creating virtual environment in .venv ..."
  "$PY" -m venv .venv || { echo "ERROR: could not create .venv. On Ubuntu run: sudo apt install python3-venv"; exit 1; }
fi

# 3. Install packages
echo "Installing packages (this can take a few minutes) ..."
.venv/bin/python -m pip install --quiet --upgrade pip
.venv/bin/python -m pip install --quiet -r requirements.txt

# 4. Create .env and (optionally) store the API key
if [ ! -f .env ]; then
  cp .env.sample .env
  echo "Created .env from .env.sample"
fi
if grep -q 'OPENAI_API_KEY="sk-\.\.\."' .env; then
  echo
  echo "Paste your OpenAI API key and press Enter (typing is hidden)."
  echo "Press Enter without typing to skip and edit .env later."
  read -r -s -p "OPENAI_API_KEY: " KEY; echo
  if [ -n "$KEY" ]; then
    .venv/bin/python - "$KEY" <<'PYEOF'
import sys, pathlib
p = pathlib.Path(".env")
p.write_text(p.read_text().replace('OPENAI_API_KEY="sk-..."', f'OPENAI_API_KEY="{sys.argv[1].strip()}"'))
PYEOF
    echo "Saved key to .env (this file is never committed to git)."
  fi
fi

# 5. Verify
echo
.venv/bin/python run.py check || true
echo
echo "Next: bash scripts/run.sh lab1        (or: make lab1)"
