---
title: IoT Hub PR 557 fix cycle 1 plan critique
ms.date: 2026-10-29
---

## Metadata

* Task ID: 140-184-pr557-fix-cycle-1
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Assess the two bounded PR #557 corrections for issues #140/#184: compiled live resource-group/requested-location/actual-location behavior, minLength and bypass mutation coverage; API operator guidance for max_messages=2, max_per_second=1.0, max_seconds=60.0 and the October 31 UTC authorization cutoff.
* Research considered: .copilot-tracking/research/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-research.md, Q1-Q2 and C1-C8.
* Source evidence inspected: infra/iot-hub-live.bicep; infra/modules/iothub-scope-guard.bicep; infra/tests/test_iothub_module.py; infra/tests/test_bicep_policy.py; src/api/README.md; RunBudget/Pacer in src/core/src/zava_forward/core/synthetic/sensor_stream.py; HubPublisher.run in src/api/src/zava_forward/api/iot_stream.py.
* Lifecycle evidence considered: src/README.md local gate guidance and the bounded-operation/critique dispositions in .copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md. Repository case-study and reference context was consulted; original historical artifacts remain unchanged.
* Dependencies and acceptance criteria: P01 follows completed research and critique disposition; P01-T01 and P01-T02 are independent; P02 follows both. Acceptance criteria 1-5 cover test behavior, constraints/dependencies, documentation, recorded checks, one Review and a local privacy-safe commit with the required trailer.
* Confirmed direction remains controlling: use the requested /tmp/mv tools during the parent implementation cycle, no Azure operations, secrets, Bicep/runtime changes, rubric edits or push. This critique runs none of those tools or operations.
* Boundary: assess implementation readiness, not implemented behavior, live authority, whole-issue delivery, hosted approval or gate success. Only infra/tests/test_iothub_module.py and src/api/README.md are source targets.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1-C2/C4, P01-T01, AC1 | Covered | Five fixtures independently vary group, requested region and actual Hub region. Matching non-UK regions defeat an equality-only bypass; both asymmetric cases defeat single-clause removal and AND-to-OR. Per-guard expectations avoid masking a wrong group result behind location rejection. |
| P01-T01, AC1-2 | Covered | One reusable assertion checks compiled input/schema presence, both minLength=1 constraints and all child dependencies. Deep-copy mutations cover constant success, removed inputs, zero/missing constraints, both location clauses, conjunction replacement and each child dependency. |
| Q2, C3/C5-C8, P01-T02, AC3 | Covered | Exact 2/1/60 settings, owner/cost/alert references, rejection of permissive defaults as approval, pre-run UTC/window checks and stop before 2026-11-01T00:00:00Z distinguish operator authorization from runtime enforcement. |
| P01 scope and non-functional requirements | Covered | Existing evaluator/context/dependency helpers support the design without production changes, new dependencies or Azure access. Two test methods and one helper are credible for table-driven cases and mutations. |
| P02-T01, AC4 | Covered | Required compiler mode prevents missing Azure CLI/Bicep from becoming accepted skipped coverage. Focused/full infra, scoped Ruff policies and four named API unit modules are specified with recorded real outcomes. |
| P02-T02, AC5 | Covered | One independent Review precedes local commit; identity/trailer, immutable adverse evidence, fetched-main full-gate attempt, nonqueued lock admission and no push are explicit. Blocked gate evidence cannot become publication acceptance. |
| Decisions, dependencies, risks and missed concerns | Covered | No unresolved implementation decision was found. Historical live/publication blockers remain outside this correction's acceptance and are not silently closed. |

## Verdict

* Verdict: Pass
* Rationale: The candidate translates both supplied findings into executable, independently falsifiable test obligations and precise operator documentation. Source inspection supports the selected helpers and confirms that no Bicep or runtime change is needed.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

The complete actionable PC-xxx finding set is empty. No evidence-backed substantive plan correction or significant/divergent user decision is required. No additional finding is withheld for a later critique.

## Strengths and Residual Risk

* The supplied live template already requires ama, requested uksouth and actual location matching the request. The plan tests those semantics rather than relying on source substrings.
* Mutation acceptance explicitly requires AssertionError from the shared assertion. Implementation must preserve that contract for missing minLength as well as missing inputs; a KeyError or evaluator exception is not successful mutation rejection.
* RunBudget permits larger general-purpose limits and Pacer uses a monotonic deadline. The proposed operator guidance correctly supplies exercise-specific limits without claiming a built-in calendar control.
* The parent explicitly preserves unresolved registry, live transport and publication blockers. Local tests and a local commit do not remove them.

## Questions or Blocking Evidence Gaps

* None for this planning boundary. No user response is required.

## Limitations

* No implementation, compilation, tests, Azure operations, full gate, independent implementation Review or commit was performed by this critique.
* Assessment uses the supplied candidate and evidence pointers; PR comments were represented by the supplied context/research, not independently fetched.
* At inspection, the active branch was feat/iot-hub-live-140. The three supplied candidate artifacts and matching state file were untracked. They were treated as parent-owned inputs, not moved or edited.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this Pass disposition, then implement P01 within the two source targets and continue the authorized validation/Review/local-commit sequence.
* Decision route: Direct parent continuation; no significant or divergent user decision.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan.md](.copilot-tracking/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-phase-details.md](.copilot-tracking/details/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-research.md](.copilot-tracking/research/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-research.md) | Supplied evidence |
| [.copilot-tracking/reviews/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan-critique.md) | This single independent critique |

## Next Steps

The active planning parent may disposition this Pass and continue P01 without another critique. No user action is required. This critique stops here; it does not implement, review implementation, commit or push.
