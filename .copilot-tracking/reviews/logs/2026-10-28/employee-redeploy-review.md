---
title: Employee redeploy independent RPI Review
description: One full-boundary review of the blocked employee redeployment attempt
ms.date: 2026-10-28
---

## Scope and Evidence

* Task ID: employee-redeploy-20261028.
* Review date: 2026-10-28.
* Review scope: Full caller request versus actual blocked execution, not a successful deployment.
* Write boundary: This review record only; existing untracked task artifacts remain untouched.
* Branch: ops/employee-redeploy-20261028; HEAD bb6df04cef68cc3694a97238d002c732c3406d81, tracking origin/main.

## Opening Review State

* Interpreted review goal: Independently assess the requested single employee app redeploy, preservation, validation, recovery and Refs-only publication against actual execution.
* Review scope: Full employee-redeploy-20261028 task, including unmet work and original critique dispositions.
* Evidence readiness: Caller identifies research, plan, phase details, original critique, changes and session state. These are the comparison inputs, pending direct reading. External backup contents are not independently inspected because this review environment prohibits file operations under the supplied temporary-directory path.
* Acceptance basis: Caller requirements, current plan markers and details, original critique, actual changes and validation evidence; safe refusal is not deployment acceptance.
* First comparison boundary: Reconcile planned markers and acceptance criteria with recorded read-only work, execution blockers and remaining work before assigning findings.
* Active read-only boundaries: No other edits, commits, publication, Azure writes, build/gate execution, agents, secrets, environment files, private datasets or lock polling/interruption/re-admission. Exactly one Review; no correction/review loop.
* Initial blockers: Reported foreign heavy-lock holder, unavailable all-in financial headroom, unsupported Single-mode recovery, and missing exact-head publication gate.

## Evidence Inventory and Limits

* Compared the complete canonical research, plan, phase details, original critique, changes and session-state files listed below, including all P01-P03 tasks, PC-001..005 and both plan follow-up items.
* Directly checked src/README.md, Local RPI gate and Stabilization validation ladder, and infra/README.md, Small employee model prerequisite. These support the full deployment/publication gate, nonqueued lock admission, separate financial prerequisite and three requested AI values. The broader runbook's two model-version variables are not permission to exceed the caller's additive-three boundary.
* Read the required project specification, knowledge-base index, owner memory and sector primer for context. Memory is not acceptance evidence. No fresh legal or regulatory judgement is made.
* Local Git inspection confirms the requested topic branch and HEAD. Its upstream is origin/main. The six pre-existing task artifacts are untracked; no local evidence commit, verified candidate or publication is established. No remote refresh was performed in this Review.
* The supplied backup comprises app-before.json, app-after.json, acr-before.json, acr-after.json, revisions-before.json and verification.json. Changes records baseline hashes and exit-0 semantic equality; these are recorded execution evidence, not independently recomputed results in this Review.
* Specifically, the recorded baseline SHA256 values are app-before.json 3193c65c51640a465e792ea4bc546f7d7f105dff1acaa1292c7934e330c6d8f6; revisions-before.json 3bd9f22fadbf627dca44bbe6dbeba1c9b716680f434a81f1298441c186de61ec; acr-before.json 9e76914c9b68fdbb2ab90bc3f87f171e961568301b53c582b450694090d720d3.
* Backup files were not opened, hashed or compared by this reviewer because their supplied location is prohibited by this environment's file-operation boundary. No full configuration, environment values or secret-reference objects were printed. No live Azure verification was performed.
* This evidence is sufficient for a credible full-request blocked-outcome verdict, not independent present-tense infrastructure attestation. The caller's account and all six canonical artifacts consistently report zero build/push/cloud writes.

## Execution Status

