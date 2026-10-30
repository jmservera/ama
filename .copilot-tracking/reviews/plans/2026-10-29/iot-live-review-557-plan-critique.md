---
title: PR 557 live IoT final-candidate plan critique
description: Independent bounded assessment of diagnostic target tests and one-call exercise guidance
ms.date: 2026-10-29
---

## Metadata

* Task ID: pr-557-review-corrections
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/iot-live-review-557-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/iot-live-review-557-phase-details.md
* Critique execution status: Complete
* Assessment count: one independent final-candidate critique; no delegated agents.
* Source HEAD: 27f7b2d0c6b3b13a59dbb886379a5b615566d394
* Lifecycle observed: feat/iot-hub-live-140 tracks origin/feat/iot-hub-live-140;
  PR #557 is OPEN against main. Existing untracked planning/state artifacts
  were left untouched.

## Inputs and Criterion Boundary

* Caller requirements: correct both supplied Copilot findings, preserve all
  existing tests, add at most one helper and two tests, move category checks
  into that helper, and change only the test module and bounded README guidance.
  No generated targets, runtime/Bicep changes, push, Azure operations or rubric
  score edits are authorized. The implementation and evidence must be committed
  locally after requested validation and independent Review.
* Research: .copilot-tracking/research/2026-10-29/iot-live-review-557-research.md,
  C1-C5, including reported successful pull/rebase, baseline 18 tests without
  skips, missing Ruff and inherited publication-gate failure.
* Direct source evidence: infra/iot-hub-live.bicep:1-48;
  infra/tests/test_iothub_module.py:31-84,488-525;
  infra/tests/test_bicep_policy.py:79-119;
  src/api/src/zava_forward/api/iot_stream.py:340-395;
  src/api/README.md:898-995; src/README.md:61-75,150-157,195-214.
* Repository context: original case study, addendum, knowledge-base index,
  owner memory and sector primer were read for orientation. No new regulatory
  claim, operational authority or company fact is inferred.
* Boundary: assess acceptance completeness, isolated mutation credibility,
  documentation consistency, scope limits, validation and local lifecycle.
  This is not implementation Review, test execution, deployment validation,
  publication eligibility or live acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1; C1-C3; P01-T01 | Covered | Details pin exactly one live diagnostic setting and both complete compiled resourceId expressions. Hub-name allowedValues already fixes the intended hub. |
| AC2; C2-C3; P01-T01 | Covered | Independent deepcopies change scope alone and workspaceId alone. Both subtests must raise AssertionError through the same helper used by the positive compiled-fixture test. |
| Test ownership and change cap; P01-T01 | Covered | One helper plus positive/mutation methods, no removals, and relocation of the existing live category checks preserve ownership without duplicate assertions or new fixtures. |
| AC3; C4-C5; P01-T02 | Covered | Both contradictory paragraphs are named. One total call includes new instances/processes and concurrent/repeated invocation; uncertain delivery requires stop, retained truth and separately approved reconciled accounting before another send. |
| Retained bounded controls; P01-T02 | Covered | Two messages, 1/s, 60s, UTC cutoff, owner/cost/alert references and distinct receiver/SQL replay semantics remain mandatory. |
| AC4; P02-T01 | Covered | Exact infra discovery selector, no skips, expected 20 tests, touched-file Ruff check/format --check and recorded actual commands/results are specified. |
| AC5; P02-T02 | Covered | Original independent critique and Review are preserved; local privacy-safe identity and Copilot trailer are specified. No push, Azure or score edits. |
| Dependencies and gate; P02-T02 | Covered | Missing tooling restoration, fresh external post-commit gate evidence and nonqueued admission are explicit; missing prerequisites or foreign ownership remain blocked rather than bypassed. |
| Decisions, risks and non-goals | Covered | Docs-only operator restriction is deliberate, not cumulative runtime enforcement. Inherited live and publication blockers remain separate and unaccepted. |

## Verdict

* Verdict: Pass
* Rationale: the candidate specifies a credible, surgical correction for both
  findings. Full-expression assertions close the target-coverage gap, isolated
  mutations prove each guard independently, and both conflicting README
  passages are addressed without changing transport behavior or approval scope.
  No substantive plan revision or unresolved user choice was identified.

## Findings

No actionable findings. Severity counts: Critical 0, High 0, Medium 0, Low 0.
No PC IDs are assigned because there is no correction to disposition.

## Strengths and Residual Risk

* Exact scope must remain
  `[resourceId('Microsoft.Devices/IotHubs', parameters('name'))]`; exact workspace
  must remain
  `[resourceId('Microsoft.OperationalInsights/workspaces', 'log-cutover-test')]`.
  Substring checks would not implement the accepted plan.
* Production diagnostic helper/mutations supply an established local pattern.
  Each changed-target fixture must retain the other target and category values,
  so unrelated malformed input cannot provide the expected rejection.
* The README restriction is explicitly operator-controlled. Publisher pacing
  is constructed per call and does not establish an exercise-wide ledger.
  The plan accepts that bounded limitation rather than implying runtime
  enforcement or authorizing another exercise.
* Local `az bicep build --stdout` compilation is the existing offline test
  mechanism, not permission for Azure resource operations.
* A blocked complete gate does not invalidate independently passing focused
  checks or prohibit the requested local commit. It also must not be reported
  as a passing gate or publication permission. Source/base/tool/dirty-input
  changes invalidate exact-candidate gate evidence under repository policy.
* The original implementation Review must retain its actual outcome. Any
  unresolved finding or unmet acceptance criterion must remain explicit rather
  than being described as delivered merely because a local commit exists.

## Questions or Blocking Evidence Gaps

None for this plan assessment. No user response is required.

## Limitations

* Research-reported baseline tests, missing Ruff and prior gate failure were
  assessed as supplied evidence, not freshly reproduced.
* No tests, formatter, gate, publisher, receiver or Azure operation were run.
  Implementation must still demonstrate the requested checks without skips.
* Only this critique artifact was written. Plan, details, research, source and
  existing evidence were not edited; nothing was committed or pushed by this
  critique worker.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record this Pass disposition, then implement P01 within
  the locked helper/test cap and execute P02.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/iot-live-review-557-plan.md](.copilot-tracking/plans/2026-10-29/iot-live-review-557-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-29/iot-live-review-557-phase-details.md](.copilot-tracking/details/2026-10-29/iot-live-review-557-phase-details.md) | Assessed implementation and lifecycle details |
| [.copilot-tracking/research/2026-10-29/iot-live-review-557-research.md](.copilot-tracking/research/2026-10-29/iot-live-review-557-research.md) | Supplied C1-C5 evidence |
| [.copilot-tracking/reviews/plans/2026-10-29/iot-live-review-557-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/iot-live-review-557-plan-critique.md) | This original independent critique |

## Next Steps

The active planning parent may disposition this Pass and continue to
implementation, requested validation, one original independent Review and a
local commit. No user action is required. No second critique, push, Azure
operation or publication authorization follows from this verdict.
