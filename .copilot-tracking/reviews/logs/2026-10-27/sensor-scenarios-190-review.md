<!-- markdownlint-disable-file -->
# Review: Sensor scenarios and documentation

## Scope and Evidence

* Task ID: 190
* Task slug: sensor-scenarios-190
* Review date: 2026-10-27
* Scope: completed bounded P01-P03 implementation and issue acceptance mapping
* Plan: .copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md
* Details: .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/sensor-scenarios-190-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/sensor-scenarios-190-changes.md
* Research: .copilot-tracking/research/2026-10-27/sensor-scenarios-190-research.md

## Opening Review State

Goal: independently assess scenario/evaluator correctness, evidence and honest
criterion-level acceptance, not fabricate live/downstream authority.
Evidence readiness: implementation markers and all local validation reconciled.
Acceptance basis: requested #190/#192/#193/#194 criteria, linked requirements,
plan and all critique dispositions. Initial comparison: new source/tests,
docs and per-check results against the complete P01-P03 boundary.
Read-only: only this review record may be edited during assessment.
Initial blockers: no assessment blocker; live/downstream acceptance remains
unmet and must not be hidden.

Review comparison anchor: `0ded682bab690d24eb59b78e704be82d337bf6cd`;
both staged and unstaged task-owned content are included. Exact final-source
synthetic CLI artifacts may be verified read-only. No second Review, source
correction, nested delegation, heavy gate, live service or private data access
is authorized. Existing validation reports are evidence, not independently
rerun checks.

## Execution Status

* Execution status: Complete.
* This is the one independent post-implementation Review, performed on
  2026-10-27. No nested agent, correction or second Review was invoked.
* All five canonical research/plan/details/critique/changes artifacts were
  read completely. Both Git diff layers and the combined working-tree diff
  against the specified base were assessed. Source and documentation content
  is staged; unstaged task updates reconcile validation, markers, handoff and
  the canonical Review path. The continuation-state file was not edited.
* Implementation execution is reported Complete for bounded P01-P03.
  Whole-issue acceptance is assessed separately below. Review could reach
  substantive conclusions despite the fresh installed-test limitation.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Deterministic isolated scenarios and observations-only comparison | Reconciled | Eleven cases, common actual pack seed, isolated truth, neutral inputs and per-check results match the plan. |
| P02 / P02-T01 | Semantic/mutation tests and simulator knowledge | Reconciled | One new test file, 15 methods, zero removals; five existing documentation files updated. No default-generator source change. |
| P03 / P03-T01 | Validation record and exact commands | Partial assurance | Reported checks completed and final-source snapshot verified; PC-004 rejection is unsupported, RV-001. Reported passes do not establish compliant execution paths. |
| Follow-Up Items: #193 | Actual #111/#133 integration remains unmet | Reconciled, open | Fixtures are not actual consumer-test use, RV-002. |
| Follow-Up Items: #194 | Runnable #184 documentation remains unavailable | Reconciled, open | No live runner or fabricated command, RV-003. |
| Follow-Up Items: #190 | Owner disposition of incomplete children | Reconciled, open | No owner deferral or parent closure support, RV-004. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/synthetic/sensor_scenarios.py | Separate exercise generator, observations-only classifier, descriptive comparison, truth join and safe snapshot CLI | Seven damp/data-quality cases and four retrofit profiles; exact 13-field schema | Eleven read-only existing tests passed; independent neutral-observation and retained-data probes passed | No reproducible implementation defect identified within the assessed contract. |
| P01-T01 | Same module, final-source synthetic snapshot | Bind observations, parameters, source and results reproducibly | 11 cases, 6,888 rows, 15 separate PASS results | All 14 manifest payload hashes and 12 analysis-input hashes verified; all retained CSV rows regenerated exactly | Engineering evidence, not R2/R3 approval or whole-issue acceptance. |
| P02-T01 | src/core/tests/test_sensor_scenarios.py | Semantic, mutation, schema, output and CLI coverage | Exactly 15 test methods and no test removals | Original final 15-test pass reported; 11 no-filesystem tests independently rerun | Filesystem/CLI tests inspected but not freshly rerun, see validation limits and RV-001. |
| P02-T01 | src/core/README.md; docs/reference/research/retrofit-synthetic-data/data-dictionary.md | Runnable offline instructions, schemas, parameters, truthful two-stage status and exact climate caveats | Complete changed sections assessed against code and retained climate metadata | Original 12 added-link/anchor checks reported passed; diff reviewed | Live-stage run acceptance remains unmet, not a documentation claim of delivery. |
| P02-T01 | docs/reference/research/iot-sensor-analytics-research-plan.md; docs/reference/README.md; docs/reference/log.md | Bounded R3 evidence, routing and append-only change record | Fixed-truth counts and exercise-only limits agree with retained report | Complete additions reviewed | No R1-R5 sign-off, real-data authority or owner deferral inferred. |

