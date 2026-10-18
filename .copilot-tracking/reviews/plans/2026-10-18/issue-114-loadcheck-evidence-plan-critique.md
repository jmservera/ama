<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-114-loadcheck-evidence

## Metadata

* Task ID: 114
* Task slug: issue-114-loadcheck-evidence
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-114-loadcheck-evidence-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md
* Critique execution status: Complete
* Review boundary: exactly one independent final-candidate plan critique; no implementation review or second critique.
* Verified branch: fix/loadcheck-evidence-114
* Verified HEAD and exact base: f91353169756dc41ebbcca944bdd3f44f7c04b89
* Severity counts: Critical 0; High 0; Medium 2; Low 0.

## Inputs and Criterion Boundary

The assessment includes the complete explicit caller scope recorded in the plan,
phase details and supplied task, not just the empty-percentile correction:

* Positive finite duration, positive integer sessions, writer range, positive homes
  and nonempty workload validation at the specified pre-store/pre-worker boundaries.
* Required-class observation integrity, sanitized worker-start/session/request
  failure accounting, healthy-class preservation and actual CLI exit behavior.
* Existing request mix, defaults, list/detail/write limits of 1/1/2 seconds,
  unrounded percentile comparisons and descriptive maximums.
* Shared monotonic deadlines, request timing outside aggregation contention,
  deterministic healthy and failing paths, old-source regressions, mutations,
  configured Ruff/mypy and coupled tests.
* Exactly two canonical source/test files, at most 16 new test methods, no test
  removals, no generated targets and no unrelated changes.
* Ordered RPI execution, immutable original critique and Review, at most two
  source correction cycles, candidate/source identity, privacy-safe commits,
  ordinary PR publication with Refs #114 only and coordinator-owned integration.
* No private datasets, .env, support, Azure/IAM/Graph/deployment/spend/AI actions;
  no real load/cost, ledger/recovery expansion or AC2/whole-issue completion claim.
* Applicable execution instructions, including repository-relative scratch
  operations and the prohibition on system temporary-directory writes.

Evidence read:

* Supplied plan, phase details and research C1-C8.
* src/core/src/zava_forward/core/synthetic/loadcheck.py and factory.py.
* src/core/tests/test_queue_benchmark.py, src/core/pyproject.toml,
  src/core/README.md and .github/workflows/src-ci.yml.
* .github/copilot-instructions.md, docs/case_study_48_original.md,
  relevant addendum sections, docs/reference/README.md and memory.md.
* docs/adrs/0001-azure-architecture.md and 0002-pilot-readiness-architecture.md,
  and the PRD NFR-002/Exercise Acceptance Contract sections.
* Activated rpi-plan-critique contract and its critique template.

Frozen input SHA-256 values:

| Input | SHA-256 |
| --- | --- |
| Plan | 62e180a95c96bdbbe846cb403f5ac83b79771d9f86e3581b5fb89024f1cc1642 |
| Phase details | e4eb97896289ef872514a3ece05cd351a8dc132c696b31213747f1362dec7db1 |
| Research | f235e1919cef5611bf6198bc8d64a9ce152a6f95376d97e22712a9d468f0d774 |
| Canonical loadcheck.py | 095f9ecc41f872024183c51e219c534ec9e5cd45fd6f4fbc6dde6753e0947a56 |

