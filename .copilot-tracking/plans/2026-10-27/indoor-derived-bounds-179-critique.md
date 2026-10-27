---
title: Indoor derived bounds final-candidate plan critique
description: One complete evidence-grounded critique for issue 179
ms.date: 2026-10-27
---

## Metadata

* Task ID: 179 / indoor-derived-bounds-179.
* Critique date: 2026-10-27.
* Plan: .copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-plan.md.
* Phase details: .copilot-tracking/details/2026-10-27/indoor-derived-bounds-179-phase-details.md.
* Critique execution status: Complete.
* This is the single final-candidate critique, not an implementation Review.

## Inputs and Criterion Boundary

* Caller direction selects outdoor-record and dwelling-derived bounds, exercise
  labels, tests and a fresh audit of all three #179 criteria. It also selects
  the existing branch, one PR to main, local validation only and no heavy gate
  for this bounded change. These decisions are not reopened.
* Primary research:
  .copilot-tracking/research/2026-10-27/indoor-derived-bounds-179-research.md,
  C1--C7.
* The issue body and its supplied owner comment were checked using the
  read-only GitHub issue interface. Criterion 3 literally requests physically
  plausible bounds derived from the outdoor record; the owner comment
  identifies the independent 8 C and 15..98% clips as the remaining defect.
  The caller explicitly requests assessment at the synthetic exercise boundary,
  without a calibration claim.
* Source/test evidence read: src/core/src/zava_forward/core/synthetic/indoor_projection.py,
  sensor_backfill.py, household_conditions.py and retrofit_effects.py;
  src/core/tests/test_indoor_projection.py, test_historical_backfill.py,
  test_climate_history.py and test_sensor_plausibility.py.
* Documentation evidence read: src/core/README.md, the supplied sensor research
  synthesis, both case-study documents, and the reference index and memory.
  Project test/static-check configuration was also inspected.
* Assessment covers requirements, C1--C7, both phases, all five tasks,
  dependencies, acceptance evidence and publication conditions. It does not
  establish calibrated physics, operational thresholds, resident approval,
  parent #177 acceptance or live PRD acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #179.1; FR1/FR3; C1/C5/C7; P01-T01 | Covered | Both model versions advance to v2, equations/parameters are published, and manifests/source fingerprints bind the changed behaviour. Historical snapshots are not rewritten. |
| #179.2; FR2; C4/C6; P02-T01 | Covered | Coefficients, domains and the three-sigma cap remain exercise assumptions. Physical RH saturation is distinguished from calibrated performance. |
| #179.3; FR1/FR2; C1--C4; P01-T01 | Covered | Temperature is derived per row from outdoor temperature and dwelling/household loss; RH derives from that temperature interval and outdoor/model vapour, not fixed indoor exercise clips. |
| FR3; C5; P01-T02 | Partial | Exact equations and RNG state are explicitly owned for the amended legacy reference test, but not equivalently specified for composed projection. PC-001. |
| #179.3; C3/C4; P01-T02 | Covered | Actual 17,544-hour paired ERA5 history, two literal hash pins, both generator paths, an explicit dated measure, independent envelopes, rounding tolerance and deterministic replay are required. |
| Validation/domain preservation; C1/C4/C5; P01-T01/P01-T02 | Covered | Existing guards, UTC/home matching, fault separation, domain endpoints and sensitivity are retained. The test budget permits parameterized cases without removing tests. |
| Documentation and criterion audit; C6/C7; P02-T01/P02-T02 | Covered | Related README/synthesis/index/log changes and a three-criterion audit are planned without rewriting original adverse outcomes or claiming live acceptance. |
| Ordered loop and delivery; P02-T02/P02-T03 | Covered | Local suites and static checks precede one independent Review. Closing #179 is conditional on evidence for all criteria; parent/live acceptance and human approvals remain separate. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* The model alternative is credible at the caller's synthetic exercise boundary.
  One targeted test-contract correction is needed before implementation; no
  change of model, source, scope or owner decision is recommended.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Make composed equation and Gaussian-call preservation directly testable

* Related IDs: FR1--FR3, #179.1/#179.3, C4/C5, P01-T02.
* Evidence: P01-T02 explicitly amends the existing exact-reference/RNG-state
  test in src/core/tests/test_indoor_projection.py. That existing test calls
  only project(). The same task requires independently reconstructed
  generator envelopes and composed sensitivity, but does not explicitly
  require composed exact-equation equality or composed RNG-state/call checks.
  In src/core/tests/test_historical_backfill.py,
  test_composed_fields_have_independent_effects_and_valid_domains checks
  directional inequalities with a fixed seed; the dated-effect test checks
  differences and neutrality, not the complete numeric equation or RNG state.