### Semantic assessment

* The classifier receives only observations and a neutral UTC window. It does
  not use truth, case labels, seeds or identity values as predictive features.
  Identity consistency and duplicate keys are validation, not label inference.
  A separately constructed three-day neutral series, unrelated to generated
  case values, produced the expected repeated-night result; raising the
  threshold changed it to NO_EXERCISE_SIGNAL, and deleting an overnight sample
  produced INSUFFICIENT.
* Grid membership, canonical timestamps, uniqueness, ordering, exact fields,
  units, synthetic source, schema, calibration and finite exercise domains
  are checked. Window/day/night coverage are distinct. Missing slots break
  persistence; UTC night boundaries and exact 12-hour/75-percent thresholds
  are exercised. Means become null on insufficiency. These are deliberately
  versioned exercise rules, not complete operational freshness, consent or
  building-condition analysis.
* Confusion has one trial per damp case, fixed truth independent of predictions,
  five binary-eligible cases and two expected-insufficient cases. Binary
  abstentions remain visible in eligibility; wrong sufficiency has separate
  counters. Classified-positive/negative rate denominators and zero-denominator
  nulls are explicit. Four retrofit cases are excluded. Mutation tests actually
  produce misses, false alerts, abstentions and wrong sufficiency.
* Default retained confusion is TP3/TN2/FP0/FN0, eligible5/classified5,
  abstained0, expected-insufficient2/correct2/incorrect0. At RH85, the same
  truth gives TP2/FN1 and a classified-positive miss rate of 1/3; RH70/75
  give TP3/FN0. These constructed counts are not prevalence or predictive
  accuracy estimates.
* Each retrofit case uses its own repeated seven-day no-effect counterfactual.
  Independent slot-by-slot probes of both channels confirmed zero pre-activation
  step, exact immediate day-14 activation, exact delayed day-21 activation and
  no-change throughout. Targets are +2 C/-10 RH points, 0/0, delayed
  +1.5 C/-6 points and -1 C/+8 points. Baseline/early/late counts and means
  are independently exposed; invalid or deficient input returns null deltas.
  This is a fictional overlay, not the existing beneficial fabric-loss model
  or a causal retrofit evaluation.
* The actual common seed remains observation provenance; internal RNG keys,
  labels, sizes and expectations are truth-only. Shared field compatibility
  and neutral filenames are preserved. All 11 retained CSVs exactly matched
  generation from current source. Changing identity/seed without changing the
  observations does not alter classifier output.
* Output preflight checks symlink components before resolution, repository and
  worktree ancestry, occupied directories and files. Fresh no-write probes
  rejected repository destinations and the occupied retained snapshot.
  Symlink/worktree/new-output behavior also has source-inspected tests and
  reported historical passes; those filesystem tests were not freshly run.
* The current source fingerprint matches
  `sha256:a55faf55844fab0ccc5c04d9612b0cac9c2f52e8daeddc28e611a032283eda06`.
  Manifest SHA-256 is
  `ce74864f5cac951a425738ce9c6f6896b539717e2b441147b64a0428b959e249`;
  report SHA-256 is
  `da00b5bced8f5a0a389efc6ad546e94bf4983c789142d5ae97d1c738ecbe2e20`.
  This is not a full-gate receipt.
* Climate documentation agrees with the retained metadata: 2026-10-27
  retrieval, 17,544 paired hours across 2023-2024, Durham returned grid cell,
  exact raw hash, Open-Meteo attribution/CC BY, historical 2026-10-22 terms,
  underlying C3S uncertainty and limited synthetic-demonstrator owner approval.
  No new licence check is claimed. Scenario weather is explicitly constructed
  and does not inherit ERA5 provenance.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P03 / P03-T01 | Wording distinguishes Review preparation from the subsequent independent Review | Avoid self-dependent completion; no scope or authority change | Plan, details, changes and handoff now agree | Original critique remains Revise | Compatible clarification, not a new acceptance criterion or material divergence. |