* Review execution status: Complete. Exactly one independent evidence comparison and original finding set are recorded here.
* Planned operational execution status: Blocked. P01-T01 is Partial because reference-only backup completed; its build did not. No completed runtime phase or successful deployment is inferred.
* Assessment date and source boundary: 2026-10-28, HEAD bb6df04cef68cc3694a97238d002c732c3406d81, supplied historical operation records and local Git inspection only.
* Review completion does not complete the deployment, evidence commit, gate, publication or human acceptance.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| P01 / P01-T01 | Safe preservation; admission and cost failures | Partial, accurately unchecked | Backup reported complete; source image build blocked by observed foreign lock owner. |
| P01-T02 | No ACR update/rule/login/token/push | Reconciled as Blocked | No built image, financial readiness or admitted push. Registry never opened, so restoration was unnecessary, not successfully exercised. |
| P02 / P02-T01 | No rollout; AI variables still absent | Reconciled as Blocked | No digest-pinned additive update, new revision, positive startup, health/log or asset evidence. |
| P02-T02 | Previous revision unchanged; no recovery necessary | Reconciled as unexecuted | Zero mutation requires no rollback, but does not demonstrate a compliant recovery procedure. |
| P03 / P03-T01 | Evidence reconciled; independent Review pending | This record supplies the one Review | Existing markers/state intentionally remain unchanged under the write restriction; their pending Review wording is the pre-review snapshot, not evidence that this Review did not finish. |
| P03-T02 | Local commit possible; publication blocked | Pending, not complete | No evidence commit or exact-head gate/receipt/assessment, push or Refs-only PR. |
| Follow-Up Items | Authenticated/live/inference acceptance unchecked; later admission required | Reconciled with qualification | Authenticated/task acceptance is separate work. Cost/recovery/admission are active prerequisites, not optional post-success residuals. |

## Completed Work Assessment

| Related marker | Evidence/files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| P01-T01 | Changes, details; externally held backup | Saved reference-only baseline to make preservation auditable | Recorded protected file permissions, baseline hashes and exit-0 semantic comparison | Reported passed; external bytes not independently inspected | Safe preparatory work only, not task completion. |
| P01-T01/P01-T02 | Changes, plan, state | Recorded nonqueued lock and failed financial evidence; stopped dependent work | PID3869238 python3; ActualCost429 then stable API Unauthorized/RBACAccessDenied | Failed/unavailable prerequisites, no waiting or session/role changes reported | Correct fail-closed execution; original goal unmet. |
| P02 | Changes and details | Recorded no-write terminal state | Old revision/digest, absent AI entries and identical app/ACR reported | Reported unchanged-state comparison, not new runtime validation | Preservation evidence is consistent; no rollout or rollback claimed. |
| P03-T01 | Canonical task artifacts and this record | Preserved original critique and one full-boundary independent Review | Complete artifact reconciliation | Lightweight document/Git inspection only | Review complete; source records left intact. |

### Terminal State Assessed

* Employee app remains ca-cutover-test-demo-api in ama; old revision ca-cutover-test-demo-api--0000006 and digest sha256:0769b52dddc5d6b350c74d6711ae53eda45d3e903ee27fac6b5a6c1d6b8b6e7e remain recorded.
* Existing 27 environment entries, one Key Vault reference, min0/max4, identity, registry and Single revision mode are reported unchanged. AI_ENDPOINT, AI_DEPLOYMENT and AI_DEPLOYMENT_STRONG remain absent.
* ACR remains public Disabled, default Allow, exports disabled, bypass None, empty IP/VNet rules and admin false. No temporary VM /32/export/public exception was opened. Exact unchanged baseline is not an exercised restore.
* No other workload, job, resource, role, identity, traffic or authentication change is reported; no paid inference, secret-value retrieval or private-data access is reported.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| Executive summary; P01/P03 | Build/gate admission now explicitly blocked | Actual foreign lock ownership, not mere lock-file existence; no expanded authority | Plan/details/changes/state all record no queue/poll/interruption and later explicit coordination | Original critique retained; no new execution permission | Compatible factual update; no user-intent divergence. |
| P01-T02/P02-T01 | Added financial stop before cloud writes | Cost API429 and one authorized alternative denied; no cost amount established | Required all-in liabilities/reserve/exposure remain unknown across artifacts | PC-003 conservatively applied; financial readiness unresolved | Correct stop, not resolved spending readiness. |
| P02-T02 | Removed automatic multiple-mode fallback; made compliant recovery a prerequisite | Official docs did not establish exact Single-mode/no-new-revision recovery | Plan/details/research addendum/changes/state consistently block mutation | PC-001 fail-closed alternative applied; original Revise preserved | Unapproved divergence avoided; feasible recovery still unresolved. |
| P02-T01 | Require timestamped positive new-revision startup/readiness, not empty logs plus401 | PC-002 and min-zero authentication boundary | Details distinguish platform/app/auth and unobserved timeout | Compatible correction, unexecuted | Stronger contract does not establish a passed check. |
| P01-T01 | Defined constructed cases/staff fixture, UID-compatible mounts, loopback HTTP/script-order and image binding | PC-004 | Details specify concrete statuses/order/identity/cleanup evidence | Compatible correction, build blocked | Planned executable proof only; not demonstrated. |
| P01-T02 | Ten-minute exception; bounded individual operations and private-first cleanup | PC-005 | Details record 60-second operations, 420-second push, 120-second restoration readback | Compatible correction; no exception opened | No observed exposure or cleanup failure. |

