---
title: Independent RPI Review - nominal pacing PR 508
description: One bounded post-implementation assessment of nominal replay pacing
ms.date: 2026-10-29
---

## Scope and Evidence

* Task ID: pr-508-nominal-pacing.
* Task slug: iot-nominal-pacing-508.
* Review date: 2026-10-29.
* Scope: one independent post-implementation Review of the supplied current task artifacts and working-tree diff against HEAD 4a9d2f2e.
* Evidence: research, plan, phase details, original plan critique, changes record, session state, changed core/API source, existing test files and direct READMEs.
* Rubric restoration is an owner-directed boundary item, not an implementation feature.

## Opening Review State

* Interpreted goal: verify nominal slot timing fixes reordered replay scheduling without changing wire payloads or existing bounded publisher behavior.
* Review scope: P01/P02 and all task-specific critique dispositions, validation and lifecycle claims.
* Evidence readiness: all six supplied task artifacts are present; contents and diff await comparison.
* Acceptance basis: supplied nominal 8-hour/28.8-second reproduction, preserved reordered payload timestamps, constructor completeness, existing publisher controls and truthful evidence reconciliation.
* First comparison boundary: reconcile current artifacts before tracing changed source and regression tests.
* Active read-only boundaries: only this review record may be written; no implementation, artifact repair, nested agents, repeated Review, Azure, full API suite or push.
* Initial blockers: none identified before comparison. Full publication gate is intentionally excluded and remains coordinator-owned.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one independent comparison completed against HEAD 4a9d2f2e081f40c390ceaa573b7a5c6cd65e2636 on feat/iot-consumer-110. All six current task artifacts, seven tracked diff paths and the directly relevant surrounding code/test behavior were assessed. No nested agent, second Review or implementation correction was used.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01/P01-T01 | Nominal metadata and suffix scheduling | Reconciled | Required datetime generated from origin/slot cadence; retained in original, duplicate and publisher snapshot constructors; scheduler reads nominal metadata. |
| P01/P01-T01 acceptance | Exact suffix sends and payload preservation | Reconciled | API regression uses real Pacer, virtual clock, speed 1000 and 60-second budget, asserts sends at 0/28.8 seconds and exact clean-row 2/5 bodies. |
| P02/P02-T01 | Requested scoped validation | Reconciled | All requested checks are recorded as passed after formatting correction; original negative regression and initial format failure remain visible. |
| P02/P02-T01 | Directly related guides and rubric | Reconciled | Direct README additions describe actual metadata/scheduling behavior; latest.json independently matches origin/main. |
| P02/P02-T01 lifecycle | Implementation completion versus lifecycle handoff | Reconciled | Checked implementation markers do not claim a completed Review, final commit or publication. State correctly identifies Review as active and review path null before this execution. |
| Follow-Up Items | Publication/hosted/human gates | Reconciled | Outside this bounded fix and explicitly coordinator-owned; not hidden active implementation. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/synthetic/sensor_stream.py | Appends required nominal_at and derives it from original origin plus slot cadence, independent of swapped observation index. Duplicate copies retain it. | All three Frame construction sites across src were inspected; two are here and the third is publisher snapshotting. | Independent two-test core run passed; recorded broader checks passed. | Conformant. No optional observation-time fallback. |
| P01-T01 | src/api/src/zava_forward/api/iot_stream.py | Copies nominal_at into defensive snapshot and uses it instead of observed_at for interval calculation. | Exact source diff changes only the copy argument and scheduling timestamp source. | Recorded selected API tests passed; independent rerun unavailable in system interpreter. | Conformant within supplied evidence boundary. |
| P01-T01 | src/core/tests/test_sensor_stream.py | Adds custom origin/cadence/suffix metadata test and extends all explicit nonempty fault cases. | Suffix equality includes required metadata; duplicate loop checks metadata on every duplicate; gap remains empty. | Two directly relevant tests independently passed. | Semantic coverage matches plan. |
| P01-T01 | src/api/tests/test_iot_stream.py | Adds one actual-Pacer virtual-clock regression preserving exact faulted wire bodies. | Confirms slots 3/4, observed delta 24 hours, two sends, 28.8-second separation, 59.5-second reserve boundary and shutdown. | Original RUN_DEADLINE/fixed-pass evidence retained in changes record and supplied by caller. | Regression distinguishes original defect; no mock of wait/scaling substitutes for actual Pacer. |
| P02-T01 | src/core/README.md; src/api/README.md; .github/rubric/scores/latest.json | Documents scheduling metadata and exact example; restores owner-selected rubric. | Source/docs diff and independent origin/main comparison. | git diff --check and rubric comparison passed. | Accurate and scope-contained. |

### Behavior and Test Reliability

