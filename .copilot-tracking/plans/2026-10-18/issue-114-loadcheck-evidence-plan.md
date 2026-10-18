<!-- markdownlint-disable-file -->
# RPI Plan: issue-114-loadcheck-evidence

## Task Metadata

* Task ID: 114
* Task slug: issue-114-loadcheck-evidence
* Plan date: 2026-10-18
* Planning status: Ready after direct dispositions of the single critique
* Phase details: .copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-18/issue-114-loadcheck-evidence-plan-critique.md

## Executive Summary

Prevent missing observations and failed workers from producing passing loadcheck evidence.
Keep the existing classes, p95 limits, default mix and valid CLI unchanged. Make two focused
source/test changes; preserve every original independent finding in immutable critique/Review.

### What You May Not Know

The existing queue benchmark tests another contract. Passing local harness tests cannot establish
Azure latency, cost, full NFR-002 or any whole-issue acceptance. Work already started may finish
after the monotonic deadline; no new cancellation behavior is planned.

### Unresolved Decisions or Blockers

None for the bounded implementation. Original critique Revise preserved; PC-001 and PC-002
dispositions below resolve the plan without repeating critique.

## User Decisions and Requirements

* Full ordered Research, Plan with one independent critique, Implement, one original independent Review.
* Exact base f91353169756dc41ebbcca944bdd3f44f7c04b89, branch fix/loadcheck-evidence-114; no unilateral integration.
* Correct only AC2 evidence trust, not AC2 completion, ledger, restore/deletion or human approval.
* No private data/.env/support, Azure/IAM/Graph changes, deployment, spend or actual AI.
* Preserve adverse original reports; separate correction receipts, at most two source correction cycles.
* Commit all task artifacts and delivery, publish PR to main with Refs #114 only, stop for coordinator.

## Goals

* Trustworthy absent/failed evidence and unchanged successful measured behavior.
* Deterministic offline regression and mutation evidence covering the actual CLI exit contract.

## Scope and Non-Goals

In scope: loadcheck.py, new focused src/core/tests/test_loadcheck.py, task-owned RPI artifacts.
No test removals. No new docs page, component-guide update (existing command remains accurate),
KB changes, web edits, queue redesign, SQL/runtime-image contract changes or unrelated cleanup.

## Functional Requirements

* Validate finite positive duration, positive integer sessions and 1 <= writers <= sessions before
  accessing store workload. Validate positive homes and nonempty seed cases before grow/store.
* CLI maps invalid duration/homes/empty workload to argparse error before open_store; direct API
  uses explicit ValueError. Keep existing options and default values.
* Missing class: n=0, p50/p95/max=None, within=False; pct([]) returns None, never invented zero.
* Record worker startup RuntimeError and unexpected pre-request session exceptions explicitly in
  sanitized error_kinds, retaining request-kind failures and original error count semantics.
* Keep successful samples for healthy workers/classes; overall errors cause nonzero CLI.
* Use monotonic for shared deadline, perf_counter for request timing; measure completion before
  acquiring aggregation lock so lock contention does not inflate individual latency.

## Non-Functional Requirements

* No raw exception text, traces or private identifiers in result. Existing type-only error format.
* No blanket successful-class failure when another worker fails. Preserve list/detail/write and
  p95 <= 1/1/2 seconds; max remains descriptive, not a new gate.
* No new runtime dependencies, abstractions or workload configuration.
* CLI tests clear environment and use constructed temporary fixtures plus patched factory only.

## Acceptance Criteria

* Zero/negative/nonfinite duration, zero sessions, invalid writer counts, nonpositive homes and
  empty workload reject explicitly; CLI invalid inputs never initialize store.
* No required observations cannot pass, including workers that start after deadline.
* Worker start/selection/request exceptions fail overall; error messages remain private.
* Overlimit p95 fails, exact-limit and all-required-class success pass deterministically.
* CLI returns 0 only for complete error-free within-limit reports and 1 for incomplete/failing runs.
* Focused/coupled core suites, configured Ruff and mypy, old-source regression/mutation probes and
  git diff --check recorded exactly. No cloud or operational acceptance from mocks.

