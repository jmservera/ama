---
title: Issue 126 AI running-cost line changes
ms.date: 2026-11-14
---

* `governance.py`: `_ai_cost_figures` (Decimal, rejects negative or non-numeric input, never 0 for missing data); `benefits_record` accepts optional `ai_total_cost` and `ai_accepted_outcomes`; `release_record` stores an `ai_running_cost` snapshot.
* `test_governance.py`: two tests (Unknown-not-zero and validation; release carries the line).
* Validation: `PYTHONPATH=tests:src TMPDIR=/dev/shm/zf-tmp python3 -m unittest test_governance` 75 tests OK (16 skipped, SQL); `ruff check` and `mypy` clean. `unittest discover` not run, by instruction.
