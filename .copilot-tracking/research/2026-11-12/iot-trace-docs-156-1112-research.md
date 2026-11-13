<!-- markdownlint-disable-file -->
# Research: demo IoT-to-UI source trace rows for the #156 register (2026-11-12)

* Task ID: `iot-trace-docs-156-1112`; parent `issue-156-demo-architecture-readiness-2305` (read-only handoff `rpi-156-architecture-readiness-2305-result.json`, outside the repository).
* Branch `research/demo-156-architecture-readiness-2305`, fast-forwarded from `eac1206c6` to current `origin/main` `e4854bd7e` (clean tree, fast-forward only, nothing moved or discarded).
* Purpose: re-verify against actual source paths every claim the handoff recommended for an additive documentation refresh. Research disposition: `executed` (bounded inline; no model, deployment, cloud, browser, test or gate run).
* Scope boundary: documentation only. Non-goals: Bicep, code, regulatory, spec, issue ticks, new issues, push, PR, merge, shared cleanup, the exhausted #184 minute-cadence and #146 routing source campaigns, any approval.

## Verified source facts (at `e4854bd7e`)

| ID | Claim | Source evidence read | Disposition |
| --- | --- | --- | --- |
| S1 | #189 has a local source screen `#/simulator` with a local browser check | `src/api/src/zava_forward/api/web/app.js:348,428` route; `web/simulator-control.js:2-4` (administrator screen, edits the control file only, cannot see or start a job); `simulator_admin.py` (added by PR 1313, commit `0dc4dd35c`, 2026-11-09); `server.py:488,1285` handlers; `checks/simulator_control_browser_check.py` (synthetic local store, pinned axe 4.10.3); `tests/test_simulator_admin.py`; `src/api/README.md` "Live simulator container" section ("no deployed job was started and live acceptance remains open") | Confirmed |
| S2 | The screen's budget alert is never verified | `simulator_admin.py` budget_alert `not_recorded`, `live_verified` False; README same section | Confirmed |
| S3 | #187 is only partially a control surface | `live_control.py` has start/stop (`enabled`), a 100-home cap and a 14-day window; `simulator_admin.py` offers the same start/stop only. Replay exists as a library: `src/core/.../synthetic/sensor_stream.py` (`Replay`, `replay`) and a speed pacer parameter in `src/api/.../iot_stream.py:384,402`. No pause control and no operator screen for replay, speed or fault selection was found in the bounded trace. Public issue state read with `gh` on 2026-11-12: #187 CLOSED, all three criteria ticked; #189 OPEN, criterion 3 (owner, time limit, budget alert) unticked | Confirmed as partial; the closed-issue state and the source are not reconciled here (non-exhaustive) |
| S4 | Employee Quality sensor panel design is Not supplied | `app.js:1146` composes `sensorPanel(id)` into the "Quality and handover" tab beside `qualityPanel` and `handoffPanel`; `ops.js:155` `qualityPanel`; `checks/quality_sensors_browser_check.py` exists. `docs/reference/research/ux/employee-case-workspace-redesign.md` names `qualityPanel` and `handoffPanel` (lines 134, 165) but contains no `sensorPanel` or sensor-panel specification | Confirmed; no versioned design supplied |
| S5 | Source cadence is 5 minutes, owner target is 1 minute | `core/synthetic/live_readings.py:24-25` (`SLOT_SECONDS = 300`, `SLOTS_PER_DAY`); `live_simulator.py:3,393`; `infra/live-simulator-job.bicep:27` (`*/5 * * * *`); `docs/capstone/demo/runbook.md` (target "not verified against the current simulator cadence") | Confirmed; recorded as a gap only, not a campaign |
| S6 | Five-home AI scope is not verified by the bounded trace | `core/assistants.py` scan is bounded by `scan_interval` and `scan_size` (defaults 60 and 20, bounds 5-3600 and 1-100, lines 362-381) with a `scan_cursor` over cases (lines 1149, 1320); neither `assistants.py` nor `sensor_view.py` references `ZF_SIM`, a control cohort or a home allow-list. `infra/main.bicep:71` `enableApiAi` default false. The five-home limit is the simulator control cohort (runbook). The search was a nonexhaustive grep of two core modules and `infra/main.bicep`; orchestrator, agents and other background paths were not traced | Not verified. No global absence of an AI guard is asserted |
| S7 | Runbook already labels the targets unverified | `docs/capstone/demo/runbook.md` lines 48-70 and 113-115 | Confirmed; the new rows cite it and do not edit it |

## Process and history constraints

* #156 criterion 1 remains unticked; C2 to C4 ticked and unchanged. All 74 snapshot designs Not supplied. Programme queue design (PR 1372, parent branch) stays PROPOSED/PARTIAL/NOT APPROVED; one D1 consumed; source-correction balance UNKNOWN. This documentation trace is distinct current-source evidence, not a code-correction grant or fresh pool.
* The executable register gate `tools/check-design-trace.py` parses only the table under `### Known screen features and exact trace or gap` up to the next `##`/`###` heading (`HEADING`, `nxt` at lines 19-45). A new `###` section after the second delta cannot change its counts. The tool is not run (documentation, link and diff review only).
* The 2026-10-18 rows (#187 at line 377, #189 at 378) and the delta sections are preserved byte-identical; the change is purely additive.

## Decisions and readiness

* Add one dated `###` section ("Demo IoT-to-UI source trace update (2026-11-12, Refs #156, #184, #187, #189, #134)") immediately after the second delta and before the link definitions, plus a KB index row and an appended log entry. No edit of earlier rows, runbook, README, Bicep, code or spec.
* Planning Readiness: `Ready`. Remaining unknowns are carried into the text, not resolved.
