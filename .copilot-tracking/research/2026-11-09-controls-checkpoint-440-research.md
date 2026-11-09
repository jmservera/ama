---
title: Lifecycle and simulator controls current-main checkpoint 440 research
ms.date: 2026-11-09
task_id: 440-controls-checkpoint-1109
---

## Disposition

Research executed 2026-11-09 (read-only Git, `gh`, coordinator evidence files). Planning Readiness: Ready. A new recurring checkpoint for #440, not a corrective cycle and not a renewal; no feature, code or policy change. The previous scoped #440 work (PR 1317, merged `2b6d80a2`) and its original C2 and Low findings are not touched; #1314 owns count and range wording follow-ups.

## Pinned identities (read 2026-11-09)

* Source `main` `48350983be156d33afb5803570e1bc0bdb5455bb`, tree `1f6f8021cfbab17ee4975ada308771ba1cbd952b`, `src` tree `99c5354df6d5ebe886d1ad1b98e6a60146543c03`. Branch `docs/demo-controls-checkpoint-440-1109` starts at that commit, clean.
* Merged PRs: 1240 (`3a9767d5c`, 16:50:00Z, lifecycle #81, head `ccc7358d`), 1317 (`2b6d80a2`, 17:11:39Z, previous 440 checkpoint), 1313 (`0dc4dd35`, 17:35:18Z, simulator controls #189, reviewed head `e192bc747`), 1318 (`9557d9da`, 17:44:15Z, #1292 diagnostic record), 1315 (`48350983`, 17:47:10Z, photo regression #954, head `c46a7a025`). Two rubric score commits (`700bf11e1`, `b4a343a16`) carry only `.github/rubric/scores/latest.json`.
* Open exclusion: PR 1320 (`ff06a15f`, chat refusal receipts, OPEN) is not on main and is not accepted here. #159 stays separate (OPEN).
* Issue states read live: #81 OPEN, #189 OPEN (live run owner, time limit and budget-alert criterion unticked), #954 CLOSED (both literal acceptance criteria ticked), #1292 OPEN, #440 OPEN, #1314 OPEN, #1288, #1258, #144, #123 OPEN.

## Source delta since the previous checkpoint base `3a9767d5c`

* 16 files, 1889 insertions and 43 deletions, all under `src/api` plus the rubric file: `live_control.py` (advisory file lock, `CONTROL_BUSY`), `live_simulator.py` and `iot` import made lazy (`IOT_SDK_MISSING`), new `simulator_admin.py` (administrator start, status and stop, view-only 403, unconfigured 503), `server.py` and `workbench.py` routes and destination, new `simulator-control.js`, `app.js` and `index.html` includes, two browser checks (`simulator_control_browser_check.py` from 1313, `photo_flag_stale_browser_check.py` from 1315), tests and README.
* No file under `src/core`, `src/agents`, `infra`, `tools` or `.github/workflows` changed after `3a9767d5c`.
* 189 production source equality: `git diff e192bc747 48350983b -- src tools infra` is one file, the new 1315 check script (448 lines, hash `620301300f3f3dc5...`). `git diff e192bc747 0dc4dd35c -- src tools infra` is empty. Runtime source on main is therefore byte-equal to the reviewed 189 head; only the photo check script is new. The 1315 delta in `src` is that one script.
* 954 projection: the tree the coordinator tested (`7c72dbd58588094956c7467e0b7b4afbe1c7fc2e`, merge of `c46a7a025` into `0dc4dd35`) has the same `src` tree as main (`99c5354d`). All 642 members of `MANIFEST-projection-src.sha256` verified OK against `git archive` of main `src` (this research, `sha256sum -c`).

## Evidence byte witnesses (external, coordinator files; read this session)

* 189 `capture-189-composed-browser/`: `sha256sum -c hashes.sha256` 78 of 78 OK; `hashes.sha256` sha256 `2f0275c1743b7af5062b08bb60057e710209d461c569b3aa6a998e6142b03e01` (matches the handoff); `browser.exit` 0; stdout ends "Simulator control browser check passed". Handoff: 13 states, 13 axe scans, 0 violations at `e192bc747`, delayed-Stop probe old exit 1 (negative control) and new exit 0. Independent Functional `independent-189-c4-final/functional-findings.json`: approve, 0 findings.
* 954 `evidence-954-current-main/`: `MANIFEST.sha256` 16 of 16 OK; browser exit 0; `browser.out` has 83 `PASS` lines and 1 `FAIL` line (the expected negative control, followed by `PASS negative control`); one `flock -n` admission 17:41:21Z to 17:41:27Z after a holder check (`fuser` exit 1, no holder). Independent `independent-954-current-main/functional-findings.json`: approve, 0 findings. Native failed-resource diagnostics exist; `literal_no_console_event` is false and informational.
* Hosted: PR 1313 and PR 1315 each read as all 19 status entries SUCCESS (coordinator ledger, #1315 re-read with `gh`: MERGED).
* 1292 #1318: docs-only, 0 of 2 historical paired campaigns reproduced, cause UNKNOWN, original failure then 4 passes in 5 total executions, manifest 26 members plus itself (coordinator ledger). No current-source SQL fix or acceptance follows.

## Document identities at `main` (draft is not approved)

BRD 0.21.0 `draft` blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 `in-review` blob `c788b917bafaede215f326f0efc71e071a687f1c`; case study original `0aec2d80`, addendum `28c19242` (ms.date 2026-11-08); ADR 0001 `d42fa5c4`, 0002 `cbe21530` (staff identity accepted 2026-10-24, rest proposed), 0003 `d6064539`, 0004 `9406c2e7`, 0005 `4d610335`, 0006 `956da1a3`, 0007 `abb21088`. All unchanged from the previous checkpoint.

## Requirement trace anchors (document-qualified)

* Simulator and IoT: PRD FR-050 and AC-066, ADR 0003 decision 6 (as cited by the #189 issue body), PRD FR-050 monitoring observations via IoT Hub. BRD OD-43 asks for the actual monitoring inventory and ownership (open decision). BRD and PRD FR numbers collide, so each trace names its document.
* Lifecycle: PRD FR-008 (controlled-transition gate) with FR-016/FR-017, as established in the issue 81 alignment section already in the pack.
* Boundaries read from source: administrator-only (`ADMIN_REQUIRED` 403), view-only administrators see options but change nothing (`VIEW_ONLY` 403), unconfigured control 503 with a named manual route (`MANUAL_ROUTE`), finite expiry at most 14 days, cohort capacity checks (`B1_QUOTA_HEADROOM`), confirmation tick, stale-control check, and budget alert reported `not_recorded`, `live_verified` false (`simulator_admin.py:131`); the control starts no job, calls no Azure API and changes no role.

## Findings and dedupe

* No new defect or refactoring is confirmed. Candidate items are all existing and owned: SQL ordering recurrence and current-source SQL acceptance (#1292, with #1314 for wording), ranking archive durability (#1258), quality sensor grounding (#1288), hosting and load (#144), chat receipts (#159 and PR 1320, not on main).
* Unverified by design: live run, budget alert (#146), SQL Server and Azure paths (189 handoff records 19 Source and 110 Core SQL/Azure skips), assistive technology, literal console zero, model-backed behavior, whole Major HVE behavior validation obligation of #440.

## Planning Readiness

Ready. Needed fresh checks are none: source equivalence to already-run trees is proven by tree and manifest identity, so no unit or browser campaign is repeated.
