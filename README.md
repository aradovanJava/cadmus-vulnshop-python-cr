# cadmus-vulnshop-cr

**CADMUS-CR-15 · Secure Coding Python · Cyber Range nodes CR1–CR4**

A deliberately vulnerable Flask storefront used across all four Cyber Range nodes.

## ⚠ Sandbox rules — read before you start

This application is **intentionally exploitable** and contains at least one
**unauthenticated remote code execution path**.

- It binds to `127.0.0.1` only. **Do not change the host.**
- Do not expose it beyond this machine. Do not put it on a network.
- Do not enter real data — every seed address is `.invalid`.
- Reset state with `rm -f vulnshop.db`.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install bandit ruff pip-audit          # the lab tool chain
python tools/verify_env.py                 # run this first
```

## Running

```bash
bash tools/run_app.sh          # http://127.0.0.1:8080/shop
```

Training accounts: `alice`, `bob`, `carol`, `adminjoe` — all with password `Password123`.

## Scanning

```bash
bash tools/scan_static.sh      # bandit + ruff + template scanner
bash tools/scan_deps.sh        # pip-audit (needs network)
```

Reports are written to `lab/out/`.

## Two tiers

| Tier | Package | What it is |
|---|---|---|
| REST API | `vulnshop/api` | JSON endpoints under `/api/**` |
| MVC + Jinja2 | `vulnshop/mvc` | Server-rendered storefront, account area, checkout, admin, support |

Weaknesses are injected in both, and several live in the Jinja2 templates rather than in
any `.py` file.

## Node map

| Node | What you do here |
|---|---|
| **CR1** | Find and classify weaknesses. Do not fix anything. |
| **CR2** | Remediate, against automated checkpoint tests. |
| **CR3** | Dependency triage, remediation, SBOM and VEX. |
| **CR4** | Build the pipeline that stops all of it recurring. |

Record your CR1 findings in `lab/FINDINGS.md` — CR2 grades you on fixing what you found.
