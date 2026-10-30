---
title: Resident AI activation timeout recovery independent RPI Review
description: One bounded post-implementation review for task563-timeout-recovery-20261030 and issue 563
ms.date: 2026-10-30
---

## Opening Review State

* Interpreted review goal: independently compare the complete new timeout-recovery artifact set, the current README diff and narrowly necessary implementation evidence against the approved operational boundary, without equating safe execution with activation acceptance.
* Review scope: task563-timeout-recovery-20261030, issue 563, ops/resident-ai-activation-563, PR 576.
* Evidence readiness: the six dated research, plan, details, critique, changes and session-state artifacts are present; their complete contents remain to be compared.
* Acceptance basis: approved resident-only activation and mandatory rollback, four additional sign-in submissions, personally monitored cost, USD20 ceiling and November 1 inference expiry, redeployment through November 15, exact backup/restoration, min0 and Manual jobs; no employees, endpoints, broad RBAC/groups or deletion of ama.
* First comparison boundary: reconcile plan markers, critique, changes and session state before tracing the supplied safe projections and named source/tests.
* Active read-only boundaries: only this review record may be written. No execution/import of supplied scripts, source/artifact fixes, network, browser, SQL, credentials, commits or gates. External reads are limited to the five expressly allowed safe projections under the supplied resident-recovery directory.
* Initial blockers: no review-blocking ambiguity identified; gate execution and actual activation acceptance are not presumed.

## Scope and Evidence

* Task: task563-timeout-recovery-20261030; artifact metadata uses 563-timeout-recovery-20261030. Issue 563, branch ops/resident-ai-activation-563, PR 576.
* Date: 2026-10-30. This is the single independent post-implementation Review, not a second critique, correction pass or exact-head publication assessment.
* Read the complete new research, plan, phase details, plan critique, changes and session-state JSON for resident-ai-activation-563-timeout-recovery dated 2026-10-30.
* Read the current src/api/README.md diff and its immediately surrounding advisor/operations contract; narrowly read SessionCodec, resident startup, browser session/login/view handling and the two named restart regressions.
* Read all five explicitly authorized external safe projections: recover.py, retry_after_wait_race.py, recovery-results.json, attempt2/recovery-results.json and anonymous-browser.json. Their SHA256 values match the changes record and the helper identities recorded in the receipts. No supplied script was executed or imported.
* Prior task artifacts and issue/PR contents were not reopened. Their history and criteria are assessed only as supplied in this task and the complete new artifact set. Repository opening context was read; no new regulatory or accessibility judgement is made.
* No nested agent, cloud/network/browser/SQL/credential operation, test execution, gate, commit, configuration mutation or source/artifact correction occurred. Read-only local Git inspection and hashing of the five permitted files were performed.
* Only this canonical review record was written. Existing dirty README and six new task artifacts were left untouched.

## Execution Status

* Review execution status: Complete. The declared operational, evidence, acceptance and closeout boundary has been compared once.
* Assessed task execution status: Partial overall. P01-T01 and P01-T02 completed the authorized activation-or-rollback branch; P02-T01 local persistence and the full local gate remain scheduled, not performed.
* P01 completion is execution through mandatory rollback, not successful activation. The Review can complete while the task outcome remains Not accepted.
* No missing evidence prevents that bounded verdict. Raw backups and live state are outside this review's authority and are not independently certified.

## Plan-to-Change Reconciliation

