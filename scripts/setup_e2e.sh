#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt
# Install Playwright browsers and dependencies
python -m playwright install --with-deps

echo "Playwright setup complete. Run: pytest items/tests_e2e/test_loader_back.py -q"