---
title: Quality sensor values and review flag, fourteenth audit (Refs #1288)
description: Fourteenth audit of the demo Quality sensor integration; a cited reading corrected to an impossible value after capture now downgrades the autonomous flag, with the per-criterion proven or unproven table
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Follows the [thirteenth audit](./issue-1288-live-r13-quality-sensor-evidence-2026-11-23.md). No Azure resource was created or changed; live legs are carried from the [twelfth audit](./issue-1288-live-r12-quality-sensor-evidence-2026-11-23.md) and were not re-probed, because the only live blocker (no approved release record, OQ-017) is a human approval and no model call is possible.

## Finding and fix

The thirteenth audit handled impossible readings present at capture time. A retained row keeps its id when corrected, so a reading cited by a returned flag could become impossible afterwards while the flag stayed an autonomous L4 `review-suggested`; only `changed_since_capture` showed the difference. `review_flag` now takes the current successful capture, and if a cited reading is impossible there, reports `implausible-readings` (not autonomous, route to the ordinary quality check). It only downgrades. Impossible rows that are not cited are still covered by the newer-readings notice.

## Evidence

* New test `test_cited_reading_corrected_to_impossible_after_capture_downgrades_the_flag`: failed first (`review-suggested` / true), passes with the change.
* `test_quality_sensor_grounding`, `test_quality_sensors_correlation`, `test_quality_sensors` (src/api): 229 run, OK, 94 skipped (SQL Server and browser prerequisites). Fixture data and a mock provider: local engineering evidence.
* ruff check clean; mypy src/api clean; src/core mypy shows the 3 errors present on the base. `ruff format --check` flags `assistants.py` on the base too (existing, not touched).

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| 3 | Proven locally (mock provider); not live | Correlation tests; no live model request |
| 4 | Unproven | No approved, unexpired release record; owner not appointed (OQ-017). Creating one would fabricate authority |
| 5 | Proven locally; not live | Flag tests; no live model output exists |
| 6 | Proven locally, now including post-capture impossible readings | New test; live states per r12 |
| 7 | Proven as local engineering evidence | 229 tests OK here; SQL Server and browser cases skipped |
| 8 | Unproven | Model leg blocked by criterion 4; no mock or deterministic substitute |

Criteria 1, 2 and 9 are ticked. No tick or closure is claimed; independent review and hosted CI remain outstanding.
