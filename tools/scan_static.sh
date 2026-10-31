#!/usr/bin/env bash
# CR1 Task 2 — static analysis. Three tools, because one is not enough.
cd "$(dirname "$0")/.." || exit 1
mkdir -p lab/out
echo "== bandit =="
bandit -r vulnshop -f json -o lab/out/bandit.json -q 2>/dev/null
bandit -r vulnshop -q 2>/dev/null | tee lab/out/bandit.txt
echo; echo "== ruff (security + blind-except) =="
ruff check --select S,BLE --no-cache vulnshop 2>&1 | tee lab/out/ruff.txt
echo; echo "== templates =="
python3 tools/scan_templates.py | tee lab/out/templates.txt
echo; echo "Reports written to lab/out/"
