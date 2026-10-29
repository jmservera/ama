---
title: IoT Hub PR 557 fix cycle 1 plan
ms.date: 2026-10-29
---

## Task Metadata

* Task ID: 140-184-pr557-fix-cycle-1
* Task slug: iot-hub-live-140-pr557-fix-cycle-1
* Planning status: Executed locally; independent critique Complete / Pass; original Review Complete / Residual work
* Phase details: .copilot-tracking/details/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-plan-critique.md

## Executive Summary

Added compiled behavioral coverage for the existing live ama/UK South guard and mutations that prove regressions are rejected. Added explicit two-message, one-per-second, 60-second operator settings and the October 31 UTC authorization cutoff beside hub-only activation guidance. Preserved existing Bicep and runtime behavior; implementation and original evidence committed locally as dd69200b after requested checks and one independent Review.

### What You May Not Know

RunBudget defaults allow 100 messages and its validation permits larger limits. It does not enforce a calendar cutoff. The operator must verify remaining UTC authorization time, not rely on the per-run deadline. This fix does not close either parent issue or repair historical live/publication blockers.

No unresolved implementation decision. Complete local gate failed API required-integration skip admission; browser/MSSQL groups were blocked. No valid publication receipt is established; focused checks do not substitute for that gate.

## Sources

* .copilot-tracking/research/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-research.md: C1-C8, executed and Ready.
* Owner request and PR #557 Copilot comments: two bounded findings; rubric score explicitly excluded.

## User Decisions and Requirements

* First git pull --rebase; completed on the clean active topic branch, already up to date.
* Complete Research, Plan, Implement and Review with dated artifacts.
* Evaluate live resource-group and requested/actual hub-location guards, minLength constraints and rejecting bypass mutations.
* State required RunBudget values and operator responsibility for the October 31 cutoff.
* No Azure operations, secrets, manual score edits or push.
* Use /tmp/mv; infra tests, Ruff check/format check and relevant unittest modules from src/api with PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
* Commit locally with the supplied Copilot coauthor trailer.

## Goals

Prove all live scope predicates fail closed in compiled templates and remove ambiguity from exercise instructions.

## Scope and Non-Goals

Source changes limited to infra/tests/test_iothub_module.py and src/api/README.md. Dated RPI artifacts are separate. Do not edit the already-correct live Bicep, runtime budgets, dependencies, scorecards, historical evidence, credentials, Azure resources or unrelated defects.

## Functional Requirements

* Reusable live-scope assertion evaluates compiled group/location expressions with independent requested and actual locations.
* Cases include valid ama/uksouth/uksouth; non-ama; matching non-UK requested/actual; UK requested/non-UK actual; non-UK requested/UK actual. Expected group and location admission are independent.
* Each guard input exists, its nested template parameter has minLength=1, and all deployed children remain guard-dependent.
* Mutation tests use the same assertion against deep copies: constant group/location success; bypass either location clause or conjunction; remove either input; weaken/remove either minLength; remove either child dependency.
* Guidance sets max_messages=2, max_per_second=1.0, max_seconds=60.0 with required owner/cost/alert references. Operators check UTC time and enough remaining window before each run and stop before 2026-11-01T00:00:00Z (through 31 October UTC); code does not enforce this date.

## Non-Functional Requirements

No production behavior change or networked tests. Use existing evaluator/helpers and formatting, no new dependencies. Preserve original critique and Review outcomes. Never claim live or whole-issue acceptance.

## Acceptance Criteria

1. Compiled live behavior passes all independent valid/invalid cases and every designed bypass mutation is rejected by an assertion.
2. Both minLength constraints and both child guard dependencies are covered.
3. Operator documentation names all requested limits and distinguishes calendar responsibility from runtime enforcement.
4. Required infra, Ruff and relevant unit checks pass or actual failures are recorded without concealed skips.
5. One critique, one Review and dated changes/state evidence persist; local commit has privacy-safe author/committer and required trailer, no push.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Address both bounded review findings

Dependencies: completed Research and dispositioned critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add live-scope behavioral and mutation tests

Follow existing assertion/deep-copy pattern; do not modify template behavior.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Document budget and cutoff

Independent of P01-T01; adjacent to DeviceActivation guidance.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and preserve local handoff

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run targeted/full infra and relevant static/unit checks

REQUIRE_AZ_BICEP=1 prevents missing compiler from becoming an accepted skip. Offline Bicep compilation only. Infra Ruff uses existing isolated E,F,I,B,UP py312 line-length100 policy. API Ruff runs project scope. API unittest selectors: test_iot_stream, test_sensor_ingestion, test_sensor_stream, test_resident_sensors using caller PYTHONPATH.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence, run one Review, commit locally

Resolve account through gh api user; repository-local noreply email for author/committer, coauthor trailer. No push. After committing original evidence, attempt complete local gate with --all, fetched origin/main and a new external directory under nonqueued shared-lock admission. Preserve failures and keep final receipt external; no cloud fallback, skip token or hosted acceptance claim.

## Test Ownership and Change Limits

Canonical source: existing live Bicep and RunBudget remain unchanged. Test owner: infra/tests/test_iothub_module.py. Add at most two test methods and one assertion helper; removals: none. Generated compiled/mutation objects stay in memory, logs/receipts external. No new test framework or dependency. Semantic coverage is evaluated guard outputs plus parameter constraints/dependencies; runtime regression coverage is the existing four unit modules.

## Dependencies

Existing /tmp/mv Python/Ruff available; offline az bicep compiler required by current tests. Full gate requires shared-lock admission and existing browser/SQL/scanner prerequisites, unrelated live authority remains blocked.

## Critique Disposition

Exactly one final-candidate critique executed: Complete / Pass, zero findings, no significant or divergent decisions required. Original critique preserved at the metadata path. No second critique.

## Follow-Up Items

* Historical live and full-gate blockers remain owned by the parent task; not acceptance criteria for these two local review corrections.
* Current full gate reproduces the parent API discovery/admission mismatch: 1338 API tests exit0 with318 skips, required SQL/browser skips are rejected, browser/MSSQL groups blocked. Distinct gate follow-up owns correction without weakening integration policy. Final evidence commits invalidate prior receipt identities; any future publication requires a new complete exact-head gate and independent exact-head assessment.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-changes.md. All source/check/local-lifecycle markers complete, not a full-gate pass. Targeted infra18, full infra470 and relevant unit94 pass; infra/API Ruff check and format check pass after one formatter correction. One original Review Complete / Residual work found no source defects; its lifecycle and inherited-parent routes are preserved. User explicitly authorized this full cycle; manual mode, no persistent automatic session, no push. Publication remains blocked.