Dependencies and decisions are coherent: Research and critique dispositions
precede P01; P01-T02 follows P01-T01; P02 follows reconciled P01; Review precedes
publication. No issue dependency or concurrent #153 file dependency is asserted.
All-writer direct workloads remain allowed. No new cancellation, sample quota,
maximum-latency gate, workload option or runtime dependency is proposed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Input validation; C3/C4; P01-T01/T02 | Covered | Explicit pre-store CLI guards and pre-worker direct validation; argparse errors versus direct ValueError are distinguished. |
| Missing observations; C1/C4; P01-T01/T02 | Covered | None metrics, false within, absent-specific/all-class cases and late-worker failure are explicit. |
| Startup/session/request failures; C2; P01-T01/T02 | Covered | Narrow request handling, type-only session failures, documented Thread.start RuntimeError, started-thread joins and healthy evidence preservation. |
| Timing/concurrency; C2; P01-T01/T02 | Partial | Implementation invariants are sound, but their distinguishing deterministic tests are not specified; PC-001. |
| Latency and healthy path; P01-T01/T02 | Covered | Raw p95 exact/overlimit comparisons, unchanged limits, healthy all-class observations and no new maximum gate. |
| Actual CLI contract; C3/C5; P01-T02 | Covered | Existing CLI only exposes data/homes/seconds; real main(), emitted JSON, 0/1 report outcomes and pre-store argparse rejection are in scope. No new sessions/writers flags are needed. |
| Private-error protection; P01-T01/T02 | Covered | Static validation text, type-only categories, sentinel-message exclusion, no BaseException catch or silent-success fallback. |
| Test execution isolation; C5/C6; P01-T02 | Partial | Environment/factory isolation is good; default temporary-directory writes are not contained; PC-002. |
| Locked footprint/test budget; P01 | Covered | Canonical loadcheck.py and new test_loadcheck.py only, at most 16 methods, no removals or generated targets. Findings can be resolved within this budget. |
| Regression/mutation/configured checks; C6/C8; P01-T02 | Covered with PC-001/PC-002 | Old-source isolation, guard/missing/error/latency mutations, coupled suites and configured Ruff/mypy are planned. |
| Ordered RPI and immutable findings; P02-T01 | Covered | One original Review, candidate/source pinning, separate correction receipts and at most two source cycles. |
| Safe publication and stop; P02-T02 | Covered | Local privacy-safe identity, required trailer, tracked artifacts, no unilateral integration, PR head/base verification and coordinator handoff. |
| AC2/NFR-002 and authority boundaries; C7; P01/P02 | Covered | Local harness trust only; deployed Azure workload, additional classes/durations/sample requirements, cost and human acceptance stay unmet. |

## Verdict

* Verdict: Revise
* Rationale: The production correction is credible and appropriately minimal.
  Two bounded planner-owned changes are needed: explicit falsifiable timing
  regression checks and a safe temporary-file execution strategy. Neither
  requires a scope expansion, source-file expansion or user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Timing fixes lack distinguishing deterministic regression criteria

* Related IDs: C2, P01-T01, P01-T02; functional monotonic-deadline and
  completion-before-aggregation requirements.
* Evidence: .copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md:35-42
  specifies shared monotonic timing and elapsed capture outside the lock.
  Its lines 50-55 prescribe patched clocks, controlled worker timing and
  failure/latency examples, but not assertions that distinguish clock choice,
  aggregation wait or completion of an already-started cycle.
  src/core/src/zava_forward/core/synthetic/loadcheck.py:43-63 currently uses
  time.time() and samples completion after acquiring the lock.
* Concern: A deterministic exact-limit test can pass with an uncontended lock
  even if completion timing remains inside the lock. Patching all time sources
  similarly can also let a wall-clock deadline survive. General concurrent
  aggregation coverage does not necessarily falsify either defect.
* Impact: The suite could accept the old timing mechanisms while certifying the
  newly claimed latency integrity and deadline behavior. This is a measurement
  trust gap, not a request for performance benchmarking.
* Smallest useful change: Extend P01-T02 with explicit subcases proving that
  wall-clock access is unnecessary, workers share one monotonic cutoff, late
  workers add no fabricated observations, an entered cycle finishes after the
  cutoff, and simulated aggregation wait does not enter request latency.
  Use per-thread scripted clocks/events or a controlled lock wrapper without
  sleeps or a new source abstraction. Add targeted mutants for wall-clock
  substitution and completion capture moved inside the lock.
* Action owner: Planning parent for plan/details correction; implementation
  parent for the bounded tests and recorded mutation results.
* Exact resolving evidence: Revised P01-T02 identifies these assertions and
  synchronization controls; implementation records deterministic passing
  assertions and detection of both timing mutants, without exceeding 16 test
  methods or changing the two-file footprint.
* Decision route: Direct planner correction. Current caller direction already
  fixes the desired timing and concurrency behavior; no significant or
  divergent user decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: CLI and coupled checks need an explicit repository-local temporary root

* Related IDs: P01-T02; test isolation and applicable no-system-temporary-write
  execution requirement.
* Evidence: .copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md:56-64
  requires actual main() invocation, an entirely cleared os.environ and coupled
  tests. src/core/src/zava_forward/core/synthetic/loadcheck.py:81 calls
  tempfile.TemporaryDirectory() without dir. src/core/tests/test_queue_benchmark.py:20
  does the same. Applicable execution instructions prohibit system temporary
  directory writes and require scratch files relative to the working tree.
