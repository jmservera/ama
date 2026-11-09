---
title: Demo stabilization checkpoint 440 research
ms.date: 2026-11-09
---

## Task identity and scope

* Task `440-demo-stabilization-checkpoint-1109`, slug `demo-stabilization-checkpoint-440`, parent task `440-visible-demo-checkpoint` (2026-11-08). State: `.copilot-tracking/rpi-sessions/2026-11-09/demo-stabilization-checkpoint-440-state.json`. Mode automatic, written from 2026-11-09T12:42Z, before any repository edit.
* Worktree `/home/azureuser/source/ama-demo-wt/issue-440-demo-checkpoint-1109`, branch `docs/demo-checkpoint-440-1109`, target `main`. Clean at start. The dirty primary checkout was not touched.
* Objective: one dated, bounded current-main demo stabilization record in the existing `docs/architecture/cutover-evidence-pack.md`, plus the existing index and append-only log. Documentation only. No coordinator, feature, test, workflow or infrastructure change. No push, pull request, board, issue or merge action.
* Research posture `focused` (bounded internal task, named sources, supplied triggers). Provenance: owner brief. Output mode `analysis` and `audit` (decision state, no new implementation recommendation outside the brief). Extensions: repository instruction file (selected, scope all), `docs/reference/method/tracking-retention-policy.md` (selected), web-design-guidelines (skipped, no web file is edited), WorkIQ and external research (skipped, no external claim is made). No interaction needed; the brief fixes scope.
* Caller controls: UNMERGED #1288 E3, #1292 E1, #144 new head, #189, #1295 and #1296 are EXCLUDED functionality; no live Azure, model, job or expense; no full gate; no private data; retained evidence only as historical with Git equivalence; honest limits kept.

## Triggers (observed 2026-11-09 via `gh`)

