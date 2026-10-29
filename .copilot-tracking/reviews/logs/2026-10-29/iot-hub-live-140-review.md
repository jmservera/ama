---
title: IoT Hub live 140 original independent RPI Review
description: One post-implementation review of task140-184 and its complete working-tree boundary
ms.date: 2026-10-29
---

## Scope and Evidence

* Task: task140-184/iot-hub-live-140; Refs #140 #184.
* Boundary: current tracked diff against ecbb5a80470292c885764c28d6833c0e5ef63dfa and all untracked task files.
* Branch: feat/iot-hub-live-140.
* Canonical artifacts: research, plan, phase details, original plan critique, changes and session state dated 2026-10-29 under .copilot-tracking.

## Opening Review State

* Interpreted goal: independently assess implementation correctness, user-intent fidelity, evidence and acceptance without treating a blocked live goal as delivered.
* Scope: the complete supplied task boundary, including existing-hub child-only infrastructure, publisher DeviceActivation and documentation.
* Evidence readiness: named artifacts and changed/untracked task files exist; detailed comparison and evidence verification pending.
* Acceptance basis: live sensor -> hub -> consumer -> SQL -> resident gauges, bounded by the supplied existing B1/one-unit, ama/uksouth, cost, identity, network and workload authorization.
* First comparison boundary: reconcile current plan/detail markers and original critique dispositions to changes, then inspect the complete source/infra diff and untracked files.
* Read-only boundaries: only this review record may be written; no source/cloud modifications, new tests, additional reviewer agents or repeated Review.
* Initial blockers: live transport/SQL/gauge acceptance is reported blocked; final exact-head gate and local commit are downstream pending. These reports require comparison, not presumed acceptance.

## Execution Status

* Review execution: Complete. Exactly one original independent post-implementation Review; no nested agents, fixes, new tests or cloud operations.
* Task execution: Partial against the requested live end-to-end outcome. The bounded conditional P01-P03 implementation is supported, but no device was issued, no message sent, no live consumer activated and no live resident gauge demonstrated.
* Boundary: HEAD remains ecbb5a80470292c885764c28d6833c0e5ef63dfa. Assessed ten tracked changed files and eight pre-existing untracked task files, plus this review-owned report. No other untracked task files appeared in the exhaustive status.
* Source, infrastructure, tests, documentation and all six canonical artifacts were read. Issue #140 and #184 bodies were independently retrieved using gh. Their existing checkboxes and stale "not started" prose are not new acceptance evidence.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Isolated existing-hub profile and actual SKU/unit guard | Reconciled | Child resources only; no hub PUT, namespace, PE or role. Shared guard change is within the explicitly authorized infrastructure work. |
| P01-T02 | Direct-PUT what-if refused, child-only apply Succeeded | Reconciled at supplied evidence boundary | Exact hub preserved; diagnostic logs disabled, metrics retained; Azure-normalized diagnostic arrays still show Modify, honestly disclosed. |
| P02-T01 | Publisher-only DeviceActivation and receiver refusal | Reconciled | Three added API tests plus two infrastructure tests; no removals, dependency change or exceeded twelve-method limit. |
| P02-T02 | Group-inclusive operator lookup found only Owner | Reconciled as conditional parking | No credential/device/public-network action or send; zero ingress is not a successful publish test. |
| P02-T03 | Disposable SQL45; third counts execution succeeded | Partially reconciled | Final three-start/40-second evidence is consistent in current phase details and plan amendment; older normative-looking one-start/45-second text remains, RV-003. |
| P03-T01 | ADR, infrastructure/API guides, synthesis, index and append-only log | Reconciled | Dated authorization is distinguished from source-only history. Original case study and owner memory unchanged. |
| P03-T02 | Static/unit/build evidence and Review/commit/gate handoff | Partial | Review completed here; commit and complete exact-head gate remain pending, RV-004. Path disposition is not executable under this review's restrictions, RV-002. |
| Follow-Up Items | Registry, keyless adapter/revision, gauges and OD-43 | Reconciled as outside current authority | Do not convert these into completed tasks or issue closure; route distinctly through RV-001. |

## Completed Work Assessment

