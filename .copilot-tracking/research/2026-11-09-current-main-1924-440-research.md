---
title: Current-main integrated journey checkpoint 440 (1924) research
ms.date: 2026-11-09
task_id: 440-current-main-1924
---

## Disposition

Research executed 2026-11-09 (read-only Git, `gh`, coordinator brief and comments). Planning Readiness: Ready. A new recurring #440 checkpoint triggered by the earlier lifecycle and shared-SQL integration trigger that remains due. It is evidence only: no source fix, test, policy or coordinator change, and no issue, board or pull request write. Earlier #440 sections, their reviews and every adverse outcome stay as authored.

## Pinned identities (read 2026-11-09)

* Source `main` `2be660e9d290f95ff05fc5a56d6539768576732b` (PR 1326 squash), tree `d09e22c71df705ad13127a490b0d742269d2f2a2`. After `git fetch origin main`, `origin/main` resolves to the same commit. Branch `test/demo-stabilization-440-1109-1924` starts there, clean.
* Subtrees: `src` `86bc00e19a167e517ae2955ad88d6e2f7b4eac26` (identical to the tree the 1326 SQL campaign executed on), `tools` `74ad3cb586db...`, `infra` `b0969f8b7b8c...`, `.github/workflows` `29eb03ea759e...`.
* Document identities, read at this commit: BRD 0.21.0 `draft` blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 `in-review` blob `c788b917bafaede215f326f0efc71e071a687f1c`; case study original `0aec2d80`, addendum `28c19242`; ADR 0001 Proposed `d42fa5c4`, 0002 (only its staff identity decision accepted 2026-10-24) `cbe21530`, 0003 `d6064539`, 0004 `9406c2e7`, 0005 `4d610335`, 0006 `956da1a3`, 0007 Proposed `abb21088`. All unchanged since the previous checkpoint. A draft or in-review document does not become approved by this record.

## Merged since the demo checkpoint (`df8e858b2`)

* Merged and now in scope: #1141 Azure Queue adapter (`4fcd1934f`, #144 slice), #1295 capstone architecture (`ad679b96b`, documentation and tools), #1308 priority ordering and SQL index bootstrap (`8d6f029ca`), #1312 chat-schema SQL selector, #1240 lifecycle (`3a9767d5c`), #1313 simulator controls (`0dc4dd35c`), #1315 photo regression (`48350983b`), #1320 metadata-only validation refusal receipts (`ba71894bb`, previously excluded as open, now merged), #1322 controls and photo checkpoint (`1a84b3b00`), #1326 current-source SQL evidence (`2be660e9d`). Rubric score commits touch only `.github/rubric/scores/latest.json`.
* Source delta from the previous checkpoint base `48350983b` is four files and 113 insertions: `chat_panel.py`, `server.py` and two `test_chat_panel.py` files (PR 1320). Nothing else under `src`, `tools`, `infra` or `.github/workflows` moved. The current `src` tree equals the 1326 SQL campaign input (that campaign ran after 1320 merged). The earlier 189 browser input (`e192bc747`) and 954 browser input (projection `7c72dbd58`, `src` tree `99c5354d`) predate 1320, so their production runtime differs from current by the 1320 chat delta; the 189 input also predates the 1315 photo-check script, so its test tree differs too. Each observation keeps its own source identity (critique PC-003).
* Excluded (not on main): #1288 Quality AI and retained-value UI (issue OPEN, no merged PR), #1258 and #1259 ranking archive durability (OPEN issues), #136 infrastructure epic (OPEN), #144 beyond the merged queue adapter, #1296 (candidate policy), and any unpublished work. None of these becomes merged-main acceptance.

## Issue states read live

#440, #123, #81, #136, #144, #146, #159, #184, #185, #189, #891, #1258, #1259, #1288, #1292, #1296, #1297 OPEN; #91, #954, #1314 CLOSED; #1324 MERGED. Latest #440 comment (19:31:53Z) states the resume scope and that literal unmet criteria stay unticked. Open #440 criteria: triage of confirmed findings (owner approval for requirement change, pivot or deferral) and the genuine independent-review plus Major HVE Builder behavior-validation obligation. This checkpoint does not satisfy either.

## Requirement trace (document-qualified)

BRD and PRD functional requirement numbers collide, so every trace names its document.