## Implementation Context Record

| Item | Record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-18/issue-114-loadcheck-evidence-research.md, Ready, C1-C8 |
| Details | .copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-18/issue-114-loadcheck-evidence-plan-critique.md, original Revise; parent dispositions complete |
| Changes | .copilot-tracking/changes/2026-10-18/issue-114-loadcheck-evidence-changes.md, implementation-owned |
| Continuation | Authorized automatic parent, after one critique dispositions |

## Sources

* Research C1-C8; core README/pyproject and source CI; issue #114 literal criteria.
* ADR 0001 Database and ADR 0002 system-of-record/audit decisions; PRD NFR-002 target boundaries.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and prove bounded evidence contract

Dependencies: completed Research and one final-candidate critique with resolved dispositions.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement harness guards and failure accounting

Change only canonical loadcheck.py: validate, null missing metrics, monotonic deadline, worker
failure accounting. No generated targets. Details P01-T01.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add focused regressions and run local checks

Depends on P01-T01. Test ownership: test_loadcheck.py exclusively for introduced/fixed behavior;
no removals, maximum 16 test methods using subtests for parameter cases. Cover semantic good path
and regressions, actual main() exit result, sanitized failure categories and concurrent aggregation.
Run existing coupled test_sqlreads/test_sqlstore/test_taskqueues/test_sqlqueues and queue benchmark
when practical. Run configured core Ruff lint/format and mypy. Old-source/new-tests red probe must
isolate imports without modifying checked-out source. Targeted mutations challenge guards, missing
observations and error/latency exit predicates. Details P01-T02.
Explicit timing tests distinguish monotonic from wall clock, shared cutoff and late workers,
completion of an entered cycle, and aggregation wait exclusion. Mutate clock selection and
completion placement. Validation scratch stays in .copilot-tracking/.issue-114-tmp, is removed
after use, and is never committed. CLI tests override tempfile.tempdir inside clear environment.

<!-- rpi:phase id=P02 -->
### [ ] P02: One independent Review and publication

Depends on P01 completion and reconciliation of plan/details/changes/state.

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Preserve original independent Review

Pin candidate commit and source SHA-256. Fresh independent worker activates rpi-review, writes
only designated review artifact; exactly one original Review. Correct findings if any in separate
receipts, max two source cycles, never rewrite originals or claim independent corrected acceptance.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Reconcile, commit and publish

Depends on P02-T01. Resolve GitHub user, set local privacy-safe identity, Conventional Commits
with required Copilot trailer. All task artifacts tracked. Report base/candidate/published head,
remote main movement and unmet gates. Push normally and create main PR, Refs #114 only.
Stop for coordinator's exact-head review, no merge/rebase/force-push.

## Dependencies

No issue dependency. #113 is hierarchy only. P01-T02 depends on P01-T01; P02 follows P01.
No dependency on concurrent #153, whose files remain untouched.

## Critique Disposition

Exactly one critique executed, original verdict Revise, SHA-256
6f40180f9bff6315e3a0296310a61ece41092f943c41b1d755dd16d293cd7012.

| Finding | Owner and disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Planning parent: applied directly | P01-T02 and details add distinguishing timing assertions and two mutants |
| PC-002 | Planning parent: adopt explicit scratch isolation | P01-T02 and details specify local root, scoped tempfile override and cleanup |

PC-002 cites a no-system-temp instruction that is not present in the parent's supplied execution
instructions. That authority claim is not adopted; the useful task-local isolation recommendation
is independently adopted under the caller's explicit safety boundary. No user decision required.
No second critique. No new mypy exemption: type canonical functions at their dynamic Store boundary.

## Follow-Up Items

* Issue #114 remaining live load/cost, annual ledger verification, recovery/deletion and human
  acceptance remain outside this slice; owner/coordinator controls future authorized work.

## Handoff

P01 complete and review-ready; authorized parent pins candidate and advances to the single
original independent Review. P02-T01/T02 remain active, not yet claimed complete.
Changes record: .copilot-tracking/changes/2026-10-18/issue-114-loadcheck-evidence-changes.md.
