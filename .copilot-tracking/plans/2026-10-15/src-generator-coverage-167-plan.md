---
title: Generator coverage baseline plan
description: Issue 167 bounded engineering closure plan
ms.date: 2026-10-15
---

Task #167. Slug: `src-generator-coverage-167`.

## Executive Summary

Add a read-only, dependency-free coverage report under core synthetic tooling.
It checks the merged inventory's routing contract without claiming generated
data conformity or owner approval. Reuse existing generator regression tests.
No generator output, private data, SQL, AI enablement or deployment is changed.

## User Decisions and Requirements

* Work only on the supplied branch/worktree and follow ADR 0006.
* Run the full RPI loop; commit research, plan, details, critique, changes and review.
* Reuse merged needs/generators; do not invent owner scope, data or approvals.
* Locally run src suites, ruff, mypy and synthetic app smoke before CI.
* Update knowledge index/log, commit with privacy-safe identity and trailer,
  push and open a main-target PR with `Refs #167`.
* Never touch `.env`, `.vscode`, issue exports or add code to `mvp/`; pip only.

## Sources and Readiness

Research: `.copilot-tracking/research/2026-10-15/src-generator-coverage-167-research.md`.
C1-C6 and W1-W4 support this slice; research is executed and Ready.
Inventory v1.2.0 remains awaiting owner review.

## Goals

Make gap routing reproducibly inspectable and reject malformed closure records.
Distinguish an engineering baseline from application/data acceptance.

## Scope and Non-Goals

New core synthetic metadata module, its tests, related README/index/log updates.
No private files are read; CLI takes only an explicit public inventory path and
prints deterministic JSON to stdout. No implicit repository lookup or data writes.
No child data-generation implementation, policy decisions or live deployment.

## Functional Requirements

* Validate nonempty unique SN IDs, supported coverage/closure values, nonblank
  notes, valid nonduplicate positive issue references for routed/delivered rows.
* Every partial/missing row needs a child route or explicit deferral; delivered
  may only describe covered rows. A deferral must contain a rationale.
* Require all four convention declarations and retain pending owner items.
* Emit source version/date/status, all rows and coverage totals in stable order.
* Explicitly state routing validation does not establish output conformance,
  owner approval or application acceptance. Invalid input exits nonzero with
  an explicit diagnostic, not a partial success report.

## Non-Functional Requirements

Standard library only, strict typing, core imports no workload. No SQL added.
Read-only metadata input/output means ZF_DATA generation paths stay unchanged.
Preserve AI proposal/release/human/consent gates; local smoke is not real inference.

## Acceptance Criteria

* [x] Engineering baseline includes all 13 needs: 2 covered, 11 partial, 0 missing.
* [x] Malformed routes, IDs, notes, deferrals and missing conventions fail.
* [x] Existing generator tests still pass without private register access.
* [x] All requested local checks recorded with honest skips/blockers.
* [x] Owner-dependent and unproduced evidence remain unticked in PR #312.

## Phase Checklist

<!-- P01 -->
### P01: Metadata coverage gate
* [x] P01-T01: Implement validator/report and semantic negative tests.
* [x] P01-T02: Document usage, provenance limits and residual criteria.

<!-- P02 -->
### P02: Validation and delivery evidence
* [x] P02-T01: Run src suites, ruff/format/mypy, report CLI and local app smoke.
* [x] P02-T02: Record one review, then commit/push/open PR; do not merge (PR #312).

## Test Ownership and Change Budget

Canonical input: existing needs-inventory.json, unchanged. Generated target:
stdout only. Test owner: src/core/tests/test_generator_coverage.py; maximum one
new test module and one production module. Exact removals: none.
Semantic coverage: valid/invalid metadata and report shape, stable ordering,
CLI errors. Regression coverage: all existing src suites and generator tests.
Validation: commands and results in changes artifact and PR.

## Critique Disposition

Executed once: `.copilot-tracking/reviews/2026-10-15/src-generator-coverage-167-plan-critique.md`.
Verdict Revise, PC-001 (Medium) addressed directly: all new test scratch uses
the ignored `src/core/tests/__pycache__/` parent, and validation/smoke uses
`src/core/.venv/tmp/` with explicit TMPDIR/ZF_DATA. No system-temp fallback or
new scratch framework. No owner decision required. Plan now implementation-ready;
no second critique.

## Follow-Up Items

Owner approval and row-owner ratification; SN-01 regeneration scope/source;
SN-03/08/09 scope/volume; per-record synthetic convention reconciliation;
#103 profiles/workflows and #144 full-volume SQL/application evidence.
No follow-up is part of active implementation acceptance.

## Handoff

Details: `.copilot-tracking/details/2026-10-15/src-generator-coverage-167-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-15/src-generator-coverage-167-changes.md`.
Implementation, validation and parent publication complete. One Review executed
Complete, outcome Residual work; PR #312 uses Refs #167 and retains unmet items.
No merge, second Review or follow-up implementation was performed.
Local validation: 903 src tests, 97 skipped; all five lint/format/mypy checks
pass; 25 migration tests pass after restoring missing tool dependencies.
CLI and actual fictional SQLite API smoke pass. Docker socket denied;
real inference/SQL Server/Azure/owner/human acceptance not produced.
