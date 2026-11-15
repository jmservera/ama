---
title: Issue 126 AI running-cost line changes
ms.date: 2026-11-14
---

* `governance.py`: `_ai_cost_figures` (Decimal, rejects negative or non-numeric input, never 0 for missing data); `benefits_record` accepts optional `ai_total_cost` and `ai_accepted_outcomes`; `release_record` stores an `ai_running_cost` snapshot.
* `test_governance.py`: two tests (Unknown-not-zero and validation; release carries the line).
* Validation: `PYTHONPATH=tests:src TMPDIR=/dev/shm/zf-tmp python3 -m unittest test_governance` 75 tests OK (16 skipped, SQL); `ruff check` and `mypy` clean. `unittest discover` not run, by instruction.

## Cycle 2 correction (independent review c1, `c6830b894`)

* Rebased onto `origin/feat/demo-233-same-home-tensions-0825` so the diff holds only Issue 126 changes.
* `release_record`: gate checks and the `ai_running_cost` snapshot now run inside `with self.lock:` so `SqlStore` reloads first; blank snapshot values fall back to `Unknown`.
* `_ai_cost_figures`: total cost of 0 or less is `Unknown`; whitespace is stripped before blank checks; ASCII-only bounded number parsing rejects non-ASCII digits and huge exponents.
* `capture_gate`: requires a dict with non-empty `named_denominator`, `quality_floor`, `total_cost_of_ai` and `cost_per_accepted_outcome`.
* Tests extended (zero, whitespace, superscript digit, huge exponent, boolean). Validation: from `src/core/tests`, `PYTHONPATH=../src:. python3 -m unittest test_governance` 75 OK (16 skipped, SQL); `ruff check` and `ruff format --check` clean. The literal repo-root command fails on a sibling-module import (`test_finance_signoffs`), a pre-existing path issue.
