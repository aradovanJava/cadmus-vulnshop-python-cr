# CR1 — Findings Record

**Name:** ______________________   **Date:** ____________

## Task 1 · Orientation

1. How many distinct HTTP entry points did you find by clicking around?

2. Which pages change behaviour depending on who is logged in?

3. Which page displays something that another user could have written?

## Task 2 · Static analysis triage

Decide your own severity *before* you read the tool's column.

| # | Rule | Location | Tool sev. | Verdict | My sev. | Why they differ |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |

Verdict codes: **TP** real and reachable · **FP-scope** right pattern, wrong place ·
**FP-context** safe here, say why · **DIS** disputed, name the fact you need ·
**NOT-SEC** real issue, not a security issue

## Task 3 · Dependencies

Declared in `requirements.txt`: ______   Resolved in the environment: ______

| Component | Advisory | CVSS | Reachable? | Evidence — how you checked |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

My remediation order:

If it differs from severity order, why? *(This sentence is the finding.)*

## Task 4 · Manual inspection

Target: at least four weaknesses that produced no tool finding. There are eighteen.

| Weakness | File | OWASP 2025 | Which question found it |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

## Task 5 · One finding in full

**ID:** VULN-______  **Category:** A____  **Severity:** ______  **Reachable by:** ______

**Title — the weakness, not the symptom**

**1 · Location** — file, line, who can reach it, and where else the same shape occurs

**2 · Root cause, stated as a decision**
*Not "the check is missing" but "we never specified who may read an order that is not their own."*

**3 · Impact in this application** — what an attacker can do, with what access, to what data

**4 · Proposed remediation** — name the pattern, and why that one

**5 · Cost** — what must change outside this file

**6 · Proof** — the test that fails now and passes after

## Final tally

Tool findings I triaged: ______   Weaknesses the tools missed: ______