| P03 completion evidence | Running API evidence replaced by final reported pass; markers and handoff completed | Reported 1,121 tests/314 skips; no new user decision | Staged and unstaged states compared; current text assessed | No second critique or Review | Descriptive update supported by supplied results, subject to execution-path qualification. |
| Review path | Details corrected to reviews/logs/2026-10-27 | Canonical template path | Current artifact pointers agree | No changed implementation scope | Reconciled. |
| P01 seed/schema contract | Common actual seed, distinct internal stream keys, identity-independent prediction | PC-001 compatibility correction | Plan/details/source/tests/docs agree | Original Revise preserved | Accurate provenance, no fabricated neutral seed. |
| P03 / PC-004 | Temporary-path prohibition rejected as absent | No superseding authorization evidenced in the artifact set | Rejection propagated to plan and changes | Original PC-004 remains intact | Not justified; RV-001. |

## Critique and Material Revision Assessment

Original critique execution Complete / verdict Revise is preserved unchanged.
This Review independently assesses dispositions rather than replacing that
verdict with the planner's readiness assertion.

| Critique ID | Recorded disposition | Independent assessment |
| --- | --- | --- |
| PC-001 | Applied with accurate provenance | Supported: actual shared seed, truth-only stream keys and invariant observations-only prediction. |
| PC-002 | Applied | Supported: half-open grid, UTC nights, per-day/window eligibility, gap breaks and inadequate-week tests. |
| PC-003 | Applied | Supported: fixed case-level population, explicit abstentions/sufficiency, exact mutation counts and non-perfect RH85 sensitivity. |
| PC-004 | Rejected as unsupported | Not supported: the supplied execution boundary forbids temporary-path file operations. A named environment or lock path is not a superseding authorization. RV-001. |
| PC-005 | Applied | Supported: exactly one test file, 15 methods, no removals. |
| PC-006 | Applied | Supported within the static local-output contract: ancestor symlinks, .git directory/file ancestry and occupied destinations are rejected before writes. |
| PC-007 | Applied | Supported: versioned manifest/report, exact source fingerprint, runtime, window, weather, parameters and relative payload hashes; retained data reproduces. |

No material expansion into absent consumers, live transport or approved
analytics occurred. Compatible PC-001/002/003/005/006/007 changes are reconciled
before the assessed implementation. P03 wording correction does not require
another critique. PC-004 cannot be dismissed simply by asserting the rule was
absent; no supported dependent-work exception is evidenced. Reported functional
results are retained, but do not prove compliance with execution restrictions.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| #193 actual #111/#133 tests | Consumers are not delivered; fixtures alone cannot implement their product behavior | #111/#133 implementation owners integrate the pack when consumer contracts exist | Open distinct integration follow-up, RV-002; not a current source defect. |
| #194 runnable live-stage instructions | #184 live publisher remains unavailable; inventing a command would be misleading | #184 delivery owner, then #194 documentation owner | Open distinct live/documentation follow-up, RV-003; not a current source defect. |
| #190 remaining child dispositions | Parent explicitly requires all children closed or deferred | Parent/owner records actual completion or explicit deferral | Open acceptance decision, RV-004; no deferral inferred. |

All three follow-ups are mirrored in changes and kept outside completed active
P01/P02 implementation claims. Their scope and next actions are sufficiently
clear; they remain unmet issue criteria rather than newly activated tasks.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: PC-004 rejection does not establish a permitted validation path

* Related scope: P03-T01; PC-004; critique disposition and readiness.
* Evidence: plan `Critique Disposition`, PC-004 row (line 157), asserts that
  the temporary-path prohibition is absent; P03-T01 (line 136) still selects
  `/tmp/ama-syn190-venv`. Changes `Implementation-Time Plan and Detail Updates`
  (lines 100-101) repeats the unsupported rejection and its validation table
  (line 108) records that environment. The original critique PC-004 correctly
  identifies the restriction present in this Review's supplied execution
  boundary. Tests at lines 267, 300, 338 and 345 use TemporaryDirectory without
  an explicitly permitted alternative strategy.
