---
title: RPI Review - IoT Hub live 140 PR557 fix cycle 1
description: Single independent post-implementation review of the frozen source correction
ms.date: 2026-10-29
---

## Scope and Evidence

* Task ID: 140-184-pr557-fix-cycle-1.
* Review date: 2026-10-29.
* Scope: working-tree diff from HEAD 3c04f84814052a7a552d4816a2fbd0834c1d3db8, limited to infra/tests/test_iothub_module.py and src/api/README.md.
* Canonical evidence: dated research, plan, phase details, changes, plan critique and rpi-sessions state with slug iot-hub-live-140-pr557-fix-cycle-1.

## Opening Review State

* Interpreted goal: independently assess both user findings, compiler-evaluated guard regression protection and explicit bounded operator instructions.
* Review scope: the complete supplied two-file source boundary and its task evidence; no Bicep or runtime behavior change is intended.
* Evidence readiness: all six canonical task artifacts located; source HEAD and two-file diff confirmed. Detailed comparison and independent bounded validation pending.
* Acceptance basis: supplied user findings, current plan criteria and critique dispositions.
* First comparison boundary: reconcile current plan/detail/change/state markers, then compare the exact diff and relevant unchanged guard/compiler context.
* Active read-only boundaries: only this review artifact may be written. No source, plan, state, historical evidence, commit, push, Azure operation, secret access, manual rubric edit, installation, full gate, SQL or browser execution.
* Initial blockers: none to review; local commit and external gate are expressly deferred to the parent after this Review.

## Execution Status

* Execution status: Complete.
* This single Review compared the full supplied source diff, all six canonical artifacts and relevant unchanged compiler/evaluator/runtime context. Independent bounded offline compilation and all 18 targeted tests passed.
* Implementation lifecycle status is separately Partial: P01 and P02-T01 are complete; P02-T02 remains pending parent reconciliation, local commit and external gate attempt. Completion of this Review does not complete that lifecycle task.
* Starting and ending HEAD: 3c04f84814052a7a552d4816a2fbd0834c1d3db8 on feat/iot-hub-live-140. Source diff: 78 added test lines and 11 added documentation lines, no deletions or other tracked source changes.
* Reviewed two-file git diff SHA-256: 3e5d39485e4414c188bb8235248a56eaadba1055ed2aee34bbc5af9c1e4d0d31.

## Scope and Evidence Inventory

* Research: .copilot-tracking/research/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-research.md, Q1-Q2 and C1-C8.
* Plan: .copilot-tracking/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan.md.
* Details: .copilot-tracking/details/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-changes.md.
* State: .copilot-tracking/rpi-sessions/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-state.json.
* Source: infra/tests/test_iothub_module.py and src/api/README.md, exact working-tree diff from the recorded HEAD.
* Read-only supporting context: infra/iot-hub-live.bicep, infra/modules/iothub-scope-guard.bicep, infra/tests/test_bicep_policy.py, src/core/src/zava_forward/core/synthetic/sensor_stream.py and src/api/src/zava_forward/api/iot_stream.py.
* Repository context: original case study, addendum, reference index and owner memory. No regulatory, deployment or private-data acceptance assessment was needed.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Compiled live scope coverage | Reconciled | One helper and two tests cover all five independent fixtures, both constraints, all 13 mutations and both child dependencies. |
| P01 / P01-T02 | Explicit bounded operator guidance | Reconciled | Exact limits and pre-run calendar/window responsibility appear immediately after DeviceActivation guidance. |
| P02-T01 | Validation Record | Reconciled | Required checks recorded as passed; original formatter failure and correction remain disclosed. Review independently reran the targeted suite. |
| P02 / P02-T02 | Pre-Review Reconciliation and Remaining Work | Honestly pending | Review is now complete in this record only; local commit and gate attempt remain parent-owned. No source defect is inferred from sequencing. |
| Follow-Up Items | Historical live/full-gate blockers | Reconciled | Kept outside the two corrections and routed distinctly below. |
| rpi-sessions state | Active phase Review, source frozen | Reconciled at intake | Stopped manual session with active Review next action is a handoff, not evidence that implementation is incomplete. Parent owns post-Review state update. |

