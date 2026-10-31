#!/usr/bin/env python3
"""Environment check. Run this first — there is no slack in a 60-minute node."""
import importlib, shutil, subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True

def check(label, condition, detail=""):
    global ok
    print("  %-28s %s %s" % (label, "OK     " if condition else "MISSING", detail))
    if not condition:
        ok = False

print("=" * 62)
print(" CR ENVIRONMENT CHECK · cadmus-vulnshop-cr")
print("=" * 62)
check("Python >= 3.11", sys.version_info >= (3, 11), sys.version.split()[0])
for mod in ("flask", "jinja2", "yaml"):
    try:
        importlib.import_module(mod); check("module: " + mod, True)
    except ImportError:
        check("module: " + mod, False, "pip install -r requirements.txt")
for exe in ("bandit", "ruff", "pip-audit"):
    check("tool: " + exe, shutil.which(exe) is not None, "" if shutil.which(exe) else "pip install " + exe)
check("templates/ present", os.path.isdir(os.path.join(ROOT, "templates")))
check("lab/FINDINGS.md present", os.path.isfile(os.path.join(ROOT, "lab", "FINDINGS.md")))
try:
    sys.path.insert(0, ROOT)
    from vulnshop import create_app
    app = create_app()
    r = app.test_client().get("/shop")
    check("app responds", r.status_code == 200, "GET /shop -> %d" % r.status_code)
except Exception as exc:
    check("app responds", False, str(exc)[:40])
print("=" * 62)
print(" ALL CHECKS PASSED" if ok else " SOMETHING IS MISSING — tell your instructor now")
sys.exit(0 if ok else 1)