* Impact: Functional pass evidence is not execution-policy conformance.
  Current planning readiness cannot be accepted on the asserted absence of
  the restriction. This Review did not access the reported environment,
  recreate it or run filesystem tests through default temporary paths.
* Destination: rpi-plan, for the unsupported assumption and validation-path
  reconciliation, not a claimed classifier defect.
* Smallest useful next action: Parent obtains a permitted, non-temporary
  execution/output strategy consistent with the task's write boundaries,
  reconciles P03 and the PC-004 disposition without changing the original
  critique, and records any necessary later validation under that strategy.
  A named lock or historical path does not authorize an exception. Do not
  fabricate compliant historical results or run a second Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: #193 actual downstream-test criterion remains unmet

* Related scope: plan Follow-Up Items #193; issue #193 third criterion.
* Evidence: issue #193 requires scenarios used by both #133 and #111 tests.
  The new test module calls only the standalone scenario/comparison APIs.
  Research C7/C12, plan non-goals, changes blockers and README explicitly
  retain consumer absence; #111 and #133 are open in the fresh issue check.
* Impact: Improvement/no-change/delayed/adverse fixture and labelled-size
  criteria are supported, but whole #193 acceptance and Closes #193 are not.
* Destination: distinct follow-up owned by #111/#133 implementation owners.
* Smallest useful next action: Integrate these retained observations into
  actual consumer tests after those contracts exist; record each consumer's
  evidence separately. Keep this PR Refs #193.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: #194 cannot yet document running both simulator stages

* Related scope: plan Follow-Up Items #194; issue #194 first criterion.
* Evidence: issue #194 asks how to run both stages and depends on #184.
  README `Two-stage simulator operation and limits` explicitly has no runnable
  live publisher, only the delivered shared contract and future prerequisites.
  Dictionary matches this limit; fresh #184 check is OPEN.
* Impact: Climate/source/licence/provenance and synthetic-only documentation
  criteria are supported. Honest contract/status coverage is not runnable
  live-stage delivery; whole #194 and Closes #194 remain unsupported.
* Destination: distinct follow-up to #184 delivery owner and subsequent #194
  documentation owner.
* Smallest useful next action: Once an authorized runner exists, document and
  validate its real command, controls and limits. Keep this PR Refs #194.
  This dependency is not a defect in the current offline implementation.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: #190 child-closure or owner-deferral criterion is not met

* Related scope: plan Follow-Up Items #190; parent acceptance and PR wording.
* Evidence: fresh issue #190 explicitly requires all children closed or
  deferred. #191 is CLOSED; #192's three scenario criteria are supported by
  the assessed implementation, but #193 and #194 have RV-002/003 residuals.
  No owner deferral is evidenced. Plan and changes correctly say not to infer it.
* Impact: Per-check reporting satisfies the other parent criterion, but
  bounded P01-P03 completion cannot establish whole-parent acceptance.
* Destination: rpi-plan, parent/owner child disposition; no source expansion
  or deferral is authorized by this Review.
* Smallest useful next action: Preserve Refs #190 and the explicit residual
  dependency records. Owner may later choose genuine completion or explicit
  deferral; neither is assumed here.

## Defects

* No reproducible implementation defect was identified in the assessed
  classifier, confusion accounting, retrofit overlays, retained-data replay,
  schema/seeds/truth separation, static output safety or provenance contract.
* RV-001 is an unsupported planning/execution assumption, not an instruction
  to patch scenario behavior. RV-002/003 are residual integrations, not defects.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-plan | Parent reconciles permitted validation paths and PC-004 disposition | Invalid assumption about execution restrictions. |
| RV-002 | Distinct #111/#133 integration follow-up | Consumer implementation owners | Actual test use is absent and outside current fixture scope. |
| RV-003 | Distinct #184 then #194 follow-up | Live delivery and documentation owners | Runner dependency is not delivered. |
| RV-004 | rpi-plan | Parent/owner records actual child completion or explicit deferral | Parent acceptance decision remains open. |

Later implementation of routed work does not require another Review.

## Residual Work

* Actual downstream integration and runnable live documentation remain the
  distinct follow-ups above, not newly active P01/P02 tasks.
