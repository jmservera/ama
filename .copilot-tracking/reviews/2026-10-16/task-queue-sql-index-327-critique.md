---
title: Final candidate critique for SQL queue membership
description: One bounded correctness and acceptance critique for issue 327
ms.date: 2026-10-16
---

## Metadata

* Task ID: #327, task-queue-sql-index-327.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/task-queue-sql-index-327-plan.md.
* Phase details: .copilot-tracking/details/2026-10-16/task-queue-sql-index-327-phase-details.md.
* Critique execution status: Complete.
* This is the one final candidate critique. No source, plan, details or research was changed.

## Inputs and Criterion Boundary

* The supplied owner direction requires indexed SQL membership on every case or
  relevant shared-context write, the existing hot ID layer, SQLite/Azure SQL
  portability, authorization after lookup, uncached parity for every queue/sort/view,
  backfill, generated 60,000-case write-cold and repeat timings, and mutation regressions.
* Planning evidence: the plan and phase details above, and
  .copilot-tracking/research/2026-10-16/task-queue-sql-index-327-research.md.
* Implementation evidence: src/core/src/zava_forward/core/sqlstore.py,
  src/core/src/zava_forward/core/store.py,
  src/core/src/zava_forward/core/taskqueues.py,
  src/core/src/zava_forward/core/mssqlstore.py, and
  src/core/src/zava_forward/core/buildings.py.
* Acceptance evidence: src/core/tests/test_taskqueues.py,
  src/core/tests/test_sqlreads.py, and src/api/tests/test_mssqlstore.py.
* Required project and knowledge-base entry documents were consulted for context.
  They do not establish queue implementation correctness.
* Assessment covers the supplied requirements, research claims, both phases, all
  four tasks, acceptance criteria, dependencies and residual risks. It is a plan
  credibility assessment, not an implementation review or operational ratification.
  No external research, private dataset access or live database execution occurred.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner-directed durable membership and retained hot IDs | Covered | Six indexed flags, SQL miss lookup and reuse of _filtered preserve the selected architecture. |
| P01-T01: generated baseline and final benchmark | Covered | Deterministic existing fixture, committed change before each first page, same-page repeats, three rounds, write/read costs and context counters. |
| P01-T02: authoritative writes and shared dependencies | Partial | Explicit transaction requirement is sound; derived-state publication and cache validity across refreshes need PC-001. |
| P01-T02: seed, migration and backfill | Partial | Transactional backfill is required, but existing constructor ordering needs the lifecycle contract in PC-002. |
| Clock, snapshot, entire policy and definition fingerprint | Partial | Inputs are identified; freshness checks on hot hits and refresh-only publication need PC-001. |
| SQLite/Azure SQL portability | Partial | Inheritance and dialect hooks are recognized; acceptance does not exercise new SQL Server schema/migration paths, PC-003. |
| P02-T01: full response parity and authorization | Covered | Independent uncached candidate selection, every view/sort, positive priority, exports, cursors and existing denial/projection semantics are retained. |
| P02-T01: rollback, mutation and bounded work | Covered with refinements | Separate lookup/write-maintenance mutations and bounded ordinary evaluation are explicit; add the targeted lifecycle and publication cases below. |
| P02-T02: validation and delivery | Covered | Existing unit/lint/type checks, honest skips, documentation and one implementation review are specified. |

## Verdict

* Verdict: Revise.
* The chosen architecture is compatible with the owner decision. Three bounded,
  planner-owned refinements are needed to turn central correctness and portability
  promises into implementable acceptance contracts. None requires a different
  architecture, a live Azure run or a new owner decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Define atomic derived-generation publication and hot-hit validation

* Related IDs: P01-T02, P02-T01; shared/cross-process invalidation and
  clock/policy/definition refresh requirements.
* Evidence: src/core/src/zava_forward/core/sqlstore.py::_sync returns early
  when meta.seq matches the process sequence; save normally advances that sequence.
  src/core/src/zava_forward/core/store.py::_queue_candidates currently keys the
  in-memory index by process version, as_of, current day and serialized policy.
  The details require a persisted fingerprint and full refreshes but do not define
  how a refresh without a case write becomes visible to an already-warm process.
