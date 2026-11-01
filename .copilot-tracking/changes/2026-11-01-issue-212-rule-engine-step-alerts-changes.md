---
title: "Issue 212 changes: HTTP proof of grouped, ranked, fatigue-tracked alerts"
ms.date: 2026-11-01
---

* Added `test_alerts_endpoint_returns_ranked_home_groups_and_precision` to `src/api/tests/test_rule_alerts.py` (test only; no production change).
* Divergence from plan: the reference log entry was dropped because no knowledge-base file changed.
* Validation: `test_rule_alerts` 7 tests OK; `test_rule_engine` 27 tests OK; `ruff check` and `ruff format --check` clean; mypy reports only missing-optional-module (`playwright`) import errors in untouched files, none in the touched file.