## Completed Work Assessment

| Marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/tests/test_iothub_module.py | Added assert_live_scope_guards and two test methods to close missing compiled behavioral coverage. | Independent group and location expected values, schema/input checks, guard dependency resolution and deep-copy mutations. | Independent 18-test run passed; reported full infra470 and isolated Ruff checks passed. | Conformant; no Bicep or runtime change. |
| P01-T02 | src/api/README.md | Added exercise-only 2/1/60 settings and operator calendar responsibility. | Exact constructor settings, owner/cost/alert references, rejection of default100/larger limits and explicit UTC stop instant. | Manual comparison with unchanged RunBudget, Pacer and HubPublisher.run. | Conformant; existing credential/routing/live caveats retained. |
| P02-T01 | Changes validation evidence | Executed required focused/full infra, API/core and static checks. | Commands, counts, durations and the initial formatter correction recorded. | Supplied checks accepted as implementation evidence, not relabeled as independently rerun. | Complete for the required focused validation scope. |

### User finding 1: independent live guards and rejecting mutations

The helper evaluates the actual compiled nested deployment parameters through the existing evaluate helper; it does not merely search source text. The injected resourceGroup().name and reference(...).location are independent of values(template, location=requested).

| Group / requested / actual | Expected group result | Expected location result | Obligation established |
| --- | --- | --- | --- |
| ama / uksouth / uksouth | ok | ok | Positive admission control. |
| other / uksouth / uksouth | empty | ok | Group independently rejects without masking the correct location result. |
| ama / westus / westus | ok | empty | Actual/requested equality alone cannot admit a non-UK region. |
| ama / uksouth / westus | ok | empty | Requested UK South alone is insufficient. |
| ama / westus / uksouth | ok | empty | Actual UK South alone is insufficient. |

Both resourceGroupMustBeAma and iotLocationMustBeUKSouth inputs and nested schemas are asserted present; each minLength must equal 1. unguarded_resources requires every deployed child to depend on iot-live-scope-guard.

All 13 mutations use deep copies and the same assertion:

* Eight parameter/schema mutations: constant-ok bypass, removed input, minLength zero and removed minLength, separately for both guard inputs.
* Three location-expression mutations: requested-region clause replaced by true(), actual/requested-location clause replaced by true(), and AND replaced by OR.
* Two child mutations: cleared guard dependencies for the consumer group and diagnostic settings separately.

The clause mutations assert that replacement changed the compiled expression. Every mutant must raise AssertionError, not an arbitrary exception; a KeyError or evaluator failure would fail the test. The independent 18-test run completed successfully, establishing rejection of the full enumerated set. Compiler-expression substrings select mutations, but behavioral evaluation supplies the acceptance oracle. Existing live SKU/unit checks and resource/output restrictions remain intact.

### User finding 2: precise operator limits and UTC cutoff

The added paragraph explicitly requires RunBudget(..., max_messages=2, max_per_second=1.0, max_seconds=60.0), required owner/cost/alert references, at most two total messages, one per second globally and 60 seconds per run. It says default100 and larger supported limits are not approval.

Before every run the operator must check UTC date/time, ensure the run fits in the remaining authorized window through 31 October 2026 UTC, stop before 2026-11-01T00:00:00Z and decline to start if insufficient time remains. It explicitly states that RunBudget does not enforce this calendar cutoff. This matches the inspected general-purpose RunBudget validation and monotonic Pacer deadline; no calendar enforcement is invented. Existing registry-permission, service-key prohibition, caller-declaration and unverified-live-transport warnings remain unchanged.

## Acceptance Criteria Assessment

