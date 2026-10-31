<!-- markdownlint-disable-file -->
# RPI Changes: gate-chat-test-572

## Metadata

* Task ID: 572
* Date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md
* Details: .copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md

## Execution Status

Full plan directed by caller. P01 complete; P02 validation blocked; original
Review Complete / Residual work; P03 attempted and Blocked. Approved source
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

### P02-T02: Original independent Review

Executed once with integrated source head b9a0db45 and full current evidence.
Record: .copilot-tracking/reviews/logs/2026-10-31/gate-chat-test-572-review.md.
Review execution Complete; source disposition supported with no blocking source
defect; overall outcome Residual work. RV-001 [Medium] preserves missing restored
API/actual Chromium execution; RV-002 [High] preserves planned later complete
committed exact-head gate/verification/assessment. No rpi-implement correction,
significant decision gap, out-of-scope source residual or second Review requested.

## Implementation-Time Plan and Detail Updates

### P02/P03: Dependency restoration, lock contention and current-main drift

The initial requested API discovery completed with 1368 tests, three errors and
320 recorded skips. Errors were missing azure.eventhub and installed API
distribution metadata, not chat/gate assertions. Restored existing core/agents/API
distributions and declared extras with pip in an external venv (no pin changes).
API pinned Ruff check/format passed independently (65 formatted files).

Restored API/browser attempt and its retry each timed out after 600s waiting for
shared lock, before executing any enclosed command (both external logs empty);
no foreign lock owner/process is interrupted and no lock is bypassed.

Current origin/main moved from 5666bd33 to 368d3bb8 (#423). The gate requires the
candidate to descend from current main. Reconcile by a local checkpoint commit
then a non-rewriting merge on the named topic, retaining upstream gate inventory
and workflow hash updates. Original Review still precedes the final candidate
evidence commit/full gate. No main or foreign worktree changes are authorized. Completed the clean merge:
checkpoint f8c40802, integrated head b9a0db45, reviewed base 368d3bb8. Upstream
src-ci workflow hash and inventory additions were retained unchanged. Only this
task's nine files differ from the new base.

Six newly created pip build/egg-info directories (171 files) were removed only
after external full tracking/generated-output archive readback and selected
restore/hash verification. Inventory and prune journal remain in the session's
pip-generated-preservation directory; no historical evidence was pruned.

## Validation Record

| Check | Status | Evidence |
| --- | --- | --- |
| Targeted tooling Ruff check/format | Passed | Two files; initial line-length failure corrected |
| tools unittest discovery | Passed before and after integration | 39 tests, 14.536s before / 12.506s after; gate-572-tooling.log and gate-572-tooling-integrated.log |
| Strict tooling mypy | Passed | Two source files, rerun after formatter |
| Initial requested API discovery | Failed: missing dependencies | 1368 tests, 3 errors, 320 skips, 577.333s; gate-572-api-browser.log |
| Restored pinned API Ruff check/format | Passed | 65 files formatted |
| Restored API/Chromium attempt | Blocked admission | 600s lock timeout; gate-572-api-browser-restored.log empty |
| Restored API/Chromium retry | Blocked admission | Second 600s lock timeout; gate-572-api-browser-retry.log empty |
| Fresh complete committed --all gate | Blocked admission, exit 1 | dd89a42f / base 1330869e; 600s shared-lock timeout; no group executed |
| Final receipt verification and independent publication assessment | Unavailable | No sealed passing receipt; publication not eligible |

## Pre-Review Reconciliation

Source/plan/detail/critique reconciliation complete. P01 checked; P02-T01
unchecked because restored API discovery and actual Chromium did not execute.
Tooling and pinned API static checks passed. Original independent Review may
assess this frozen source and explicit missing execution without inventing success.
P03 remains the later full committed gate/publication prerequisite. Original
independent Review found no blocking source defect. Its outcome remains unchanged.

## Blockers

Shared heavy lock contention prevents restored API/browser execution after two
600s admission timeouts. Original holder PID 2699791 and waiters were observed
read-only; none were interrupted. Current-main ancestry is now reconciled.
The complete committed gate subsequently also timed out after 600s. Its observed
foreign holder was PID 2770814; no process was interrupted and no bypass used.

## Remaining Work

P02-T01 actual validation and P03-T01 committed full gate/publication remain.
Attempt the fresh committed full gate under its own unchanged lock. This is
an immediately relevant evidence sequencing update, not a weakened criterion or
permission to publish with missing execution.

## Post-Review Publication Handoff

No unresolved blocking source findings; original Review evidence findings remain.
Commit original dated evidence, then run a fresh --all gate with current fetched
base and a new external directory. Require actual browser/MSSQL and receipt
verification before eligible independent exact-head assessment and push/PR.
No passing receipt is claimed by this pre-gate commit. Final authoritative logs
and receipt remain external; any later candidate/evidence commit invalidates it.

## P03: Original Committed Full-Gate Attempt

Original Review/evidence committed at 1a481c4f. Main advanced again only through
agent configuration #599; incorporated it without rewriting via merge dd89a42f.
No task source changed after original source Review. Fresh attempted candidate:
dd89a42faa8d35b488711dbce6a3bfe57d7d8931. Reviewed fetched main:
1330869ea675ff019958846330108b4f45e163ce.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 600 --base 1330869ea675ff019958846330108b4f45e163ce --out /home/azureuser/.copilot/session-state/5c131725-48a1-4ff5-b1e9-6b13fd4f57ae/files/gate-572-final-dd89a42f
```

Exit 1 after 600s admission timeout:
`BLOCKED: Global heavy-resource lock timeout`. External complete-gate log:
`/home/azureuser/.copilot/session-state/5c131725-48a1-4ff5-b1e9-6b13fd4f57ae/files/gate-572-final-dd89a42f.log`.
No required group executed; actual browser and MSSQL remain unproven. No passing
receipt was sealed, so --verify-receipt and eligible independent publication
assessment were unavailable. No push or PR was performed, as AC4 forbids
publication before verified complete evidence. Issue closure is not claimed.

This later evidence preserves, rather than replaces, original Review
Complete / Residual work and original critique Complete / Revise. Final
blocker-record commit is not the attempted candidate; retry requires a new output
directory and its exact new committed head/current fetched main. Do not reuse a
receipt or erase adverse logs. No source correction or second Review is needed.

## Follow-Up Items

None.
