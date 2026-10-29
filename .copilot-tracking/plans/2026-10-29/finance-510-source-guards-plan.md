<!-- markdownlint-disable-file -->
# RPI Plan: Finance review source guards

## Task Metadata

* Task ID and slug: finance-510-source-guards
* Plan date: 2026-10-29
* Planning status: Complete; implementation, requested validation, independent Review and local commit delivered
* Phase details: .copilot-tracking/details/2026-10-29/finance-510-source-guards-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/finance-510-source-guards-plan-critique.md

## Executive Summary

Block working-review disclosure when any retained source is missing, even if a
schema is stale or a field was rejected/replaced. Count only currently usable,
field-permitted staged alternatives as conflicts. Keep original history intact.

### User Decisions and Requirements Highlights

* Complete the four-phase RPI loop and commit locally on docs/finance-96; no push, Azure or rubric-score edits.
* Keep tests outside the installed package and run the four requested core checks.

### What You May Not Know

Storage uses KeyError for absent bytes and DocumentStoreError for outages.
Availability cannot be inferred from clean metadata or a historical freshness
result. Historical staleness alone must not suppress otherwise available history.

### Unresolved Decisions or Blockers

* No implementation blockers. Missing tools were installed from existing manifests in an isolated external environment after actual command-not-found failures.
* Publication and complete local gate are not claimed by this local-only task.

## User Decisions and Requirements

* Fix RV-001 and RV-002 on PR #510 with regression coverage for each.
* Read every distinct retained source needed by history and snapshots independently of current-field/schema freshness.
* Preserve non-mutating checks and per-report cache reuse; distinguish missing bytes from service failure.
* Qualify alternatives with the review path's freshness and field policy; retain staged history.
* Run git pull --rebase first, completed with no changes; commit locally only.
* Do not push, use Azure or hand-edit .github/rubric/scores/latest.json.

## Goals

* Restore truthful and fail-closed working-review diagnostics without granting authority or modifying evidence.

## Scope and Non-Goals

* Canonical targets: src/core/src/zava_forward/core/form_review.py, src/core/tests/test_form_review.py, src/core/README.md.
* Tracking targets: this task's dated research, plan, details, critique, changes, Review and session JSON.
* Generated targets: none. Exact removals: none.
* Exclude staging rewrites, financial decisions, new dependencies, unrelated fixes and publication.

## Functional Requirements

* FR1: Preflight current fields, prior/new history evidence and each saved diagnostic's fields/history/attachments, reading every represented source independently of freshness.
* FR2: Missing source bytes raise DocumentUnavailable before returning history, reasons or diagnostic snapshots; storage-service errors propagate distinctly.
* FR3: Review and diagnostic alternatives share source-kind policy checking and _current exact version/hash/kind/actual-byte checks.
* FR4: Unavailable or stale unreviewed alternatives are excluded from Conflict, never deleted from staging.

## Non-Functional Requirements

* At most one byte read per distinct document within each report, including visibility, history, snapshots, current fields and alternative checks. Exact-tuple freshness remains separately memoized.
* A new report/request always checks again. Action preflight may share its digest cache with its resulting report; candidate acceptance retains independent validation.
* No scanning or source saves/deletes during validation. No broad exception suppression.

## Acceptance Criteria

* AC1: Stale-schema, rejected and replaced history cannot be returned with clean metadata but absent bytes; saved snapshots are covered independently.
* AC2: Both JSON and SQLite tests prove denial and unchanged persisted history/diagnostics/staging; failed actions preserve versions/audit.
* AC3: Shared-source report tests still pass and new histories/snapshots/alternatives reuse one byte read per document; later reports detect removal or restored bytes.
* AC4: Two current conflicting candidates still produce Conflict; version/hash/kind/byte mismatch, missing bytes, pending/deleted/generated metadata and field-disallowed kinds do not produce misleading Conflict.
* AC5: Outages remain DocumentStoreError in retained-source and alternative paths; no successful-looking fallback.
* AC6: Requested unittest discovery, ruff check ., ruff format --check . and mypy pass from src/core; related staging regressions pass.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-29/finance-510-source-guards-research.md, C1-C6, Ready |
| Plan | .copilot-tracking/plans/2026-10-29/finance-510-source-guards-plan.md |
| Details | .copilot-tracking/details/2026-10-29/finance-510-source-guards-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-29/finance-510-source-guards-plan-critique.md, Complete / Pass, no findings |
| Changes role | .copilot-tracking/changes/2026-10-29/finance-510-source-guards-changes.md, implementation evidence |
| Readiness | Research and Plan complete; implementation-ready |
| Continuation | Explicit bounded full-loop request; parent advances after critique |

## Sources

* Research C1-C6: verified source, storage contracts, rollback and external fixtures.
* PR #510 comments 4418151984 and 4418152062: exact requested defects.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Restore source guards and regressions

* Dependencies: completed Research and independent final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Guard retained sources with reusable availability reads

* Add a local digest reader translating only missing-source KeyError.
* Traverse current and diagnostic report-shaped evidence, including history prior/new and attachment references.
* Share digest cache across action preflight and its report while keeping exact-source freshness cache.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Qualify alternatives with current source and field policy

* Use a shared source-policy guard for candidate review and alternatives.
* Match case/schema/digest, exclude human-only fields, memoize freshness by full tuple.
* Catch only DocumentUnavailable for unusable unreviewed alternatives; propagate service failures.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Add external regressions and update the contract

* Test owner: existing FormReview class in src/core/tests/test_form_review.py.
* Maximum additions: eight test methods, optional bounded fixture helpers; no new test file or removed test.
* Semantic coverage: JSON/SQLite persistence, no mutation/scans, missing/service errors, conflict eligibility.
* Regression coverage: user repros plus existing exact-tuple/read-count assertions.
* Update src/core/README.md in place with availability/freshness distinction and alternative behavior.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and independently review

* Dependencies: P01 complete.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run requested and related targeted checks

* From src/core: PYTHONPATH=src:tests:../agents/src:../agents/tests python -m unittest discover -s tests -p 'test_form_review*'; ruff check .; ruff format --check .; mypy.
* Also run test_form_staging using the same import path.
* Prove new regression failure against baseline before accepting the fix.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Execute one independent Review and commit locally

* Fresh independent worker activates rpi-review, evaluates exact bounded diff, writes one dated Review.
* Preserve outcome/findings and route later work without repeating Review.
* Resolve gh identity; repository-local privacy-safe author/committer; commit all task changes and dated evidence.
* Verify clean status, commit content, no rubric changes and no push. No publication-gate claim.

## Dependencies

* Existing public synthetic JSON/SQLite fixtures and installed project packages.
* Local executable availability, restored only after missing-dependency failure.

## Critique Disposition

* Single independent final-candidate critique executed: Complete / Pass, no PC findings. No residual risk waiver.

## Follow-Up Items

* None.

## Handoff

* Source implementation complete: P01 and P02-T01. Requested discovery: 26 tests pass; staging: 17 pass; core lint/format/mypy pass.
* P02-T02 complete: independent Review Complete / Conformant, no findings; implementation and original dated RPI evidence committed locally as 5ce4bae3.
* No remaining task or follow-up. Bounded manual session stopped; no push, Azure or rubric-score change.
* Changes artifact: .copilot-tracking/changes/2026-10-29/finance-510-source-guards-changes.md.
