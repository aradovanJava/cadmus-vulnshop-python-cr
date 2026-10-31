#!/usr/bin/env python3
"""
Template security scanner — the third tool in the CR1 chain.

Bandit and ruff read Python only. Three of the injected weaknesses live in
Jinja2 templates and are invisible to both. This scanner closes that gap by
reporting one thing: a variable rendered through the |safe filter, which
disables the auto-escaping that Jinja2 gives you for free.

It deliberately does NOT report anything else. Everything else in the
templates is yours to find by reading.

    python tools/scan_templates.py [--json]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")
SAFE_FILTER = re.compile(r"\{\{\s*([^}]+?)\|\s*safe\s*\}\}")


def scan():
    findings = []
    for dirpath, _, files in os.walk(TEMPLATES):
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT)
            with open(path, encoding="utf-8") as fh:
                for lineno, line in enumerate(fh, 1):
                    for m in SAFE_FILTER.finditer(line):
                        findings.append({
                            "rule": "TPL001",
                            "name": "unescaped_output",
                            "severity": "MEDIUM",
                            "confidence": "HIGH",
                            "cwe": "CWE-79",
                            "file": rel,
                            "line": lineno,
                            "expression": m.group(1).strip(),
                            "code": line.strip(),
                            "message": ("Value rendered with |safe. Jinja2 auto-escaping is "
                                        "disabled for this expression."),
                        })
    return findings


def main():
    findings = scan()
    if "--json" in sys.argv:
        print(json.dumps({"findings": findings}, indent=2))
        return 1 if findings else 0
    print("=" * 72)
    print(" TEMPLATE SECURITY SCAN  ·  cadmus-vulnshop-cr")
    print("=" * 72)
    for f in findings:
        print("\n>> [%s:%s] %s" % (f["rule"], f["name"], f["message"]))
        print("   Severity: %s   Confidence: %s   %s" % (f["severity"], f["confidence"], f["cwe"]))
        print("   Location: %s:%d" % (f["file"], f["line"]))
        print("   Expression: %s" % f["expression"])
        print("   %s" % f["code"])
    print("\n" + "-" * 72)
    print("%d finding(s). The scanner reports |safe and nothing else —" % len(findings))
    print("the rest of the template weaknesses are found by reading.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