* Competent R2/Asset method sign-off, agreed R3 error limits and operational
  freshness/consent handling remain future analytics/research-owner work.
  No new material evidence gap prevents judging this bounded exercise pack;
  no immediate rpi-research invocation is required by this Review.
* Physical calibration, real resident/data authority, hosted/human approval and
  publication gates remain unperformed. This Review grants none of them.
  No heavy/full gate was requested or executed.

## Blockers and Remaining Work

* No blocker prevented completing this Review.
* Current workflow acceptance is blocked by RV-001; parent #190 acceptance
  also lacks child closure/deferral, RV-004.
* Current plan markers say P01-P03 Complete; semantic implementation evidence
  supports bounded completion, but not the unsupported execution-path
  justification. Any later correction/validation is parent-owned continuation,
  not work performed or silently completed during this Review.
* No files except this canonical Review record were intentionally changed.
  No commit, push, PR update, source fix, gate, Azure operation, private data
  access, secret access or nested delegation was performed.

## Validation Evidence

| Command or assessment | Scope | Status | Summary |
| --- | --- | --- | --- |
| git status; staged, unstaged and base-to-working-tree diffs | Task-owned candidate against 0ded682bab690d24eb59b78e704be82d337bf6cd | Passed | Both layers assessed; no source delta hidden by staged-only comparison. |
| gh issue view 190/192/193/194; dependency status checks | Acceptance and named dependencies | Passed | Exact criteria read; #191 closed, #111/#133/#184 open. No issue mutated. |
| python3 installed import before bounded test discovery | Fresh installed-package test capability | Failed / unavailable | ModuleNotFoundError: zava_forward. Discovery did not run. No dependency installation was made under the review-only write authority. |
| python3 -B read-only source-loaded unittest selection | Eleven existing tests with no filesystem activity | Passed | 11 tests, 0.703s. Explicit source loading only for bounded probes; not represented as an installed-distribution/full-15-test run. |
| python3 -B independent in-memory probes | Neutral generic observations, overnight gap, all retrofit slots/channels and invalid parameters | Passed | Threshold change alters a neutral series; night gap abstains; all activation/no-step/counterfactual assertions pass. |
| python3 -B read-only retained-snapshot verification | Synthetic final-source evidence | Passed | 14 payload hashes, 12 analysis hashes, exact report/manifest hashes, exact source fingerprint and all 11 regenerated CSV case sequences verified. |
| No-write _destination probes and source inspection | Output refusal | Passed, bounded | Repository and occupied snapshot refused without creating output. Historical symlink/worktree/filesystem tests inspected, not freshly rerun. |
| Original final new-test command | All 15 scenario tests | Passed, reported | Changes reports 15 tests, 4.806s. Four filesystem/CLI methods not rerun here because the supplied execution/write boundary does not permit their default strategy. |
| Original core regressions | 17 sensor/model/provenance/dependency modules | Passed, reported; 1 skipped | 173 tests, 82.977s; opt-in local SQL skip is not a pass. Not rerun. |
| Original API discovery | Full supplied API test discovery | Passed, reported; 314 skipped | 1,121 tests, 904.506s. Not rerun as instructed; skips do not prove live/cloud acceptance. |
| Original ruff check/format and mypy | Two new Python files | Passed, reported | Scoped results accepted as supplied evidence, not a fresh global-cleanliness claim. |
| Original Markdown link scans | Five changed documentation files | Mixed, reported | Twelve new local links/anchors passed; ten historical missing targets failed the initial broad scan. Baseline link debt is not a new source defect. |
| git diff --check | Current unstaged diff | Passed | Fresh command exited zero. |
| Heavy/full gate, SQL/live/browser/scanner and hosted/human gates | Publication/operational acceptance | Not run / unavailable | Outside authorized bounded Review; no --all or --changed invocation, cloud fallback or fabricated approval. |

## Issue Closure Recommendation

| Issue | Criterion-level assessment | Truthful PR reference |
| --- | --- | --- |
| #192 | Each case has an actual seed, label and expected outcome; scenario snapshot is separate from general data; independent fixed-truth confusion/sensitivity supports bounded R3 evidence | Closes #192 is the only supported closing reference on implemented issue criteria, subject to resolving RV-001 and ordinary publication/merge gates. This does not close or approve all R3 research. |
| #193 | Improvement/no-change/adverse plus delayed case and exercise direction/size supported; actual #111/#133 test use unmet | Refs #193 only. |
| #194 | Backfill/schema/status, climate provenance and simulated-data limits supported; runnable live-stage instructions unavailable | Refs #194 only. |
| #190 | Per-check results supported; all children closed/deferred criterion unmet | Refs #190 only. |
| #191 | Already closed; existing tests/API reused rather than reimplemented | No new closing claim needed. |