The conservative updates preserve exactly one employee revision, additive-three settings, min zero and unrelated state. No significant exception was accepted. Planning completion means a reconciled blocked plan, not an execution-ready candidate. Fresh compliant recovery evidence or a materially divergent proposal belongs in planning before affected work; this Review grants neither permission nor another rollout.

## Critique and Material Revision Assessment

| Original finding | Recorded disposition | Independent assessment |
|---|---|---|
| PC-001 High | Fail closed; unsupported mode fallback removed | Compatible blocked alternative satisfies the critique's planning correction, not recovery feasibility. RV-001 remains active. |
| PC-002 High | Positive timestamped startup/readiness required | Contract reconciled in details; actual new-revision validation not run. Covered by RV-003, not a second duplicate finding. |
| PC-003 High | Cost gate added; both query failures retained | Financial prerequisite enforced but evidence unavailable. RV-002 remains active. |
| PC-004 Medium | Constructed HTTP fixture/order/image-binding recipe added | Design correction recorded; no actual built-image HTTP evidence. RV-003 covers the unmet execution. |
| PC-005 Medium | Concrete exception/command/restore bounds added | Correctly planned, unexercised because ACR never opened. RV-003 covers remaining operation. |

* Original critique remains Complete / Revise, with all five original findings preserved. This Review neither upgrades its verdict nor performs a second critique.
* Dependent-work pause was honored in the supplied evidence: no build, push, registry opening or app mutation followed the blocking discoveries.
* Research's historical Complete / Ready and answered Q3 are qualified by its final subsequent-planning paragraph. They cannot establish current rollout readiness.
* Changes' statement that Review assesses read-only/blocked evidence is interpreted as the available execution evidence, not a narrowed acceptance boundary. All requested deployment and publication obligations are assessed here.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Authenticated employee acceptance and task-release/model binding | No authorized staff session, inference, model acceptance or task-release exercise in this bounded redeploy | Owner arranges separately authorized authenticated/task-specific acceptance | Open distinct follow-up FU-EMP-ACCEPT; RV-005. Not a redeploy defect or new active task. |
| Coordinator establishes cost/recovery and explicitly re-admits after lock release | No background waiting, polling, financial access expansion or improvised recovery allowed | Coordinator supplies evidence and later explicit admission event | Not optional residual work: these block existing P01/P02 and gate admission. Route once through RV-001/RV-002/RV-003/RV-004; do not expand scope. |

State's empty prioritized_follow_ups array does not erase the plan's explicit follow-ups. This record supplies their dispositions without editing session state or treating empty metadata as closure.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Compliant recovery remains unestablished before the permitted one-revision update

* Related scope: P02-T02; original PC-001; preservation and rollback requirements.
* Evidence: Plan Critique Disposition and details P02-T02 explicitly cannot establish restoring the old revision/digest and effective traffic in Single mode without another revision; changes records no mutation.
* Impact: The requested verify-or-rollback contract is not executable on current evidence. Simply leaving mode/traffic different would exceed authority.
* Destination: rpi-plan.
* Smallest useful next action: Planning parent establish a supported bounded recovery sequence with baseline-mode/traffic and revision-set assertions, or retain the existing mutation block. Any necessary material exception requires explicit owner direction before execution. Do not retry critique or review.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Required all-in financial readiness cannot be established from denied cost queries

