---
title: Issue 111 third live re-verification of the sensor analysis criteria
description: Fresh 2026-11-18 signed-in demo probes and test run for issue 111, with a per-criterion proven or unproven result
ms.date: 2026-11-18
ms.topic: reference
---

Refs #111. Scope: synthetic demo, desktop only, docs and evidence only (no source change, Tier FOCUSED). Live Azure read-only under the owner decisions of 2026-11-18. No credentials are recorded; the sign-in script reads them from the owner's files at runtime and prints nothing from them.

## Result

| Criterion | Issue state | This run |
| --- | --- | --- |
| C1 Outputs are reproducible from retained readings | Ticked | Re-confirmed as engineering evidence: 26 core sensor tests pass; the live sensors payload for one demo case is `retained-reading-view-v2` and two consecutive reads had identical content |
| C2 Thresholds are sourced or labelled exercise values | Ticked | Re-confirmed: `sensor_analysis.py` pins `ANALYSIS_VERSION = "sensor-analysis-exercise-v1"` and `EXERCISE_LABEL = "EXERCISE VALUE: fictional, not sourced"`, and rejects other labels |
| C3 Research phases R1 to R3 complete before a derived measure is used beyond an exercise rule | Unticked | Unproven, and not provable for the demo (below) |

## Evidence

Raw files are in [issue-111-live3-raw](./issue-111-live3-raw/).

* Tests: `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests.test_sensor_analysis tests.test_sensor_non_authority` gave `Ran 26 tests ... OK (expected failures=1)` ([core-sensor-tests.txt](./issue-111-live3-raw/core-sensor-tests.txt)). SQLite-backed; no SQL Server run here.
* Live app: `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000032`, image digest `sha256:5368f4e4...c5e7ac` (full value from `az containerapp show`).
* Playwright Chromium, 1366 by 900. Entra sign-in with the employee test account reached `/app` (the workbench screenshot showed resident names and is not retained); `/api/me` 200, `/api/cases` 200 with 16 items ([live-walk.txt](./issue-111-live3-raw/live-walk.txt)).
* `/api/cases/{id}/sensors` for the first case with a payload returned 200 with `version` `retained-reading-view-v2`, `calibrated` false, `freshness` `stale` ([sensors-first-case.json](./issue-111-live3-raw/sensors-first-case.json)). Two consecutive reads had no differing keys. In the first run the byte hash of two reads differed; the second run showed no differing keys, so the cause was most likely a time-dependent field, but this was not isolated.
* `/api/sensor-drafts` and `/api/sensor-review-drafts` returned 403 "Your role does not include this" for the employee role. No `SENSOR_REVIEW_DUE` task creation was observed or attempted.

## Why C3 cannot be proven on the demo

* The research plan ([iot-sensor-analytics-research-plan.md](./iot-sensor-analytics-research-plan.md), phase table) requires R2 sign-off by a competent building-physics reviewer and Asset, and R3 methods meeting agreed false-alert and miss limits. Both are named-human approvals; the owner decisions of 2026-11-18 waive billing, DPO/Legal and assistive-technology testing, not this research sign-off.
* R1 still lacks the official standards texts (BSI, BRE and similar), which were not read.
* The runtime gate that blocks non-exercise rule activation until R1 to R3 are complete was merged in #1780 into the parent topic PR #1641, not into main. The main source in this worktree has no such gate, and the deployed demo image cannot show it.
* The latest owner comment on #111 states that the named research or professional owner must approve R1 to R3 completion.

Follow-ups: name the accountable approver; read the official standards for R1; agree R3 limits; merge #1641 so the gate reaches main and a deployment.