| Plan criterion | Assessment | Evidence and limit |
| --- | --- | --- |
| AC1: independent compiled behavior and mutation rejection | Met | Five fixtures and 13 mutants; independently rerun 18-test suite passes without skips. |
| AC2: both minLength constraints and child dependencies | Met | Exact minLength=1 for both schemas and rejected removal/weakening; both child dependency mutants rejected. |
| AC3: explicit settings and calendar responsibility | Met | Added operator paragraph has all requested bounds and unambiguous UTC cutoff/window checks. |
| AC4: required checks pass or honest failures recorded | Met for recorded implementation scope | Targeted18, fullinfra470, API/core94 and infra/API Ruff pass recorded. Initial formatter failure retained. Only targeted18 and diff hygiene independently rerun here. |
| AC5: critique, Review, evidence and local privacy-safe commit | Partially met; lifecycle residual | One Pass critique and this one Complete Review exist with dated evidence. Local commit/identity/trailer and external gate attempt are pending parent action under P02-T02; no push is authorized. |

## Implementation-Time Plan and Detail Update Assessment

| Area | What changed and why | Triggering evidence and user decision | Reconciliation | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 and P02-T01 statuses | Bookkeeping now marks implemented and validated work complete. | Executed two-file correction and recorded checks under original owner direction. | Plan, details, changes and state agree on the source-frozen Review handoff. | Existing independent critique Complete / Pass remains applicable. | Supported status updates, not a design revision. |
| Source design and mutation strategy | Changes record reports no implementation-time design updates. | Existing evaluator handles compiled conditional createObject shape. | Actual diff matches the planned helper, fixtures, mutation set and operator paragraph. | No material revision, divergent decision or fresh planning need. | Confirmed intent preserved; no dependent work resumed against an unresolved decision. |
| P02-T02 | Deliberately remains unchecked. | Owner requires Review before local commit; Review cannot mutate plan/state. | This record distinguishes completed Review from pending parent lifecycle. | No plan correction needed. | Honest pending marker; not an implementation defect. |

## Critique and Material Revision Assessment

* Exactly one final-candidate critique records Complete / Pass and zero PC findings. There are no undispositioned critique findings.
* Its explicit mutation-rejection concern is satisfied: missing inputs/constraints produce assertion failures, and the test requires AssertionError rather than treating evaluator exceptions as success.
* No significant or divergent implementation decision was found. The two-file diff preserves unchanged Bicep/runtime behavior and requires no additional owner decision or material plan revision.
* No premature dependent-work resumption was found: P01 followed critique disposition, P02-T01 followed implementation, and local commit/gate work remains deferred.
* Historical parent artifacts and adverse outcomes were not edited or reclassified by this Review. This bounded correction cannot supersede their live/publication assessments.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Historical live and full-gate blockers | Two local test/documentation corrections neither establish deployment/transport/resident-gauge acceptance nor repair publication prerequisites. | Parent task owner retains original blocker handling and approval boundaries. | Remains distinct follow-up RV-002; not active implementation scope and not a defect in this diff. |

## Findings

No Critical, High or Medium findings and no source defects were found. The complete actionable set comprises two Low lifecycle/follow-up entries, not requests for additional implementation.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Finish the deliberately deferred local lifecycle

* Related scope: P02 / P02-T02 and AC5.
* Evidence: current plan leaves P02-T02 unchecked; details, changes and state agree that Review precedes local commit and external gate attempt. HEAD is still the specified pre-fix commit.
* Impact: the source corrections are supported, but the complete task lifecycle cannot yet be claimed complete or publication-ready.
* Owner: active RPI parent.
* Destination: distinct follow-up, P02-T02 post-Review local lifecycle; not rpi-implement, rpi-plan or rpi-research.
* Smallest useful next action: reconcile this original Review into parent-owned records, resolve privacy-safe author/committer through gh api user, commit locally with the required trailer, then perform the authorized external gate attempt under existing prerequisites and lock rules. Record actual failures honestly. This reviewer does not perform those actions.
* No second Review is required or requested. No push is authorized.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Retain inherited live and publication blockers as separate follow-up