* PRD FR-050 with AC-066 to AC-068 (simulated monitoring through IoT Hub, retained values, sensor data is not acceptance evidence), BRD FR-048 and AC-090, BRD RULE-014, ADR 0003 decision 6 (Basic IoT Hub). Source boundary: `live_control.py`, `live_simulator.py`, `simulator_admin.py`, `sensor_consumer.py`, `sensor_ingestion.py`.
* PRD FR-044 and BRD FR-044 with AC-084 (real AI per record, proposal against reviewed, case access independent of the model), ADR 0004 option C staged, ADR 0005 synthetic development only. Source boundary: `assistants.py`, `chat_panel.py`, `ai_boundary` tests and call-site inventory.
* PRD FR-008 controlled transition gate with FR-016 and FR-017 (lifecycle, resident decisions, complaints route), merged by #1240. Human approval, resident consent and legal review stay with named humans.
* PRD FR-003 and ADR 0002 staff identity decision (Entra principal, assigned roles); administrator-only simulator control with view-only refusal.
* ADR 0006 (`src` layout and cut-over) for the package boundaries core, agents, api.

## Journey read from source (not a live observation)

* Simulator and control: finite control document, owner, approval reference, 14 day maximum expiry, cohort 1 to 100, fail closed, advisory lock, lazy IoT SDK import, administrator-only screen.
* Persistence and employee UI: receiver admission of `live-sim-reading-v1` and consent, mapping and window checks exist in core; no employee retained-sensor-value route or script was identified in the inspected `src/api` paths (earlier C1 qualification keeps this limited to the inspected paths). The retained-value employee view and the sensor input to the real Quality model are #1288, unmerged.
* AI-unavailable: unconfigured or failed model paths return named manual routes; deterministic rules are not presented as actual AI; no actual model call is made in tests.
* Chat: #1320 records one metadata-only receipt for a route-refused malformed ask and none for a refused user.

## Classification (carried and to be confirmed)

* Local observed (current source): the selected checks of the implementation phase.
* Local observed, historical and source-equivalent (reused, not rerun): #1326 SQL campaign (148 tests, 67 on SQL Server, 0 skips, source tree `86bc00e1`), #1313 and #1315 browser observations (the `src` runtime source differs only by the #1320 chat receipt delta). Limits recorded by #1326 Q1: query exit status not retained, no timeout-path receipt, mutable image tag with `--pull=never`.
* Azure observed: none for sensors or Quality. Implemented, unverified: simulator jobs, Hub admission, sensor SQL grants, deployed parity, resident own-home freshness. Deferred: production compliance, legal, security hardening, live run, budget alert (#146, #189). Blocked: #1288, #1258, #1259, #136, #185. Unknown: startup failure cause of #1292, deployment parity, calibration validity, work-package identity.

## Check selection rationale (demo-targeted tier)

* Heavy SQL: not rerun. The `src` tree is unchanged from the #1326 input, which stays the evidence with its limits. The lock was observed free (`flock -n`) but no necessary distinct heavy check exists.
* Native unit and HTTP-level tests in an owned virtual environment (editable installs of this worktree, verified import paths), selected by affected package boundary: core sensor consumer and live, resident sensors, chat panel, lifecycle gates, resident decisions and queue, quality procurement, AI consumption safety; API live control and simulator, simulator admin, IoT stream and credential hygiene, sensor ingestion and handover demo, AI boundary and call-site inventory, chat panel, assistants, resident assistant, role matrix, photo availability; agents queue adapter and worker.
* Browser: playwright is not installed in the isolated environment and the only changed runtime source since the browser observations is server-side chat receipt logic, so no browser run is selected. Recorded as not run, not as passed. No assistive-technology, actual-model or live check is possible or claimed.

## Findings candidates and owners

No defect is confirmed at research time. Existing owners for known gaps: #1288 (employee retained values and Quality AI grounding), #1258 and #1259 (ranking archive), #1292 and #81 (SQL ordering, lifecycle), #189 (live run owner, time limit, budget alert), #144 (hosting and load), #159 (chat), #891 (per-call chat activation), #146 (monitoring alert), #185 (device provisioning), #1297 (skip contract). Any defect observed in the checks will be compared to these before proposing a new issue.

## Qualification Q1 (appended 2026-11-09 after the frozen head; original rows unchanged)

* The original row joining PRD FR-008 with FR-016 and FR-017 for resident decisions and the complaints route is preserved as an error. PRD FR-008 governs controlled gates. PRD FR-016 and FR-017 are provider-package and quality-disposition records. This checkpoint asserts no resident or complaints requirement ID and invents no replacement or approval.
* The original native Review verified the correction in the evidence pack only, not in all tracking records.
