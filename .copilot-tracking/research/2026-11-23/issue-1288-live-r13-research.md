# Issue 1288 r13 research

Task: issue-1288-live-r13. Planning Readiness: Ready. Disposition: executed (reuses the r12 note, docs/reference/research/issue-1288-live-r12-quality-sensor-evidence-2026-11-23.md).

## Per-criterion triage (unticked 3 to 8)

| Criterion | Can code, tests or tooling satisfy it? |
| --- | --- |
| 3 | Source delivered (#1331) and covered by existing tests; live proof needs a model call |
| 4, 8 | Blocked by the missing approved release record (OQ-017, a human approval). Faking or bypassing the gate would fabricate authority and a deterministic outcome; the 2026-11-23 override (#2326) covers suspensions only, not release records |
| 5 | Visible AI output needs a live model call (same block) |
| 6 | Partly code. r12 saw one unexplained HTTP 503 on GET /api/cases/ZF-2025-0148/sensors. `server.py` (~line 1447) catches `Exception` and returns the unavailable state with no log, so the cause cannot be diagnosed |
| 7 | Covered by existing tests (local engineering evidence) |

## Selected work

Criterion 6 (first criterion code can improve): log the cause class and raise site (never the message, which may carry connection details) for the sensor read 503 and the sensor-drafts 503, keeping the response, human route and explicit unavailable state unchanged. Regression test in src/api/tests/test_quality_sensor_grounding.py.

Tier: FULL (src change), logging-only in a non-security path. The complete gate belongs to the coordinator; no rpi-checks --all run here. Targeted tests, mypy and ruff run locally.