* Concern: Durable flags, the fingerprint certifying them and the hot IDs must
  describe one generation. A refresh-only transaction can otherwise leave warm
  processes using old IDs, or a process with another policy/snapshot can use SQL
  flags produced for a different evaluator. A fingerprint check only on cache
  misses does not solve this. Reading the fingerprint before lookup without
  protecting or validating the lookup generation also leaves a refresh race.
* Impact: Queue inclusion can disagree with uncached selection despite correct
  per-case writes and a successful one-process clock test.
* Smallest useful change: Specify a durable generation or equivalent publication
  protocol. Capture evaluator inputs once per evaluation transaction; publish
  affected flags and their certified fingerprint atomically; validate hot hits
  against durable state; obtain or validate IDs against the same generation.
  State how refresh-only changes invalidate process IDs without changing business
  rowversions or audit meaning. Define mismatched process fingerprints as refresh,
  retry or explicit refusal, never silent reuse. Preserve bounded ordinary writes.
* Action owner: Planning parent, with implementation owner executing the protocol.
* Exact resolving evidence: Updated P01-T02 contract and P02-T01 tests with two
  independently opened stores: warm A; refresh B without a case write; reread A
  against the uncached oracle. Cover as_of, day, taskqueues.VERSION and policy
  content changed without changing its version. Add controlled interleaving of
  refresh and lookup, plus refresh failure rollback; assert no mixed generation,
  stale hot hit or partially certified flags. Retain the planned writer-lock
  interleaving test for authoritative linked-case/shared-document evaluation.
* Decision route: Direct planner correction compatible with confirmed owner direction.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Specify when evaluator-ready initialization permits backfill and seed evaluation

* Related IDs: P01-T02, P02-T01; restart/backfill, transactional seed and
  authoritative shared-state requirements.
* Evidence: src/core/src/zava_forward/core/sqlstore.py::__init__ invokes
  _migrate before initializing cases, data and as_of. _seed writes cases before
  shared DOCS and the source as_of; the fallback as_of is installed after _seed.
  Store.work_context needs as_of, cases and shared data. buildings.record validates
  case scopes against all homes and package scopes against procurement packages.
* Concern: Existing _row backfill can run on a single decoded case; queue backfill
  cannot simply follow that pattern. The details do not define an evaluator-ready
  phase or explain how seed evaluation sees the complete shared documents and case
  universe. Evaluating too early can fail startup or persist false blockers and
  certify them as current. A legacy database with missing as_of also needs its
  effective snapshot established before evaluating queues.
* Impact: First seed or old-schema upgrade can produce incorrect durable membership,
  even when later ordinary writes use authoritative transactional state.
* Smallest useful change: Explicitly stage schema addition separately from
  evaluator-ready backfill, or construct a complete transaction-local evaluator
  independent of partially initialized Store fields. Establish effective as_of,
  policy/day inputs, shared documents and all required linked cases before
  evaluation; publish the ready fingerprint only after the complete backfill
  succeeds. Preserve existing data/default precedence and do not silently mark
  default-zero columns complete.
* Action owner: Planning parent, with implementation owner choosing the compatible staging.
* Exact resolving evidence: Updated lifecycle order and tests for fresh seed and
  pre-queue schema upgrade containing shared building holds, linked cases and
  procurement scope. Include an old database without as_of and the existing
  environment/source precedence. Assert physical flags and first-read uncached
  parity, then reopen without the seed file and verify parity again. Inject a
  backfill evaluation failure and prove readiness is not published and a later
  reopen completes correctly.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Add acceptance evidence for the new SQL Server schema and migration paths