* Related scope: P01-T02/P02-T01; original PC-003.
* Evidence: Changes records API2025-03-01 ActualCost429 exit1 followed by API2023-11-01 explicit-period Unauthorized/RBACAccessDenied exit1; plan/details/state retain unknown headroom. src/README.md requires complete all-in evidence.
* Impact: Neither fresh operation authority, min zero nor zero inference establishes funds for registry/revision/hosting exposure. Cloud writes remain financially blocked.
* Destination: rpi-research.
* Smallest useful next action: Owner/coordinator provide existing authorized sanitized dated evidence covering accrued costs, outside-group and remaining liabilities, reserve, currency/lag/exclusions and bounded redeploy exposure. Do not repeat denied calls, grant roles, change login or infer zero costs.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Requested image publication and employee redeploy were not executed

* Related scope: P01-T01/P01-T02/P02-T01/P02-T02; PC-002/004/005 execution evidence.
* Evidence: Changes and details report foreign PID3869238 python3 holding the shared heavy lock; no build/push/cloud writes. Old revision/digest and all 27 original environment entries remain; the three requested AI variables are absent.
* Impact: No new image manifest or healthy digest-pinned employee revision exists for this task. Safe preservation and a fail-closed stop do not satisfy the core caller request.
* Destination: rpi-implement, conditional on RV-001/RV-002 and a later explicit coordination event after lock ownership is free.
* Smallest useful next action: Keep execution blocked now. On separately authorized admission, finish existing tasks once: source-context build under nonblocking lock, exact-image synthetic HTTP proof, existing-ACR digest push with bounded one-IP exception/exact restoration, one additive-three/min-zero update and bounded positive revision verification or pre-established recovery. No lock polling, foreign-process interruption, blind mutation retry or additional revision.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Evidence commit and required exact-head publication gate remain pending

* Related scope: P03-T02.
* Evidence: Git inspection shows six pre-existing untracked task artifacts at merged-main HEAD. Changes/details state no admitted full gate, no passing receipt, no push/PR. The deployment-class full gate is independently required by src/README.md and is also lock-blocked.
* Impact: The requested Refs-only PR has not been delivered; an evidence-only candidate cannot inherit #515's historical exception or substitute this Review for the publication assessment.
* Destination: rpi-implement for remaining accepted P03-T02 work, not an unrelated residual issue.
* Smallest useful next action: Parent may make the separately authorized local evidence commit using resolved privacy-safe identity and requested trailer, retaining original adverse outcomes. This Review does not commit. Publication stays blocked until later explicit gate admission, a clean committed candidate, fetched current main, full exact-head gate, immediate receipt verification and independent exact-head assessment. Only then conditionally push the requested topic and open a PR using Refs #514, #515, #516, without closure keywords. Any later candidate/base/input change invalidates prior gate evidence.

<!-- rpi:review id=RV-005 -->
### RV-005 [Low]: Authenticated employee and task/model acceptance remains a distinct owner follow-up

* Related scope: Plan Follow-Up Items; protected-authentication and no-inference boundary.
* Evidence: Research, plan, details and changes all defer authenticated assets/UX, task-release/model binding and human/live/inference acceptance. No session or model invocation was authorized or exercised.
* Impact: Even later engineering deployment checks would not establish authenticated user experience, stronger-task quality, financial approval or live task acceptance.
* Destination: Distinct follow-up FU-EMP-ACCEPT, owned by the project owner/operator.
* Smallest useful next action: Separately scope and authorize authenticated employee journeys and task/model-binding acceptance with appropriate human approval and financial prerequisites. Do not add these to this redeploy or bypass authentication.

## Defects

