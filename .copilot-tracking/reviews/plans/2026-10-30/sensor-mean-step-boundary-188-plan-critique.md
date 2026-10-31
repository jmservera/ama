---
title: Sensor mean-step boundary correction plan critique
description: Single independent original final-candidate critique for PR 587, Refs 188
ms.date: 2026-10-30
---

## Metadata

* Task ID: 188-pr587-mean-step-boundary
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/sensor-mean-step-boundary-188-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/sensor-mean-step-boundary-188-phase-details.md
* Critique execution status: Complete
* Assessment: exactly one independent final-candidate plan critique; original verdict preserved below.

## Inputs and Criterion Boundary

* Caller requirements: ordered Research, Plan, Implement and Review; exact reference-adjusted cross-multiplication before division; the three-prefix recurring-mean reproducer; external regression ownership; pip-only/src-only execution; sensor tests and full-core lint/format/type checks under the requested 600-second heavy lock; unchanged branch/base; local commit with Copilot trailer; no push, Azure, secrets or private datasets.
* Research: .copilot-tracking/research/2026-10-30/sensor-mean-step-boundary-188-research.md, Q1-Q3 and C1-C6.
* Named source evidence: src/core/src/zava_forward/core/synthetic/sensor_consistency.py and src/core/src/zava_forward/core/sensor_consumer.py.
* Named test/configuration/documentation evidence: src/core/tests/test_sensor_handover.py, src/core/tests/test_resident_sensors.py, src/core/pyproject.toml, src/core/README.md, src/README.md and .github/copilot-instructions.md.
* Repository context: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory was context, not evidence.
* Decisions and dependencies: P01 follows completed Research and critique disposition; P01-T02 follows regression and arithmetic correction; P02 follows validation and artifact reconciliation, then independent original Review and local commit.
* Locked inventory: existing src/core/tests/test_sensor_handover.py owns the regression; at most one new parameterized unittest method; no removals. Production targets are sensor_consistency.py and the directly related core README. No generated targets or dependency/configuration changes.
* Boundary: assess planning credibility and source-level arithmetic/test/configuration fidelity, not implementation correctness already demonstrated, physical sensor accuracy, actual transport/SQL acceptance, whole #188 completion or publication readiness.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1: recurring-mean defect | Covered | Current report subtracts independently divided means; nonconstant suffix reference distinguishes the requested example from existing constant-reference tests. |
| Q2, C3, functional formula | Covered | Opposite-side counts correctly scale both reference-adjusted sums; the inclusive limit uses the same count product before division. |
| P01-T01: required reproducer | Covered | Details specify one home, contiguous slots, fourth-slot handover and three samples on each side, with the required 10.00 prefix and 9.99/10.00/10.00 reference suffix. |
| P01-T01: signs, channels and unequal counts | Covered | Two prefix counts, two channels, two signs and three deltas yield 24 subcases in one method; the shared 0.02 offset in the unequal-count variant exercises subtraction of the prefix reference. |
| P01-T01: isolation and assertions | Covered | Target-channel point/stddev limits are 1.0; the other channel remains unchanged with zero tolerance. Mean-step checks, aggregate result and error magnitude are required assertions. |
| C2, P01-T02: typing/configuration fidelity | Covered | Python >=3.12; dev extra pins ruff 0.17.1 and mypy 2.4.0. Full-core commands retain existing strict configuration and exclusions rather than weakening them. |
| P01-T02: requested test surface | Covered | Details combine test_sensor_*.py and test_resident_sensors.py through unittest discovery in one runner without duplicate suites. |
| P01-T02: environment and lock | Covered | Research records a missing-package failure; isolated pip installation, absolute environment binaries, core working directory and flock -w 600 are specified. |
| P02-T01: ordered Review and persistence | Covered | One independent original Review follows implementation validation, retains its original outcome, and precedes explicit-path local commit with privacy-safe identity and requested trailer. |
| C5-C6, scope and evidence boundaries | Covered | No push, Azure, private-data access or whole-issue closure; focused checks are explicitly not the later complete publication receipt or live acceptance. |

## Verdict

* Original verdict: Pass
* Rationale: the bounded candidate directly fixes the divided-mean cancellation defect, has count-sensitive external regression coverage, preserves the report/statistics contract, and specifies the requested component validation and local-only evidence boundary. No substantive plan correction or unresolved user decision is supported by the supplied evidence.