| Marker | Files | Change and purpose | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 | infra/iot-hub-live.bicep; infra/iot-hub-live.bicepparam; infra/modules/iothub-scope-guard.bicep | Pin existing hub; guard actual location/B1/one unit before child writes | Existing-resource reference; both children depend on guard; no hub deployable resource or networking switch | Independently rerun existing compiled IoT suite: 16 passed | No substantive infrastructure defect identified. Defaulted extra guard parameters preserve production callers. |
| P02-T01 | src/api/src/zava_forward/api/iot_stream.py; src/api/tests/test_iot_stream.py | Factor unchanged hostname/group/approval checks into publisher-only declaration | HubPublisher accepts either activation; HubReceiver rejects DeviceActivation before bindings, credentials or client construction | Supplied positive/negative, compatibility and ingestion tests; direct source inspection | No substantive source defect identified. Declarations do not verify deployed permission; README says so. |
| P02-T03 | Canonical changes and phase details | Real local SQL proof and counts-only cloud inspection | SQL45 reported passed on owned disposable SQL2022; three named cloud executions terminal; final tables absent/count0 | Supplied execution evidence, not independently rerun cloud/SQL | Establishes bounded local persistence engineering and cloud schema absence, not transport causality. |
| P03 | docs/adrs/0003-journey-derived-capabilities-runtime-fit.md; docs/reference/README.md; docs/reference/log.md; docs/reference/research/iot-sensor-analytics-research-plan.md; infra/README.md; src/api/README.md | Preserve dated authority, cost assumptions, blockers and API contract | Complete documentation diff inspected; new relative links reviewed | Independent git diff --check passed | No whole-issue, deployed-consumer or gauge-success claim found. Cost scenarios remain estimates, not actual billing or enforced caps. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Change and reason | Trigger and authority | Reconciliation and assessment |
| --- | --- | --- | --- |
| P01 | Replace proposed direct hub PUT with existing-hub child reconciliation | What-if exposed deletion of service-owned properties; existing hub already satisfies authorized B1/one-unit scope | Compatible narrowing, not a new resource authorization. Refused what-if retained; no unsafe apply claimed. |
| P02-T02 | Park registry/device/network actions | Group-inclusive assignment evidence only Owner; no operator role or service-key authority | Preserves explicit owner limits and original live objective as unmet. No ineffective hub receiver grant selected. |
| P02-T03 | Replace assumed retry0/300 and one start with actual retry1/600 and three finite starts | Two retained driver failures, diagnosed unsupported timeout string; last success; job definition unchanged | Numerical final bound is explicit: six possible platform attempts/3600 seconds, process40 seconds, no fourth start, reserved ancillary allowance. Compatible bounded troubleshooting within stated authority, not proof of actual billed cost. Older current-looking descriptions require RV-003. |
| P03-T02 / PC-001 | Keep historical /tmp/mv instruction despite critique | Owner tooling preference and successful commands cited as rejection rationale | Successful execution does not establish permission under this review's explicit no-temporary-directory boundary. Future execution must use an allowed path or be blocked; RV-002. This Review does not retroactively infer the parent's execution permissions. |
| Follow-Up Items | Separate additional roles/adapter/schema/view work | Actual authorization and schema observations | Correctly remains outside active implementation. Separate approval and acceptance evidence required, RV-001. |

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with 3 High and 1 Medium findings; it was not overwritten or repeated.
* PC-002 is substantively addressed more strongly by eliminating hub PUT entirely. Exact child profile, pinned hub name, actual resource checks and guarded dependencies support the admission boundary.
* PC-003 has an explicit local-before-cloud dependency and a reported ordered command history. SQL45 precedes cloud counts in that history. No independent timestamped command log was supplied for every local prerequisite, so this is assessed as implementation-record evidence, not fresh cloud audit.
* PC-004 has a recorded bounded amendment based on actual immutable job settings and diagnosed failures. All executions are reported terminal; no fourth start is authorized. The amendment is not silent, but authoritative/historical wording needs reconciliation under RV-003.
* PC-001 is explicitly dispositioned, but not resolved for this reviewer execution environment: retain the original adverse critique and route the continuation-path decision through RV-002.
* No significant architecture expansion requiring broader cloud authorization was implemented. The justified narrowing does not constitute acceptance of the full user outcome. A second critique or Review is not requested.
* Supplied evidence describes dependent cloud work as paused until relevant checks passed; no independent cloud action was taken to recreate this history.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Exact-hub registry authority and device connectivity | New operator role and public-network changes are not currently authorized | Owner decides exact scoped permission and reachable device path before issuer acts | Open; RV-001 / FU-REGISTRY. No automatic self-grant. |
| Keyless receive adapter and API revision | Requires separately approved paid adapter/network/data roles and deployed consumer invocation | Owner and cloud/API delivery owner approve and implement a bounded receive path | Open; RV-001 / FU-TRANSPORT. Built-in group is not an Entra receive workaround. |
| SQL/projection/resident freshness | Sensor tables absent; no DDL or application/view activation authorized here | SQL/API/resident delivery owner obtains approval, initializes synthetic controls and reconciles view | Open; RV-001 / FU-GAUGES. Browser refresh alone cannot rebind the view. |
| Credential lifecycle / OD-43 and parent criteria | Actual issue/rotate/revoke and broader simulator acceptance not exercised | Named credential owner Juan Manuel Servera and parent issue owners obtain distinct evidence | Open; RV-001 / FU-LIFECYCLE. Local tests do not establish this acceptance. |

