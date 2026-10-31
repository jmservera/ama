---
title: Sensor standard-deviation inclusive boundary plan critique
ms.date: 2026-10-31
---

## Metadata

* Task ID: 188-pr-587-second-correction
* Task slug: sensor-stddev-boundary-188
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/sensor-stddev-boundary-188-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/sensor-stddev-boundary-188-phase-details.md
* Original critique execution status: Complete
* Original verdict: Pass
* Execution count: One independent final-candidate assessment.

## Inputs and Criterion Boundary

* Caller requirements: second correction for PR #587, Refs #188 only, on
  feat/sensor-ingestion-consistency-188; exact inclusive stddev acceptance,
  supplied nine-sample suffix, external-package regressions, requested core
  unit/lint/format/types, pip rather than uv, local-only privacy-safe commit
  with Copilot trailer. No Azure, secrets, private data or push.
* Research: .copilot-tracking/research/2026-10-31/sensor-stddev-boundary-188-research.md,
  including C1-C6 and its alternatives, readiness and limitations.
* Named source evidence: src/core/src/zava_forward/core/synthetic/sensor_consistency.py,
  src/core/tests/test_sensor_handover.py, src/core/README.md,
  src/core/pyproject.toml and the local-gate section of src/README.md.
* Project context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory is context, not proof.
* Decisions and dependencies: one new parameterized unittest method containing
  32 subcases; no removals, generated targets or dependency changes; private
  exact Fraction/pvariance predicate with symmetric residual guard; original
  failure before production changes; requested validation before one independent
  Review and local persistence.
* Assessment boundary: credibility of the supplied local correction plan,
  not implemented correctness, executed validation, approval of the whole
  issue or authorization to publish. Full publication and live gates are
  explicitly outside this correction and remain unsatisfied.
* Read-only branch inspection confirmed feat/sensor-ingestion-consistency-188
  and existing untracked dated planning/research/session artifacts. They were
  not moved, staged, committed or edited.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Exact inclusive acceptance; C1/C4; P01-T02 | Covered | The guarded squared inequality is equivalent to the requested absolute root difference for nonnegative variances and tolerance. |
| Decimal-intent tolerance; C4; P01-T02 | Covered | Fraction conversion of Decimal readings preserves their exact values; Fraction(str(tolerance.stddev)) preserves the comparator's existing decimal-intent interpretation. |
| Actual test owner; C5; P01-T01 | Covered | HandoverTests in src/core/tests/test_sensor_handover.py already owns statistical and inclusive-boundary regressions outside the packaged src tree. |
| Supplied suffix; P01-T01 | Covered | Nine temperature readings at 18.55 twice, 21.45 twice and 20.00 five times, with a constant unchanged three-reading opposite side, fit the existing twelve contiguous rows for one home. |
| Fixture matrix; P01-T01 | Covered | Two channels times two sides times two directions times four limit cases gives exactly 32 subcases in one new method. |
| Zero tolerance and sign guard; C4; P01-T01/P01-T02 | Covered | Retained zero-tolerance tests cover equal nonzero variances; the planned unchanged constant side at positive stddev tolerance requires the negative-residual acceptance branch. |
| Side/channel isolation and no cancellation; P01-T01/P01-T02 | Covered | Independent per-side booleans combined with all preserve the existing maximum-error contract; target point/mean checks and unchanged sibling zero tolerance isolate stddev. |
| Retained report contract; C1/C2; P01-T02 | Covered | Existing pstdev diagnostic values, error subtraction, means, point/mean checks and output keys remain unchanged; README explains diagnostic-only rounded roots. |
| Requested validation; C3/C6; P01-T02 | Covered | Installed absolute pip-environment Python, core working directory, handover and sensor discovery, changed-source/test ruff checks and changed-source mypy match the bounded request. |
| Ordered evidence and local persistence; P02-T01 | Covered | Original failure, critique and independent Review are retained; explicit task staging, privacy-safe identity, Copilot trailer and Refs #188 precede a local-only commit. |
| Publication/live boundary; C6; P02/follow-up | Covered | No push, issue closure, publication receipt or live transport/calibration claim is authorized or inferred. |

## Verdict

