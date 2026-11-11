---
title: Issue 144 extension 2 changes
description: Actual changes, evidence and limits for the result-attribution binding (E2)
ms.date: 2026-11-10
task_id: issue-144-extension2-attribution
---

## Status

Implemented and locally validated at the DEMO targeted tier. Base: origin/main 83c28132ceb7c8609569c4c4fe9f1f9bca1ded58 merged by an ordinary merge (merge commit 7bb8fc2b3222fb42892910d26cf232fcd2f21fe5). Refs #144 only. Registered prospectively before implement-start.

## Changes

* `src/core/src/zava_forward/core/assistants.py`: `complete_result` derives the attribution root from the stored reservation of the permitted `meter_id` (new `_permitted_root`), rejects a conflicting caller `meter_root` or `meter_id`, or a missing reservation, with `result-rejected` before any settlement, and passes a copied envelope bound to the stored `meter_id` and `meter_root` to `_settle_meter` and `complete`.
* `src/api/tests/test_ai_consumption_api.py`: three regressions on the real store and owned local fixture: valid output with the root omitted publishes output attribution on the reserved root and later review accounting; conflicting root and id are rejected without settlement or output and a correct retry still completes once; a failed result without a root settles the meter and publishes no output.

## Not changed

B scope, the E1 clock fix, fence, consent and captured-readings gates, `complete`, `shape_result`. The no-marker path still forwards caller attribution (not part of the finding; routed below).

## Evidence

Logs are under the external `144-extension2-attribution-1110/logs/`; exits were read directly.

| Log | Content | Exit |
| --- | --- | --- |
| 01 | reproduction import error (kept) | 1 |
| 02 | reproduction on the real store: omitted root gives no output record, conflicting root attributes to the caller root | 0 |
| 07 | RED on frozen source: 2 causal failures, 1 control passes | 1 |
| 08 to 11 | format, ruff, GREEN of the three new tests | 0 |
| 12 | api selectors including real sensor fixtures e1, e2, c7: 511 tests, 129 skipped | 0 |
| 13, 14 | core affected selectors 59 tests; agents `test_dispatch` 15 tests | 0 |
| 15 | core mypy strict, 296 files | 0 |
| 16 | api test mypy first run, one no-any-return error (kept) | 1 |
| 17 to 22 | format, lint, mypy, `test_ai_consumption_api` 32 tests after the fix | 0 |
| 23 | import origins resolve inside this worktree | 0 |

## Skips and unobserved

* Real MSSQL selectors not run: the project fixture needs a task-labelled disposable container and manifest with no ready provisioning tool for this task, and the new tests are not MSSQL-parameterized. The heavy lock was free at the probe, not taken. MSSQL is unobserved, not passed.
* The 129 skips are existing SQL or environment skips, including the real sensor-fixture SQL classes.
* The first reproduction run and the launch, research-open and plan-done markers were recorded after the research records were written (one chain, no earlier chain).
* No full gate, Docker, cloud, provider or model call.