* Related scope: plan Follow-Up Items, distinct from the present two-file corrections.
* Evidence: research residual uncertainty, plan Follow-Up Items and changes Blockers/Follow-Up Items preserve registry/live transport/resident-gauge and historical publication limitations.
* Impact: local test success and documentation corrections do not establish actual Hub/SQL transport, resident acceptance, credential authority, whole-issue delivery or hosted/publication acceptance.
* Owner: parent task 140-184 owner and the existing operational/publication approval owners.
* Destination: distinct historical parent follow-up; no new active plan scope and no source-defect route.
* Smallest useful next action: preserve the original outcomes and carry unresolved criteria forward under their existing owners; any future operational action requires its own authority. This Review authorizes no Azure, secrets, SQL, browser or push operation.

## Defects

* None within the frozen source boundary. No rpi-implement route is warranted.

## Routed Findings

| Finding | Severity | Destination | Owner / next action | Reason |
| --- | --- | --- | --- | --- |
| RV-001 | Low | Distinct P02-T02 lifecycle continuation | Active parent: evidence reconciliation, local commit and authorized external gate attempt. | Pending sequence, not a source defect. |
| RV-002 | Low | Distinct historical parent follow-up | Parent/approval owners retain original live and publication blockers. | Explicitly out-of-scope residuals, not implied acceptance. |

Later implementation of any separately routed work does not require this Review to run again.

## Residual Work

* RV-001: post-Review parent lifecycle remains incomplete; the Review itself is complete.
* RV-002: historical live/publication work remains separately owned and unresolved.

## Blockers and Remaining Work

* Review blockers: none.
* Source blockers or remaining source edits: none found.
* Remaining active plan work: parent completion of P02-T02; this Review does not alter its unchecked marker.
* Publication/live acceptance: not established. Full-gate prerequisites and inherited blockers remain separate from this source verdict.
* Review authority excluded installation, full gate, SQL/Azure/browser operations, secret access, manual rubric edits, commits and push; none was attempted.

## Validation Evidence

| Command or assessment | Scope | Status | Evidence / qualification |
| --- | --- | --- | --- |
| REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 /tmp/mv/bin/python -m unittest discover -s infra/tests -p test_iothub_module.py -q | Compiled IoT tests | Passed, independently executed | 18 tests in 9.264s, OK, no skips. Only offline az bicep build via existing helper; no Azure resource operation. |
| git diff --check | Working-tree diff | Passed, independently executed | No whitespace errors. |
| git diff HEAD --numstat; git rev-parse HEAD; two-file diff SHA-256 | Frozen boundary | Passed, independently inspected | Exactly the specified two tracked source files; HEAD unchanged; digest recorded above. |
| Manual complete diff and unchanged supporting-context comparison | Both user findings | Passed, independently performed | All fixture/mutation/constraint/dependency and operator limit/cutoff obligations assessed. |
| REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 /tmp/mv/bin/python -m unittest discover -s infra/tests -q | Full infra suite | Passed, supplied implementation evidence | Changes records 470 tests in 111.568s, no skips. Not rerun: user limited this Review to bounded offline checks. |
| /tmp/mv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_iothub_module.py | Changed infra test | Passed, supplied implementation evidence | Existing isolated policy; no new tooling. Not independently rerun. |
| /tmp/mv/bin/ruff format --isolated --line-length 100 --check infra/tests/test_iothub_module.py | Changed infra test | Passed after recorded initial failure, supplied implementation evidence | Initial one-wrap failure and formatter correction preserved, not concealed. Not independently rerun. |
| cd src/api && /tmp/mv/bin/ruff check . && /tmp/mv/bin/ruff format --check . | API project | Passed, supplied implementation evidence | 59 files already formatted. Not independently rerun. |
| From src/api: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests /tmp/mv/bin/python -m unittest test_iot_stream test_sensor_ingestion test_sensor_stream test_resident_sensors -q | Four specified API/core modules | Passed, supplied implementation evidence | 94 tests in 19.502s, no skips. Not independently rerun. |
| Complete local gate / SQL / browser / live Azure / hosted acceptance | Publication or operational scope | Skipped in this Review | Explicitly forbidden here; local commit and permitted external gate attempt belong to the parent after Review. No success inferred. |

