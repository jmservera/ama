---
title: Sensor checkpoint recovery research (Refs #440 #184 #110)
description: Current-main qualified research for the already-due #184/#110 sensor contract, retention and handover stabilization record
ms.date: 2026-11-05
ms.topic: reference
---

* Task: `sensor-checkpoint-recovery`, owner issue #440 (open, parent #123), scope report `/home/azureuser/.copilot/session-state/77149bdf-2f9a-4b04-b1dc-af3109946991/files/sensor-checkpoint-scope.json` (external, read as data).
* Research disposition: `executed` (new read-only git-blob and issue reads) reusing the scope report for the unmerged-PR and authorization inventory. Planning Readiness: `Ready` for a documentation-only record.
* Boundary: documentation only, local only. No push, PR, merge, code, coordinator, workflow, issue or cloud change. No private dataset, billing file or cohort file read. Heavy SQL, images, browser and FULL gate not run.

## Source identities (observed 2026-11-05)

| Item | Value | How observed |
| --- | --- | --- |
| Accepted current main | `c6d5a8f3c3a35892322300be27b9747f7b11362d`, tree `876679c32ff8f8a3d35822d9e46d8b377ce15428` | `git fetch origin main` then `git rev-parse origin/main` and `c6d5a8f3^{tree}` |
| Working base (pinned parent topic) | `3d7ad2feaa9c4cba5fe917edd2fbc40e40a5c246` (merge of #1209), tree `b35f4e4808a4eb74bfee55f098bb101369358d98`, branch `docs/stabilization-recovery-wave-123` | `git rev-parse HEAD` |
| Delta base to main | One merged commit (#1210). `git diff --stat HEAD c6d5a8f3 -- src docs infra` is empty; the delta is `tools/rpi-checks.py`, `tools/test_rpi_checks.py` and `.copilot-tracking` records only | `git diff --name-only HEAD c6d5a8f3` |
| Merged covered PRs | #1209 (merge `3d7ad2fea`, 2026-11-05T09:31:21Z, preserves verified active delivery state in `tools/backlog-sync.py`), #1210 (merge `c6d5a8f3`, 2026-11-05T10:01:58Z, installs isolated Chromium before API discovery in `tools/rpi-checks.py`) | `gh pr view` |
| PR relevance | Both are delivery tooling. Neither changes sensor contract, ingestion, retention or handover source. They are covered as the trigger window, not as sensor acceptance | stat of both merge commits |
| Evidence pack blob at main | `docs/architecture/cutover-evidence-pack.md` `2566e8efd7084346421fffb101d5b171100dfd63`, identical to the working tree base | `git rev-parse c6d5a8f3:path` |

Because source, docs and infra are byte-identical between the working base and
current main, reading the sensor source through `git show c6d5a8f3:<path>` is
the current-main identity; no parent-topic-only observation is used for
acceptance. Any parent-topic observation is labelled separately in the record.

## Document identities at main

| Document | Status, version, date | Blob |
| --- | --- | --- |
| `docs/brds/agentic-retrofit-programme-brd.md` (BRD-2026-AMA48-001) | draft, 0.21.0, ms.date 2026-10-24 | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (PRD-2026-AMA48-001) | in-review, 0.21.0, ms.date 2026-10-25 | `c788b917bafaede215f326f0efc71e071a687f1c` |
| `docs/adrs/0002-pilot-readiness-architecture.md` | Status `Proposed`, no version field, ms.date 2026-10-24; its "no IoT Hub" sensor position is amended by ADR 0003 decision 6 | `cbe21530043ff15432cc6dce1086d080f5eb15b4` |
| `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` | Accepted with amendment by the owner 2026-10-15 (reconciled 2026-10-18), no version field, ms.date 2026-10-29; exercise Basic hub only, live gates separate | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| `docs/reference/research/iot-sensor-analytics-research-plan.md` | Research synthesis, not an approval | `d29c68f1095b3448d125ece0a5766f82edb83f48` (equal at main and base) |

Requirement IDs collide across documents and must be document-qualified:

* BRD FR-048 is in-use monitoring capture, AC-090 its criterion, RULE-014 the sensor-data authority rule and OD-43 the real-inventory decision that blocks operational use of FR-048 with real data but not the simulator exercise.
* PRD FR-050 is simulated in-use monitoring through Azure IoT Hub, with AC-066 (idempotent ingestion), AC-067 (review-signal authority) and AC-068 (method evidence).
* BRD FR-050 is the opt-in working memory requirement (AC-093) and PRD FR-048 is appointment commitment. Neither is sensor work. Issues #184, #110 and #188 cite "FR-048, OD-43" under the BRD and "FR-050, AC-066" under the PRD; they must not be read across documents.
* ADR 0002 is Proposed and ADR 0003 is the only accepted decision here; draft or proposed documents and the scope-report candidate limitations are not approvals.

## Issue criteria read as data (2026-11-05)

* #440 (open, updated 2026-11-05T10:17:33Z): C1 to C6 ticked earlier; C7 (triage of confirmed findings) and C8 (genuine artifacts and Major HVE Builder static review, behavior testing and host validation of the coordinator change) unticked. Owner approval is needed for requirement changes, pivots and deliberate deferrals. No ticked criterion here authorizes broader acceptance.
* #184 (open, parent #165): "all child stories closed or deferred" unticked, "simulator never connects to or represents real devices" ticked, "no device key or connection string in source, logs or telemetry" unticked. Depends on #140, #110, #177.
* #110 (open, parent #109): distinct IoT Hub identity per simulated device with schema version and stable reading ID unticked; idempotent append, visible DQ handling, no public ingestion endpoint and no device key in source ticked. Body status line still reads "Not started" (stale text, not changed here).
* #188 (open, parent #184, depends on #110, #183, #186): queryable-together per home, statistical handover within declared tolerance and idempotent window rerun all unticked.
* Child states read: #183 closed 2026-10-27, #186 closed 2026-10-18, #185, #189 and #140 open.

## Current-main source observations (git blob identities, source inspection only)

| Path at c6d5a8f3 | Blob | Observation |
| --- | --- | --- |
| `src/core/src/zava_forward/core/synthetic/live_readings.py` | `289051eed757b0e2b37fdea04aa16a68cb9eb974` | Pure generator `live-sim-generator-v1`, message `live-sim-reading-v1`, 300-second UTC slots, illustrative UK-like monthly daily temperature, humidity and irradiance averages (a synthetic assumption), per-home bounded offsets and smoothed noise. Row fields: `sensor_id`, `reading_id` (`LIVE-<sensor>-<YYYYMMDDTHHMM>Z`), `home_id`, `observed_at`, `temperature_c`, `humidity_pct`, `sunlight_wm2`, `temperature_unit=degC`, `humidity_unit=percent`, `sunlight_unit=W/m2`, `source_type=SYNTHETIC`, `scenario`, `seed`, `schema_version`, `injected_fault=none`, `label`. No `calibrated` field |
| `src/core/src/zava_forward/core/sensor_consumer.py` | `8125b88beeb430e2bc996b22fe3259e0cdf4c7af` | `_shape` requires exactly `READING_FIELDS` of `synthetic/sensor_faults.py` (13 string fields including `calibrated`, `temperature_unit`, `humidity_unit`) and schema `sensor-fault-input-v1`. `READING_COLUMNS` has 11 stored columns and no sunlight or unit column; units and calibration come from trusted per-sensor controls. `observed_series` returns stored rows per exact home selection |
| `src/core/src/zava_forward/core/synthetic/sensor_faults.py` | `3bff9625c652cbd8320fc3f01da250258883b12a` | `SCHEMA_VERSION = sensor-fault-input-v1`, fixed fault classes, fictional exercise values |
| `src/core/src/zava_forward/core/synthetic/sensor_identity.py` | `0b716fb454e259585996dfa45712e9651f70d184` | `home_key`: non-empty string, no surrounding whitespace, at most 128 UTF-16 code units, no control characters; `sensor_key` is `S` plus ten base32 characters of the SHA-256 of the UTF-8 home ID |
| `src/core/src/zava_forward/core/synthetic/sensor_backfill.py` | `b381fba755a0d95ddc25edaedf9553e831eebfc3` | Backfill schema `reading-v1` (and composed `sensor-fault-input-v1`), reading ID `<sensor>-<epoch seconds>`, cadence three per day by default |
| `src/api/src/zava_forward/api/iot_stream.py` | `8eeaccbb3c26d1a4c4dd00e190a39274462c2dc7` | Fresh receivers start at the retained beginning (`starting_position="-1"`, non-inclusive), no checkpoint store; device ID must equal `SYN-<sensor key>` |
| `src/api/README.md` (Live simulator container section) | `e1a8f3ed2cb19ce2a15b0a22e76a5e8bd2e50270` | States that `sunlight_wm2` is not accepted by the current #110 consumer schema and that teaching it is a #110 decision; no live send, device registration, Hub receipt or throttle proof |
| `src/core/README.md` (stock export) | `b5469625a4f849ec6f5fc20eef7f1f610ad0c38e` | Export accepts 128-unit home keys while consumer availability and `observed_series` are bounded to 64 UTF-16 units; longer keys give `HOME_UNAVAILABLE` (documented, deliberate) |

## Findings and classification

| Id | Finding | Classification | Existing owner |
| --- | --- | --- | --- |
| F1 | Live generator output is not admissible by the main consumer: version `live-sim-reading-v1` differs from `sensor-fault-input-v1`, the field sets differ (extra `sunlight_*`, `label`, `injected_fault`; missing `calibrated`) and `_shape` requires an exact set. Already documented by the main API README | implemented-unverified (source inspection; no execution) | #188, with open PR #1203 (excluded) |
| F2 | Retained raw weather and wire (sunlight W/m2 in the wire message) versus indoor observed series (`sensor_reading` stores temperature and humidity only, units and calibration from controls): no outdoor or sunlight value is indoor evidence and no equivalence is claimed | implemented-unverified; physical calibration unknown | #188, #110; research plan ADR boundaries |
| F3 | Reading ID and timestamp joins differ across producers: backfill `<sensor>-<epoch>` at three per day versus live `LIVE-<sensor>-<slot>` at 288 per day. Stable `(sensor_id, reading_id)` idempotency holds within a producer; cross-producer series continuity at the handover time is unobserved | implemented-unverified; local constructed handover witnesses are historical | #188 |
| F4 | Retention: fresh receivers replay the retained beginning, SQL outcomes are the durable state, retention expiry bounds recovery, concurrent receivers are uncoordinated, commit uncertainty is not rollback, poisoned envelopes stop. Unsupported or missing windows are not a pass | implemented-unverified (source and README); Azure behaviour not observed | #110, #188 |
| F5 | Distinct Hub identities, authenticated routing and joint Azure SQL query and restart are unobserved. The 2026-10-29 bounded B1 hub exercise (metrics only) issued no device and sent no stream | Azure observed (historical, infrastructure only); acceptance blocked | #110, #185, #140 |
| F6 | Composed SQLite and SQL Server handover witnesses (zero default tolerance, negative controls, reopened-window replay) and the 45 constructed ingestion tests are dated historical local observations, not re-executed against c6d5a8f3 | local observed (historical, original dates and heads) | #188 |
| F7 | Physical calibration, indoor-risk thresholds, retention lawful basis and real resident consent | unknown; OD-43 not decided | BRD OD-43 owners |
| F8 | Candidate FULL validation of #1203 and #1205 and actual native gate receipts | blocked (heavy lock owned by native rpi96 FULL gate, PID 1361642 alive at 2026-11-05 observation, 11 minutes elapsed, command targeting c6d5a8f3; refresh only, no authority over it) | Coordinator |
| F9 | Source-only drift risk: 64 versus 128 unit home bounds are documented and deliberate | deferred (documented) | none new |

Deduplication: F1 to F4 and F6 are owned by #188 (continuity and seam, PR #1203 head `c9a14573d76a128c028ca2371ed9612b41461b8a`, open, excluded) and #110 (ingestion). F5 is owned by #185 (PR #1205 head `dbacb32f8713c5c1acf088f8d8b536193f3269be`, open, excluded) and #140. Run controls are #189. The checkpoint owner is #440. A GitHub issue search for sunlight, live-sim, consumer schema and weather handover found only #184, #110, #188 and #440 (and unrelated #128, #360). No new confirmed defect was found, so no new issue is named.

## Exclusions

* Unmerged #1203 (public `c9a14573`, user-reported unpublished local `834e2bec`) and #1205 (public `dbacb32f`) and unmerged #128 sources are not read, not main and not accepted. Reported limits: the live-envelope admission, sunlight witness handling, corrected false handover pass and dry-run provisioning command are candidate claims, labelled separately only.
* Owner-recorded authorizations on #184 (2026-11-04 requirement, 2026-11-05 USD700-cap scoped authorization, admin-only controls) are existing, are not requested again and do not waive exact-head validation, capacity or secret controls.

## Disposition inputs

* Recommendation basis: continue the bounded record; fix current admission and handover engineering in #188 and #185 once their heads are validated; versioned weather-to-weather continuity is proposed research, not an approved pivot.
* Closure and expansion gates are stated in the plan. No owner approval is requested or inferred.

## Limits

* No SQL, browser, image, FULL, cloud or model run; nothing here is local-observed or Azure-observed for this head. Source inspection is not execution.
* Issue state, comments and PR state are GitHub reads on 2026-11-05 and may change.