| Current plan scope | Changes/session-state evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| Research C1-C9; FR3 | Process nonce investigation, anonymous health and earlier helper diagnosis | Reconciled | Directly read current nonce/startup/UI behavior supports fresh post-rollout login; the previous private helper itself was not reopened. |
| P01-T01; FR1-FR2; AC1 | Both exact-backup capture sequences precede their enable-update; enabled_config checks true; ready/traffic and health evidence | Reconciled within safe evidence | Two documented variables only; no source image deployment. Backup byte hashes are recorded, not independently recomputed from forbidden raw files. |
| P01-T02; FR3-FR5; AC2-AC5 | First waiter failure, preserved wrapper, second authenticated view, explicit fallback, immediate verified rollback | Reconciled | Checked task markers describe executed failure branch, not an accepted AI answer. |
| NFR1-NFR3 | Safe helper, wrapper, sanitized receipts and all 63 automation command results | Reconciled | Credential handling stays inside automation; no recordings or request body/header export in these projections. Existing runtime reuse is reported after missing dependency evidence. |
| P02-T01; AC6 | Pre-Review Reconciliation and review-ready boundary; session active_phase Review | Partially executed, truthfully pending | One passing critique is present. This Review supplies the original review record; local commit/full gate have no current result or receipt. See RV-002. |
| Plan Follow-Up Items | Private telemetry diagnosis, human acceptance and exact-head publication prerequisite mirrored in changes/state | Reconciled | Remain distinct later work; no unapproved active inference retry or expanded permissions. |

The changes opening's active/pending statements and its early "Pending" section are chronological starting states, superseded explicitly by the first/second run and Pre-Review Reconciliation sections. They do not substantiate current completion. The plan handoff's Review transition and state review:null represent the pre-Review handoff, not a claim that this record or P02 already existed.

## Completed Work Assessment

| Related marker | Evidence/files | Change and reason | Completion/validation evidence | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 | Safe recover.py; both recovery-results.json projections | Back up before applying only ENABLED and ENDPOINT; ready/warm before credentials | 32 first-run and 31 second-run Azure commands, each with argv/time/exit/output hashes; enabled_config all true | Supported as recorded operational execution; all 63 CLI exits zero do not imply overall success. |
| P01-T02, first run | recover.py; first receipt | Fresh login replaces stale cross-restart authentication; initial waiter incorrectly accepts still-visible sign-in as a settled state | Login 200; own-case GET dispatched; unexpected_ui_state before any enabled assistant request; rollback_verified true | Failed intermediate implementation validation preserved honestly; no model cause inferred. |
| P01-T02, second run | retry_after_wait_race.py; second receipt | Preserve original helper/run; authenticated waiter first awaits asynchronous content or explicit error | Login 200, view 200, content true/signin false; second total submission | Addresses the observed waiter race without altering session security or increasing the authorized submission ceiling. |
| P01-T02, consent/AI | Second receipt checks and HTTP sequence | Client/server consent negative checks then one synthetic pest request | Client no-request; server 400 consent error; pest POST 200 in 3.915s with explicit rules fallback | Consent evidence supported; actual AI acceptance fails. See RV-001. |
| P01-T02, rollback | Helper rollback/invariants; both receipts; changes direct-comparison report | Remove precisely the two previously absent variables after any failed verification | Both rollback flags true; final recover-safe-180814; health 200; anonymous 403; all effective invariants true | Supports safe disabled restoration within the supplied evidence boundary, not a new live-state attestation. |
| P02 documentation | src/api/README.md | Add ten-line operations caveat covering process-bound tokens, fresh login, async view and bounded waits | Current diff agrees with directly read implementation; no behavior/test-source change | Narrowly relevant and consistent; does not weaken nonce, consent or cost controls. |

## Operational Safeguards and Backup Assessment

