---
title: ci-affected Cycle 2 formatting correction review
ms.date: 2026-11-14
---

## Review

Execution: executed once. Outcome: conformant, no open findings.

* Local runs of the exact CI commands exit 0: `test_ci_affected.py` (25 tests OK), `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, and `ruff format --isolated --line-length 100 --check` on the four files.
* No `.pyc` files are tracked.
* Focused tier. Not run: full gate; hosted CI for the exact head; nothing pushed.
