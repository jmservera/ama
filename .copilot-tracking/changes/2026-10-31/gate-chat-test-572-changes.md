<!-- markdownlint-disable-file -->
# RPI Changes: gate-chat-test-572

## Metadata

* Task ID: 572
* Date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md
* Details: .copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md

## Execution Status

Full plan directed by caller. P01 complete; P02 validation active; P03 pending. Approved source
boundary: gate/parser/tests and src guide only; no UI/workflow/dependency edits.
Single critique Complete / Revise with PC-001 resolved directly; no blockers
known at source implementation entry.

## Execution Summary

Implement exact successful verbose case validation shared by runtime and receipt
verification. Inherited dispatch/coverage and narrow discovery exception remain.
Requested API/tooling and actual Playwright validation precede original Review;
fresh full committed gate and publication follow it.

## Completed Work

### P01: Exact-case success proof

tools/rpi-checks.py extends check_skips with optional expected_test and supplies
the exact verbose chat ID from both Runner.command and verify_commands. One
reported test, one exact successful result and no other result/skip are required.
Existing generic suites and skip contracts are unchanged.

tools/test_rpi_checks.py adds two methods for parser compatibility and live
Runner.command rejection; expands the existing receipt mutation test with wrong,
missing, duplicate and extra success lines and incorrect counts. Mutations
recompute hashes/counts before verification. Both successful receipt fixtures
now name the required case. src/README.md explains the exact-case proof.

Completion evidence: all 39 tooling tests passed; targeted Ruff check/format pass.
Initial lint found a two-character line-length excess; fixed and formatter run
before successful validation. No runtime/UI/workflow/dependency changes.

## Implementation-Time Plan and Detail Updates

### P02/P03: Dependency restoration, lock contention and current-main drift

The initial requested API discovery completed with 1368 tests, three errors and
320 recorded skips. Errors were missing azure.eventhub and installed API
distribution metadata, not chat/gate assertions. Restored existing core/agents/API
distributions and declared extras with pip in an external venv (no pin changes).
API pinned Ruff check/format passed independently (65 formatted files).

Restored API/browser attempt timed out after 600s waiting for shared lock, before
executing any enclosed command (empty external log). A bounded retry is queued;
no foreign lock owner/process is interrupted and no lock is bypassed.

Current origin/main moved from 5666bd33 to 368d3bb8 (#423). The gate requires the
candidate to descend from current main. Reconcile by a local checkpoint commit
then a non-rewriting merge on the named topic, retaining upstream gate inventory
and workflow hash updates. Original Review still precedes the final candidate
evidence commit/full gate. No main or foreign worktree changes are authorized.

Six newly created pip build/egg-info directories (171 files) were removed only
after external full tracking/generated-output archive readback and selected
restore/hash verification. Inventory and prune journal remain in the session's
pip-generated-preservation directory; no historical evidence was pruned.

## Validation Record

| Check | Status | Evidence |
| --- | --- | --- |
| Targeted tooling Ruff check/format | Passed | Two files; initial line-length failure corrected |
| tools unittest discovery | Passed | 39 tests in 14.536s; external session log gate-572-tooling.log |
| Strict tooling mypy | Passed | Two source files, rerun after formatter |
| Initial requested API discovery | Failed: missing dependencies | 1368 tests, 3 errors, 320 skips, 577.333s; gate-572-api-browser.log |
| Restored pinned API Ruff check/format | Passed | 65 files formatted |
| Restored API/Chromium attempt | Blocked admission | 600s lock timeout; gate-572-api-browser-restored.log empty |
| Restored API/Chromium retry | Queued | gate-572-api-browser-retry.log; shared lock respected |

## Pre-Review Reconciliation

Not ready: implementation and validation pending.

## Blockers

Shared heavy lock contention currently prevents restored API/browser execution.
Main ancestry drift requires non-rewriting topic integration before final gate.

## Remaining Work

P02-T01 validation, P02-T02 original Review and P03-T01 committed full gate/publication.

## Follow-Up Items

None.
