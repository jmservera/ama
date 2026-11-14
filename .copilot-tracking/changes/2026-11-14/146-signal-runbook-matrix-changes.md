---
title: Alert signal matrix changes (Refs #146)
ms.date: 2026-11-14
---

## Changes

* Added `infra/tests/test_alert_runbook_signal_matrix.py` (7 tests, pass).

## Validation

* `python3 -m unittest discover -s infra/tests -v`: 587 run, 1 error, 4 skipped. The error is `test_bicep_policy` `test_ledger_alert_queries_match_the_verifier_markers`: `zava_forward.orchestrator` is not installed here (pre-existing, unrelated).
* `ruff check` and `ruff format --check` on the new file pass. The directory-wide commands report 72 errors and 22 files to reformat in existing files (pre-existing on the base commit).
* Not run: hosted CI and the full local gate (Focused tier).