* The helper captures resident app, revisions, authentication, jobs and the two named employee app baselines before each mutation. Raw stdout/stderr are kept outside Git; receipts preserve their hashes and ordered commands. The first run's rollback-app hash equals the second run's before-app hash, supporting continuity between attempts.
* Static reading confirms enabled invariants remove only the expected two additions before comparing effective environment, compare the remainder of the template, configuration, workload profile, identity and authentication, compare jobs, and compare employee template/configuration/identity. Scale must remain min0/max1 and every returned job Manual.
* Normalization is limited to the resident revision suffix and an inert empty value accompanying an unchanged secretRef. Rollback restores effective configuration, not historical revision lists, runtime timestamps or byte-identical entire Azure resource documents.
* Both supplied receipts record all enabled/restored checks true, backup_complete true, browser_closed true and activation_verified false. Readiness code requires latest==ready, Succeeded and exactly one 100%-traffic revision before proceeding. Final restoration is ca-resident-demo--recover-safe-180814 with health 200 and anonymous assistant denial.
* Direct first-original-to-final effective comparison is reported passed in changes; its raw inputs and standalone comparison output were not supplied for this Review. It is reported corroboration, not an independently repeated comparison. No hidden stronger backup, permission, hash or live-state proof is inferred.
* Hashes establish consistency of the supplied safe files with the changes record; they do not prove the contents of unopened backup files, their filesystem modes or current cloud state. Private root0700/file0600 and absence of other private exports are implementation reports plus the helper's restrictive umask/configuration, not an independent filesystem audit.
* Observed command argv mutate only the resident enablement variables and revision suffix. There is no supplied mutation for employees, roles/groups, endpoints/networking, secrets, jobs or deletion of ama. Configuration/identity checks support preservation of the known estate; this is not a subscription-wide change audit.
* The persistent total is copied only after the wrapper requires the first verified rollback and one prior submission. The receipts show one new submission in each attempt, cumulative 2/4, both login responses 200; no authentication-denial retry. The first rollback restarted the process, so the second fresh login follows observed session invalidation, not a blind retry.
* Exactly one consented pest request occurred after enabled rollout, with no inference retry. The negative consent and anonymous requests are not evidence of paid inference. Actual transport/completion/spend remains unknown, not zero.
* USD20 and exclusive 2026-11-01T00:00:00Z inference expiry remain the declared contract. No setting or source change extends them; authorization to redeploy through November 15 does not extend inference authority. Personally monitored cost does not prove accounting availability or remaining balance. No ledger/SQL diagnosis or access was sought in this Review.

## Acceptance Assessment

| Criterion | Result at reviewed boundary | Basis |
| --- | --- | --- |
| AC1, exact backup/permitted delta | Supported within safe projection limits | Ordered capture/hashes, backup flags and static invariant mechanism; raw backup bytes intentionally not opened. |
| AC2, actual grounded AI pest answer | Unmet | HTTP 200 rendered "Summary by rules - AI unavailable or usage limit reached"; no AI answer observed. |
| AC3, thin AI label/sources/out-of-scope | Not proven overall | One known repair-guidance source was collapsed on the fallback reply; AI geometry, semantic grounding and out-of-scope request did not execute after the failed AI assertion. |
| AC4, anonymous/client/server consent protection | Supported for observed checks | Anonymous 403 before activation and after restoration; enabled client no-consent no-request and server no-consent 400. No additional anonymous check during the enabled interval is claimed. |
| AC5, submission ceiling/preservation/rollback | Supported within safe projection limits | 2/4 cumulative submissions, preserved invariants, both mandatory rollbacks verified; final baseline disabled. |
| AC6, critique/Review/persistence/full gate | Partial | Exactly one Complete/Pass critique with zero findings; this is the one Complete Review. Local commit and full gate remain pending, no passing receipt. |

Neither issue 563 closure, successful enabled service, semantic/human acceptance, accessibility conformance nor publication readiness follows from these results.

## Implementation-Time Plan and Detail Update Assessment

| Affected marker | Update and trigger | User intent and reconciliation | Planning/critique assessment |
| --- | --- | --- | --- |
| P01-T02 / FR3 | First login 200 exposed the still-visible pre-login form before async view completion | Wrapper preserves first failure/rollback, copies the cumulative counter and changes only the authenticated wait predicate; current plan/details/changes/state explain it | Immediately relevant implementation refinement, not a significant/divergent scope or security decision. Existing Complete/Pass critique remains the sole critique; no new owner decision required. |
| P01-T02 / FR5 | Actual pest fallback rather than required AI | Plan/details/state retain Unmet/Not proven acceptance while marking mandatory rollback execution complete | Applies the pre-critiqued failure branch, not a relaxed acceptance criterion. No permission to spend remaining submissions or retry inference. |
| P02-T01 / follow-ups | Inactive pod embedded 404 and workspace perimeter denial prevent diagnosis | Changes and state retain alternatives and route private telemetry work separately; no networking/RBAC workaround | No new operational design or invalidated nonce assumption; material runtime evidence gap is RV-001, not a reason to silently expand scope. |
| P02-T01 | Local commit/full gate remain scheduled after this original Review | Plan checkbox remains open and final changes/state distinguish Review from persistence/publication | Expected parent continuation, not a fabricated check result. RV-002 records the outstanding publication prerequisite. |

