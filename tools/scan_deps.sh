#!/usr/bin/env bash
# CR1 Task 3 / CR3 — dependency analysis. Needs network access.
cd "$(dirname "$0")/.." || exit 1
mkdir -p lab/out
echo "== declared vs resolved =="
grep -cvE '^\s*(#|$)' requirements.txt | xargs echo "declared in requirements.txt:"
pip freeze 2>/dev/null | wc -l | xargs echo "resolved in this environment:"
pip freeze > lab/out/dependency-tree.txt 2>/dev/null
echo; echo "== pip-audit =="
pip-audit -r requirements.txt --format json -o lab/out/pip-audit.json 2>/dev/null
pip-audit -r requirements.txt 2>&1 | tee lab/out/pip-audit.txt
