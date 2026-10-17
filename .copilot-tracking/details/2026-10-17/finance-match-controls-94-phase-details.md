---
title: Finance match controls 94 phase details
ms.date: 2026-10-17
---

## Metadata

Task 94, finance-match-controls-94. Plan:
.copilot-tracking/plans/2026-10-17/finance-match-controls-94-plan.md.
Research: .copilot-tracking/research/2026-10-17/finance-match-controls-94-research.md.
No declared dependency; parent 93. Focused, backend-only.

<!-- rpi:phase id=P01 -->
## P01: Demonstrate and repair exact finance gaps

<!-- rpi:task id=P01-T01 -->
### P01-T01: Failing-first finance-owned regression tests

Use existing tiny dataset fixture and staff factory, temporary JSON/SQLite,
distinct same-role managers and email/code/OID aliases. Exercise all independent
decisions, not just GEO versus manager. Prove missing legacy preparer refuses;
line-level no-budget/no-commitment/duplicate/aggregate exceptions; ambiguous
commitment refuses; stale matched invoice cannot exceed budget/commitment.
Capture failing tests before implementation, then require zero unexpected failures.
No private finance CSV or default working data. PC-001 requires JSON save/audit
failure before and after actual write: unchanged in-memory and reopened state,
no durable failed-operation success event and valid subsequent audit chain.
PC-002 requires status notes through Paid outside this system leave approved
budget/commitment and grant/cash unchanged. Held acceptance/status refusal retains
hold/disposition; Keep on hold followed by independent disposition remains valid.
Completed: initial 22 cases produced 18 failures/5 errors before source edits;
later local judgments add true threaded concurrency and fresh OID denial.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Minimal finance and SQL hook corrections

Use current registered staff validation from change_provenance._actor. Finance
stores minimal preparer identity snapshots (email/code/OID); legacy records use
registered preparer lookup, never infer unknown identity. Compare populated
stable values across aliases. Current actor and independence recheck at save
under existing SQL transaction through one finance validator hook. Protect
pending success audit and case rollback on errors. Keep human decisions/manual
holds and external status note. Match aggregate blockers attach to all affected
lines; recheck matching at acceptance. Do not add unverifiable milestone policy.
Completed: finance-owned correction and exactly one shared SQL save hook.
Directly coupled regression now requires rejecting a newly received duplicate
before accepting the original, instead of trusting its earlier Matched label.

<!-- rpi:phase id=P02 -->
## P02: Verify and publish criterion evidence

Current correction TWO: COORD-002 external coordinator Revise on 852b342.
Canonical SqlStore._discard must quarantine failed audit/touched state before
DB reads, preserving snapshot state and prior legitimate audit. Finance guard
must retain original failure and explicitly attach/log recovery failure.
Inject actual audit INSERT failure plus early one-shot/persistent discard SELECT
failure; prove durable Proposed budget, no false success, lock release, next
healthy operation and intact audit chain on SQLite and isolated local MSSQL.
Actual overlap with #84 / PR #382 is this same recovery primitive; no foreign
worktree read, cherry-pick, rebase or merge. Coordinator sequences integration.
Implemented: `_discard(pending=())` preserves an explicitly supplied pre-operation
audit prefix and clears failed audit/touched/validation state before snapshot
restore and recovery I/O. `_seq = -1` forces healthy refresh. Finance,
save-refusal and outer lock-exit attach/log secondary recovery errors while
preserving the original failure; a failed legitimate-audit flush retains its
prefix for retry. These are canonical recovery changes, not duplicate backend
logic. Exact shared `_discard` and adjacent recovery overlap remains disclosed.

Correction TWO evidence: first three new SQLite tests failed before fix.
Combined local 158 passed plus added internal-save-refusal case passed; actual
SQL Server 18 passed plus added refusal case passed. Five new inherited tests
cover early/persistent SELECT failure after actual INSERT, prior audit, lock-exit
failure and original save refusal. At the first recovery read, failed approval
and touched state are already absent and cached budget is Proposed. Reopened
state/ledger, original error notes/logs, cross-thread lock release and healthy
subsequent approval/chain are asserted. No independent closure/Pass claimed.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Focused persistence/API checks and documentation

Temporary SQLite reopen after successful and refused writes; inject audit/save
errors and prove no durable success event/state. Separate stores compete for
same case; revoke staff role/OID without case sequence change, including between
validation and save, and require refusal. Verify held/unknown and record-only
status via loopback authenticated HTTP. New tests must start responsive local
HTTP and close connections/server. Use existing local MSSQL CI contract on an
isolated uniquely named throwaway container/database if possible; never wipe
shared services. Document exact skipped/unavailable evidence instead of guessing.
Focused lint/format/type checks; existing exemptions do not prove strict typing.
JSON ordinary-error recovery is distinct from SQLite transaction rollback and
unpromised abrupt-crash atomicity. HTTP assertions compare exact responses and
reopened ledger/hold/disposition deltas. There is no banking/execution seam to
instrument; prove state invariance and inspect the closed finance action set,
not merely status labels or audit verb names.
Update core guide and existing Finance journey synthesis/index/log, not memory.
Evidence: 54 focused JSON/SQLite/existing finance/HTTP cases and 47 existing
SQL/role tests passed. Fourteen isolated local SQL Server cases passed after
correcting driver-pooled connection cleanup for only each owned UUID database.
Ruff and configured focused mypy passed. Two typed test harnesses use existing
scoped untyped-boundary conventions; no new ignore_errors or dependency.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Independent Review and delivery

One independent canonical Review with exact three criterion matrix and changed
boundary. Separate critique execution/verdict from Review execution/outcome.
Actual blockers require correction (maximum two coordinator correction batches)
and objective targeted validation, not a fake pass with future routing.
No repeat full Review. Human operational adoption remains outside engineering.
Review executed Complete, Not accepted, one High RV-001. Coordinator correction
ONE must reproduce persistent os.replace failure in the existing JSON harness,
make ledger rollback independent of a second successful save, and expose any
failed state restoration as an uncertain durable outcome rather than success.
Completed correction ONE: primitive regression failed before fix, then 55 focused
tests and tools passed. Audit rollback precedes/does not depend on recovery save.
Restoration failure is explicitly uncertain; subsequent chain/reopen assertions
pass. No independent reassessment or second full Review is implied.
Check authenticated account privacy email before conventional commit with
Co-authored-by trailer; push branch and main-targeted PR Refs #94. No merge,
rebase, force push or nested delivery. Persist phase execution and final state.
Completed: source/evidence commit 6248521 verified at origin; main-targeted
PR #383 open and mergeable at inspection. Hosted checks running, no result
invented. Authenticated author/committer email is the account's noreply address.
Final evidence-only commit/push publishes closeout; session stops by caller
direction with no child work or merge.
