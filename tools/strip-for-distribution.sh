#!/usr/bin/env bash
# Produces the participant copy of the repository.
# Run this BEFORE placing the app on the participant VM image.
set -e
cd "$(dirname "$0")/.." || exit 1
rm -f VULNERABILITY_MAP.md docs/ANSWER_KEY.md docs/FIXES.md
rm -rf lab/out vulnshop.db __pycache__ .pytest_cache
find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
echo "Instructor material removed. This tree is safe to distribute."
echo "Remaining docs/:"; ls docs/ 2>/dev/null || echo "  (none)"