* No implemented runtime/code defect or unauthorized cloud change is established by the available evidence.
* RV-003/RV-004 are unmet accepted implementation/publication work, not demonstrated code bugs. RV-001 is a decision/feasibility gap; RV-002 is an evidence gap. Fail-closed execution is appropriate but does not close these findings.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| RV-001 High | rpi-plan | Planning parent proves compliant recovery or retains block | Unestablished recovery assumption. |
| RV-002 High | rpi-research | Owner/coordinator supplies authorized sanitized cost evidence | Material financial evidence gap. |
| RV-003 High | rpi-implement | Later explicitly admitted operator completes existing P01/P02 | Accepted runtime delivery unexecuted. |
| RV-004 Medium | rpi-implement | Parent handles pending local commit; later admitted P03-T02 gate/publication | Accepted evidence/publication work unexecuted. |
| RV-005 Low | Distinct follow-up FU-EMP-ACCEPT | Owner/operator separately scopes acceptance | Deliberately excluded nonblocking acceptance work. |

Later implementation of routed findings does not require another RPI Review. This original finding set and original critique remain preserved.

## Residual Work

* FU-EMP-ACCEPT is the separate owner-operated authenticated/task/model acceptance item. It is not a defect or a reason to expand this run.
* Deployment prerequisites, the actual redeploy and local commit/publication remain active unmet work, not residual tasks that may be silently dropped.

## Blockers and Remaining Work

* Build and full gate: historically observed foreign heavy-lock owner; no review-time recheck, polling, interruption, waiting or re-admission.
* Cloud writes: unknown complete all-in headroom and unestablished supported Single-mode recovery. No role, mode or spending exception is inferred.
* P01-T01 backup is reported complete, build remains blocked. P01-T02 and P02 remain unexecuted. P03-T01 receives this one Review; P03-T02 commit/gate/publication remains pending.
* External equality evidence is not independently revalidated here. No present-time remote state, hosted checks, PR existence or financial/authenticated/runtime acceptance is asserted.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
|---|---|---|---|
| Review-time git status --short; branch; log; upstream inspection | Local branch and evidence candidate | Passed | Requested topic at stated HEAD, six original task artifacts untracked, upstream origin/main. No commit/push performed. |
| Canonical artifact and relevant policy reads | Full requirements/markers/critique/follow-ups | Passed | All P01-P03 and PC-001..005 compared once; no source mutations. |
| Recorded safe GETs and semantic equality assertions, exit0 | Existing app/config/template/identity/registry/scale and ACR | Passed as reported; independent check unavailable | Backup hashes/equality recorded by execution, not recomputed by this reviewer. |
| Recorded lslocks observation | Shared heavy-lock ownership | Blocked admission | PID3869238 python3 reported; no polling or lock attempt in Review. |
| Recorded ActualCost API2025-03-01 query, exit1 | Financial readiness | Failed | HTTP429; no amount or headroom established. |
| Recorded explicit-period API2023-11-01 alternative, exit1 | Financial readiness | Failed | Unauthorized/RBACAccessDenied; no authorization change attempted. |
| Source image build and actual synthetic HTTP/script-order/image identity checks | P01-T01 | Not run / Blocked | Foreign heavy lock; no image exists for this task. |
| ACR exception/login/push/digest and exact restoration | P01-T02 | Not run / Blocked | No image or financial readiness; registry never opened. Unchanged policy is not restoration proof. |
| One new revision, additive AI configuration, health/readiness/log/assets and recovery | P02 | Not run / Blocked | No app writes; no new runtime to validate. No rollback required or demonstrated. |
| Full local gate, receipt verification, independent exact-head assessment | P03-T02 | Not run / Blocked | Foreign lock; no committed candidate or passing receipt. No gate run by this reviewer. |
| Authenticated employee UX, task/model/live/inference and human acceptance | Separate acceptance | Not run / Outside scope | No authorized session or paid inference; no financial, auth or UX acceptance inferred. |

## Outcome

