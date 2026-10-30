---
title: Employee progress dashboard 533 plan
description: Scoped current-main acceptance completion
ms.date: 2026-10-30
---

## Task Metadata

* Task ID: 533
* Task slug: employee-progress-dashboard-533
* Planning status: Ready; single critique completed, finding disposition recorded
* Details: .copilot-tracking/details/2026-10-30/employee-progress-dashboard-533-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/employee-progress-dashboard-533-plan-critique.md

## Executive Summary

Preserve the already implemented dashboard and archive. Add precise regressions for filtered multi-page traversal at a non-default page size and rendered boundary controls. Execute fresh API/unit/static and local Playwright/axe checks, preserve original Review and commit locally without pushing.

### What You May Not Know

Issue #533's first four boxes are already checked and #540 merged. The remaining owner comment asks for deployed-site checks, excluded by this local-only task. Local success cannot establish that acceptance. Required complete final gate also remains distinct from component checks.

## User Decisions and Requirements

* Full ordered RPI loop with dated artifacts; exact #533 scope.
* Use assigned branch and base 5634f9a077d175a931c15e3400114665d8c071ee; no push.
* No Azure, deploys, live sign-in, credential files, secrets, private data or uv.
* Preserve Fluent 2 foundations, native semantics, WCAG baseline, plain language, non-colour signals and reduced motion.
* Run requested full API discovery, Ruff, format, mypy and real local Playwright/axe under flock -w 600 /tmp/ama-rpi-heavy.lock.
* Commit with authenticated privacy-safe identity and required Copilot trailer; Refs #533 only.

## Goals

* Prove the existing in-scope behaviour on the supplied current-main baseline.
* Close narrow regression gaps without unrelated production changes.

## Scope and Non-Goals

In scope: src/api tests, existing progress browser checker, related README, dated evidence. Production changes only if fresh checks expose a directly related defect, recorded as an amendment before editing. No redesign or framework change, historical artifact rewriting, issue mutation or remote publication.

## Functional Requirements

* Preserve synthetic-only daily/weekly flow, backlog, median/p90, journey, overdue/stalled, team and AI usage with date range and demonstration labels.
* Every chart retains its semantic same-value table.
* Archive filters compose; stable pages contain every matching record exactly once and preserve URL state.
* Empty, first, final and beyond-final pages expose correct controls and canonical page state.

## Non-Functional Requirements

* All component checks pass; no browser JS errors or axe violations in exercised states.
* Retain native semantics, keyboard focus, 320/390/1280 reflow and reduced motion.
* Treat any unavailable full-gate prerequisite as a blocker, not a component success or skipped acceptance.

## Acceptance Criteria

* AC1: daily/weekly flow plus at least four statistics.
* AC2: every chart has a table alternative.
* AC3: filtered, paged archive, URL state and boundary tests.
* AC4: figures labelled demonstration data.
* AC5: browser and unit checks pass locally; explicitly separate outstanding deployed-site evidence.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-30/employee-progress-dashboard-533-research.md (executed, Ready).
Changes: .copilot-tracking/changes/2026-10-30/employee-progress-dashboard-533-changes.md, implementation-owned.
One independent final-candidate critique precedes implementation; one independent Review follows completed checks.

## Sources

* Research C2-C7 and W1-W2.
* src/api/README.md progress guide and src/README.md complete local gate.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Strengthen exact acceptance coverage

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add filtered custom-limit paging regression

Add one inherited test method in ProgressDashboard, run against JSON and SQLite, checking filtered non-default-limit traversal, first/final/beyond pages, exact IDs, counts and no overlap. Do not remove any tests.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Assert rendered page boundaries

Extend existing browser flow to assert first/final/empty unavailable links, table counts, preserved filters and beyond-empty URL canonicalization. Update related README coverage description. No web runtime edits expected.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and preserve evidence

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute component validation

Under the shared heavy lock, use existing /tmp/mv/bin Python (system Python lacks tools), caller's exact source/fixture paths, complete API discovery, Ruff check/format and mypy. Fetch only public pinned axe 4.10.3 into a fresh external evidence directory; verify SHA256 through existing checker. Run local constructed-data progress browser checker; no credential files or live sign-in.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Review, commit and attempt final gate

Refresh guidelines, independently review exact diff and evidence once, preserving original outcome. Reconcile plan/details/changes/state; resolve gh api user and local noreply identity, commit with required trailer. Fetch main read-only, attempt complete tools/rpi-checks.py --all with external output; runner already owns shared lock, do not recursively acquire it. Do not push. Report actual receipt status and every unmet acceptance.

## Dependencies and Test Ownership Lock

#529 is merged. Test owner: existing ProgressDashboard and checks.progress_browser_check. Exact removals: none. Maximum additions: one Python test method inherited by SQLite and six logical browser boundary assertions in the existing flow. Canonical targets: src/api/tests/test_progress_dashboard.py, src/api/checks/progress_browser_check.py and src/api/README.md. Generated targets: new external browser/gate outputs only. Semantic coverage remains existing metric/API tests; additions are archive paging regressions. Validation evidence includes full commands, exit results, actual counts, external paths and acceptance matrix.

## Critique Disposition

Single critique executed, original verdict Revise preserved. PC-001 (planning parent): rejected as inapplicable to this parent's execution context and conflicting with confirmed caller direction. The critique asserts a temporary-system file-operation prohibition not present in the parent's instructions. The caller explicitly requires /tmp/ama-rpi-heavy.lock, the repository documents /tmp/mv and external outputs, and the locked 41-test research baseline already executed successfully. Do not copy a worker-specific restriction into parent policy. Continue with the explicitly requested shared lock, existing interpreter and fresh external outputs; no replacement lock or tooling change. Missing real prerequisites still block the complete gate. Resolving evidence: user request, research C5/C7 and actual successful baseline command. No second critique.

## Follow-Up Items

* Owner/coordinator: deployed employee-site dashboard/archive check; outside explicit local-only permission.
* Coordinator: current-main integration and exact-head receipt assessment. Read-only fetch found origin/main 9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19; preserve assigned base and branch, no automatic rebase. Full-gate status belongs to external final-gate evidence, never inferred from component checks.

## Handoff

Source implementation and all plan execution tasks complete; single independent Review completed. Component result: 1372 tests, OK with 318 explicit skips; Ruff/format/mypy passed; actual local browser and 11 axe states passed. Full gate was attempted but is blocked by the newer-main/base mismatch. Publication remains coordinator-owned.

Review executed once: Complete / Residual work, no implementation defects, RV-001/RV-002 retained. P02-T02's post-Review execution is recorded by the local candidate commit and external failed preflight logs, not a second Review. No full receipt exists. Consult changes for exact external paths and limitations.

Final P02-T02 disposition: executed, local candidate 01c0e9405228686278dea36349397322c39cc45f committed with required identity/trailer. Complete gate attempted, but BLOCKED before execution: reviewed base differs from freshly fetched origin/main. The earlier ignored-cache blocker was resolved by finite manifest, complete tracking/cache archive, verified full readback, selected-file restore/hash checks and protected-source checks before/after removal. No receipt exists. All plan execution markers are complete; the gate itself did not pass. This final administrative evidence is committed separately without rewriting the original critique/Review. Coordinator must resolve newer-main lineage and rerun the complete gate; no automatic rebase or push.
