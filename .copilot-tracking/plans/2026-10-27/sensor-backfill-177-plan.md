---
title: Sensor historical backfill stacked delivery plan
ms.date: 2026-10-27
---

Task: #177 / sensor-backfill-177. Status: Ready for bounded implementation.

## Executive Summary

Deliver reviewable exercise components on separate child branches, preserving
the current generated stock, legacy payloads and monitoring exclusions. Stop
#178 at owner source/reuse approval and #183 at the consumer identity decision.
Parent remains a draft coordination PR: no child PR or local branch merge is
authorized. Its one scoped gate covers only its committed evidence/docs, not
unintegrated child implementations. Actual two-year climate-grounded backfill
and whole-parent acceptance remain blocked.

## User Decisions and Requirements

* Full ordered Research, Plan, Implement, Review; dated artifacts in all five roots.
* One child branch per #178/#179/#180/#181/#183 from feat/sensor-backfill-177.
  Child PRs target parent; parent alone targets main. Do not merge.
* Unit/focused checks only for children. One parent `--changed` gate after
  `git clean -fdxq`, zero lock wait, foreground, external output.
* ADR 0006 src packages, tests outside packages; no new mvp code, uv, private
  data, .env, secrets, Docker or Azure activity.
* Stable existing home lineage, deterministic synthetic inputs, no blame.
* Owner decision blocks only that child; comment once; no unsupported ticks.
* GitHub noreply identity, required coauthor trailer, Refs references only.

## Goals

Provide small independently testable projection, dated retrofit and household
variation primitives without claiming an integrated historical generator.

## Scope and Non-Goals

In scope: core synthetic modules, focused tests, component documentation,
child evidence, blocker comments, unmerged draft PRs. Out of scope: importing
PR #425, changing consumer schema/identities, reading a full private register,
inventing household/measure records, creating consent, actual SQL writes,
full-stock generation and child integration by merge.

## Functional Requirements

* #179: typed, versioned exercise indoor projection by dwelling/age/construction;
  deterministic supplied outdoor input; explicit bounds and validation.
  Extract/reuse existing equation where compatible, preserving legacy values.
* #180: immutable explicit synthetic measures keyed by stock home ID and UTC
  completion instant; effect applies inclusively from completion, no effect
  without measures; explicit supported kinds and exercise magnitudes.
* #181: per-ID/seed household schedules, setpoints, ventilation and moisture
  variation with documented distributions; declined/unknown yields no model
  observations; neither inferred resident behaviour nor a fault judgement.
* #178/#183: evidence-only child branches describe exact blockers. No new
  source adoption and no alternate ingestion path.

## Non-Functional Requirements

No dependencies added. No resident data. No default generator behaviour shift.
Errors explicit. Type-safe new modules. Stable seed and home ID inputs, no
wall clock. Each child remains reviewable until owner integration.

## Acceptance Criteria

* Bounded code and tests exist on eligible children; each has a PR to parent.
* Tests directly cover formulas/bounds, deterministic results, timing, unknown
  measures, monitoring exclusion and unchanged legacy projection.
* Each original issue criterion is audited, not automatically ticked.
* Parent PR explicitly states unresolved dependencies and limited gate scope.

## Phase Checklist

<!-- P01 -->
### P01: Preserve source decisions and delivery boundaries

* [x] P01-T01: Commit parent foundation before branching any child.
* [x] P01-T02: Create evidence-only #178 child and one blocker comment.

<!-- P02 -->
### P02: Implement isolated exercise components

* [x] P02-T01: #179 extract typed projection and exercise contract/tests.
* [x] P02-T02: #180 add dated per-home measure factor/tests.
* [x] P02-T03: #181 add neutral household profiles and consent-aware series/tests.
* [x] P02-T04: #183 record ingestion incompatibility and one blocker comment.
* [x] P02-T05: Focused checks, commits, pushes and child draft PRs to parent.

<!-- P03 -->
### P03: Review and parent publication

* [ ] P03-T01: One independent post-implementation Review across all child diffs.
* [ ] P03-T02: Reconcile evidence; commit parent candidate and original Review.
* [ ] P03-T03: Exact cleanup dry-run, then authorized clean; one scoped gate,
  receipt verification where possible, parent draft PR; report hosted checks.

## Test Ownership and Locked Boundary

Core owns semantic tests. Remove no tests. Add at most three test modules:
`test_indoor_projection.py`, `test_retrofit_effects.py`,
`test_household_conditions.py`. Canonical code is under
`src/core/src/zava_forward/core/synthetic/`; generated targets: none.
Run each new module plus existing backfill/stock/fault/plausibility/determinism
selectors for #179; Ruff and mypy on new modules and tests. Do not run full
package/all-tier checks per child. Gate selection may require Docker for
runtime paths: do not run it on unintegrated child source or claim those paths
were covered by the documentation parent gate.

## Dependencies and Blockers

Owner reuse approval and approved paired two-year climate input; #425 pending.
Stable stock identity compatibility with #110 is unresolved. Full existing
60,000-home stock remains private and is not read. No measure date is invented.
Parent/child integration awaits owner action because merge is prohibited.

## Follow-Up Items

1. Owner source/reuse decision (#178/#425), then grounded projection validation.
2. Owner consumer identity decision (#183/#110/#188), then actual writer integration.
3. Owner integration/review of children, then aggregate scoped gate and parent readiness.

## Critique Disposition

One final-candidate critique executed, original verdict Revise, seven findings.
No second critique.

| Finding | Disposition | Resolution |
| --- | --- | --- |
| PC-001 High | Accepted | Fingerprint extracted helper, record model metadata, test byte sensitivity and manifest revision. |
| PC-002 High | Accepted | Use visible `git clean -ndx`; require no unknown/unpreserved deletion candidates before authorized clean. |
| PC-003 High | Rejected, erroneous premise | Worker asserted a /tmp prohibition absent from caller/parent instructions. Caller explicitly requires /tmp lock and new external output; current environment permits both. No gate bypass or runner edit. |
| PC-004 Medium | Accepted | Foundation precedes every child; all fork the recorded common SHA. |
| PC-005 Medium | Accepted | Public projection accepts -80..60 C, RH 0..100, supported bounded factors only; rejects nonfinite/singular values explicitly. Intervals are exercise API support, not historical facts. |
| PC-006 Medium | Accepted | Original Review findings get severity, affected SHA and disposition. Substantive defects block acceptance, even for draft components; later repairs are not independently reviewed here. |
| PC-007 Medium | Accepted | Successful receipt only, explicit `--required-scope partial`, current fetched base; stale/failed receipt blocks with no second gate. |

## Handoff

Details: `.copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md`.
Changes will be `.copilot-tracking/changes/2026-10-27/sensor-backfill-177-changes.md`.