## Findings

No actionable PC-xxx findings.

Severity counts: Critical 0; High 0; Medium 0; Low 0.
The actionable finding set is complete for the supplied boundary; no additional
discoverable findings are withheld for another critique.

## Strengths and Residual Risk

* Let B and A be before/after counts, and D_before and D_after be actual-minus-reference sums. The planned numerator abs(D_after * B - D_before * A) divided by B * A is algebraically the reference-adjusted mean-step magnitude. Comparing that numerator to Decimal(str(limit)) * B * A preserves inclusivity without recurring division in the decision.
* In the required positive boundary example, D_before=0.00, D_after=0.30 and B=A=3. The numerator is 0.90, the scaled 0.1 limit is 0.9, and the reported magnitude is 0.10. Negative shifts produce the same absolute magnitude.
* With B=2, A=3 and a common 0.02 offset, D_before=0.04 and D_after=0.06 plus the signed step times 3. At either signed 0.10 step the numerator is 0.60, exactly the scaled limit 0.6. Below/above steps give 0.54/0.66. This variant detects omitting prefix-reference subtraction or assuming equal counts.
* The fixture must follow the details' local window handover, not reuse the module's existing HANDOVER blindly: that constant splits the full replay into six/six samples. The supplied details already select the fourth slot for three/three and a second two/three prefix-count variant; there is no missing planning decision.
* Decimal-derived two-decimal strings stay within the observation shape contract. A constant offset within each side leaves population standard deviation unchanged; generous target-channel limits avoid masking the mean-step result. Unchanged sibling-channel observations/reference preserve all zero-tolerance checks.
* Existing test style uses unittest subTest and narrows the object-valued report's series to a list before indexing nested metrics. The candidate is compatible with that style and existing strict mypy settings without introducing packaged tests or configuration relaxations.
* Existing report keys and divided means/stddev remain unchanged. Only mean_step_error is derived from the decision numerator; its float representation remains a report metric, not the threshold oracle.
* Default Decimal context, admitted small fixed-point values and finite constructed windows are the supplied boundary. Arbitrary ambient context mutation is explicitly not a new supported contract.
* The plan explicitly accepts that focused arithmetic evidence cannot establish live transport, physical calibration, whole #188 acceptance or publication eligibility. Complete publication gating, hosted checks and human approval remain separate.

## Questions or Blocking Evidence Gaps

None for this bounded planning assessment. No significant or divergent user
decision is required.

## Limitations

* No implementation, tests, installs, heavy-lock operation, Azure operation, commit, push or nested agent was executed.
* Research's recorded arithmetic/oracle results and missing-package failure were reviewed as supplied evidence; their raw execution logs were not supplied or independently rerun. The source and algebra support the planning decision, while implementation must retain actual red-to-green and validation evidence.
* Read-only status inspection confirmed feat/sensor-ingestion-consistency-188 and existing untracked parent tracking artifacts. No branch/base change was made, and historical PR/base verification was not repeated remotely.
* Only this critique artifact was written; all supplied plan/details/research and existing work remained untouched.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record the Pass disposition and advance to P01-T01, adding the owned regression and capturing its original failure before production edits.
* User response required: no.
* Do not repeat this critique; retain this original verdict and route any later implementation/Review findings through their owning phase.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/sensor-mean-step-boundary-188-plan.md](.copilot-tracking/plans/2026-10-30/sensor-mean-step-boundary-188-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/sensor-mean-step-boundary-188-phase-details.md](.copilot-tracking/details/2026-10-30/sensor-mean-step-boundary-188-phase-details.md) | Assessed bounded execution details |
| [.copilot-tracking/research/2026-10-30/sensor-mean-step-boundary-188-research.md](.copilot-tracking/research/2026-10-30/sensor-mean-step-boundary-188-research.md) | Supplied arithmetic and contract research |
| [.copilot-tracking/reviews/plans/2026-10-30/sensor-mean-step-boundary-188-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/sensor-mean-step-boundary-188-plan-critique.md) | Complete single original critique |

## Next Steps

The active planning parent records this Pass and proceeds through the ordered
implementation, validation and independent original Review phases. No user
action is required. This critique execution stops here without invoking a peer
stage or repeating the assessment.