* Concern: Creating only the seed JSON locally does not constrain main()'s
  internal directory. Clearing the environment also makes an inherited TMPDIR
  strategy alone unreliable in CLI tests, especially before tempfile has
  cached its directory. The planned coupled checks have the same default-path
  exposure.
* Impact: Otherwise-correct tests can write to a forbidden location or be
  blocked before producing the required CLI/coupled evidence.
* Smallest useful change: Specify a repository-local scratch root for all
  validation processes and ensure tempfile's selected directory remains local
  inside clear-environment CLI tests, for example through an explicitly scoped
  tempfile.tempdir override or test-local TemporaryDirectory wrapper.
  Record directory cleanup and exclusion from delivery. Do not change the
  runtime public contract, add a committed fixture, or edit coupled tests.
* Action owner: Planning parent for the execution strategy; implementation
  parent for scoped setup, checks and cleanup.
* Exact resolving evidence: Revised details state the local scratch/override
  mechanism; recorded validation commands select that root; CLI tests assert
  the factory's ZF_DATA/ZF_STATE paths resolve beneath it; final status confirms
  no scratch files enter the committed footprint.
* Decision route: Direct planner correction. The execution prohibition is
  already explicit and requires no new user authorization.

## Strengths and Residual Risk

* The two-file correction addresses the actual evidence producer rather than
  unrelated queue benchmarks or store/runtime architecture.
* Type-only errors and failure counts remain separate from successful-class
  measurements. A failed worker must fail overall without falsifying healthy
  measured classes.
* The actual parser has integer seconds and no session/writer switches.
  Preserve those options: CLI nonfinite strings can be rejected by argparse,
  while direct run() must reject nonfinite numeric values explicitly.
  Invalid CLI arguments normally exit 2; valid-but-failing reports return 1.
  These are compatible with the plan, not reasons to add CLI options.
* Existing source migration exemptions do not exempt the new test module.
  Configured strict mypy applies to test_loadcheck.py; typed adapters/casts or
  typed canonical functions must keep the locked footprint, rather than adding
  pyproject exemptions. This is an implementation constraint, not an additional
  finding because the plan already requires configured mypy.
* Shared deadlines permit startup skew, and already-started calls/cycles may
  outlive the requested duration. The parent explicitly accepts this behavior.
  No barrier, timeout/cancellation redesign or minimum sample quota is requested.
* Offline tiny fixtures and mutations do not establish actual database load,
  deployed revision behavior, cost, full NFR-002, AC2 or issue completion.
* P02 correctly preserves an adverse original Review and reports correction
  evidence without promoting it into independent corrected acceptance.

## Questions or Blocking Evidence Gaps

* None requiring user input. Both findings have direct dispositions within the
  confirmed scope.
* Live issue metadata was not fetched because this critique prohibits cloud
  calls. Whole-issue criteria are assessed only to the extent supplied in the
  caller/research/plan; operational or issue-completion acceptance is excluded.

## Limitations

* This is a plan credibility assessment, not execution or implementation
  verification. No test, application, mutation, package installation, cloud call,
  nested agent, source edit, commit or state edit was performed.
* Pre-existing untracked plan/details/research/state artifacts were observed and
  left untouched. Only the designated critique artifact is authored.
* Research's historical probe claims are attributed to C4, not independently
  re-executed. The source mechanisms supporting them were directly inspected.
* All actionable concerns found within the supplied boundary are reported here.
  There is no withheld follow-on finding set or second-critique recommendation.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Record direct dispositions and update P01-T02 with the
  timing assertions/mutations and repository-local scratch strategy; then
  continue the authorized implementation.
* User response required: No.
* Preserve this original report unchanged, including its Revise verdict.

## Relevant Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-18/issue-114-loadcheck-evidence-plan.md](.copilot-tracking/plans/2026-10-18/issue-114-loadcheck-evidence-plan.md) | Frozen final-candidate plan assessed in this critique |
| [.copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md](.copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md) | Phase details and direct correction target |
| [.copilot-tracking/research/2026-10-18/issue-114-loadcheck-evidence-research.md](.copilot-tracking/research/2026-10-18/issue-114-loadcheck-evidence-research.md) | Supplied C1-C8 evidence and accepted scope |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-114-loadcheck-evidence-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-114-loadcheck-evidence-plan-critique.md) | Single original critique, Complete execution and Revise verdict |

## Next Steps

The active planning parent should disposition PC-001 and PC-002 directly, finalize
the plan/details without another critique, and proceed through the authorized
implementation and single original Review gates. No user action is required.
This critique worker stops after returning the report identity and hash.
