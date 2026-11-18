---
title: Issue 1641 src-ci workflow hash re-pin changes
ms.date: 2026-11-18
---

* `tools/rpi-checks.py`: `WORKFLOW_HASHES["src-ci.yml"]` re-pinned from `4fb913e1ac29...` to `9346fcfb84d15ba69f5449ba55652a51457fd866e709808c7606acd9f62a6b18`, computed with the tool's `digest()` after commit f2f07675b raised the src-ci project job `timeout-minutes` 25 to 45. Other four entries unchanged. No test or doc pins the old hash outside the 2026-11-08 changes record (historical, preserved).
* Cause: full gate preflight failed with `Workflow matrix drift: src-ci.yml` (log `/tmp/gate1641d.log`, retained).
* Classification: gate-tool edit, FULL tier; gate semantics unchanged apart from the pinned hash (check stays strict).
* Validation: `python3 -m unittest tools.test_rpi_checks -q` 109 tests OK; `ruff format --isolated --line-length 100 --check` clean on both tool files; `python3 -m mypy tools/rpi-checks.py` clean; drift comparison `WORKFLOW_HASHES[n] == digest(n)` true for all WORKFLOWS. Plain `ruff check` reports 12 pre-existing findings in untouched lines. Full gate re-run left to coordinator.