These are distinct follow-up work, not new active Pxx tasks or source defects merely because they remain open.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: The requested live sensor-to-resident outcome remains unproven and blocked

* Scope: full user outcome; P02 and plan Follow-Up Items.
* Evidence: .copilot-tracking/rpi-sessions/2026-10-29/iot-hub-live-140-state.json records registry-authority, keyless-receive and cloud-sensor-schema blockers. The changes record reports no sends, no devices, no cloud consumer revision, all three sensor tables absent and no gauge observation. The actual #184 parent criteria remain unproven.
* Impact: Child diagnostics and local SQL tests cannot be accepted as live telemetry delivery, current resident readings, complete #140/#184, AC-066 or OD-43. The conditional plan AC4 is honestly satisfied by a blocker record, not by the full user goal.
* Destination: distinct follow-ups FU-REGISTRY, FU-TRANSPORT, FU-GAUGES and FU-LIFECYCLE above; owner authorization followed by their respective delivery owners.
* Smallest useful next action: retain explicit blocked live acceptance. Owner chooses whether to authorize the narrowly scoped registry/connectivity step; do not activate any further step merely to clear this Review. Later acceptance needs correlated device message, hub receipt, controlled SQL write/idempotency and resident projection/freshness evidence.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: The rejected scratch-path critique leaves continuation instructions incompatible with this execution boundary

* Scope: PC-001; P03-T02.
* Evidence: .copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md, Critique Disposition, retains /tmp/mv because commands worked and parks only on actual failure. .copilot-tracking/details/2026-10-29/iot-hub-live-140-phase-details.md, P03-T02, still commands that path. The current review instructions prohibit temporary-directory operations, require review-only writes and do not allow success to override that boundary. src/README.md documents additional temporary paths and a shared temporary gate lock.
* Impact: A continuation cannot treat the existing disposition as permission to execute prohibited file operations or silently relocate/bypass gate internals. This is a future execution/readiness decision gap, not evidence that the publisher source is defective or that the parent's past commands lacked authority.
* Destination: rpi-plan, owned by the active parent.
* Smallest useful next action: reconcile the continuation's actual higher-priority storage constraints and explicitly identify a permissible existing tooling/output arrangement. If the unchanged complete gate cannot run within them, record it Blocked with the required environment change; do not weaken the gate, bypass its lock or run until a filesystem error occurs. Preserve the original critique and historical results.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Current-looking SQL admission prose still contradicts the final three-execution amendment

* Scope: P02-T03 and PC-004 evidence reconciliation.
* Evidence: .copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md, Critique Disposition, says one execution, login10, retry0/timeout300 and process45. Its later amendment says three starts, actual retry1/timeout600 and process40. .copilot-tracking/changes/2026-10-29/iot-hub-live-140-changes.md, Amendments and Divergences, still says one execution/process45, whereas Validation and live outcomes and phase details report three/process40/login20.
* Impact: Final state can be inferred, but the canonical record is not fully reconciled and can mislead a later operator or acceptance reader about which admission bounds were actually used. This does not invalidate the explicitly retained terminal outcomes or justify another execution.
* Destination: later rpi-implement documentation/evidence correction within the accepted direction, owned by the parent.
* Smallest useful next action: label original one-start/assumed-timeout text explicitly historical and append or consolidate an authoritative final-state summary: three total starts, first two Failed/third Succeeded, actual retry1/600, process40/login20, maximum six attempts/3600 seconds, no fourth start. Preserve original failures and decisions; do not rewrite the original critique or this Review.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Local commit and complete exact-head gate are still required downstream lifecycle work

