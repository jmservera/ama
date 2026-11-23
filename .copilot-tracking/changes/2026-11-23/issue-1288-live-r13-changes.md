# Issue 1288 r13 changes

Status: complete. Tier FULL (src change); logging only, no gate or security semantics changed. The coordinator owns the complete gate; rpi-checks --all was not run.

## Changes

* src/api/src/zava_forward/api/server.py: `_log_sensor_unavailable` logs exception class and raise site (never the message) for the `/sensors` and `/sensor-drafts` 503 paths. Response bodies and the human route are unchanged.
* src/api/tests/test_quality_sensor_grounding.py: `test_sensor_read_failure_stays_unavailable_and_logs_cause_class_only`.

## Validation

* `unittest test_quality_sensor_grounding test_home_sensors_tab`: 37 tests OK. `ruff check` clean; `mypy` in src/api: no issues (373 files).
* Not run: browser/SQL-gated cases, hosted CI, live probe (no model call is possible; see below).

## Per-criterion table (issue 1288, unticked)

| Criterion | Status | Basis |
| --- | --- | --- |
| 3 consumes identical IDs | Proven locally (mock provider), unproven live | Existing grounding tests; no live model request |
| 4 release-admitted proactive flag | Unproven | Approved release record absent (OQ-017); human approval, not code |
| 5 employee sees finding, IDs, model, status | Unproven live | Needs a live model output |
| 6 explicit unavailable states and human route | Proven locally; this change makes the 503 cause diagnosable | New regression test; r12 live saw the explicit states |
| 7 focused tests correlate UI and snapshot | Proven as local engineering evidence | Existing tests plus 37 run here |
| 8 finite live walkthrough | Unproven | Model leg blocked by the missing release record |

No tick or closure is claimed. Independent review and hosted CI remain outstanding.