* Outcome: Not accepted.
* Rationale: The complete caller request is materially unmet: no build, push, employee update, new revision, AI variables, runtime verification, committed evidence or Refs-only PR. Preservation and fail-closed restraint are justified, but do not constitute a successful deployment or completion.
* Severity summary: 3 High, 1 Medium, 1 Low; zero demonstrated unauthorized mutations or runtime code defects.
* Review execution Complete; operational execution Blocked with Partial preservation; residual acceptance FU-EMP-ACCEPT remains separate.
* No runtime success, financial approval, authorization acceptance, authenticated UX acceptance, inference quality or human/live approval is established.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---|---|---|
| Demonstrated implementation defect | None established | Do not invent a source defect from blocked work. |
| Unmet accepted implementation/publication | rpi-implement, RV-003/RV-004 | Parent retains blockers and pending commit; conditional later admitted execution/gate/publication. |
| Decision gap or invalid assumption | rpi-plan, RV-001 | Establish compliant recovery before mutation. |
| Material evidence gap | rpi-research, RV-002 | Obtain authorized sanitized all-in financial readiness evidence. |
| Nonblocking residual work | Distinct FU-EMP-ACCEPT, RV-005 | Owner separately authorizes authenticated/task/model acceptance. |

* Review execution status: Complete.
* Operational execution status: Blocked; P01-T01 Partial.
* Outcome: Not accepted.
* Validation coverage: Document/Git comparison completed; execution equality only reported, external direct verification unavailable; failed financial queries retained; no build, gate or runtime checks rerun.
* Blockers: Recovery, financial evidence and later explicit lock admission; publication also requires committed exact-head candidate, full receipt and independent publication assessment.
* This is the complete original finding set for one Review. No fix, second Review, agent, commit, Azure write or publication was performed.

## Artifacts

| Artifact | Description |
|---|---|
| [.copilot-tracking/research/2026-10-28/employee-redeploy-research.md](.copilot-tracking/research/2026-10-28/employee-redeploy-research.md) | Research and qualified historical readiness. |
| [.copilot-tracking/plans/2026-10-28/employee-redeploy-plan.md](.copilot-tracking/plans/2026-10-28/employee-redeploy-plan.md) | Current blocked plan and requirements. |
| [.copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md](.copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md) | Preservation and unexecuted operational contracts. |
| [.copilot-tracking/reviews/plans/2026-10-28/employee-redeploy-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/employee-redeploy-plan-critique.md) | Original Complete / Revise critique. |
| [.copilot-tracking/changes/2026-10-28/employee-redeploy-changes.md](.copilot-tracking/changes/2026-10-28/employee-redeploy-changes.md) | Recorded backup, failures and no-write terminal state. |
| [.copilot-tracking/rpi-sessions/2026-10-28/employee-redeploy-state.json](.copilot-tracking/rpi-sessions/2026-10-28/employee-redeploy-state.json) | Pre-review automatic-parent state; unchanged. |
| [src/README.md](src/README.md) | Full local gate, financial and nonqueued admission rules. |
| [infra/README.md](infra/README.md) | Employee model prerequisite and configuration contract. |
| [docs/case_study_48_original.md](docs/case_study_48_original.md) | Original project context. |
| [docs/case_study_48_addendum.md](docs/case_study_48_addendum.md) | Qualified project and acceptance context. |
| [docs/reference/README.md](docs/reference/README.md) | Knowledge-base index. |
| [docs/reference/memory.md](docs/reference/memory.md) | Owner context, not evidence. |
| [docs/reference/research/sector/housing-association-primer.md](docs/reference/research/sector/housing-association-primer.md) | Sector context, not company acceptance evidence. |
| [.copilot-tracking/reviews/logs/2026-10-28/employee-redeploy-review.md](.copilot-tracking/reviews/logs/2026-10-28/employee-redeploy-review.md) | This one complete original Review. |

## Next Steps

Return this result to the active parent. Retain the blocked outcome and pending local evidence commit/publication. Route RV-001 to rpi-plan and RV-002 to rpi-research; only after those prerequisites and a later explicit lock-free coordination event may RV-003/RV-004 proceed through rpi-implement. Keep FU-EMP-ACCEPT distinct. Do not poll, re-admit, run gates, mutate Azure, push, open a PR or repeat Review on this record's authority.