## Outcome

* Outcome: Residual work.
* Both bounded source findings are conformantly addressed; no source defect, invalid plan assumption, unaccepted divergence or material research gap was found.
* Residual work reflects honestly pending P02-T02 local lifecycle and explicitly retained parent follow-up, not a request for further Bicep/runtime changes.
* Severity counts: Critical 0; High 0; Medium 0; Low 2, both residual/follow-up only.
* This verdict applies only to the frozen working-tree boundary. It is not a commit receipt, full-gate pass, PR approval, issue closure or operational authorization.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement handoff needed. |
| Decision gap or invalid assumption | None | No rpi-plan handoff needed. |
| Material evidence gap | None within reviewed source scope | No rpi-research handoff needed. |
| Non-blocking local lifecycle residual | RV-001, distinct P02-T02 continuation | Active parent reconciles evidence, commits locally and records authorized external gate attempt. |
| Inherited out-of-scope residual | RV-002, historical parent follow-up | Existing parent/approval owners retain live/publication blockers and original outcomes. |

* Review execution: Complete; implementation lifecycle: Partial.
* Outcome: Residual work; source corrections conformant.
* Validation coverage: independent compiled18 and diff/manual checks; supplied fullinfra470, API/core94 and Ruff evidence explicitly distinguished.
* Blockers: none to Review or these source corrections; publication/live prerequisites remain unproven.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-research.md](.copilot-tracking/research/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-research.md) | Q1-Q2 and C1-C8 evidence. |
| [.copilot-tracking/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan.md](.copilot-tracking/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan.md) | Assessed plan and acceptance criteria. |
| [.copilot-tracking/details/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-phase-details.md](.copilot-tracking/details/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-phase-details.md) | Phase obligations and observed completion. |
| [.copilot-tracking/reviews/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan-critique.md) | Preserved independent Pass critique. |
| [.copilot-tracking/changes/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-changes.md](.copilot-tracking/changes/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-changes.md) | Implementation and supplied validation evidence. |
| [.copilot-tracking/rpi-sessions/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-state.json](.copilot-tracking/rpi-sessions/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-state.json) | Source-frozen Review handoff state. |
| [infra/tests/test_iothub_module.py](infra/tests/test_iothub_module.py) | Reviewed compiled guards and rejecting mutations. |
| [src/api/README.md](src/api/README.md) | Reviewed bounded operator instructions. |
| [infra/iot-hub-live.bicep](infra/iot-hub-live.bicep) | Unchanged live guard context. |
| [infra/modules/iothub-scope-guard.bicep](infra/modules/iothub-scope-guard.bicep) | Unchanged minLength schemas. |
| [infra/tests/test_bicep_policy.py](infra/tests/test_bicep_policy.py) | Existing compiler/evaluator/dependency helpers. |
| [src/core/src/zava_forward/core/synthetic/sensor_stream.py](src/core/src/zava_forward/core/synthetic/sensor_stream.py) | Unchanged RunBudget and Pacer. |
| [src/api/src/zava_forward/api/iot_stream.py](src/api/src/zava_forward/api/iot_stream.py) | Unchanged publisher enforcement context. |
| [.copilot-tracking/reviews/logs/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-review.md](.copilot-tracking/reviews/logs/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-review.md) | This single independent Review. |

## Next Steps

The active parent may consume this original Review, reconcile its own lifecycle records and continue P02-T02 with the required privacy-safe local commit and separately authorized external gate attempt. Preserve the two residual routes and all historical outcomes. Do not push, repeat Review or infer live/publication acceptance. No user response or further implementation-stage handoff is needed for the reviewed source corrections.