* Payload generation and selection, observation timestamps, schema/version, wire serialization, reading IDs, reference hashing, truth records and selected-stock provenance are unchanged. Metadata remains outside the payload. Original/faulted payload comparisons are explicit in the new regression.
* For duplicate frames and multiple devices at one slot, nominal datetimes are equal, so the existing nonnegative interval calculation produces zero model delay. Stable slot sorting and device selection are unchanged. Consecutive distinct slots use configured cadence, including suffixes and custom origins.
* Burst still explicitly passes zero model spacing. Actual global rate admission remains inside send after connection, message construction and attempt-truth preparation. Budget, binding, supplied deadline/rate validation, stop/pause/cancellation, disconnect, exception sanitization and cleanup code are unmodified.
* Existing publisher tests cover actual send rate across devices, setup/preparation delay, stricter/invalid supplied controls, binding refusal, distinct clients, stop/deadline/cancellation and bounded cleanup. Existing core Pacer tests exercise rate, positive bounded polling and deadline controls. Their recorded selected-module passes support preservation; not every scenario was independently rerun.
* The new virtual clock starts from real monotonic time before Pacer construction, satisfying existing supplied-deadline validation without changing production clocks. Patched sleep advances only virtual time; no real 28.8-second wait is needed. The patch is context-managed. A 28.8-second target lies well below both the virtual 60-second deadline and stated 59.5-second publication allowance. Floating-point assertions use assertAlmostEqual rather than exact elapsed equality.
* The fake SDK client and inert certificate paths avoid network, credential reads or real-device activity. The new API test adds no production-clock patch or SDK behavior change. It deliberately tests Pacer's virtual deadline, not a fully virtualized asyncio wall-clock timeout.
* Exactly two new unittest methods were added in the existing test files, with no removals. No mvp, generated payload or unrelated production edits appear in the tracked diff.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01 | Distinguishes material in-scope findings from unrelated deferral. | Original PC-001; existing one-Review/no-return-to-implementation constraint. | Plan Critique Disposition, task details, changes and state preserve original Revise and require blocked successful handoff for material in-scope findings. | Direct compatible correction; no new technical decision or repeated critique needed. | Resolved; original adverse critique remains intact. |
| P02-T01 lifecycle | Separates completed implementation from subsequent Review and commit. | Avoids circular completion prerequisites; caller explicitly confirms lifecycle interpretation. | Checked markers, detailed completion evidence, changes remaining-work prose and active Review state agree. | Descriptive reconciliation, not new scope or revised acceptance. | No missing-implementation finding for pending commit. |
| P02-T01 validation | Ruff reformatted newly added API call, then all requested API checks reran. | Initial format failure retained in changes evidence. | Current diff uses corrected formatting and final checks are separately recorded. | Ordinary implementation correction; no material plan revision. | Reconciled. |

## Critique and Material Revision Assessment

* Latest critique: the sole independent critique is Complete / Revise, with PC-001 Medium and no other findings. Its original verdict and recommendation are preserved, not rewritten to Ready.
* PC-001 disposition: current plan/details explicitly prevent a successful fix handoff if material in-scope Review findings remain. The accepted unresolved-blocker option satisfies the critique without authorizing another Review or post-Review implementation within this task.
* Material technical revisions: none. Required nominal metadata, three constructors, two-test allocation, actual-Pacer regression and scoped validation implement researched C1-C5 and confirmed intent.
* Dependent-work pause: supplied state and changes evidence record critique resolution before implementation; current artifacts expose no unresolved critique dependency or premature resumption.
* Justification: no unaccepted scope, payload, control, configuration or publication divergence was found.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Publication/hosted/human gates before push or merge | Caller excludes full API suite and prohibits push; local publication gate would exceed this invocation. | Coordinator, in separately authorized publication lifecycle. | Open distinct follow-up, mirrored in changes and research. Not an implementation defect or active P01/P02 task. |

## Findings

No substantive RV findings identified. Severity counts: Critical 0; High 0; Medium 0; Low 0. No placeholder RV entry is created.

## Defects

* None identified within the assessed task boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | No rpi-implement, rpi-plan or rpi-research handoff required. | No substantive defect, decision gap or material research gap found. |

Later implementation of any separately identified finding would not require this Review to run again.

## Residual Work

* Coordinator-owned publication/hosted/human gates remain distinct from this implementation verdict. No final external receipt, exact-head publication assessment or release approval is established here.
* Parent owns final lifecycle reconciliation and requested privacy-safe Conventional Commit with required trailer after this Review. No push is authorized. A pending commit is not missing implementation.

## Blockers and Remaining Work

