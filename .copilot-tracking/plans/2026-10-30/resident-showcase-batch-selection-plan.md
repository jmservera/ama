---
title: Resident showcase batch selection plan
description: Bounded correction for the PR 590 SQL regression test
ms.date: 2026-10-30
---

## Task Metadata

Task: 521-pr590-batch-selection. Slug: resident-showcase-batch-selection.
Branch: chore/resident-authority-extension-521. PR 590. Refs #521.
Readiness: Ready; single critique completed and findings disposed.

## Executive Summary

Select the unique rendered view batch by its definition text instead of position.
Strengthen the empty-history assertion to verify the projected sensor home ID,
so the constant fallback cannot masquerade as optional-table coverage.

### What You May Not Know

Both SQL branches return `[]`; only the optional-table branch projects HOME-A.
The existing migration tests already use content-based single-match selection.
SQL integration remains local opt-in, not Azure or operational acceptance.

## Sources

.copilot-tracking/research/2026-10-30/resident-showcase-batch-selection-research.md,
C1-C5. User request dated 2026-10-30.

## User Decisions and Requirements

* Complete the full small-correction RPI loop with dated artifacts.
* Replace both stale calls with a small content-based helper and inspect all
  other indexed renderer uses in the module.
* Prove the empty-table test rejects the wrong batch.
* Validate from src/core with the file's existing unit tests and Ruff
  check/format check on changed Python files; record commands/results.
* Use the shared heavy lock only for heavy runs. No Azure access or push.
* Commit locally using Conventional Commits, Refs #521 and the required trailer.

## Goals

Restore meaningful empty-table projection coverage resilient to batch insertion.

## Scope and Non-Goals

Only src/core/tests/test_resident_showcase_sql.py and this task's RPI evidence.
No production SQL/runtime/configuration change, deployment, full publication gate,
issue closure, unrelated fix, or historical evidence rewrite.

## Functional Requirements

The helper returns exactly one batch containing
`CREATE OR ALTER VIEW resident_showcase.v_resident_case`.
Setup and cleanup both use it. Empty tables must yield HOME-A plus `[]`.

## Non-Functional Requirements

Keep the helper private and typed; reuse list-unpacking prior art. Fail explicitly
on absent/ambiguous view definitions. Retain SQL isolation and opt-in guards.

## Acceptance Criteria

* No indexed render(USER) selections remain in the file.
* Always-run regression tests cover view relocation and missing/duplicate matches.
* The empty-table assertion distinguishes NULL fallback from the projected home.
* Focused tests and Ruff commands pass; integration skips are stated separately.
* Independent critique and one post-implementation Review are preserved.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and validate batch selection

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement helper and semantic regression assertions

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Execute focused validation and record evidence

P01-T02 depends on P01-T01.

## Test Ownership and Coverage Lock

Canonical target and test owner: src/core/tests/test_resident_showcase_sql.py.
Generated targets: none. Exact removals: none. Maximum additions: two test
methods under RenderTests. Existing SQL method adjusted, not duplicated.
Semantic coverage: HOME-A/[] versus NULL/[] under empty tables.
Regression coverage: reordered render output and absent/ambiguous markers.
Validation: focused unittest discovery, Ruff check and Ruff format --check from
src/core, plus a bounded mock-backed negative experiment invoking the actual
empty-table method directly with HOME-A/[] (pass) and a forced migration batch
with NULL/[] (expected AssertionError). Restore patches and require a passing
rerun. This is simulated coverage, not SQL execution.
No heavy test run without flock -w 600 /tmp/ama-rpi-heavy.lock.

## Critique Disposition

Critique execution: complete, once. Original verdict: Revise. Artifact:
.copilot-tracking/reviews/plans/2026-10-30/resident-showcase-batch-selection-plan-critique.md.

* PC-001 accepted directly: details now name the actual method, controlled
  wrong-batch/fallback mutation, exact failure oracle and restoration pass.
* PC-002 rejected: its claimed prohibition on /tmp operations is not present
  in the parent's applicable instructions and conflicts with the user's exact
  authorized /tmp lock. Preserve that lock for heavy work; do not substitute
  another lock or claim SQL execution. Reuse the available pinned external
  venv for lightweight focused checks. No new installation is necessary.
* No significant/divergent user decision, second critique or scope expansion.

## Follow-Up Items

* None.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-30/resident-showcase-batch-selection-changes.md.
Independent Review completed after implementation and reconciliation:
Complete / Conformant, no findings. Review:
.copilot-tracking/reviews/logs/2026-10-30/resident-showcase-batch-selection-review.md.

Implementation reconciled: P01 complete; 13 executed unit tests pass, 27 explicit
SQL skips, both Ruff checks pass. Mock-backed actual-method fallback rejection
and old-index mutation both fail as intended; restored renderer tests pass.
No remaining active task, amendment, material divergence or source follow-up.
