---
title: "RPI Plan Critique: sensor-scenarios-190"
description: Independent final-candidate assessment and complete actionable finding set for task 190
ms.date: 2026-10-27
---

## Metadata

* Task ID: 190
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md
* Research: .copilot-tracking/research/2026-10-27/sensor-scenarios-190-research.md
* Critique execution status: Complete
* Execution boundary: Exactly one independent final-candidate assessment; no nested agents.
* Original verdict: Revise

## Inputs and Criterion Boundary

* Caller requirements: ordered Research, Plan, Implement and independent Review;
  one eventual branch PR to main for #190/#192/#193/#194; truthful criterion-level
  evidence; no full gate, Azure, private data, secrets or uv. This worker is
  authorized only to write this critique and then stop.
* Supplied plan, details and research were read completely. Supporting evidence
  read: src/core/src/zava_forward/core/synthetic/sensor_backfill.py,
  src/core/src/zava_forward/core/synthetic/sensor_faults.py,
  src/core/src/zava_forward/core/synthetic/provenance.py,
  src/core/src/zava_forward/core/synthetic/__init__.py,
  src/core/src/zava_forward/core/synthetic/sensor_identity.py,
  src/core/tests/test_sensor_plausibility.py, the offline sensor contract in
  src/core/README.md, the R2/R3 table and constraints in
  docs/reference/research/iot-sensor-analytics-research-plan.md, and
  docs/reference/research/climate-paired-source-178/open-meteo-era5-durham-2023-2024-metadata.json.
* Repository context read: docs/case_study_48_original.md and opening context of
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory was not treated as evidence.
* Named issue evidence: read-only GitHub issue bodies for #190, #192, #193 and
  #194 on 2026-10-27. Their acceptance criteria agree with research W1-W4.
* Dependencies and decisions assessed: reuse clean backfill, seven damp cases,
  four paired retrofit profiles, separated truth, exercise-only evaluator,
  local validation and honest unmet downstream/live acceptance.
* Assessment is of implementation credibility, not implementation acceptance,
  scientific validation, approved operational thresholds or publication approval.
  No tests, installation, gate, deployment or downstream-consumer execution was
  performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #192; C2/C3; P01-T01 | Partial | Appropriate reuse and seven named cases; observation seed conflicts with truth-only requirement, PC-001. |
| #192; C6; P01-T01/P02-T01 | Partial | Sufficiency and sensitivity are explicit, but temporal eligibility and confusion accounting need executable definitions, PC-002/003. |
| #193; C4/C5; P01-T01 | Covered | Four explicit exercise deltas, completion day 14, delayed day 21, paired weekly baseline/no-change and serialization tolerance; no physical or causal acceptance claimed. |
| #193 actual #111/#133 test use | Unmet, correctly retained | Plan expressly does not substitute standalone fixture tests for actual consumer use. |
| #194; C10/C12; P02-T01 | Covered with residual dependency | Existing README/dictionary, both-stage distinction and exact climate caveats planned; runnable live #184 remains unavailable. |
| Shared schema, reproducibility and safe output; C3/C9 | Partial | Seed contradiction, incomplete output rejection coverage and underspecified reproducibility metadata, PC-001/006/007. |
| P02-T01 test ownership | Partial | Details meet one-file/24-method boundary; plan authorizes two files, PC-005. No removals are planned. |
| P03-T01 local validation | Partial | Appropriate scoped tests/lint/types and independent Review; forbidden scratch path, PC-004. |
| #190 child disposition and publication | Covered as a boundary, not fulfilled | Per-check results and Refs required; remaining child criteria, human/hosted approval and actual PR delivery are not proven by a plan. |

## Verdict

* Verdict: Revise
* Severity summary: 4 High, 3 Medium, 0 Low, 0 Critical.
* Rationale: The bounded scenario approach is credible, but the seed contract
  cannot currently satisfy its own truth-separation promise. Temporal
  sufficiency and confusion eligibility need precise rules to avoid misleading
  evidence. The scratch path violates an explicit execution restriction, and
  test ownership must be reconciled before implementation.
* This is the original assessment. All actionable findings available within the
  supplied boundary are recorded below; no second critique is requested.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The shared observation seed contradicts truth-only seeds

* Related IDs: #192 truth separation; C3; P01-T01; plan functional/non-functional requirements.
* Evidence: .copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md:54-69
  requires seeds in truth only and the shared 13-field contract.
  src/core/src/zava_forward/core/synthetic/sensor_faults.py:27-41 includes
  `seed`; its `observation()` at lines 116-124 copies the original seed.
  .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md:27-29
  selects distinct reproducible seeds.
