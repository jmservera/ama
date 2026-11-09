---
title: Sensor integration retained-evidence checkpoint 440 research
description: Research for the due sensor parent integration checkpoint, reading retained r20 evidence rather than supplied summaries
ms.date: 2026-11-06
---

## Identity and method

Task `440-sensor-retained-evidence-checkpoint`. New bounded continuation after the published R10 correction (PR #1235). Start HEAD `59a90fd32f9dc5cf8b3a8cedb7a1d3692597f5ea`, ignored-inclusive status clean. Target stays `feat/discovery-assurance-integration-123` (PR #1222); local handoff only. The `rpi-research` skill body was loaded in this session earlier. Posture focused, inline, no worker. Reads only: no test, SQL, browser, container, scanner, install or lock.

## Prior coverage finding

The pack already has a Sixteenth checkpoint (sensor parent integration) from the post-integration batch. It marked the receipt figures as "supplied, historical". This cycle does not create a duplicate checkpoint; it adds a retained-evidence verification as a qualification and answers the explicit current-image-risk and SQL-kind requests with data read from files.

## Fresh pins (git fetch, exit 0, this session)

* Main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`; parent `origin/feat/live-simulator-integration-184` `9476dc9610368a9a1bd46c88314586885638580d`, tree `30167885b00d308d7b29e9a78a064f4af834ce98`.
* BRD blob `34d88395de861e9799eb9e24121a21c92c7a5adc` (0.21.0 draft), PRD blob `c788b917bafaede215f326f0efc71e071a687f1c` (0.21.0 in review) on the parent. Draft and in-review are not approval.
* Parent versus main: 99 files, +1967 and -81 including tracking records; the Sixteenth's 19-file figure counted source and tests only and is a different scope.

## Retained evidence read (observed this session)

| Item | Observation |
| --- | --- |
| `/mnt/ama-gates/g188-r20-1106/receipt.json` | sha256 `e575146936c97ffb4e397dd78a75951a079000c18c979d3374f863e6c1c95014`, equal to `receipt.sha256`; status passed, scope full, jobs 1, failure null, 205 commands, 17 executed groups, none skipped, image cache fresh, not resume-eligible, sealed 2026-11-06T08:47:53Z |
| Receipt identity | head `6887377845648502f2a5509801ee5d9807869703`, tree `30167885...` (equals parent tree), base and merge base `bb3a3b03...` |
| Hosted-only (not run locally) | GitHub approvals and checks, OIDC and Azure what-if, manual release and deployment, real AI acceptance |
| Maintained real SQL (`0176-mssql.log`) | Ran 285 tests, OK, skipped 1: `MssqlHazardReferral.test_json_postsave_audit_failure_reports_persisted_uncertainty`, reason "JSON-only separate-file audit ordering" |
| Package skips (not real SQL) | core 2363 tests with 226 skips; API 1941 tests with 338 skips; orchestrator 104 OK |
| Owned SQL supplement (`/mnt/ama-gates/e188-r20-1106/sql-sensor.log`) | Ran 68 tests, OK; `cleanup.json` status removed-and-absent-confirmed. It is outside the receipt command list |
| Image scans (`api`, `agents`, `orchestrator`, `importer` all-reports) | each 42 findings, 40 High and 2 Critical, fixable 0 (computed from the Trivy JSON this session) |
| Browser `case-journey-results.json` | browser 156.0.8078.4, axe 4.10.3; scans read show zero violations and one "incomplete" colour-contrast item on four quality-history states; I read only the first eight scans and did not assess the whole file |
| Native log `/tmp/rpi-188-r20-postfull-handoff-r59-20261106.log` | 109 lines; the 205 commands include 192 exit 0 and 13 exit 1 (expected probes: namespace imports, missing yaml and pptx probes, SQL readiness attempts) per the child's own account, which I did not re-derive from the receipt command list |

## Source boundaries (static reading on the parent)

* Weather reference version `synthetic-weather-continuity-v1` (`src/core/src/zava_forward/core/synthetic/sensor_consistency.py:36`); its docstring says the result is not witnessed Azure continuity, physical accuracy, indoor evidence or calibration.
* Consumer receipts carry `replay` (`src/core/src/zava_forward/core/sensor_consumer.py:189, 677`); indoor-contract rows are a separate reading-v2 path (line 738). The Sixteenth's cited paths used shortened names and its line numbers were not re-read here.
* No claim of live Hub, credential issuance, secure storage, teardown, resident consent, calibration or statistical validity.

## Contrarian wave

* The 42 versus 39 increase: cause not verified; plausible newer scanner database is the child's hypothesis only. Image risk is unchanged in kind (zero fixable is not security-clean).
* The receipt belongs to child head `6887377`; parent `9476dc96` is the squash with the same tree, so file content is identical but the receipt is not a new gate at the parent commit. Nothing here relabels it.
* No new defect is established; absence of evidence is not a defect. Existing owners #184, #185, #188 hold the open criteria.

## Synthesis

Accepted: add one additive qualification under the Sixteenth section, a log entry and a minimal index note. Rejected: new checkpoint number, repeated gates, new issues, source edits. Research disposition executed; Planning Readiness Ready. Recommendation to carry: CONTINUE independent lanes, HOLD closure of #184, #185, #188 and dependent expansion.
