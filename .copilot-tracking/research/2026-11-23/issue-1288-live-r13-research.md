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
---
title: Research r13 for issue 1288 (implausible sensor readings reach the Quality model)
date: 2026-11-23
---

Disposition: executed. Tier FULL only if src changes (it will); no rpi-checks --all, no push. Planning Readiness: Ready.

## Evidence

* Prior audits r2..r12 (docs/reference/research/issue-1288-live-r*): criteria 4 and 8 blocked only by a missing approved release record (OQ-017); that is owner-only and is not bypassed.
* Code gap found in this round: `sensor_view.reading_health` flags fault or out-of-range latest readings in the employee UI only. `capture_source` (the snapshot the model receives) carries no such marker, and `review_flag` / the proactive trigger treat only `conflicting_readings` as blocking. An impossible reading (for example 250 %RH) can therefore be sent to the model and cited in an autonomous L4 flag while the UI says "do not rely on it". This contradicts criterion 3 (identical evidence) and criterion 6 (rejected or conflicting readings give an explicit insufficient state, no silent normal).
* Live: read-only probe of the demo only; no model consumption possible without a release.

## Plan target

Add an `implausible_readings` marker and notice to the captured sensor source, block the autonomous flag and proactive trigger for it (status `implausible-readings`, human route), label it in the UI, and test it locally.
