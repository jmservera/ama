---
title: "Changes: #146 RAI window reconcile and disabled-task owner status"
ms.date: 2026-11-14
task_slug: demo-146-rai-window-reconcile-0003
---

## Changes

* `src/core/src/zava_forward/core/monitoring_coverage.py`: `reconcile_events` accepts `prior_event_ids`, returns `new` and a bounded `checkpoint`; new `disabled_task_status`.
* `src/core/src/zava_forward/core/assistants.py`: disabled registered tasks carry `status` (owner role, individual, owner gap, reason).
* `src/core/tests/test_monitoring_coverage.py`, `src/api/tests/test_assistant_release.py`: new assertions.

## Validation (Focused tier)

* ruff check and format --check on the two files that were already clean: pass. `assistants.py` and the API test file have pre-existing ruff findings (not touched beyond the edit).
* mypy `--follow-untyped-imports` on `monitoring_coverage.py`: pass (plain run only reports the pre-existing untyped `rai_release` import).
* `test_monitoring_coverage` + `test_scenario_manifest` (42 tests): OK. API `test_assistant_release` + `test_assistants`: 196 tests OK (66 skipped, SQL fixtures).
* Not run: full local RPI gate, hosted CI. Not pushed.

## Divergences

None. No infra, Bicep or workbook files touched.
