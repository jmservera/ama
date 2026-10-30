---
title: Faster local gate 470 final-candidate plan critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: 470. Slug: faster-local-gate-470.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/faster-local-gate-470-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/faster-local-gate-470-phase-details.md.
* Critique execution status: Complete.
* Assessment: one independent final-candidate critique; no second pass requested.

## Inputs and Criterion Boundary

* Caller direction: complete the authorized RPI loop with local commits only.
  No push, PR creation, Azure execution, deployment, sign-in, credentials or
  secrets. No runner redesign, test removals or test additions.
* Current research: .copilot-tracking/research/2026-10-30/faster-local-gate-470-research.md,
  including its recorded #470/#475 acceptance and historical timing evidence.
  Remote issue and PR evidence was not independently retrieved in this critique.
* Supporting contracts: src/README.md, local RPI gate; tools/rpi-checks.py,
  lock admission, command timing, receipt construction and main execution.
* Required project context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md, with bounded context reads where material is large.
* Acceptance boundary: AC1/AC2/AC3/AC5 functionality is reported merged by #475;
  this candidate documents and attempts the remaining AC4 full serial/parallel
  measurement. Prepared evidence cannot satisfy the PR-recording condition.
* Dependencies: foreign-owned heavy lock, bounded admission, local prerequisites,
  resource capacity, immutable external outputs and reviewed current main.
* This assessment concerns plan credibility, not implementation acceptance,
  actual test execution, an exact-head Review or authority to publish.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1, AC2, AC5; P02-T01 | Covered | Existing canonical tools/test_rpi_checks.py target; no new tests or scope weakening. Results remain to be executed. |
| AC3; P02-T02 | Partial | Admitted jobs are recorded, but AC4 qualification does not explicitly exclude a second run admitted at one worker; PC-001. |
| AC4; P01-T01, P02-T02 | Partial | Same source/base, fresh outputs and order caveats are specified; controlled-comparison qualification needs PC-001. |
| Research Q1-Q3 | Covered | Merged functionality is not reimplemented; partial historical timings are rejected; real failures remain blockers. |
| Lock safety and failed-run qualification | Covered | Self-locking runner, bounded wait, no nested flock, no interference with foreign ownership, immutable adverse evidence and justified stop on common prerequisite failure. |
| P02 candidate identity; P03-T01 | Covered | Candidate committed before benchmark; evidence commits invalidate final receipt status; final current-main/exact-head gate remains a distinct publication prerequisite. |
| Local-only handoff and acceptance | Covered | No push, PR, merge or issue closure; coordinator must publish successful measurements before AC4 is proven. |
| Validation and implementation scope | Covered | Required API discovery and static checks retained; documentation-only implementation; zero test additions and no removals. |

## Verdict

* Verdict: Revise.
* Rationale: the bounded approach is credible, but the plan needs one explicit
  benchmark eligibility rule before successful full runs can be presented as a
  comparable serial/parallel result. This is a direct correction within current
  user direction, not a request for broader work.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Qualify actual parallel admission and execution comparability

* Related IDs: AC3, AC4, P01-T01, P02-T02, research Q2/Q3.
* Evidence: the plan makes two passing full runs plus PR recording the explicit
  AC4 threshold. The details say requested workers may be capped but do not
  define the acceptance consequence. The research explicitly says a single
  admitted worker does not prove a speedup. tools/rpi-checks.py:2343-2352 applies
  worker_limit after lock acquisition; tools/rpi-checks.py:2107 records admitted
  jobs. Separate invocations independently collect tool/environment identities.
* Concern: requested jobs 3 can execute with one admitted worker, and identical
  commit/base alone does not establish equivalent toolchain/package versions,
  available resources or scanner inputs across independent full executions.
  Recording these facts without a comparison disposition still permits two
  passing but noncomparable runs to be labelled the missing parallel benchmark.
* Impact: coordinator-ready evidence could overstate AC4 or attribute a timing
  difference to scheduling when there was no parallel capacity or a material
  execution-condition change.
* Smallest useful change: add a comparison-eligibility checklist to P01-T01 and
  P02-T02. Require serial admitted jobs 1 and parallel admitted jobs greater
  than 1; retain the requested value and disclose any cap. Record both receipt
  identities, full selected groups/extras, relevant tool/package versions and
  resource limits. Compare those conditions and disclose scanner/database,
  cache and order differences; classify material uncontrolled differences as
  qualified/noncomparable rather than controlled speedup evidence. Specify
  one identical elapsed-time boundary for both runs, separate from queue wait,
  and record how it is calculated. No rerun, runner change, reverse-order
  experiment or positive speedup threshold is mandatory. If admission remains
  one or comparability is unavailable, retain actual timings and leave the
  parallel-comparison acceptance unproven with its exact blocker.
* Action owner: planning parent, with implementation/evidence collection by the
  same delivery parent and later PR publication by the coordinator.
* Exact resolving evidence: revised plan/details contain the eligibility and
  timing rules; the later evidence table records requested/admitted jobs,
  commit/base, full scope, receipt paths, elapsed boundaries, relevant identity
  and resource comparisons, exits and an explicit comparison disposition.
  Until those measurements exist, the documents must not mark AC4 proven.
* Decision route: direct planner correction. Existing user direction already
  requires honest measurements or blockers; no significant or divergent user
  decision is needed.

## Strengths and Residual Risk

* Same-candidate serial then parallel full runs are an appropriate bounded
  baseline, not a fabricated reconstruction of historical pre-#475 execution.
* Cache/order bias is already disclosed. A single ordered pair is descriptive
  evidence, not a causal or statistically robust performance claim.
* Failed commands, lock timeout, missing downloads and partial execution never
  become successful full timing. Avoiding repetition of an identical failed
  prerequisite is explicitly permitted without satisfying acceptance.
* Benchmark receipts may become historical after Review/evidence commits.
  Preserve them as same-candidate measurements; do not relabel them final.
  The distinct final exact-head gate and immediate current-main verification
  remain required before any later authorized publication and independent
  exact-head assessment.
* A foreign lock owner or insufficient prerequisites may leave AC4 unmet.
  That is an allowed, honestly reported outcome, not authority to weaken gates.

## Questions or Blocking Evidence Gaps

* No user question is required. Actual resource admission and complete
  measurements are implementation-time evidence, not facts assumed here.

## Limitations

* No heavy checks, installations, source changes, commits, publication, credential
  access or additional agent dispatch occurred.
* Existing regression coverage and issue acceptance were assessed from the
  supplied current research and plan, not independently re-executed.
* Only this critique artifact was written. Plan, details, research and state
  remain unchanged by the critic.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: planning parent.
* Smallest next action: incorporate the comparison-eligibility rule directly
  into P01-T01/P02-T02 and record this original critique's disposition.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/faster-local-gate-470-plan.md](.copilot-tracking/plans/2026-10-30/faster-local-gate-470-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-30/faster-local-gate-470-phase-details.md](.copilot-tracking/details/2026-10-30/faster-local-gate-470-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-30/faster-local-gate-470-research.md](.copilot-tracking/research/2026-10-30/faster-local-gate-470-research.md) | Current supplied research |
| [.copilot-tracking/reviews/plans/2026-10-30/faster-local-gate-470-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/faster-local-gate-470-plan-critique.md) | Original independent critique |
| [src/README.md](src/README.md) | Local gate and publication contracts |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Existing admission, timing and receipt implementation |

## Next Steps

The active planning parent should resolve PC-001 directly, preserve this original
Revise outcome, finalize the plan without another critique, and continue the
authorized RPI loop subject to admission and evidence gates. No user action is
required; no publication is authorized.