## Outcome

* Outcome: Not accepted for the aggregate #190/workflow acceptance boundary.
* Rationale: No assessed implementation defect was reproduced, and #192's
  implemented criteria have substantive evidence. However, the PC-004 rejection
  does not support execution conformance, and #190/#193/#194 cannot be declared
  complete while explicit dependencies and child dispositions remain unmet.
* This is not a claim that acknowledged out-of-scope consumers are source
  defects, nor a withdrawal of verified exercise results. Bounded semantic
  completion, permitted execution, whole-issue acceptance and publication
  approval are separate judgements.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No source fix is prescribed by this Review. |
| Decision gap or invalid assumption | rpi-plan | Parent resolves RV-001 validation-path assumption and RV-004 child disposition without inventing authorization. |
| Material evidence gap | None for current fixture assessment | Future R2/R3 approval remains analytics/research-owner work, not presumed acceptance. |
| Non-blocking residual work | Distinct integration/live follow-ups | #111/#133 owners for RV-002; #184 then #194 owners for RV-003. These block their own whole-issue acceptance. |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: full task artifact/source/doc comparison; 11 fresh
  no-filesystem tests and independent in-memory probes; exact retained
  synthetic hashes/source/rows verified; original broader passes retained
  with clear reported/skipped/unavailable qualifications.
* Blockers: RV-001 execution-path reconciliation; RV-004 parent child
  disposition. No review-progress blocker and no second Review required.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/sensor-scenarios-190-research.md](.copilot-tracking/research/2026-10-27/sensor-scenarios-190-research.md) | Complete task research and dependency/evidence boundary. |
| [.copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md](.copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md) | Current P01-P03 plan, dispositions and follow-ups. |
| [.copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md](.copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md) | Exact implementation, temporal and validation contracts. |
| [.copilot-tracking/reviews/plans/2026-10-27/sensor-scenarios-190-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/sensor-scenarios-190-plan-critique.md) | Preserved original Complete / Revise critique. |
| [.copilot-tracking/changes/2026-10-27/sensor-scenarios-190-changes.md](.copilot-tracking/changes/2026-10-27/sensor-scenarios-190-changes.md) | Implementation summaries, exact retained hashes and reported validation. |
| [src/core/src/zava_forward/core/synthetic/sensor_scenarios.py](src/core/src/zava_forward/core/synthetic/sensor_scenarios.py) | Assessed generator, classifier, comparison and CLI. |
| [src/core/tests/test_sensor_scenarios.py](src/core/tests/test_sensor_scenarios.py) | Fifteen scenario tests; eleven independently rerun without writes. |
| [src/core/README.md](src/core/README.md) | Scenario and two-stage operation guide. |
| [docs/reference/README.md](docs/reference/README.md) | Knowledge-base addition and explicit limits. |
| [docs/reference/log.md](docs/reference/log.md) | Appended change record. |
| [docs/reference/research/iot-sensor-analytics-research-plan.md](docs/reference/research/iot-sensor-analytics-research-plan.md) | Bounded R3 evidence and retained approval gates. |
| [docs/reference/research/retrofit-synthetic-data/data-dictionary.md](docs/reference/research/retrofit-synthetic-data/data-dictionary.md) | Updated sensor schemas, provenance and exercise fields. |
| [.copilot-tracking/reviews/logs/2026-10-27/sensor-scenarios-190-review.md](.copilot-tracking/reviews/logs/2026-10-27/sensor-scenarios-190-review.md) | This single independent Review and complete RV-001 through RV-004 set. |

## Next Steps

Return this one Review result to the active parent. Parent routes RV-001 and
RV-004 to rpi-plan, retains RV-002/003 as distinct dependent follow-ups, and
preserves the original critique and this outcome. Only #192 has evidence for
a future Closes reference; use Refs #190/#193/#194. Do not infer owner deferral,
publish through a blocked gate, correct source during Review or start another
Review. This worker stops after writing the canonical record.