* Scope: AC5; P03-T02 handoff.
* Evidence: git HEAD remains the supplied base with the complete implementation and original task evidence dirty/untracked. No committed candidate or external complete receipt exists in the supplied task set. The plan, changes and caller correctly identify these steps as pending.
* Impact: Targeted passing checks and this Review cannot establish committed-head validation, publication readiness, hosted approval or human acceptance. This is an expected pending lifecycle condition, not an implementation bug or a fabricated failed gate.
* Destination: distinct follow-up FU-LOCAL-LIFECYCLE, active parent.
* Smallest useful next action: after resolving routed documentation/planning items, preserve original Review/critique outcomes; resolve authenticated GitHub identity and local noreply author/committer; make the requested local-only commit with trailer and Refs #140 #184. Run the unchanged complete local gate only if filesystem/tool/lock prerequisites permit, retain its external receipt and verify it against the actual candidate/base. If blocked, record that fact. Do not push, use closing keywords, claim hosted/human approval or rerun this Review.

## Defects

* No substantive runtime or deployed-template code defect found in the complete supplied source/infra boundary.
* RV-003 is a low-severity implementation evidence/documentation reconciliation defect, routed to rpi-implement. RV-002 is a planning readiness gap, not a source defect.

## Routed Findings

| Finding | Destination | Owner / next action | Route basis |
| --- | --- | --- | --- |
| RV-001 | FU-REGISTRY; FU-TRANSPORT; FU-GAUGES; FU-LIFECYCLE | Owner decisions and distinct delivery owners above | Residual full-outcome work beyond current authority |
| RV-002 | rpi-plan | Active parent reconciles admissible continuation paths or records gate blocked | Execution decision/readiness gap |
| RV-003 | rpi-implement | Parent corrects current-vs-historical SQL evidence wording without new execution | Documentation reconciliation defect |
| RV-004 | FU-LOCAL-LIFECYCLE | Parent owns local commit and complete exact-head gate | Expected pending lifecycle work |

Later implementation of routed findings does not require another Review. No material unresolved receive-auth research question was discovered: existing research already identifies the shared-key limitation. Do not reopen research merely to seek an unauthorized workaround.

## Residual Work

* The four live follow-ups remain separate from this bounded task's conditional implementation acceptance.
* Local commit/gate work remains separate from live authorization, actual deployed end-to-end evidence, hosted checks and human approval.
* Do not close #140 or #184, alter their acceptance checkboxes, or infer authority after the stated October31 window from these results.

## Blockers and Remaining Work

* Live: absent registry data authority/reachable approved path; unapproved keyless receive adapter and API revision; absent sensor tables and unreconciled resident view; unproven credential lifecycle.
* Continuation: RV-002 path/admission decision; RV-003 evidence wording; RV-004 local lifecycle.
* Conditional source/child-reconciliation tasks have implementation evidence, but checked P03 handoff is not evidence that downstream commit/gate ran.

## Validation Evidence

