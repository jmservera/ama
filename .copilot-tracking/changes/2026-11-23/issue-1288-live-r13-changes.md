---
title: Changes r13 for issue 1288
date: 2026-11-23
---

Refs #1288. Tier FULL (src change); targeted tests only, no `rpi-checks.py --all`, no push. Azure untouched (no resources created).

## Files

* `src/core/src/zava_forward/core/sensor_view.py`: `implausible()` and `implausible_readings` / `implausible_notice` in the captured sensor source (same limits as the UI health badge).
* `src/core/src/zava_forward/core/assistants.py`: no proactive request while captured readings are implausible; `review_flag` status `implausible-readings` (not autonomous, human route).
* `src/api/src/zava_forward/api/web/assistants.js`: title and status notice for the new state.
* `src/api/tests/test_quality_sensor_grounding.py`: test written first (failed with `KeyError: implausible_readings` before the change).
* `docs/reference/research/issue-1288-live-r13-quality-sensor-evidence-2026-11-23.md`.

Note: the test edit predates the implement-start witness (witness qualification "source already dirty"); it is the failing-first test.

## Validation (targeted, local)

* `test_quality_sensor_grounding`, `test_quality_sensors_correlation`, `test_quality_sensors`, `test_accessibility_baseline`, `test_content_standard` (src/api): 275 run, OK, 94 skipped (SQL Server and browser prerequisites).
* `test_sensor_view*` and `test_heldout_eval` (src/core): OK. ruff check and format: clean. mypy: src/api clean; src/core 3 errors identical to the base (opentelemetry stubs, one unused ignore), not caused by this change.

## Per-criterion table (unticked criteria)

| Criterion | Status | Evidence |
| --- | --- | --- |
| 3 snapshot consumes identical IDs and values | Proven locally (mock provider); not live | Correlation tests; new test shows the same implausible marker in the API view and the model request |
| 4 release-admitted proactive flag | Unproven | Missing approved release record, owner not appointed (OQ-017); owner-only. New code also stops proactive requests on impossible readings |
| 5 finding, IDs, time, model, unapproved status visible | Proven locally; not live | Existing flag tests; no live model output |
| 6 missing, stale, rejected, unavailable states with human route | Proven locally, now including impossible readings | New test: `implausible-readings`, not autonomous, ordinary quality check |
| 7 focused SQL, API, browser tests correlate | Proven as local engineering evidence | Fixture and mock provider; SQL Server and browser cases skipped here |
| 8 finite live walkthrough with real model | Unproven | Blocked by the same missing release record; not fabricated or mocked |

Live evidence is carried from the [twelfth audit](../../../docs/reference/research/issue-1288-live-r12-quality-sensor-evidence-2026-11-23.md); this run did not re-probe Azure. Limit: only implausibility present at capture time is handled. No tick or closure claimed.