* Review blockers: none. Missing system-interpreter API dependency limits independent rerun coverage, not the available static assessment or caller-supplied completed check evidence.
* Remaining active implementation: none identified.
* Publication: intentionally not assessed or approved; excluded full API/publication gate remains coordinator-owned.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| git diff HEAD -- named source/test/README paths | Exact changed implementation | Passed | Reviewed against 4a9d2f2e; production changes confined to nominal metadata propagation and scheduling source. |
| Frame constructor search across src Python files | Constructor completeness | Passed | Exactly three call sites; original, duplicate and publisher snapshot all supply nominal_at. |
| git diff --check | Current task diff | Passed | Independently observed no whitespace errors. |
| git diff --quiet origin/main -- .github/rubric/scores/latest.json | Owner-directed rubric restoration | Passed | Independently observed exact match. |
| From src/core: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest -q test_sensor_stream.ReplayTests.test_nominal_timing_uses_configured_origin_cadence_and_suffix test_sensor_stream.ReplayTests.test_faults_are_separate_truth_and_nominal_slot_replay | New/extended core semantic assertions | Passed | Independently executed 2 tests in 0.008s. |
| From src/api: same environment and python3 -m unittest -q test_iot_stream.PublisherTests.test_out_of_order_suffix_uses_nominal_pacing_and_preserves_payloads | Exact new publisher regression | Unavailable | Attempt failed during import: system Python 3.12.3 lacks azure.eventhub; no test body executed. No dependencies installed or excluded tooling path accessed during this read-only Review. |
| Exact publisher regression on original code | Negative regression evidence | Failed as expected, reported | Caller and changes record retain RUN_DEADLINE, 1 test in 0.015s; not independently rerun or source reverted. |
| Exact publisher regression on fixed code | Positive regression evidence | Passed, reported | Caller and changes record retain 1 test in 0.013s with exact send instants/payloads. |
| Ruff check .; Ruff format --check .; mypy in core/API | Requested static checks | Passed, reported | Core format 108 files/mypy 161; API format 58/mypy 109. Independent Review did not rerun these checks. |
| API initial Ruff format --check . | Historical failure | Failed, corrected, reported | New call wrapping corrected with Ruff; all requested API checks subsequently reran. Original failure retained. |
| Requested PYTHONPATH with unittest test_sensor_stream test_sensor_consumer test_dependency_rule | Core selected modules | Passed, reported | 49 tests in 16.636s; not independently rerun as a suite. |
| Requested PYTHONPATH with unittest test_iot_stream test_sensor_ingestion test_dependency_rule | API selected modules | Passed, reported | 72 tests in 28.996s; not independently rerun as a suite. |
| Full API suite; complete local publication gate; Azure/live acceptance; push | Explicitly excluded | Skipped | Caller scope prohibits these; no full-gate, live or publication claim. |

Reported checks are supplied implementation evidence, not fresh reviewer execution. Historical checks used the caller's existing environment; this Review performed no file operations in temporary directories, installed nothing and wrote only this record.

## Outcome

* Outcome: Conformant.
* Rationale: source and tests implement the researched nominal scheduling contract, preserve intentionally reordered payloads and existing publisher controls, and reconcile completed markers, critique dispositions and bounded validation. No material defect or unjustified divergence was identified. Independent API runtime confirmation is limited by the system interpreter dependency; the verdict also uses the supplied completed scoped API checks and negative/positive regression evidence.
* This is implementation-scope conformance, not whole-product acceptance or permission to publish.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No actionable RV finding. |
| Decision gap or invalid assumption | None | No actionable RV finding. |
| Material evidence gap | None | Scoped implementation evidence is sufficient, with independent rerun limitation disclosed. |
| Non-blocking residual work | Distinct publication follow-up | Coordinator retains external final gate, hosted/human approval and publication responsibilities. |

* Execution status: Complete.
* Outcome: Conformant.
* Validation coverage: independent core semantic tests, diff/constructor/rubric checks and static behavioral trace; supplied scoped core/API/static checks; independent API rerun unavailable as recorded.
* Blockers: none for reviewed implementation; publication intentionally outside scope.
* Parent continuation: preserve this one Review outcome, reconcile lifecycle state and create the requested commit without push. Do not repeat Review.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/iot-nominal-pacing-508-research.md](.copilot-tracking/research/2026-10-29/iot-nominal-pacing-508-research.md) | Assessed research C1-C5. |
| [.copilot-tracking/plans/2026-10-29/iot-nominal-pacing-508-plan.md](.copilot-tracking/plans/2026-10-29/iot-nominal-pacing-508-plan.md) | Assessed current plan and follow-up. |
| [.copilot-tracking/details/2026-10-29/iot-nominal-pacing-508-phase-details.md](.copilot-tracking/details/2026-10-29/iot-nominal-pacing-508-phase-details.md) | Assessed completed phase details. |
| [.copilot-tracking/reviews/plans/2026-10-29/iot-nominal-pacing-508-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/iot-nominal-pacing-508-plan-critique.md) | Preserved original Revise/PC-001. |
| [.copilot-tracking/changes/2026-10-29/iot-nominal-pacing-508-changes.md](.copilot-tracking/changes/2026-10-29/iot-nominal-pacing-508-changes.md) | Assessed implementation and validation history. |
| [.copilot-tracking/rpi-sessions/2026-10-29/iot-nominal-pacing-508-state.json](.copilot-tracking/rpi-sessions/2026-10-29/iot-nominal-pacing-508-state.json) | Assessed active Review lifecycle state. |
| [.copilot-tracking/reviews/logs/2026-10-29/iot-nominal-pacing-508-review.md](.copilot-tracking/reviews/logs/2026-10-29/iot-nominal-pacing-508-review.md) | This single independent Review. |

## Next Steps

The active parent preserves this Complete / Conformant result, reconciles its lifecycle records and performs the requested commit-only handoff. No corrective RPI stage, repeat Review or user action is required. Coordinator retains separate publication gates; do not push.