* Concern: Directly normalizing each seeded backfill exposes the actual
  per-case generator seed in analysis. Removing the field instead breaks the
  promised shared schema. Distinct case-linked seeds also create an avoidable
  shortcut into evaluator metadata.
* Impact: An implementation could pass a field-list check while violating the
  central separation requirement, or deliver an incompatible observation shape.
* Smallest useful change: Distinguish the actual generator seed from the required
  observation field. Preserve all 13 fields, use a documented common neutral
  observation seed value across cases, keep actual per-case seeds and mappings
  in truth, and prohibit the comparator from consulting seed/identity as labels.
  Reconcile the truth-only wording accordingly.
* Action owner: Planning parent; implementation owner executes the clarified contract.
* Exact resolving evidence: Matching plan/details definitions; one-file tests
  demonstrating exact shared fields, one common observation seed, actual seeds
  only in truth, and unchanged comparator predictions when allowed neutral
  identity/seed values or truth labels are changed without altering readings.
* Decision route: Directly actionable planner correction; no significant or divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Coverage and continuity rules leave unsafe temporal classifications open

* Related IDs: #192; #193; C6; P01-T01/P02-T01.
* Evidence: .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md:33-37
  requires both contiguous expected timestamps and >=90% coverage, then
  consecutive-hour and repeated-night classification. Lines 40-44 require
  three weekly comparison means. The research-plan constraints explicitly make
  missing/stale/invalid data INSUFFICIENT.
* Concern: It is unclear whether any missing slot invalidates a case or whether
  up to 10% missing slots are allowed. A high overall coverage ratio can hide a
  concentrated gap in an overnight or retrofit comparison window. Neither the
  overnight UTC interval/night assignment nor treatment of a gap within an RH
  run is defined. Seven-day deltas could be computed from an inadequate week
  despite acceptable full-pack coverage.
* Impact: Missing periods can become reassuring negatives, artificial
  consecutive runs, misleading overnight counts or biased before/after means.
* Smallest useful change: Define the expected half-open hourly grid and separate
  uniqueness/order/on-grid validation from allowed missingness. State the
  sufficient-data rule per evaluated window, gap-breaking run semantics,
  overnight UTC hours/night grouping and the exact baseline/early/late ranges.
  Make inadequate windows produce INSUFFICIENT with visible reasons, not a
  negative or numeric success. Keep all values exercise-only.
* Action owner: Planning parent.
* Exact resolving evidence: Reconciled temporal rules in details, then tests
  with equal total missing counts distributed differently, a gap inside a
  12-hour run, midnight/night boundaries, and a deficient retrofit week despite
  >=90% overall coverage. Report expected/present/valid counts for each window.
* Decision route: Directly actionable planner correction; exercise definitions do not require a new operational-policy decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Confusion denominators are named but not independently defined

* Related IDs: #190 per-check reporting; #192 R3 confusion support; C6; P01-T01/P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md:59-61
  and .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md:48-51
  promise confusion cells and eligible/excluded denominators without defining
  their population or classification rules. Details lines 31-33 mix binary
  target outcomes and two insufficient targets; four retrofit cases are also
  present in the same 11-case pack.
* Concern: A report could count observation rows as independent trials, fold
  insufficient cases into true negatives, mix retrofit and damp populations,
  or silently exclude an unexpected INSUFFICIENT prediction. Recomputing truth
  from each threshold's predictions would manufacture perfect sensitivity
  results. Generic mutation coverage does not settle these accounting choices.
* Impact: Numerically reproducible output would not necessarily provide genuine
  detection, miss, false-alert or sufficiency evidence for #192/R3.
* Smallest useful change: Specify case-level damp trials separately from
  retrofit delta checks, fixed evaluator-owned expected labels, TP/TN/FP/FN
  definitions and denominator formulas. Account independently for expected
  insufficient cases and unexpected insufficiency on otherwise evaluable
  truth; publish all population reconciliations and null/not-computable rates
  for zero denominators. Rerun observations-only classification at 70/75/85
  against the same truth, not threshold-generated answers.
* Action owner: Planning parent.
* Exact resolving evidence: A report contract with reconciled total, eligible,
  binary-classified and excluded/abstained counts; tests inject a false alert,
  miss, wrong sufficiency outcome and zero-denominator subset and assert exact
  changed cells/rates. At the intended default, explicitly account for all
  seven damp cases, including the two expected insufficient cases, and keep all
  four retrofit cases out of that binary confusion population. State that these
  hand-designed cases do not estimate operational prevalence or approved limits.