## Critique and Material Revision Assessment

* Exactly one supplied final-candidate critique records execution Complete, verdict Pass and zero findings. No PC-xxx disposition is missing.
* Its coverage includes FR1-FR5, NFR1-NFR3, AC1-AC6, task dependencies and failure restoration. It explicitly does not certify live execution, remaining budget or rollback success.
* The only implementation refinement is the asynchronous authenticated waiter; it preserves the approved intent and security contract and is reconciled in the current artifacts. No significant/divergent decision requiring renewed planning was identified.
* Research's earlier bounded timeout explanation remains supported by current source, not a diagnosis of the later fallback. Details' "No research gap" is read as pre-implementation readiness; it does not override the new runtime evidence gap recorded in its completion/follow-up text.
* No evidence shows affected work resumed past an unresolved material planning decision. This Review does not rerun or overwrite the original critique.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner/next action | Assessment and route |
| --- | --- | --- | --- |
| Actual runtime fallback diagnosis | Disabled after failed verification; allowed evidence cannot distinguish runtime causes and public telemetry access is denied | Separately authorized private-perimeter operator/research owner | Open, RV-001 to rpi-research. No ledger read, public networking or broader role workaround. |
| Human resident/content and operational acceptance | Requires real AI availability and direct human judgement; automation cannot provide it | Owner selects later human acceptance work after technical evidence exists | Open distinct follow-up HUMAN-563; no defect or new active P01 task, no approval inferred. |
| Fresh exact-head/current-main publication gate and independent exact-head approval | Local persistence/gate closeout is unfinished; publication is coordinator-owned | Active parent finishes P02-T01; coordinator retains publication prerequisite if blocked | Open, RV-002; preserve original Review and actual blocked/pending status. |

## Findings

This is the complete substantive finding set for the supplied task boundary: Critical 0, High 1, Medium 1, Low 0. Findings are not automatically source defects.

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Activation acceptance is unmet and the runtime fallback cause remains unknown

* Related scope: P01-T02, AC2-AC3, plan runtime-diagnosis follow-up; session blockers B1/B2.
* Evidence: .copilot-tracking/changes/2026-10-30/resident-ai-activation-563-timeout-recovery-changes.md, Second Run and read-only diagnosis sections; permitted attempt2/recovery-results.json checks.enabled_pest and failure.actual_ai_not_observed_no_retry. Login/view succeeded, then the consented pest POST returned 200 in 3.915s with the explicit AI-unavailable/usage-limit rules label.
* Impact: The original timeout is no longer the observed blocker, but no actual generated pest answer, semantic grounding, thin AI label or out-of-scope acceptance was established. Mandatory rollback correctly prevents leaving an unverified activation enabled. Whole-issue or activation success cannot be claimed.
* Cause boundary: Inactive pod console retrieval reportedly returned embedded 404 despite CLI exit0. The narrowly filtered existing-workspace query reportedly failed with NspValidationFailedError. These do not identify accounting admission, managed identity, transport or response-validation failure. No SQL/ledger cause or zero-cost inference is inferred.
* Destination: rpi-research for the existing distinct runtime-diagnosis follow-up, not rpi-implement on an unproven source defect and not a new current-task retry.
* Smallest useful next action: Under separate authorized existing private-perimeter access, establish the fallback stage using minimal sanitized operational telemetry. Retain the disabled baseline, cost/expiry limits and no-ledger/public-access/broad-RBAC boundary. Any later activation requires its own applicable authority and evidence; the two unused submissions are not an instruction to spend them.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Local persistence and the full publication gate have no current completion evidence

