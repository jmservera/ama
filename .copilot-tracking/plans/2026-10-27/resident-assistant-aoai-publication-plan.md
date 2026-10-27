---
title: Resident assistant publication plan
ms.date: 2026-10-27
---

Task ID: 469-publication-2026-10-27.
Parent: #469 resident-assistant-aoai. Mode: automatic.

## Executive Summary

Publish the existing managed-identity assistant without changing its runtime,
Azure resources or ingress. Current main is already integrated. Preserve
original adverse evidence, archive/restore-check cleanup candidates, run
component tests and the scoped exact-head gate, retain complete coverage,
then verify and obtain independent exact-head assessment before push and a
non-draft PR. Private migration and authenticated MI smoke remain unmet.

## User Decisions and Requirements

* Full dated Research, Plan, Implement and Review for this publication step.
* Use feat/resident-assistant-aoai; fetch main and integrate only if stale.
* Acquire heavy lock with timeout zero in foreground; stop on contention.
* `git clean -fdxq` before scoped gate in a new external output directory;
  run src/core, src/api and infra unit tests.
* PR must say `Refs #469`, without closing keywords, and disclose USD20
  inside owner-approved resident USD30 plus private migration and MI gaps.
* No deployment, Azure operations, ingress edit, secrets, uv, merge or main
  push. Demo ingress deliberately remains open through 2026-12-31.
* Commit with the required Copilot coauthor trailer and privacy-safe identity.

## Goals

Establish reproducible publication evidence and open a reviewable, non-draft
PR without claiming whole-task/live acceptance.

## Scope and Non-Goals

Only dated publication evidence and local validation/publication operations.
No production changes, source refactor, dependency changes or Azure access.
Original implementation critique and Not accepted Review remain unchanged.

## Functional Requirements

Run unchanged repository gate and component unittest discovery. Preserve
all prior evidence; disclose actual SQL/integration skip status precisely.
Push only the approved branch without force; PR base main.

## Non-Functional Requirements

Clean exact committed head/base; new external output; preserved failed
attempts; no lock bypass, data/service fallback or weakened check. Archive
and restore-check the finite cleanup set and full tracking snapshot first.
No shared Docker cleanup, container takeover or global configuration edits.

## Acceptance Criteria

* Required component suites pass, with existing opt-in skips distinguished
  from actual SQL integration executed by the gate.
* Requested changed-path receipt passes; its selected groups cover the
  complete required matrix, or a separate complete gate also passes.
* Fresh main fetch, final clean-head receipt verification and independent
  exact-head assessment precede push. No new commit afterward.
* Authorized branch pushed and non-draft main-targeting PR exists with the
  required scope, evidence, budget and unmet-items wording.
* Human and hosted review remain pending; no merge or deployment occurs.

## Test Ownership and Change Limits

Existing component tests and gate remain canonical. Test removals: none.
New tests: zero. Source/generated target additions: none. Tracking evidence
only. Semantic coverage is unchanged and actual SQL must exercise the
already-written accounting tests. Component discovery supplies regression
coverage. All heavy output and final receipts stay external.

## Phase Checklist

<!-- P01 -->
### P01: Preserve and prepare

* [x] P01-T01: Finish critique; preserve finite clean selection; commit
  publication evidence with owner privacy-safe identity.

<!-- P02 -->
### P02: Validate

* [x] P02-T01: Archive/restore-check caches and tracking; run authorized
  clean; hand off lock to foreground scoped gate at timeout zero.
* [x] P02-T02: Run component unit suites, retain full required gate coverage,
  record exact results, amendments and failures externally and in changes.

<!-- P03 -->
### P03: Review and publish

* [x] P03-T01: Execute one independent publication Review and reconcile
  dated plan/details/changes/state without regrading parent acceptance.
* [ ] P03-T02: Commit final evidence; rerun gate if head changed; fetch main,
  verify final receipt, obtain independent exact-head assessment, push
  branch and open non-draft PR. If anything required fails, do not publish.

## Critique Disposition

Executed once, verdict Revise; original critique retained at
`.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-publication-critique.md`.

* PC-001 rejected for this executor: the asserted prohibition on temporary
  paths does not exist in the parent execution boundary, and conflicts with
  the caller's explicit `/tmp/ama-rpi-heavy.lock` instruction. Actual initial
  lock acquisition already succeeded. No runner/lock bypass is required.
* PC-002 rejected as factually inapplicable to execution: `main()` explicitly
  selects `required_scope="partial"` for automatic verification when the
  selected groups are not the complete matrix (tools/rpi-checks.py:2263).
  `--required-scope` controls standalone receipt verification only. Clarified
  that standalone partial verification, if needed, uses that flag, while
  final publication always requires default full verification.

Both dispositions are parent-owned and evidence-backed; no new user choice
or second critique. Plan and phase details are Ready for Implement.

## Follow-Up Items

Private SQL migration and authenticated managed-identity resident smoke are
explicitly outside this task. Human accessibility/privacy/live acceptance
and hosted checks remain separate. Do not start follow-up work automatically.
Child Review RV-001 (Medium) routes live integration; RV-002 (Low) routes
hosted/human acceptance, with no established implementation defects.

## Handoff

Research, Plan, P01/P02 and the one independent child Review are complete.
Review execution Complete, outcome Residual work, no blocking source defect.
P03-T02 deliberately
remains unchecked until final evidence commit, fresh gate/verification,
exact-head assessment, push and PR are observed. This is post-Review
publication maintenance, not additional source implementation or a Review
loop. Private migration/MI and hosted/human approval stay separate.
Fresh fetch after Review found main advanced to d455d67d (documentation,
tracking and rubric score only); integrate by ordinary merge, preserving
unmerged local commits and both knowledge-log additions, then rerun the gate.
Changes target:
`.copilot-tracking/changes/2026-10-27/resident-assistant-aoai-publication-changes.md`.
Research:
`.copilot-tracking/research/2026-10-27/resident-assistant-aoai-publication-research.md`.