* Decision route: Directly actionable planner correction; no user decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: The proposed validation environment uses a forbidden scratch path

* Related IDs: P03-T01; caller execution restrictions; research residual installation gap.
* Evidence: .copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md:135
  directs installation under `/tmp/ama-syn190-venv`. Supplied research also
  mentions a `/tmp` lock. Current execution instructions prohibit file
  operations in `/tmp`, `/var/tmp` or temporary directories.
* Concern: Following the canonical validation task violates the execution
  boundary before tests can run. Test helpers and subprocess defaults may also
  create forbidden temporary files unless an allowed strategy is explicit.
* Impact: Planned validation is not runnable as written; an attempted shortcut
  would breach restrictions rather than provide valid evidence.
* Smallest useful change: Replace the proposed environment with a named,
  persistent, permitted project-relative validation location or an already
  installed permitted environment. Define an explicit non-temporary output
  strategy compatible with external snapshot safety, and constrain any
  filesystem test helpers/subprocess scratch accordingly. Do not execute the
  historical lock suggestion or add a gate to this bounded task.
* Action owner: Planning parent.
* Exact resolving evidence: Corrected plan/details validation instructions,
  explicit permitted paths, and subsequent command records showing pip/local
  tests use those paths without forbidden scratch writes. Preserve original
  research as dated evidence; supersede its path advice in the active plan.
* Decision route: Directly actionable planner correction; no user decision required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: The plan permits twice the authorized new test-file count

* Related IDs: P02-T01; caller test-ownership boundary.
* Evidence: .copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md:118-120
  permits two new files. Details at
  .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md:64
  and the caller authorize one new core test file, at most 24 test methods.
* Concern: The summary and executable details provide conflicting ownership
  limits; the looser summary can authorize unnecessary test proliferation.
* Impact: Implementation could violate an explicit caller constraint despite
  following one canonical planning artifact.
* Smallest useful change: Set both artifacts to exactly one new test file,
  src/core/tests/test_sensor_scenarios.py, at most 24 test methods, zero test
  removals. Keep existing suites owned by their current files.
* Action owner: Planning parent.
* Exact resolving evidence: Reconciled plan/details limits and implementation
  diff/test inventory proving one new test file, <=24 new methods and no removed
  tests. Parameterized subcases can cover the required semantic cases.
* Decision route: Directly actionable planner correction; no user decision required.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Existing snapshot helpers do not establish external-path safety

* Related IDs: P01-T01/P02-T01; C9; external output non-functional requirement.
* Evidence: .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md:25-27,51
  proposes provenance helpers and outside-repositories/nonsymlink output.
  src/core/src/zava_forward/core/synthetic/provenance.py:33-41 checks only the
  destination's own symlink status and emptiness; it neither rejects symlinked
  ancestors nor detects repository roots.
* Concern: Helper reuse alone cannot enforce the promised boundary. A
  non-symlink leaf reached through a symlink ancestor can resolve inside a
  repository, and an empty destination in another worktree is still repository
  output. The generic safe-output test promise does not enumerate these cases.
* Impact: Generated fixtures could be written into tracked working areas or an
  unintended location while the leaf-directory check succeeds.
* Smallest useful change: Specify pre-write path validation for resolved
  destinations and existing ancestors, ordinary repositories and `.git`-file
  worktrees, existing files and nonempty directories. Do not infer safety from
  the current helper. Reject unsupported destinations before creating output.
* Action owner: Planning parent; implementation owner adds module-local enforcement without altering default backfill behavior.
* Exact resolving evidence: Explicit rejection contract and bounded tests for
  symlink leaf/ancestor, repository/worktree destinations, existing file and
  nonempty directory, plus successful permitted external output. Assert rejected
  requests leave existing contents unchanged and create no snapshot payload.
* Decision route: Directly actionable planner correction; no user decision required.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Reproducibility provenance does not yet identify the generating contract

* Related IDs: #194 schema/provenance; C9/C10; P01-T01/P02-T01.
* Evidence: .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md:47-52
  promises input hashes and truth parameters; lines 70-73 promise documented
  fields. The selected provenance helper also provides `source_revision()`,
  but the candidate does not require recording the scenario/evaluator revision,
  transitive source fingerprint, runtime, exact observation windows or payload
  inventory. No concrete manifest contract is supplied.