| Command or evidence | Scope | Status | Result / limit |
| --- | --- | --- | --- |
| PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s infra/tests -p test_iothub_module.py -q | Existing production/main and live compiled IoT contracts | Passed, independently executed | 16 tests, 9.375 seconds. No new tests or generated source files. |
| git diff --check | Complete tracked working diff | Passed, independently executed | No whitespace errors. |
| git diff against supplied base; git status --short --untracked-files=all; gh issue view 140/184 | Review boundary and actual issue text | Passed, independently executed | Exhaustive task file inventory and acceptance claims compared; no remote mutation. |
| PYTHONDONTWRITEBYTECODE=1 python3 dependency import probe | Reviewer system Python runtime | Unavailable for API replay | azure.eventhub missing; no ruff/mypy on default PATH. No installation or alternate temporary venv use under review-only authority. Not a candidate test failure. |
| API Ruff / format / mypy | Owning API package | Passed in supplied implementation record | 58 formatted files, 110 source files typed; not independently rerun. |
| Relevant API/core unittest | Activation, replay, ingestion, resident sensors | Passed in supplied implementation record | 94 combined tests; local mock/SQLite coverage, not live transport. |
| ZF_SENSOR_MSSQL=1 test_sensor_ingestion | Owned disposable real SQL Server | Passed in supplied implementation record | 45 tests; reported owned containers removed. Not rerun: would create/write additional resources beyond this review. |
| Production/live build/lint/build-params; policy suite | Infrastructure | Passed in supplied implementation record | Policy54 and IoT16; IoT16 independently repeated above. Full policy suite not repeated: an existing test writes temporary files and review permits no such operations. |
| Initial direct-PUT what-if | Proposed hub mutation | Rejected in supplied implementation record | Service-owned deletions exposed; no apply. This is an admission success, not a failed live delivery test. |
| Child-only apply and safe property/diagnostic projections | Existing hub only | Succeeded in supplied implementation record | Logs0/metrics1; original hub settings unchanged. No fresh cloud verification performed. |
| Three named counts-only executions | Existing private Manual initializer | Failed, Failed, Succeeded in supplied implementation record | Final execution 19:06:25Z-19:06:59Z; absent tables/count0. All terminal; driver failures preserved. No DDL or row reads claimed. |
| Group-inclusive roles, apps/jobs, ingress | Live constraints | Supplied observation only | Owner only; four apps all min0, eight jobs allManual; no sends, zero ingress. Not operational acceptance. |
| Complete committed exact-head gate / receipt verification | Full candidate | Not run / pending | Expected after local commit; RV-002 and prerequisites govern admission. No full-gate pass claimed. |
| Actual device-to-hub-to-SQL-to-resident proof; hosted/human acceptance | Full user outcome | Blocked / not performed | Explicit live authority/schema/revision blockers; no inferred approval. |

## Outcome

* Review execution: Complete.
* Task execution: Partial.
* Outcome: Not accepted for the full requested live sensor-to-resident result or publication readiness. Bounded source/child-reconciliation progress is supported, but live delivery is parked, not delivered; RV-002 also leaves an unresolved continuation-readiness decision.
* Severity summary: 0 Critical, 1 High, 2 Medium, 1 Low. One low documentation reconciliation defect; no substantive runtime/source defect established.
* The full user result is not relabeled Conformant or Conformant with justified divergence merely because conditional plan AC4 permits recording a blocker. The safe narrowing is justified; unexecuted live acceptance remains residual work.
* This is the original one-pass outcome. Later corrections or gates do not change this original verdict or authorize a repeated Review.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | rpi-implement, RV-003 | Parent reconciles documentation only, preserving history |
| Decision gap | rpi-plan, RV-002 | Parent establishes permissible execution paths or blocks gate |
| Material research gap | None | Known authority/adapter limitation already researched |
| Residual live work | Distinct RV-001 follow-ups | Owner decides authorization; respective owners produce actual causal evidence |
| Residual lifecycle work | FU-LOCAL-LIFECYCLE, RV-004 | Parent local commit and complete exact-head validation; no push |

* No action was taken outside this report's write boundary.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/iot-hub-live-140-research.md](.copilot-tracking/research/2026-10-29/iot-hub-live-140-research.md) | Compared research and authority/adapter evidence. |
| [.copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md](.copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md) | Compared current plan, dispositions and follow-ups. |
| [.copilot-tracking/details/2026-10-29/iot-hub-live-140-phase-details.md](.copilot-tracking/details/2026-10-29/iot-hub-live-140-phase-details.md) | Compared task procedures and final amendments. |
| [.copilot-tracking/reviews/2026-10-29/iot-hub-live-140-plan-critique.md](.copilot-tracking/reviews/2026-10-29/iot-hub-live-140-plan-critique.md) | Original Revise retained. |
| [.copilot-tracking/changes/2026-10-29/iot-hub-live-140-changes.md](.copilot-tracking/changes/2026-10-29/iot-hub-live-140-changes.md) | Compared implementation, failures and validation record. |
| [.copilot-tracking/rpi-sessions/2026-10-29/iot-hub-live-140-state.json](.copilot-tracking/rpi-sessions/2026-10-29/iot-hub-live-140-state.json) | Compared blockers and continuation state; unchanged. |
| [.copilot-tracking/reviews/logs/2026-10-29/iot-hub-live-140-review.md](.copilot-tracking/reviews/logs/2026-10-29/iot-hub-live-140-review.md) | This single original independent Review. |

## Next Steps

Return to the active parent: route RV-002 to planning, RV-003 to a later documentation implementation, and retain RV-001/RV-004 as distinct live/lifecycle work. The parent owns any eligible continuation and the requested local-only commit. Do not rerun this Review, push, close issues, weaken validation, or imply human/hosted approval.