* PR 1222 (#123/#128/#440): MERGED `d4d6827fe60be651cd922ab9656688c18c978e1d` at 09:12:23Z, head `5ecc1fe9dd214b8f2b8080f680f3f9d6d03842e5`. Source change: `paired_equity.py` plus tests and README; added about 1966 lines to the evidence pack and index/log (W1 `git show --stat`). Constructed-cohort diagnostic only; `fairness_evidence=False` and `activation_allowed=False` per its body.
* PR 1304 (#184/#185/#188): MERGED `23e944c1fccf0c4578e7beb0740ddd55c3f935b2` at 12:19:47Z, head `68fc3e61b187175e87bedd412a2b8d8c261be435`, 19 hosted entries returned (the body says 19 hosted checks passed; counted from `statusCheckRollup`, not individually re-read).
* #440 comment `6740015794` (2026-11-09T12:25:55Z): scoped trigger. Next checkpoint pins fresh main, qualifies BRD/PRD/ADR status, simulator to persistence to UI/Quality-model contracts, manual/failure/consent boundaries and unmerged exclusions; whole #184/#136/parent closure unproven; "no fabricated record/live approval".

## Pinned identities (read-only fetch 2026-11-09T12:38Z)

* `origin/main` = `HEAD` = `df8e858b2150198e5e22c73d224a0d3592c73daa`, tree `af1e9ea329f7ff5116c1279ab780ef649b1593cd`, a rubric-bot commit (`chore(rubric): record score 78/100`).
* `git diff --name-only 23e944c1f df8e858b2` lists only `.github/rubric/scores/latest.json`. So main equals the PR 1304 squash for every source, infra, tool and document path.
* A local-only ref `origin/pr1304` was fetched (`refs/pull/1304/head`, `68fc3e61b`) to compare. It is a local read-only ref, not a repository write.
* Documents at this tree (blob via `git rev-parse HEAD:path`): BRD 0.21.0 `draft` `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 `in-review` `c788b917bafaede215f326f0efc71e071a687f1c`; original case study `0aec2d8070117a647574b1fadc8cfbdd2af68598`; addendum `28c1924285eed255e53c1e359e0ad98eedab1d22`; parity matrix `91b5d33d47f2e73640513a0bca86cbf0412be7dc`.
* ADR statuses (headers read): 0001 Proposed `d42fa5c4...`; 0002 Proposed with owner-accepted staff identity decision 2026-10-24 `cbe21530...`; 0003 Accepted with amendment 2026-10-15 (Basic IoT Hub) `d6064537...`; 0004 Accepted 2026-10-15 `9406c2e7...`; 0005 accepted for synthetic development only `4d610335...`; 0006 Accepted 2026-10-15 `956da1a3...`; 0007 Proposed, not accepted `abb21088...`.
* `docs/reference/memory.md` blob `e1268db9...`, dated 2026-09-30; read for context only, not evidence.

## Wave 1 (wider): candidate areas and questions

Q1 Which requirement and decision IDs does the sensor path trace to, BRD against PRD. Q2 What on main implements each hop simulator to persistence to UI to actual Quality model to attributed flag. Q3 What auth, tenant, admin, consent, approval, failure and identity boundaries exist for those hops. Q4 What retained 184 evidence may be reused and on what proof. Q5 What can be observed locally now with tiny existing tests. Q6 What are the gaps, owners and dependent gates. Q7 Is any new defect confirmed.

## Wave 2 (deeper): evidence

### Requirement and decision trace (document-qualified)

* C1 BRD `docs/brds/agentic-retrofit-programme-brd.md:1588` FR-048 (consented, lawfully recorded in-use monitoring retained with source, mapping, calibration and time, separate from analysis) with AC-090; `:1589` RULE-014 (an absent AI flag or sensor alert is not acceptance evidence; sensor data informs a decision only after validity rules). BRD FR-044 (`:1602`) and AC-084 cover agent output provenance and named human review.
* C2 PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1425` FR-050 (simulated humidity/temperature through Azure IoT Hub, validated and appended to Azure SQL with provenance, deterministic review signals that only create a human review task) with AC-066, AC-067, AC-068 (`:2162-2164`). PRD FR-044 (`:1419`) real AI in each accepted build, optional per record, proposed versus reviewed distinct, case access independent of model availability.
* C3 ID collisions: BRD FR-050 is opt-in staff memory (`:1665`), PRD FR-048 is offered versus confirmed appointments (`:1423`); neither is sensor work. Every trace in this record names its document.
* C4 ADR 0003 decision 6 (`docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:114`): IoT Hub is the ingestion product; Accepted with amendment 2026-10-15, owner acceptance not extended to other parts. ADR 0004 option C staged covers employee chat, not sensor Quality review.
* C5 BRD and PRD are draft and in-review. They are not approved, and no document edit is made here.

### Hop-by-hop source reading on main `df8e858b2`

* C6 Simulator: `src/api/README.md:2025-2135`; code `src/api/src/zava_forward/api/live_simulator.py`, `live_control.py:28-100`. One synthetic reading per home per 5-minute UTC slot, `live-sim-reading-v1`, `source_type=SYNTHETIC`, no AI; control document `live-sim-control-v1` with owner, approval reference, `enabled`, hard `expires_at` (at most 14 days from start), cohort 1 to 100; sink `iothub` refuses without it and fails closed on stop, expiry or unreadable file.
* C7 Transport and jobs: `infra/live-simulator-job.bicep` and `infra/live-receiver-job.bicep:34-36` (immutable `@sha256:` image only, tags refused, scope guard on resource group `ama`, environment `cae-cutover-test-demo`, `routingReady` false by default, receiver has its own identity, share mounted read-only, manual trigger). Authored and compiled; the header says NOT deployed.
* C8 Persistence: `src/core/src/zava_forward/core/sensor_consumer.py:431` (admission of `live-sim-reading-v1`, 16-field closed shape, slot alignment, consent, window and clock checks), `:734` `observed_series` keeps the indoor `reading-v2` contract and excludes live rows; `retained_envelopes` returns the original 16 fields; sunlight lives only in the retained witness. `src/core/src/zava_forward/core/sensor_sql.py` is a sensor-only SQL connector with no DDL, seed or case write. The README states live rows are not calibrated indoor evidence and pre/post retrofit context shows as missing.
* C9 Employee UI: no employee route, template or script on main reads retained live readings. `grep -rl -i sensor src/api/src/zava_forward/api` returns `live_control`, `sensor_ingestion`, `live_simulator`, `live_receiver`, `sensor_handover_verify`, `iot_stream` and the resident script `resident_demo/web/demo.js`, and no employee `server.py` or `web/` file. The resident demo shows own-home readings with textual channel statuses (`resident_demo/web/demo.js`, per the audit citations, not re-read in depth). `retained_envelopes` is consumed only by core tests and `sensor_handover_verify.py`.
* C10 Quality model input: `src/core/src/zava_forward/core/assistants.py:156-160` builds the `quality-evidence` source from `quality.active_records` (measure, state, versions, labelled items) and checklists only. No sensor key is in the source. `assistants.py:47-56` registers `quality-evidence` roles and the missing-evidence rules; autonomy is proposal-only through `Assistants.review`. `src/core/README.md:1136-1178` states that no new sensor AI task is authorised and that map points carry no sensor fields.
* C11 Attributed flag: none exists on main for sensors. The prior pack (2026-11-08 visible-demo checkpoint) records the Quality L4 autonomous flag as proposal-only. The only sensor-derived human task is the deterministic review signal in PRD AC-067, not model output.
* C12 Auth, tenant, admin: staff access derives from a verified Entra principal in the configured tenant with assigned application roles (PRD FR-003 `:1378`; ADR 0002 owner decision). Authentication trusts the ingress-provided X-MS-CLIENT-PRINCIPAL header and validates no token signature (`src/api/src/zava_forward/api/auth.py:7-14`), so it is safe only when reachable solely through the platform ingress (deployment prerequisite, not observed here). Simulator administration is Azure RBAC on the share and job; an in-app admin screen is not delivered (`src/api/README.md:2107-2110`); this is #189's unmet detail. The receiver and simulator use separate identities and minimum grants (`infra/live-receiver-job.bicep:9-10`, README grant text).
* C13 Manual, failure, consent, approval, identity boundaries: stdout dry-run sink; fixed-code errors only with no traceback or driver text; missing certificate is non-retryable; stale, missing and unavailable states are explicit; quality acceptance stays a human decision (#91 closed 2026-10-17); resident consent is checked at admission; package identity here means the image digest (C7) and the case/measure identity of Quality records (C10). Work-package identity is UNKNOWN: an image digest is not work-package identity and the work-package path was not examined here.

### Retained 184 evidence and Git equivalence

* C14 `git diff --stat 68fc3e61b df8e858b2 -- src infra tools .github/workflows pyproject.toml` is empty. All non-tracking differences between the PR 1304 head and main are the rubric file. Therefore the source under test in the 184 handoff (`handoff-184-current-main-validation.md`, HEAD `68fc3e61`, tree `39e2a3f4b7599844e45fe7c441910ea6ff0d08f6`) is byte-identical to main for `src`, `infra`, `tools` and workflows. Equivalence of source is proven by Git; the runs are historical and were executed by that session.
* C15 Reused only as historical observed (coordinator handoff and PR 1304 body, logs not committed and not re-read by this task): owned disposable SQL default 70 and analysis 10 tests, zero skips; Core `sensor*` 192 OK with 11 offline opt-in skips, device 48, live 22, resident_sensors 10, historical_backfill 10; API `live*` 66 with 2 SQL-need skips, `iot*` 49, `sensor*` 103; paired-equity 23; API mypy 0 errors in 199 files and Ruff exit 0; `tools` rpi-checks 102. Limits carried: mutable SQL image tag with contemporaneous digest and pip-freeze hashes (not a hermetic attestation), some earlier piped producer exits not individually captured, no executed-selector import trace, original failing logs overwritten by reruns, a send-rate timing assertion once failed then passed (root cause unproven), original mypy 53 errors in 48 files from a missing playwright 1.64.0, carried Low (exact-grant receiver main, rejected DQ, replay SQL coverage) open.

### Current observations (this task, tiny existing tests only)

* C16 Installed `src/core`, `src/agents`, `src/api` editable from this worktree into an external venv `/home/azureuser/source/ama-demo-wt/venv-440-1109` (the pre-existing editable installs pointed at the dirty primary checkout, so were not used). Import paths verified to this worktree. Logs are external in `/home/azureuser/source/ama-demo-wt/logs-440-1109/`, not committed. HEAD `df8e858b2`. Python 3.12.3.
* First attempts failed on harness imports only (producer exit 1): `core-sensor-consumer-live.log` (missing `sensor_consumer_fixture`, tests dir not on `PYTHONPATH`) and `api-assistants.log` (missing `test_mvp`). Both retained unchanged. Not product failures; reruns added `tests` to `PYTHONPATH`.

  | Command (cwd) | Producer exit | Result |
  | --- | --- | --- |
  | `python -m unittest -v tests.test_live_control tests.test_live_simulator` (`src/api`, `PYTHONPATH=../core/tests:../agents/tests`) | 0 | 64 tests OK, 0 skips |
  | `PYTHONPATH=tests python -m unittest -v tests.test_sensor_consumer_live` (`src/core`), log `core-sensor-consumer-live-r2.log` | 0 | 10 tests OK, 0 skips |
  | `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest -v tests.test_assistants` (`src/api`), log `api-assistants-r2.log` | 0 | 120 tests, 58 skipped ("needs disposable SQL Server (ZF_TEST_MSSQL=1)"), 62 ran OK |

* C17 These runs prove control fail-closed logic, simulator mechanics and live-envelope admission on fixtures, and assistant contract mechanics, at this exact tree. They do not prove SQL behavior (SQL not run, owned resource avoided), a live Hub send, the employee UI, a real model call, or any acceptance. SQL-skipped assistant tests are not SQL evidence. No Quality-sensor test exists because no such path exists.

## Wave 3 (contrarian)

* Counter-hypothesis A: main already has an employee sensor view. Rejected by C9 (search over `src/api` and the `assistants.py` capture). Residual: the search is textual; a differently named path is not excluded (stated as a limit, as in the 2026-11-08 record).
* Counter-hypothesis B: PR 1304 plus 19 green hosted checks means the IoT demo path works end to end. Rejected: its body leaves AC1, AC3 live evidence and the integrated Quality UI/model same-ID proof unmet; jobs, certificates, route, grants and quota are unverified (audit blockers T1, Q1 to Q3).
* Counter-hypothesis C: the retained 184 results are fresh because source is identical. Rejected: byte equivalence proves what source ran, not that the logs, image and environment are current; they remain historical observed. Not relabelled.
* Counter-hypothesis D: the #1296 High REVISE (eleven of 27 matches), #1288 E3, #1292 E1 or #144 corrections change main. Rejected: all are unmerged, excluded, coordinator-reported (briefs of 2026-11-09), not observed by this task. The #1296 result is an adverse, unmerged candidate-policy outcome, not current-main pass or native validation, and no coordinator change follows here.
* Counter-hypothesis E: a new defect is visible. None reproduced. Stale text in the #184 issue body ("not started", "no Hub module") is an observation by the 2026-11-09 audit, not re-verified by this task and not a code defect; no issue is proposed. #1297 (sensor MSSQL skip binding) already owns the skip-contract concern, so it is referenced, not duplicated.

## Classification (parent synthesis)

| Class | Item |
| --- | --- |
| Local observed (this task) | Git identities and equivalence; document blobs and statuses; source reading above; the three test runs with exits |
| Local observed, historical | 184 SQL 70 plus 10, Core and API suites, static checks (source-equivalent, environment not re-proved) |
| Azure observed | None for sensors. Earlier one generic employee chat model answer (2026-11-08, PR 1290) is not sensor or Quality evidence |
| Implemented, unverified | Simulator, control, receiver jobs, consumer admission against real Hub, sensor-only SQL grants, deployed jobs; resident own-home sensor view freshness |
| Deferred | Production compliance, legal, security hardening, named human approvals; live admission of finite cohort and model |
| Blocked | Employee retained-value UI and actual Quality model input (#1288, unmerged), admin screen (#189), live transport prerequisites (#185, #140, #110) |
| Unknown | Current deployment parity with main; certificates, route, quota and cost headroom; calibration and statistical validity; generator provenance authentication |

## Gaps, owners, gates (deduplicated against existing issues)

* Missing hop: persistence to employee UI to actual Quality model to attributed flag (owner #1288, unmerged). Admin start/status/stop surface (#189). Provisioning and credentials (#185, #140). Receiver live ingestion (#110, #188 three live criteria). Persistence ordering (#1292, #81 via PR 1240). Worker/queue (#144 via PR 1141). Skip contract (#1297). Chat activation per call (#891). Architecture deck (#1295).
* Affected closure and expansion gates: #184, #185, #188, #110, #189 and #136 closure, parent #123 and #440 triage and independent-review criteria stay unproven. Dependent expansion on the actual Quality sensor path waits for #1288 plus finite admission. Independent lanes (#189 source, #1292, #144, #1295, #1296) continue.
* Recommendation (bounded, no pivot or deferral inferred): CONTINUE the existing demo path through the existing owners; HOLD closure claims; no fix or new issue proposed by this checkpoint. Exact resume conditions: (1) #1288 merged on main and independently assessed at its exact head; (2) provenance of the dedicated synthetic source authenticated without inferring from `SYN-` ids or labels; (3) finite admission naming owner, cohort at most 100, duration, call and token ceilings and cost headroom; (4) certificates, route and grants verified by an authorised operator; (5) one retained observation of identical reading ids and values in the UI and snapshot, plus a privacy-compatible traceable link (not raw values in logs) to the provider request per PRD AC-067, and a visible unapproved flag with model, version and time.

## Decisions and readiness

* Parent decisions: accepted C1 to C17 as evidence; rejected counter-hypotheses A to E as stated; deferred any live, SQL, browser, model or full-gate observation.
* Research disposition: `executed`. One complete cycle (three waves) with no new substantial finding expected from a second cycle; the next likely sources (live systems) are outside authority.
* Planning Readiness: `Ready` for a documentation-only implementation. Required gates before Implement: critique once; no test required for the doc change beyond link and diff review; produce changes and review records.

## Not done

* No `.copilot-tracking` edit of historical records, no private data, no credential read, no Azure, model, SQL, browser or full-gate run, no push or issue write.

## Qualification C1 (2026-11-09, added after independent readiness review)

Claims C9 to C11 and C17 above and the closing hop conclusions were written as categorical absence ("no employee route", "none exists", "no such path exists"). The evidence is bounded to the inspected paths: a textual search of `src/api` and a reading of the registered `quality-evidence` snapshot (`assistants.py:97-180`, caller `:504-509`), which also holds permitted document metadata. Read them as "not identified in the inspected paths; a differently named path remains unverified". The original text and outcome are not regraded. See `2026-11-09-demo-stabilization-checkpoint-440-c1-qualification-research.md`.
