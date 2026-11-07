---
title: Issue 135 exception screen r2 quarantine label correction details
ms.date: 2026-11-07
---

## Phase 1 details

* In `test_exception_register_screen.py` set `failedAi.original_source.status` to `"Not reviewed"` and `quarantined.original_source.status` to `"Quarantined"`. Add `legacyQuarantined` (lowercase status, with reason) and `noReason` (failed_ai_run, no `error`, status `"Not reviewed"`) to `base.items`, and assert the labels in `test_failed_ai_quarantine_and_workflow_only_distinction`.

## Phase 2 details

* `exceptionHappened`: quarantined when `typeof status === "string" && status.toLowerCase() === "quarantined"`. Fallback wording only when `item.error` is a non-empty string; otherwise "Requested AI help did not deliver a model result. How it failed is Unknown."

## Validation

* From `src/api`: `python3 -m unittest tests.test_exception_register_screen tests.test_data_operator_screen`, `ruff check`, `ruff format --check`, `mypy`, `node --check`.
