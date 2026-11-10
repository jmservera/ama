---
title: Issue 109 sensor-review stack integration preparation research
ms.date: 2026-11-10
task_id: 109-integration-preparation-1110
---

## Objective

Prospective preparation only: research and plan the later ordinary integration of the sensor-review stack (child #111 draft boundary under declared parent `feat/demo-sensor-review-109-1110`) into `main`. This record does not integrate, merge, push, retarget or accept anything. It is not new IoT work and not a claim that epic #109 is delivered.

## Exact identities (read-only observation after `git fetch`, 2026-11-10)

| Ref | Identity | Note |
| --- | --- | --- |
| local `feat/demo-sensor-review-109-1110` (this worktree) | `6cc59776666620309fb6b67ad2fdafb343d40998`, tree `eaf44bcdec8bdf5e9dfab2e73b1ded5459d8ff3c`, clean | Root fast-forwarded the previously empty parent to current main before launch. Zero unique authored commits; tree equals `origin/main`. |
| `origin/main` | `6cc59776666620309fb6b67ad2fdafb343d40998` | Registry PR #1393 (source-only). Also contains oracle repair #1392 (`57d32c0d0`) and docs #1394 (`15516ff3d`). |
| remote `origin/feat/demo-sensor-review-109-1110` | `06374dfcac47cf6bcce9e7b91f573e8565ab45e8`, tree `41b0eb476b90a064edceff7ab7d35a7b73c60d64` | Declared target of child PR #1395. An ancestor of main; unmoved and not pushed by this task. |
| child `origin/feat/demo-sensor-drafts-111-1110` (PR #1395 head) | `2b050647bff51eef4c1b34d6434bba7eae3d5f9a`, tree `e05b9c07d51d6a5f95250f5e9ba23f83c114aa74` | Ordinary `--no-ff` merge of child `325cb5c0c` and parent `06374dfcac`. Open, not merged; Root has given no merge permission. |

Main is three commits ahead of the remote parent (`git log 06374dfcac..6cc59776`): #1394, #1392, #1393. The child lacks them, so a direct child-versus-main diff shows main-only files as deletions. That is a base difference, not child work.

PR #1395 (live read-only `gh pr view`, 2026-11-10): base `feat/demo-sensor-review-109-1110`, head equals the identity above, mergeable, source-only checks (`src-changes`, `src-no-working-data`, `image-paths`, `src-namespace`, `src-agents`) succeeded, while `mssql`, `src-core` and `src-api` were still in progress. Hosted CI is therefore not yet a success for the exact head and is not claimed.

## Dry-run composition evidence

`git merge-tree --write-tree --name-only origin/main origin/feat/demo-sensor-drafts-111-1110` exits 0 with tree `b7d5494fa300ef65a8795da88ffe3c3d7375b4b6` and no conflicted paths. This predicts a clean ordinary merge of the current child head with current main. It is a prediction for the current child head only. The later merge is of the actually merged child-parent remote head, which may differ, so the prediction must be recomputed then.

## Child boundaries (net source diff `06374dfcac..2b050647`, excluding `.copilot-tracking`)

* `src/core/src/zava_forward/core/sensor_review_draft.py` (new, 388 lines): default-off flag `ZF_SENSOR_REVIEW_DRAFTS`, case key `sensor_review_drafts`, schema `sensor-review-draft-v1`, state `PROPOSED_UNAPPROVED`, roles Quality Inspector and Retrofit Programme Manager, max 20 drafts. Imports `sensor_analysis`, `sensor_analysis_store`, `sensor_consumer`, `sqlstore.CommittedReloadError`, `store.Store`, `synthetic.sensor_scenarios`. The served policy carries no approval, so the served write path refuses; approvals exist only in tests via a private synthetic seam. It creates no task, owner, queue entry, model call, ranking, hold, clock or consent change.
* `src/core/src/zava_forward/core/projection.py` (+1): `redact_staff_detail` drops `sensor_review_drafts` from generic staff detail.
* `src/api/src/zava_forward/api/server.py` (+34/-2): GET `/api/cases/<id>/sensor-drafts` and POST `/api/cases/<id>/sensor-draft`, dispatched ahead of generic case routes. `CommittedReloadError` maps to HTTP 409 with `outcome: committed`.
* `src/api/src/zava_forward/api/web/ops.js` (+29): proposed-not-approved draft section on the sensor screen.
* `src/api/checks/quality_sensors_browser_check.py` (+96): browser recipe extension. Not run by the child at the final tree.
* Tests: `src/core/tests/test_sensor_review_draft.py` (619 lines; 65 discovered, `JsonDraftCases`, `SqliteDraftCases`, opt-in `MssqlDraftCases` gated by `ZF_SENSOR_DRAFT_MSSQL=1`, 22 cases) and `src/api/tests/test_sensor_review_draft_api.py` (6 tests).
* Manifest: `src/core/pyproject.toml` adds a scoped `[[tool.mypy.overrides]]` with `disallow_untyped_calls = false` for the draft module and its tests. This is a scoped exemption, not unchanged strict typing.
* No schema, migration, infra, workflow, Dockerfile, permission or dependency line is authored by the child.

## Overlap with main-ahead changes

* `src/core/pyproject.toml` is the only file both sides changed: main (#1393) edits the `iothub` extra and `dev` list near the top; the child appends a mypy override block at the end. They are disjoint hunks, and the dry merge is clean. After integration the Core `dev` extra carries `azure-iot-hub==2.7.0` and `six==1.17.0`, so a venv built for the child alone (`/tmp/zf-111-1110/venv`) may lack them. Missing-dependency failures in configured mypy or tests are then a prerequisite finding, not a defect to repair, and a shared install is not authorized.
* Main's other source changes (`device_registry_azure.py`, `test_device_registry_azure.py`, `script_retry.py`, workspace browser checks and `test_workspace_scripts.py`) do not overlap child files. The Registry module is source-only; real identity issuance, credential owner, secure storage, teardown and live Hub, SQL, UI and model approvals remain unproven.

## Requirement and decision status (document-qualified; candidate versus approved)

IDs collide across documents, so every ID is qualified.

* BRD `docs/brds/agentic-retrofit-programme-brd.md` v0.21.0, `status: draft`, ms.date 2026-10-24: BRD FR-048 (in-use monitoring) with BRD AC-090, BRD OD-43 (monitoring inventory and ownership; blocks operational use with real data, not the simulator exercise). BRD FR-050 is unrelated (opt-in agent memory, if adopted under OD-44). The BRD is a draft, not approved.
* PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` v0.21.0, `status: in-review`, `exercise_status: author-complete-unsigned-pending-review-and-owner-acceptance`, ms.date 2026-10-25: PRD FR-050 with PRD AC-066, AC-067, AC-068, all verification status "Not run". BRD AC-066 to AC-068 are different requirements (regulatory source register, monitoring, change workflow). PRD AC-067 permits `SENSOR_REVIEW_DUE` only from an approved rule and only for a human; PRD AC-068 requires research phases R1 to R3 before any derived measure is used beyond an exercise rule.
* ADR 0003 (ms.date 2026-10-29), Status: accepted with amendment by the project owner 2026-10-15, decision 6 (IoT Hub as ingestion product); it explicitly records no deployment, cost, credential, DPO or legal approval, and no completion of issue #110. ADR 0002 sensor section is amended by ADR 0003 decision 6.
* The PRD is in review and the BRD is a draft: candidate, not owner-approved, requirement text. The child's `PROPOSED_UNAPPROVED` draft state matches that boundary.

## Issue scope (live read-only `gh`, 2026-11-10)

* #109 (open epic): the "Existing delivery and status" line "Not implemented" is historical. It must not be used to recreate delivered ingestion, simulator, UI or Registry work. Open criteria: (1) complete the scoped stabilization checkpoint defined in #440 before epic closure, merged children alone do not satisfy it; (2) all child features closed or deferred; (3) no sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking. All stay open.
* #111 (open): local versioned analysis and retained-store derivation delivered; open: outputs reproducible from retained readings (full SQL Server and task-flow reproducibility), approved `SENSOR_REVIEW_DUE` wiring, R1 to R3 method approval, UI and assistive-technology acceptance. Only "thresholds sourced or labelled exercise values" is ticked. PR #1395 uses `Refs #111` and does not claim these.
* #110 (open): local ingestion slices ticked; distinct real Hub identities and live Hub or Azure SQL acceptance unproven. #184 (open): live streaming stage 2, not started per its text. #112 closed.
* #440 (open): stabilization checkpoint; existing records for NomUX and Bicep observation (`handoff-440-nom-ux-operational-retry-1110`, `handoff-440-bicep-observation-1110`, on a different topic branch) are distinct and do not cover sensor integration. Its open criteria include triage and gating of epic closure and dependent expansion on blocking findings, and owner approval for pivots or deferrals.

## Child evidence read (Root files)

* `handoff-111-parent-adoption-1110.md`, `pr111-parent-qualified-1874.txt`, `independent-111-parent-adoption-1869/functional/` (`functional-findings.json`, `read-ledger.json`): verdict approve, zero findings at every severity, bounded to child head `2b050647b` against the declared parent only, explicitly not whole #111/#109, not current main `15516ff`, not a future tree and not publication approval.
* Child-run checks (staged merge before commit): draft suite 65 run, 22 opt-in skips; analysis 30, 10 skips; API 6; Ruff check and format pass; configured Core mypy pass over 290 files with the scoped exemption; actual disposable MSSQL `MssqlDraftCases` 22 run, 0 skips, exit 0, own container removed. Skips are not SQL passes. Synthetic local SQL is not Azure IoT Hub, Azure SQL or live continuity acceptance.
* Residual gaps: unforced `ConflictError` and `CommittedReloadError` branches unproved; scoped mypy exemption; no sensor browser run on the final tree; child review and critique were self-performed apart from Root's reviewer; parent-authored content (497 paths) was not reviewed by the child.

## Dependency and unresolved facts

* The later integration depends on PR #1395 actually merging into the remote parent branch. Merge method and the resulting remote parent head are unknown today. A squash would yield no child ancestry; an ordinary merge yields a merge commit. The plan reads the actual remote head then and never assumes `2b050647b` is an ancestor.
* Hosted checks for the exact child head were incomplete at observation time.
* The new #440 sensor-integration checkpoint is due (affected epic closure and dependent expansion) but is not created or run here. Root routes it through issue #440 RPI.

## Planning readiness

Ready for prospective planning. Research disposition: executed (read-only; no tests, runtimes, agents, pushes or GitHub writes). Candidate versus approved: BRD draft and PRD in-review are candidates; ADR 0003 decision 6 is owner-accepted for the exercise; no operational sensor rule, method approval or live acceptance exists.