* Related IDs: P01-T02, P02-T01, P02-T02; SQLite/Azure SQL portability.
* Evidence: src/core/src/zava_forward/core/mssqlstore.py has separate TABLES DDL
  and an _indexes translation of shared INDEXES. Its _columns hook differs from
  SQLite. The shared SqlStore._migrate currently classifies only support/days as
  integers. src/api/tests/test_mssqlstore.py has server-free checks for a narrow
  upsert syntax pattern; its live suites are opt-in, and its parity subclass wraps
  test_sqlreads.Parity, not StoreQueueParity or the planned focused queue module.
* Concern: Running existing suites with live MSSQL skipped does not demonstrate
  that six new columns are integer-typed in both schemas, added correctly on
  upgrade, or indexed through the SQL Server translation. Existing portable-upsert
  checks alone will not catch these omissions. New queue tests will not
  automatically become SQL Server behavior tests through inheritance.
* Impact: SQLite can satisfy every local membership assertion while the inherited
  Azure SQL store has incompatible DDL, missing indexes or an untested upgrade.
* Smallest useful change: Add server-free assertions for all six SQL Server column
  definitions, integer migration statements, translated indexes and the new shared
  lookup/refresh statements through the dialect boundary. Wire the relevant new
  behavioral tests into the existing opt-in MSSQL harness for future configured
  runs. Keep live Azure/container execution outside this task and disclose skips.
* Action owner: Planning parent for acceptance scope; implementation owner for tests.
* Exact resolving evidence: P02-T01 names these checks; passing server-free tests
  exercise fresh schema, missing-column migration, lookup and refresh dialect
  paths. Test discovery shows the new queue behavior cases are eligible for the
  existing opt-in SQL Server harness, with unconfigured live cases reported skipped,
  not claimed passed. No additional test-module budget is needed.
* Decision route: Direct planner correction within the required portability scope.

## Strengths and Residual Risk

* Membership is derived from the existing evaluator rather than a second semantic
  implementation. Viewer-specific context remains request-time and authorization
  remains downstream of candidate lookup.
* Shared building validation includes linked-case and package-scope dependencies;
  the research correctly warns against relying on stale process state.
* The benchmark distinguishes committed-write cold reads from same-page repeats
  and calls for disclosing write/startup/rebuild costs. It does not promise that
  remaining filtering, global ranking or sorting becomes free.
* Independent uncached parity and separate lookup/write-maintenance mutations are
  appropriate acceptance oracles. Preserve the existing semantic tests.
* Live Azure performance and operational ratification remain expressly outside
  local evidence. These accepted boundaries are not blockers.

## Questions or Blocking Evidence Gaps

* No unresolved owner choice. The findings refine execution and acceptance of
  confirmed direction; they do not request another candidate critique.

## Limitations

* No implementation was proposed or modified and no tests were executed.
* Findings concern gaps in the candidate's lifecycle and acceptance contracts,
  not claims that an unwritten implementation already contains these bugs.
* No prohibited paths or private datasets were read.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add atomic generation/fingerprint publication and hot-hit
  validity rules to P01-T02, then incorporate all three findings' resolving tests
  into P02-T01 and finalize the plan directly.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/task-queue-sql-index-327-plan.md](.copilot-tracking/plans/2026-10-16/task-queue-sql-index-327-plan.md) | Assessed final candidate plan. |
| [.copilot-tracking/details/2026-10-16/task-queue-sql-index-327-phase-details.md](.copilot-tracking/details/2026-10-16/task-queue-sql-index-327-phase-details.md) | Assessed implementation and acceptance details. |
| [.copilot-tracking/research/2026-10-16/task-queue-sql-index-327-research.md](.copilot-tracking/research/2026-10-16/task-queue-sql-index-327-research.md) | Supplied research boundary. |
| [.copilot-tracking/reviews/2026-10-16/task-queue-sql-index-327-critique.md](.copilot-tracking/reviews/2026-10-16/task-queue-sql-index-327-critique.md) | Complete one-pass actionable finding set. |

## Next Steps

Planning parent applies compatible PC-001 through PC-003 refinements and finalizes
without another critique. No user action is required. This critique stops here.
