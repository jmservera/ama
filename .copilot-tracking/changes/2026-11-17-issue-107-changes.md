---
title: Issue 107 changes
ms.date: 2026-11-17
---

Status: complete. Probe-before-plan deviation: a measurement probe edit preceded the plan; it was reverted (diff preserved in the evidence dir) before implement-start, then reapplied.

* `src/api/tests/test_assistant_restart_non_replenishment.py`: five added live variations (provider, endpoint, deployment, data, provenance) in `MaterialMismatch.variations()`.
* `docs/reference/log.md`: dated audit entry; no tick or closure.

Validation (FOCUSED, local SQLite proxy only):

* `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p test_assistant_restart_non_replenishment.py -q` in `src/api`: 14 tests OK.
* `ruff format --isolated --line-length 100 --check` on the test file: formatted after one reformat; `ruff check` on the file: all checks passed.
* `mypy` in `src/api`: Success, no issues in 309 source files.
* Not run: rpi-checks.py (full gate held by another job), actual SQL, old image, real AI/Azure, browser (no web change).
