---
title: Issue 144 extension 2 phase details
description: Phase details for the result-attribution binding
ms.date: 2026-11-10
task_id: issue-144-extension2-attribution
---

## Phase 1: source

* File `src/core/src/zava_forward/core/assistants.py`, method `complete_result`, plus a helper `_permitted_root(db, meter_id)` returning the reservation root or `None`.
* Success: caller root omitted gives the stored root in the envelope passed to `complete`; conflicting root or id gives `result-rejected` and `False` before settlement.

## Phase 2: tests

* File `src/api/tests/test_ai_consumption_api.py`, class `ConsumptionApi`, new tests after `test_settlement_binds_to_the_marker_and_late_results_settle_the_meter_only`. Use `permit_setup`, `permit_request` and `proposal` from `test_assistants`; real store, no invented envelope values beyond the real usage fields.

## Phase 3: validation commands

* Run from `src/api` and `src/core` with the own venv, `PYTHONDONTWRITEBYTECODE=1`, the documented test-helper `PYTHONPATH` only. Logs in `144-extension2-attribution-1110/logs/` with exits captured directly.
* Pre-change RED run of the new tests on the frozen source first; first failures kept.

## Planned changes

* `src/core/src/zava_forward/core/assistants.py`: `complete_result` binding and `_permitted_root`.
* `src/api/tests/test_ai_consumption_api.py`: attribution regressions.
