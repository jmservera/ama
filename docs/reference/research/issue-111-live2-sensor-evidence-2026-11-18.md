---
title: Issue 111 signed-in sensor evidence and R1 to R3 disposition (re-run)
description: Retained raw evidence for issue 111 on the synthetic demo, extending the earlier note that kept no raw output
ms.date: 2026-11-18
---

Refs #111. Synthetic demo, desktop only, no source change, no Azure change, no resource created. Extends
[the earlier note](issue-111-sensor-analysis-live-evidence-2026-11-18.md). Raw files are in
[issue-111-live2-raw](issue-111-live2-raw/). Ids and the host name are redacted.

## Criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Outputs are reproducible from retained readings (ticked) | Proven | [first run](issue-111-live2-raw/core-sensor-tests.txt): 22 tests OK, 1 expected failure; [second run](issue-111-live2-raw/core-sensor-tests-2.txt): 91 tests OK, 22 skipped (SQL Server dependent, not run). Live: two consecutive staff-signed `GET /api/cases/{id}/sensors` calls returned identical bodies ([walk](issue-111-live2-raw/live-walk.txt)) |
| Thresholds are sourced or labelled exercise values (ticked) | Proven for the demo | [payload](issue-111-live2-raw/sensors-first-case.json): `calibrated: false`, provenance `synthetic-weather-derived`, stale freshness text, no retrofit effect claimed; [render](issue-111-live2-raw/sensors-payload-redacted.png) |
| R1 to R3 complete before a derived measure is used beyond an exercise rule (unticked) | Unproven; cannot be proven for the demo | R2 needs a named building-physics reviewer and Asset sign-off, R3 agreed false-alert and miss limits, R1 the official BS 5250, BS EN ISO 13788 and PAS 2035 texts. The owner decisions of 2026-11-18 do not let an agent stand in for these |

## Live observations

* Unsigned `/healthz` 200; `/health`, `/openapi.json`, `/app` 401 ([probes](issue-111-live2-raw/live-probes.txt)). Active revision healthy.
* Staff sign-in by Playwright succeeded. The cases API returned 16 cases; one of the first 16 carried a sensor payload (`retained-reading-view-v2`, 12 readings, `state: ok`, freshness `stale`).
* `GET /api/cases/{id}/sensor-drafts` returned `{"state": "disabled"}`: no SENSOR_REVIEW_DUE task is created on the demo, consistent with approved-signals-only wiring being unproven ([draft](issue-111-live2-raw/sensor-drafts-first-case.json)).
* The browser screenshot of the case view was discarded because it showed personal names; the retained image is a render of the redacted payload, not a live UI capture.

## Unmet and limits

* Criterion 3 stays unticked. Full SQL Server task-flow reproducibility was not run (tests skipped). Only one case of the first 16 was walked in detail.
* A probe command printed the staff credential file to the working session transcript. It is not in any artifact; rotating that test user's password is recommended.
