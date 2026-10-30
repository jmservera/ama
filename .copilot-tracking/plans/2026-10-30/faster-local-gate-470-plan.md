---
title: Faster local gate 470 plan
ms.date: 2026-10-30
---

## Task Metadata

Task ID: 470. Slug: faster-local-gate-470. Planning status: Ready.
Details: `.copilot-tracking/details/2026-10-30/faster-local-gate-470-phase-details.md`.
Critique: `.copilot-tracking/reviews/plans/2026-10-30/faster-local-gate-470-plan-critique.md`.

## Executive Summary

Verify the already-merged features and attempt the remaining full serial versus
parallel benchmark. Add a reproducible procedure to the existing source guide;
do not change the runner or manufacture another optimization.

### What You May Not Know

The only unmet issue criterion is measured full timing in the PR. Historical
partial timing does not prove it. A foreign heavy-lock owner, inherited failures,
resource admission or unavailable downloads may prevent completed measurements.
The existing runner locks itself; an outer flock would deadlock. No push or PR
is authorized, so actual PR publication remains coordinator-owned.
Implementation admission timed out for the full serial run and corrected API
suite. No successful full timing or final receipt exists; AC4 remains unmet.

## User Decisions and Requirements

* Execute all four dated RPI phases in order for #470 on the supplied branch/base.
* Use pip, local synthetic checks and the shared heavy lock; no Azure, live
  sign-in, secrets, credential files, deployment, push or issue closure.
* Run API discovery, Ruff lint/format and mypy; retain adverse evidence.
* Commit locally with the required coauthor trailer and `Refs #470` only.

## Goals

Produce honest, reproducible full-gate timing evidence without weakening gate
scope or disturbing another task's resources.

## Scope and Non-Goals

In scope: `src/README.md` benchmark procedure, dated RPI artifacts, existing
focused tests, local serial/parallel full-gate attempts.
Non-goals: application/web changes, duplicated selection/concurrency/resume
implementation, shared-cache/image-reuse redesign, infrastructure changes.

## Functional Requirements

* Preserve existing changed-path selection, explicit partial scope, default
  partial rejection, bounded scheduling and immutable resume behavior.
* Benchmark `--all --jobs 1` then `--all --jobs 3` against identical committed
  source/base, with separate new external output directories.
* Record requested/admitted jobs, full scope, status, elapsed time and blockers.
* A comparison is eligible only when serial admits one worker, parallel admits
  more than one, both complete and verify as full, tool/resource conditions
  match, and both use the same timing boundaries. Otherwise report individual
  observations, not a measured parallel improvement.

## Non-Functional Requirements

* Shared lock excludes foreign heavy work; existing runner owns its internal
  lock with a 600-second timeout. Other heavy checks use explicit flock.
* Receipts stay external. Failure or partial completion never becomes a
  successful full-run timing. No numeric speedup threshold is invented.
* No changes to tests: exact removals none, maximum additions zero. Canonical
  regression target `tools/test_rpi_checks.py`; no generated test targets.
  Semantic evidence is actual complete full execution, not mocked timing.

## Acceptance Criteria

* AC1: changed paths select groups and receipt scope (existing regression).
* AC2: default full verification rejects partial receipts (existing regression).
* AC3: independent parallel groups preserve lock/resource limits (regression
  plus actual admitted-worker/full-run evidence where feasible).
* AC4: measured full before/after timing is recorded in the PR. Prepare
  coordinator-ready evidence; do not mark proven unless both full runs pass
  and the coordinator records the measurements in the PR.
* AC5: selection and scope tests pass.

## Sources

Research: `.copilot-tracking/research/2026-10-30/faster-local-gate-470-research.md`.
Existing guide, runner/tests, issue #470 and merged #475.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve implementation and document benchmark

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add same-candidate serial/parallel benchmark procedure

Document fresh outputs, effective jobs, lock wait versus execution, cache/order
caveats and failed-run qualification in `src/README.md`.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and measure

Depends on P01. Restore only actually missing dependencies with pip.

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Run required API and focused gate checks

Use the caller's exact API discovery paths and project lint/format/mypy.
Run gate regressions and strict tooling static checks. Keep logs external.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Attempt full serial/parallel measurement

Commit candidate before full runs; use unchanged commit/base and new external
outputs. Do not retry inherited failures or modify source outside scope.
If blocked, record exact command/result and leave AC4 unmet.
Completed disposition: full serial runner exited 1 after its 600-second
foreign-lock timeout; parallel was not launched against the same blocker.
This marker means the planned attempt was disposed, not that AC4 passed.

<!-- rpi:phase id=P03 -->
### [x] P03: Independent Review and local handoff

Depends on P02 attempt disposition.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run one independent Review and commit dated evidence

Preserve original findings. Leave human approval unchecked. Commit locally,
then require fresh final exact-head full gate before coordinator publication.
A later evidence commit invalidates earlier receipts; never label them final.
Review executed Complete, outcome Not accepted: RV-001 full timing missing,
RV-002 corrected API execution missing, RV-003 publication handoff residual.
Original Review is preserved; no fixes or second Review are part of this task.

## Dependencies

Docker and pinned local toolchain; free host lock; sufficient local storage;
package/browser/scanner downloads; current reviewed origin/main.

## Critique Disposition

One independent critique executed, verdict Revise, preserved unchanged at the
named critique path. PC-001 (Medium, planner-owned) applied directly: explicit
comparison eligibility now requires parallel admission above one worker,
comparable conditions and identical timing boundaries in P01-T01/P02-T02.
No significant/divergent decision and no second critique are required.

## Follow-Up Items

* Coordinator must put actual successful full timings in its PR and satisfy
  final exact-head publication gates; pushing is excluded from this task.
* Coordinate free heavy-lock admission for corrected API validation and a
  same-candidate serial/parallel pair. Preserve initial missing-Node and
  lock-timeout evidence; these do not establish benchmark acceptance.
* RV-001 routes full timing evidence and RV-002 routes corrected API evidence
  to distinct later research/evidence work. RV-003 retains coordinator-owned
  final publication and approval gates. No source defect was identified.

## Handoff

Planning complete, Ready after direct PC-001 disposition. Changes record:
`.copilot-tracking/changes/2026-10-30/faster-local-gate-470-changes.md`.
RPI Review is complete / Not accepted, not issue completion. P02-T01/P02 remain
unchecked. Final post-commit gate output is external at
`/mnt/ama-rpi-gates/issue470-20261030-validation/final-gate.log`; it cannot
retroactively relabel the original Review or supply the missing full pair.
