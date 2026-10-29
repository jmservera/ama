---
title: PR 557 IoT test contracts plan critique
description: Independent final-candidate assessment of the bounded test-only plan
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: pr557-test-contracts-2026-10-29
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/iot-pr557-test-contracts-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/iot-pr557-test-contracts-phase-details.md
* Critique execution status: Complete
* Assessment: one independent final-candidate critique; original findings below
  are preserved for parent disposition, not replacement by another critique.

## Inputs and Criterion Boundary

* Caller requirements: full RPI loop for the two named PR #557 comments;
  test-only live build-params regression and complete evaluated consumer-group
  name; no Azure service calls, push, scorecard changes or implementation here.
* Research: .copilot-tracking/research/2026-10-29/iot-pr557-test-contracts-research.md,
  including C1-C6, W1, selected alternatives and completed research disposition.
* Direct evidence: infra/tests/test_iothub_module.py:1-235 and 590-620;
  infra/tests/test_bicep_policy.py:1-170 and 590-645, plus selector lookup;
  infra/iot-hub-live.bicepparam; infra/iot-hub-live.bicep.
* Scope lock: infra/tests/test_iothub_module.py is the sole source target;
  at most three new test methods and one narrow assertion helper; no removals,
  generated targets or production changes. Dated original RPI evidence is
  separate from that source budget.
* Dependencies: existing local Azure CLI/Bicep compiler and shared evaluator;
  restore Ruff only after the reported missing-dependency failure. P01 depends
  on research and critique disposition; P02 depends on P01.
* Acceptance boundary: exact approved hub, location, SKU and units; compiled
  referenced-template comparison; wrong-hub and wrong-group rejection; IoT
  discovery, both existing main parameter selectors, touched-file Ruff and
  zero skips; original independent Review and local commit.
* Assessment covers all supplied requirements, research conclusions, decisions,
  phases, tasks, dependencies, acceptance criteria and relevant execution risks.
  It does not reassess unrelated PR comments, operational Azure safety,
  regulatory evidence or publication readiness.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller scope and change budget | Covered | One source file, no generated targets, and two proposed new methods plus one helper fit the explicit ceilings. Existing tests remain. |
| Research C1/C3, P01-T01 | Covered | Local build-params, return-code check, nested JSON parsing, whole template comparison and exact four-entry parameter map are explicit. |
| Approved live values | Covered | infra/iot-hub-live.bicepparam specifies iot-cutover-test-rzsrg, uksouth, B1 and integer 1; plan lists the same values. |
| Research C2/C4/C5/C6, P01-T02 | Covered | Existing values helper supplies fixture; evaluator supports ARM format; proposed full equality follows an existing evaluated-name convention. |
| Negative name coverage | Covered | Both wrong hub with retained suffix and wrong group use the same narrow assertion as the positive test. |
| Referenced-template decision | Covered | Comparing parsed templateJson with independently compiled self.live proves the selected compiled contract, not just a source substring. |
| P02-T01, requested validation | Covered | IoT discovery, both main parameter contracts, touched-file Ruff, zero skips and diff check are specified. BicepPolicyTests and both named methods exist. |
| Dependencies and no-cloud boundary | Covered | Commands are local compiler operations; dependency restoration is accounted for; no deployment or service validation is planned. |
| P02-T02, Review disposition | Partial | PC-001: unconditional deferral does not distinguish an acceptance-blocking finding from unrelated later work. |
| Local commit and publication limits | Covered | Privacy-safe identity resolution, original evidence and trailer are planned; no push, publication receipt or hosted approval is claimed. |

## Verdict

* Verdict: Revise
* Rationale: The implementation and validation design is credible and bounded.
  One direct planner correction is needed to ensure the single Review cannot
  expose an unmet requested contract while the workflow still declares success
  by deferring all findings. This does not require another critique.
* Severity counts: Critical 0, High 0, Medium 1, Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Gate completion on the single Review's acceptance findings

* Related IDs: P02-T02; acceptance criteria for both requested contracts and
  completion of the RPI loop.