* Concern: Envelope containment and directional changes are weaker than the
  promised preservation of the composed equation and exactly two Gaussian
  calls. A small error in the composed moisture/ventilation calculation can
  remain inside the allowed RH envelope and preserve the tested inequalities.
  An extra discarded Gaussian call after projection can preserve the current
  row while advancing subsequent rows. Byte-repeat tests still pass for
  either deterministic defect. Sharing a helper makes these mistakes less
  likely but does not directly test the composed caller contract.
* Impact: The existing plan can produce green containment/sensitivity/replay
  evidence without directly demonstrating FR3 for both entry points. This
  weakens the claimed unchanged-equation and RNG-order regression evidence.
* Smallest useful change: Reserve one of the maximum 12 new canonical test
  methods for an independent composed numeric reference and RNG contract.
  Parameterize non-saturated cases with non-unit ventilation and an active
  loss multiplier, including a multiplier of 1 for comparison. Check both
  returned values against independently calculated B, V and capped residuals.
  Check random.Random state against a reference consuming exactly the two
  specified draws. Use a recording Gaussian stub to assert call count,
  argument order and scales in ordinary, forced-tail and RH-saturation cases,
  so saturation cannot silently skip the second draw. Keep this in the
  canonical test file; no separate suite or new dependency is needed.
* Action owner: Planning parent, followed by the implementer.
* Exact resolving evidence: Revised P01-T02 explicitly owns composed numeric
  equality and two-call/state checks, within the existing test budget.
  Implementation evidence then records passing parameterized checks in
  src/core/tests/test_indoor_projection.py for project_composed(), alongside
  the retained/amended legacy reference and RNG-state test. The expected
  calculation must not call the production projection/bound helper.
* Decision route: Direct planner correction. Existing caller direction already
  requires independent algebra and exactly two Gaussian draws; no significant
  or divergent user decision is necessary.

## Strengths and Residual Risk

* The RH envelope is algebraically valid: supported inputs give nonnegative V,
  and saturation pressure increases over the proposed indoor temperature
  interval. Its lower endpoint therefore uses B+0.9 and its upper endpoint
  uses B-0.9; clipping each endpoint to 0..100 handles saturation correctly.
* A direct arithmetic check using the largest supported fabric loss,
  1.3 * 1.3 * 1.2 = 2.028, places composed B-0.9 no lower than 1.3096 C
  and B+0.9 no higher than 38.3 C. Positive dated multipliers no greater than
  1 cannot worsen these extrema. The legacy setpoints also remain within
  these conservative limits. Removing the old floor does not force the
  existing saturation helper outside its -80..60 C input domain.
* Per-row bounds use the paired record, dwelling fabric and applicable
  schedule/household/dated inputs. The retained physical RH range is not a
  renamed 15..98% exercise clip.
* The capped Gaussian is a winsorized exercise residual, not an unbounded
  Gaussian or evidence that three sigma is a physical confidence interval.
  The candidate labels this tail policy as an exercise assumption.
* The plan distinguishes nominal output from deliberately corrupted packets,
  uses the actual public history rather than a constructed climate substitute,
  and preserves source hashes and historical acceptance outcomes.
* Actual building-physics plausibility remains uncalibrated. The eventual
  criterion audit must explicitly describe model-consistent synthetic bounds
  and must not present them as empirical validation or operational approval.
  This limitation is already accepted in the supplied candidate boundary.

## Questions or Blocking Evidence Gaps

* None requiring user input. PC-001 is a bounded planner-owned correction, not
  a request for calibration data or a new research cycle.

## Limitations

* No implementation exists in the candidate and no tests were run by this
  critique. Planned passing results, complete history traversal and v2
  provenance remain obligations for implementation and the single Review.
* No private datasets, secrets, environment files, Azure resources, deployments
  or heavyweight gates were accessed. No source, test, plan, phase-detail,
  research or existing Review artifact was changed.
* Evidence inspection stayed within the supplied model/caller/test/document
  boundary. This critique cannot establish broader physical or legal validity.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the explicit composed exact-equation and Gaussian
  call/state test obligation to P01-T02, record this critique's disposition,
  and finalize the plan without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-plan.md](.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/indoor-derived-bounds-179-phase-details.md](.copilot-tracking/details/2026-10-27/indoor-derived-bounds-179-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-27/indoor-derived-bounds-179-research.md](.copilot-tracking/research/2026-10-27/indoor-derived-bounds-179-research.md) | Primary supplied research |
| [.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-critique.md](.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-critique.md) | Complete single critique and finding set |

## Next Steps

The active planning parent should directly resolve PC-001, preserve this
Complete / Revise outcome and finalize without another critique. It may then
continue the authorized ordered RPI loop. No user action is required.