* Verdict: Pass.
* Rationale: The plan is credible for the requested bounded implementation.
  Exact arithmetic, fixture ownership and the fixed 32-subcase matrix are
  coherent with the actual comparator and retained tests. The requested local
  validation and persistence steps are explicit, with broader gates deferred
  rather than claimed satisfied.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC findings were identified across the supplied boundary.
There is consequently no finding-specific resolving evidence or correction
owner to assign. This records the complete original finding set, not a
withheld or deferred critique pass.

## Strengths and Residual Risk

* For exact a, b and t >= 0, squaring the nonnegative absolute root difference
  gives a+b-2*sqrt(a*b) <= t*t. With r=a+b-t*t, r <= 0 accepts immediately;
  otherwise both sides of r <= 2*sqrt(a*b) are nonnegative, so squaring gives
  r*r <= 4*a*b without introducing false acceptance. Equality is inclusive.
  Variance order is immaterial.
* The nine-sample reference variance is 4*(29/20)^2/9 = 841/900 and its
  stddev is 29/30. Outward spread 1.60 has stddev 16/15; inward spread 1.30
  has stddev 13/15. Both differ from the reference by exactly 1/10.
  Changes 0.14 and 0.16 give errors 7/75 and 8/75, respectively, proving
  below-limit acceptance and just-above rejection without rounded oracles.
* The immediately smaller float tolerance is interpreted through its string,
  as before. It is strictly below 1/10, so the exact 0.15 fixture must reject.
  This tests tolerance widening independently of the 0.16 reading mutation.
* The fixture's paired negative and positive offsets sum to zero, preserving
  both means at their channel centre. Point errors stay at most 0.16, below
  the target tolerance 1; mean-step error stays zero. Temperature and humidity
  use separate tolerances; the sibling channel remains identical at zero
  tolerance. Side placement at index 3 or 9 leaves at least two samples on
  both sides and changes no cadence or metadata.
* At t=0, the inequality reduces to (a-b)^2 <= 0, accepting exactly equal
  variances. Existing clean-report coverage retains this case for nonconstant
  data. Existing constant-reference stddev regressions cover a zero variance
  against a changed variance. The planned unchanged constant side has a=b=0
  and t>0, so r<0; omitting the guard would incorrectly reject passing cases.
* Exact rational arithmetic costs more than rounded roots. The research
  explicitly accepts that bounded implementation risk and makes no live
  throughput claim. No new performance acceptance obligation is invented.
* One original post-implementation Review may identify later work. Its
  adverse evidence must remain intact; this plan Pass cannot upgrade a later
  non-passing Review or authorize publication.

## Questions or Blocking Evidence Gaps

* None within the supplied planning boundary. No user decision is required.

## Limitations

* No implementation, test execution, installation, commit, remote operation
  or nested agent was performed during this critique.
* Research arithmetic probe and environment installation are supplied prior
  evidence, not independently rerun here. The algebra above is an analytical
  assessment, not a claimed executed regression.
* Exact helper typing, source-tree installation behavior and actual tool
  outcomes remain implementation/validation responsibilities. P01 requires
  recorded checks and failure-to-success evidence before local completion.
* No fresh complete publication receipt, hosted/human approval or live
  Hub-to-Azure SQL/calibration evidence was assessed or established.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this Pass disposition, then proceed to
  P01-T01's single owned regression method and original-failure capture.
* User response required: No.
* Do not commission a second critique. Preserve this original verdict.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/sensor-stddev-boundary-188-plan.md](.copilot-tracking/plans/2026-10-31/sensor-stddev-boundary-188-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/sensor-stddev-boundary-188-phase-details.md](.copilot-tracking/details/2026-10-31/sensor-stddev-boundary-188-phase-details.md) | Assessed fixture matrix and execution details |
| [.copilot-tracking/research/2026-10-31/sensor-stddev-boundary-188-research.md](.copilot-tracking/research/2026-10-31/sensor-stddev-boundary-188-research.md) | Supplied C1-C6 research |
| [.copilot-tracking/reviews/plans/2026-10-31/sensor-stddev-boundary-188-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/sensor-stddev-boundary-188-plan-critique.md) | Original complete critique and Pass verdict |

## Next Steps

The active planning parent may finalize the critique disposition and continue
to P01-T01. No user action is required. This critic stops here; all implementation,
validation, independent Review and local commit actions remain with the parent,
and publication/live gates remain out of scope and unsatisfied.