* Evidence: .copilot-tracking/plans/2026-10-29/iot-pr557-test-contracts-plan.md:128-131
  says to route findings to later work instead of repeating Review.
  .copilot-tracking/details/2026-10-29/iot-pr557-test-contracts-phase-details.md:72-79
  likewise preserves and routes findings, then proceeds to commit and clean-state
  verification without a finding-disposition completion condition.
* Concern: The instructions apply equally to unrelated observations and a
  finding that the new regression does not actually prove one of the two named
  contracts. A single Review is an execution limit, not permission to treat
  acceptance-blocking findings as delivered work.
* Impact: Passing commands and a local commit could be reported as completion
  despite the independent Review demonstrating that the requested fix remains
  unproven. Original findings would exist, but would not control task status.
* Smallest useful change: Add the same explicit disposition rule to P02-T02 in
  plan and details: classify every Review finding against the two requested
  contracts; record unresolved in-scope acceptance failures as blocked or
  incomplete, not successful delivery. Route genuinely out-of-scope work
  separately. A local checkpoint commit may preserve evidence but does not
  establish acceptance. Preserve the one-Review limit and original findings.
* Action owner: Planning parent.
* Exact resolving evidence: Both P02-T02 descriptions explicitly require an
  acceptance-linked finding disposition and prohibit a successful completion
  claim with unresolved in-scope blockers. The eventual changes/closeout record
  must retain the original Review verdict and identify each finding's disposition,
  with blocked/incomplete status where an acceptance failure remains.
* Decision route: Direct planner correction. The user already requires complete
  delivery and a single independent Review; no significant or divergent user
  decision is necessary.

## Strengths and Residual Risk

* Exact parameter-map equality detects missing, added or changed entries,
  including the approved integer unit count, without changing production files.
* Reusing the positive assertion for both mutations prevents a disconnected
  negative test from pretending to exercise the actual full-name contract.
* Two new test methods and one helper are sufficient; no broader abstraction
  or changes to main environment loops are necessary.
* Compiled-object comparison deliberately checks semantic template identity.
  It does not independently lock the spelling of the using path when another
  source compiles identically; the supplied research and details explicitly
  select this semantic boundary.
* Fixture-based evaluation verifies resource parentage without Azure service
  access. It does not prove a live deployment or actual hub state, which the
  caller excludes.
* Publication gates remain unperformed and unclaimed. Local-only completion
  must not be presented as publication approval.

## Questions or Blocking Evidence Gaps

* No decision-critical research gap or unresolved user choice.
* PC-001 is a plan handoff correction, not an instruction to implement,
  repeat Review or widen scope.

## Limitations

* No implementation, compiler invocation, test execution, dependency restore,
  Azure operation, GitHub service lookup or commit was performed by this
  critique. Reported research probes and Ruff absence are supplied evidence,
  not independently rerun validation.
* PR comment provenance is taken from research W1 and the caller's exact scope;
  no unrelated remote research was performed.
* Existing task artifacts were present as untracked parent work on
  feat/iot-hub-live-140. They were not altered, moved, staged or committed.
* This artifact contains the complete actionable finding set from this one
  assessment. The plan, details, research, source and state remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: Planning parent.
* Smallest next action: Directly correct P02-T02 disposition in plan and details,
  preserve this original finding, and record its resolution before implementation.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/iot-pr557-test-contracts-research.md](.copilot-tracking/research/2026-10-29/iot-pr557-test-contracts-research.md) | Supplied focused research and evidence decisions |
| [.copilot-tracking/plans/2026-10-29/iot-pr557-test-contracts-plan.md](.copilot-tracking/plans/2026-10-29/iot-pr557-test-contracts-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/iot-pr557-test-contracts-phase-details.md](.copilot-tracking/details/2026-10-29/iot-pr557-test-contracts-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/reviews/plans/2026-10-29/iot-pr557-test-contracts-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/iot-pr557-test-contracts-plan-critique.md) | Original independent critique and PC-001 |

## Next Steps

The active planning parent corrects PC-001 directly and records disposition
without another critique. No user action is required. This bounded critique
stops here; implementation and all other artifact edits remain with the parent.