* Related scope: P02-T01, AC6, coordinator publication follow-up.
* Evidence: .copilot-tracking/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan.md open P02/P02-T01; changes Pre-Review Reconciliation/review-ready boundary; session-state next_action. Candidate inputs were dirty/untracked at review intake. A foreign heavy-lock holder was previously reported; no current-candidate full gate attempt/result or passing receipt is supplied.
* Impact: Review execution can finish, but overall task execution is Partial and publication remains blocked. Focused tests, anonymous/live browser results and earlier lock evidence cannot substitute for a clean committed exact-head/current-base full gate.
* Destination: Active parent P02-T01 scheduled closeout, with distinct coordinator publication follow-up PUBLICATION-563 if unavailable. This is residual incomplete work, not an application defect or a decision gap.
* Smallest useful next action: Parent preserves this original Review, performs the authorized local persistence with authenticated privacy-safe identity, required trailer and Refs #563 only, then attempts the bounded literal flock-w600 admission and native nonblocking gate without holding both locks. Record actual timeout/race/failure/no-receipt or genuine completion; no passing-gate claim now. Coordinator owns publication and independent exact-head approval; no push is authorized here.

## Defects

* No demonstrated source/security defect remains in the reviewed README-only implementation delta.
* The initial waiter defect was corrected in the preserved wrapper during implementation, with the original failure retained. It is not routed again.
* RV-001 is an observed acceptance failure plus a material evidence gap, not an attributed accounting/model/application bug. RV-002 is unfinished closeout, not a reason to add or bypass tooling.
* No rpi-plan destination is required: no unaccepted significant/divergent decision was established.

## Validation Evidence

| Check/command or evidence | Status | Coverage and limitation |
| --- | --- | --- |
| Read-only Git status/branch/current README diff | Passed in this Review | Expected continuing branch; README and six new task artifacts already present; no commit/PR lifecycle query performed. |
| sha256sum on the five expressly permitted projections | Passed in this Review | All match changes. Helpers match both receipts; no raw backup/config/log/counter/credential or other session opened. |
| Source/test inspection | Passed as static comparison | Process nonce, fresh startup codec, asynchronous loadView and both restart regression definitions agree with the documented fix. No tests run by reviewer. |
| First recover.py execution | Failed, as supplied | Exit2 after login200 waiter race; no enabled model request; mandatory rollback verified. |
| Wrapper execution | Failed activation, as supplied | Exit2 after actual HTTP200 rules fallback; corrected login/view wait succeeds; rollback verified. Failure not hidden by zero Azure CLI exits. |
| Existing core/API restart tests | Passed, reported | Corrected selectors ran 2 tests in1.121s. Earlier nonexistent API HttpTests selector failed and remains recorded. Raw test runner output not separately supplied/read. |
| Local DOM waiter fixture | Passed after correction, reported | Delayed content0.311s and explicit sign-in error; initial empty-text fixture failed. Not a live browser check by this reviewer or actual AI evidence. |
| Anonymous/browser and enabled consent checks | Passed within supplied observations | Anonymous-browser zero sign-ins; enabled client no-request/server400; cumulative2/4 logins. Scope does not establish semantic or human acceptance. |
| Actual AI pest answer | Failed | Explicit unavailable/usage-limit rules fallback; transport/completion/spend unknown. |
| AI label geometry/grounding/out-of-scope | Skipped after failed AI assertion | No later inference retry; collapsed fallback source observed only. |
| Exact effective restoration | Passed as supplied, bounded | Both safe receipts/invariant mechanism agree; direct original-to-final comparison reported. Raw backups/current cloud not independently verified. |
| Inactive console and existing-workspace diagnosis | Unavailable/failed, reported | Embedded404 and perimeter denial; no hidden stronger diagnostic proof. |
| git diff --check | Passed, reported before Review | No full lint/build/test suite inferred. |
| Current candidate complete local gate/receipt | Not performed/pending | Scheduled after original Review and local commit. Prior foreign lock observation is not a current full gate result. |
| Human resident/content/operational acceptance; hosted checks | Not performed | Separate owner/coordinator gates; no conformance or issue closure claim. |

## Blockers and Remaining Work

* Actual activation is blocked by RV-001; known-good disabled effective baseline is the supported final operational outcome.
* P01 execution is complete by its preplanned rollback branch. It must not be relabelled accepted activation.
* P02-T01 remains open for parent local persistence and actual full gate attempt/result. Publication cannot proceed on this Review or focused tests alone.
* Existing telemetry access limitations are not permission to change network/RBAC/SQL or inspect the ledger. Human acceptance remains distinct.
* This Review has no unresolved review-execution blocker and does not authorize another critique or Review.