* Concern: Hashing observations proves which bytes were evaluated, not which
  generator, seed interpretation, thresholds or runtime produced them. The
  selected explicit synthetic weather must not inherit a misleading claim
  that these particular scenario rows were generated from the ERA5 packet.
* Impact: Future users cannot reliably reproduce or compare snapshots, and
  documentation could blur synthetic scenario climate with the separately
  sourced/limited-approved climate-backed mode.
* Smallest useful change: Define a minimal versioned truth-side manifest and
  report schema before implementation: generator/comparator versions, complete
  relevant source fingerprint, runtime, actual generation seeds/parameters,
  UTC window/cadence, synthetic-weather identity, case inventory and relative
  payload hashes. Bind report results to observations and the evaluated rule
  configuration. Keep label-bearing metadata outside analysis and avoid
  absolute paths or wall-clock fields in byte-identical payloads.
* Action owner: Planning parent.
* Exact resolving evidence: Documented field/type/units/status definitions in
  the planned dictionary update; tests showing byte-identical same-input
  snapshots, changed payload/configuration identity when inputs change, and
  accurate synthetic-weather provenance distinct from the existing ERA5
  retrieval/licence/limited-approval documentation.
* Decision route: Directly actionable planner correction; no user decision required.

## Strengths and Residual Risk

* Clean `sensor_backfill.readings()` plus observation normalization avoids
  modifying legacy seeded output. Disabling implicit faults is explicitly
  planned rather than assumed.
* The retrofit profiles are transparently fictional overlays, not a claim that
  the beneficial-only loss model represents adverse effects. Paired weekly
  noise/cycles, a no-change counterfactual and delayed activation are appropriate
  construction controls; executing them still needs the planned boundary tests.
* A condensation-prone label is evaluator truth for an exercise, not evidence of
  surface condensation. No diagnosis, resident blame, legal clock, autonomous
  task, consent override or causal retrofit conclusion is authorized.
* Existing climate metadata distinguishes modelled ERA5 reanalysis, retained
  bytes, historical candidate terms and synthetic-demo-only approval. Preserve
  those exact distinctions while correcting stale dictionary claims.
* #193 actual use by #111/#133 tests remains UNMET; preparing neutral fixtures
  is not integration. Runnable live #184 remains UNMET; documenting its intended
  contract is not a delivered runner. #190 closure remains UNMET absent proven
  child completion or explicit owner deferral. Use Refs for incomplete work,
  including #194 while runnable live-stage coverage is incomplete.
* Agreed false-alert/miss limits, competent R2 review, physical calibration,
  real-data approval and hosted/human acceptance are not established. The
  candidate correctly retains these limits; this critique grants none of them.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is needed to resolve PC-001 through
  PC-007. The caller has already selected the bounded exercise scope.
* No decision-critical missing evidence prevents assessing this plan. Actual
  numerical results, downstream/live delivery and publication remain unproven,
  not assumed failures of code that has not yet been implemented.

## Limitations

* Code inspection was bounded to supplied evidence and directly relevant
  contracts, not an open-ended repository audit. Dependency absence was assessed
  from supplied research and the documented runtime boundary, not a fresh
  exhaustive implementation search.
* No file except this critique was intentionally created or modified by this
  worker. No plan, research, state, implementation or prior review was edited.
* No new scientific, regulatory or climate-licensing research was performed.
  No fresh operational conformance or complete-local-gate claim is made.

## Recommended Next Action

* Highest-impact finding: PC-001, the seed/truth/schema contradiction.
* Action owner: Planning parent.
* Smallest next action: Reconcile the observation seed contract, then incorporate
  the complete PC-001 through PC-007 set into the active plan/details before P01.
* Preserve this original Revise verdict and disposition each finding against
  exact resolving evidence. Do not run another plan critique.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md](.copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md) | Assessed final candidate; unchanged by critique. |
| [.copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md](.copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md) | Assessed task contracts; unchanged by critique. |
| [.copilot-tracking/research/2026-10-27/sensor-scenarios-190-research.md](.copilot-tracking/research/2026-10-27/sensor-scenarios-190-research.md) | Supplied evidence synthesis; unchanged by critique. |
| [.copilot-tracking/reviews/plans/2026-10-27/sensor-scenarios-190-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/sensor-scenarios-190-plan-critique.md) | Original independent Complete / Revise assessment. |

## Next Steps

The active planning parent should resolve the seven directly actionable findings,
record their disposition without rewriting this original outcome, and then
continue the authorized ordered RPI flow. No user action is required. This
critique worker stops here; it does not implement, run Review, commit, push or
open a PR.