## Outcome

* Review execution: Complete.
* Assessed task execution: Partial overall; P01 Complete through mandatory rollback; P02 local closeout pending.
* Outcome: Not accepted for activation/whole-task acceptance.
* Rationale: Safe recovery sequencing and rollback are supported within the supplied evidence boundary, and safeguards are preserved. Nevertheless AC2-AC3 remain unmet/not proven and AC6 persistence/gate is incomplete. Successful HTTP status, safe restoration and passing focused regressions cannot replace actual AI or publication evidence.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defect | None established | Do not invent a source fix from an unexplained fallback. |
| Decision gap or invalid assumption | None requiring rpi-plan | Preserve the approved failure branch and unchanged authority. |
| Material evidence gap | RV-001, rpi-research | Separately authorized private-perimeter fallback diagnosis; no retry or expanded access here. |
| Residual active closeout/publication | RV-002, parent P02-T01 / PUBLICATION-563 | Original Review local persistence, real bounded gate result, then coordinator exact-head publication prerequisites. |
| Distinct non-blocking human follow-up | HUMAN-563 | Owner selects direct resident/content/operational acceptance only after actual AI evidence. |

Later work does not require this Review to run again. All original critique, adverse validation, rollback evidence and this verdict remain historical evidence rather than being rewritten into later success.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/resident-ai-activation-563-timeout-recovery-research.md](.copilot-tracking/research/2026-10-30/resident-ai-activation-563-timeout-recovery-research.md) | Complete new research C1-C9 and authority boundary |
| [.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan.md](.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan.md) | Requirements, acceptance, execution markers and follow-ups |
| [.copilot-tracking/details/2026-10-30/resident-ai-activation-563-timeout-recovery-phase-details.md](.copilot-tracking/details/2026-10-30/resident-ai-activation-563-timeout-recovery-phase-details.md) | Phase completion and remaining closeout |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan-critique.md) | Sole independent critique, Complete/Pass, zero findings |
| [.copilot-tracking/changes/2026-10-30/resident-ai-activation-563-timeout-recovery-changes.md](.copilot-tracking/changes/2026-10-30/resident-ai-activation-563-timeout-recovery-changes.md) | Complete commands, hashes, outcomes and retained failures |
| [.copilot-tracking/rpi-sessions/2026-10-30/resident-ai-activation-563-timeout-recovery-state.json](.copilot-tracking/rpi-sessions/2026-10-30/resident-ai-activation-563-timeout-recovery-state.json) | Pre-Review continuation, blockers and priorities |
| [src/api/README.md](src/api/README.md) | Current operations diff and unchanged advisor authority contract |
| [src/core/src/zava_forward/core/resident_showcase.py](src/core/src/zava_forward/core/resident_showcase.py) | Process-bound SessionCodec |
| [src/api/src/zava_forward/api/resident_demo/__main__.py](src/api/src/zava_forward/api/resident_demo/__main__.py) | Fresh startup codec |
| [src/api/src/zava_forward/api/resident_demo/web/demo.js](src/api/src/zava_forward/api/resident_demo/web/demo.js) | Narrow session/sign-in/asynchronous view trace |
| [src/core/tests/test_resident_showcase.py](src/core/tests/test_resident_showcase.py) | Named codec restart/key-change regression |
| [src/api/tests/test_resident_demo_api.py](src/api/tests/test_resident_demo_api.py) | Named API restart/session-denial regression |
| [.copilot-tracking/reviews/logs/2026-10-30/resident-ai-activation-563-timeout-recovery-review.md](.copilot-tracking/reviews/logs/2026-10-30/resident-ai-activation-563-timeout-recovery-review.md) | This single independent Review and complete RV finding set |

## Next Steps

Return this record to the active parent. Parent owns the already scheduled local commit and bounded literal flock-w600/native nonblocking full-gate attempt without double-locking, preserving pending/blocked status if no receipt exists. Coordinator alone owns later publication prerequisites. RV-001 belongs to separately authorized rpi-research; HUMAN-563 remains owner-selected later acceptance. Stop here: no new operational action, second Review, push or approval is authorized.
