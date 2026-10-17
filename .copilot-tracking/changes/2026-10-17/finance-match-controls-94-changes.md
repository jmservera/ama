---
title: Finance match controls 94 changes
ms.date: 2026-10-17
---

## Scope and execution

Task 94, finance-match-controls-94. Full plan execution authorized.
Plan: .copilot-tracking/plans/2026-10-17/finance-match-controls-94-plan.md.
Details: .copilot-tracking/details/2026-10-17/finance-match-controls-94-phase-details.md.
Research executed then Plan with exactly one completed final-candidate critique.
PC-001/002 compatible evidence requirements applied directly. No source changes
before Implement. Baseline: 29 existing finance/signoff tests passed.

## P01-T01: Failing-first

Completed before production edits: 22 new semantic tests ran, with 18 failures
and 5 errors (subtest recovery cascades included). Demonstrated missing OID/code
independence, unknown-preparer refusal, integer line IDs, ambiguous commitment
refusal, stale acceptance, fresh permission and JSON ordinary-error restoration.
Raw local output retained in session files/finance-before.txt; no private input.

## Amendments, divergences and remaining work

No divergent decisions. JSON ordinary-error rollback matrix and ledger invariance
are critique clarifications, not new scope. Only shared production edit is
SqlStore.save's finance validation hook, possible #90 overlap.
No Store/server/web changes; #84 signoffs regression preserved.

## P01-T02: Finance correction completed

Finance emits actual zero-based line indices for aggregate and line exceptions,
refuses ambiguous commitments, recomputes acceptance against current invoices,
and captures email/code/OID preparer identities. Reused registered-staff prior
art with fresh actor/independence validation inside the SQL writer transaction.
Finance-owned caught-error restoration preserves JSON state/ledger and drops
SQL pending success audits. No payment/authority/currency model added.

Immediately relevant local judgments: existing duplicate regression now expects
current-match refusal, then explicitly rejects the duplicate before acceptance.
This is the intentional directly coupled behavior shift, not a weakened test.
Two small pyproject mypy additions follow existing typed-harness/untyped-store
patterns and recognize the reused fixture import; no new ignore_errors or
dependencies. Plan/details/test ownership reconciled; one critique retained.

## P02-T01: Focused validation and durable documentation

| Check | Result | Evidence |
| --- | --- | --- |
| Baseline existing finance/signoffs | 29 passed | Before source edits |
| Failing-first new controls | 22 ran, 18 failures/5 errors | Initial alias/line/unknown/stale/fresh/recovery failures, including subtest cascades |
| New JSON/SQLite controls + existing finance/signoffs + authenticated HTTP | 54 passed | Temporary tiny fixtures, responsive loopback HTTP, reopen/ledger invariance |
| Existing SQL store/role matrix/endpoint inventory | 47 passed | Shared save-hook and untouched authority surfaces |
| Local isolated SQL Server finance class | 14 passed, 65.894s | Real SQL engine; reopen, rollback, role/OID freshness, same-role/alias and simultaneous writers |
| Ruff changed Python targets/format new harnesses | Passed | Existing migrated source exemptions retained |
| Configured mypy finance/sqlstore/core harness and API harness | Passed, 3 + 1 files | Migrated-source exemptions remain, not universal strict typing |

First local MSSQL run: all 14 test bodies ran but each cleanup errored on
pooled connections; no pass claimed. Corrected harness drops only its newly
created UUID database after SINGLE_USER disconnection; complete rerun passed.
Ephemeral loopback container removed by exact ID. Random local password was
process-only and never printed or committed. No shared service/database cleanup.

API fixture logs explicitly show law-store checks unavailable; finance HTTP
and persistence assertions pass independently, with no regulatory acceptance.
No UI edit/browser run required for this backend-only change. Existing screen
line/refusal rendering read, not claimed as newly browser-validated.

Updated core/API guides, existing Finance journey synthesis, reference index and
append-only log. Original/memory unchanged. Full PRD contract/allocation and
real accepted-milestone authority remain outside exact criterion acceptance.
Review and delivery remain P02-T02; no engineering blocker known.

## Pre-Review reconciliation

P01/P01-T01/P01-T02 and P02-T01 complete in plan/details. P02-T02 is the
Review/delivery lifecycle item, deliberately pending until those actions occur.
Final candidate: 25 finance-owned JSON/SQLite/HTTP checks passed after typed
harness edits; Ruff/format/configured mypy and git diff --check passed.
Five changed documentation files have zero missing local link targets; log is
verified append-only, original/memory unchanged. Exact local MSSQL container
absent after cleanup. No remaining implementation blocker or divergent decision.
Ready for one independent Review; production controls already fully implemented.

## Independent Review and coordinator correction ONE

Review executed once, Complete; outcome Not accepted. High RV-001 reproduces
persistent os.replace failure: recovery's second save fails before audit-tail/head
rollback, leaving a false success audit. This is an actual delivery blocker,
not future-only routing. Caller preauthorized up to two coordinator corrections.
Correction ONE will add failing-first primitive I/O coverage, make audit rollback
independent of state restoration and explicitly flag an uncertain durable outcome
if restoration cannot persist. Preserve original Review verdict; do not repeat
full Review or critique. No significant direction/scope decision changed.

### RV-001 resolving evidence

Correction ONE completed. The new persistent os.replace regression first failed
with a durable finance_budget_approve event despite refusal. Audit-tail/head
rollback now runs before and independently of the recovery state save. A second
state-save failure raises an explicit RuntimeError: durable outcome may be
unknown, reload persisted records before retry. Neither error is suppressed or
converted to success. The test proves unchanged in-memory/reopened finance,
no failed-operation success event, restored audit head and valid subsequent
approval/audit chain after the primitive becomes available.

Post-correction: 55 focused JSON/SQLite/existing-finance/HTTP tests passed
(9.655s), Ruff/format passed and configured mypy passed for 3 + 1 files.
SQL code is unchanged by this JSON-only correction; prior 14 real SQL Server
and 47 SQL/role regression results retain their exact tested boundary.
No second full Review or critique. Original independent Review remains
Complete / Not accepted for its pre-correction candidate, not relabelled Pass.
Coordinator test evidence resolves its sole RV-001 blocker for delivery.
Correction budget used: one of two; no outstanding engineering finding.

## P02-T02 delivery

Completed source/evidence commit 6248521, conventional fix(core) with Copilot
trailer and authenticated account's noreply author/committer email, pushed to
feat/finance-match-controls-94. Verified remote source hash and opened
https://github.com/jmservera/ama/pull/383 targeting main, Refs #94, with exact
criterion evidence and original Review/correction distinction. PR mergeable
at inspection; hosted MVP CI/validation and Source CI running, not claimed passed.

Final evidence-only commit/push publishes closeout, dated PR body and state.
All P01/P02 markers complete, no active engineering blocker, no remaining
implementation work. Full PRD/platform/human/browser boundaries remain explicit
limitations, not approval or inferred issue dependencies. Automatic session
stopped per caller's explicit final-push boundary; no child, merge, rebase,
force push or main write.

PR body reused already reviewed/corrected artifacts rather than creating another
nested PR-review workflow. Existing unrelated tracked .copilot-tracking/pr/pr.md
was preserved; this task's body is dated and task-specific.

## Coordinator finding COORD-002 and correction TWO

Caller supplied external independent coordinator verdict Revise on exact
852b342: failed SQL save leaves success audit pending; _discard reads cases
before clearing it. Early recovery read failure permits outer _finish to
reload/flush false finance_budget_approve although budget remains Proposed.
Valid hash chain is not truthful transaction evidence. This is separate from
the original single RPI Review and correct JSON correction ONE, both retained.

Correction TWO is explicitly authorized; no new full Review/critique. Fix the
canonical primitive before fallible I/O, retain prior legitimate audit, preserve
original error and expose recovery failure by exception notes and repository
logging. Prove fail-before/after on SQLite and actual isolated local SQL Server.
Actual overlap: #84 PR #382 is correcting SAME _discard primitive. No inspection
of another dirty worktree, cherry-pick, merge/rebase/force push; coordinator owns
sequencing common helper and both callers later. No blocker waived because
another PR exists. Original 852b342 completion is not an independent Pass.

### COORD-002 resolving evidence

Correction TWO is implemented and locally validated, not independently closed.
Three new SQLite tests failed before production edits: each surfaced the
recovery OperationalError instead of the original audit-insert error. The
actual INSERT ran before injection, so transaction rollback is exercised rather
than bypassed. Raw output: session files/finance-cycle2-before.txt.

Canonical `_discard(pending=())` now snapshots touched IDs and unconditionally
replaces pending audit with only an explicitly supplied prior prefix, clears
touched/validation state and invalidates `_seq` before recovery I/O. Cached case
and recommendation snapshots restore before database reads. Even a persistent
first SELECT failure therefore leaves no failed approval or dirty case for
outer `_finish` to flush. A healthy future entry must reload persisted state.
Finance supplies a copy of its pre-operation pending audit only. Minimal
save-refusal and lock-exit guards preserve the original exception when recovery
also fails, attaching explicit notes and logging full recovery diagnostics.
There is no success-shaped fallback or duplicate backend implementation.

Five finance-owned regressions now cover first-read failure, persistent read
failure, prior legitimate pending audit, persistent lock-exit failure and
internal save-refusal recovery. They check staged state at the first recovery
I/O, original exception identity plus notes/logging, durable/cached Proposed
budget, no false approval, released lock from another thread, preserved prior
audit and a subsequent healthy approval with a valid ledger chain. During
test development, the lock-exit variant initially checked deferred prior audit
before retry; the assertion now runs after the healthy retry, when it must
persist exactly once.

| Correction TWO check | Result | Boundary |
| --- | --- | --- |
| First three SQLite tests before fix | 3 expected failures | Recovery error masked original INSERT error |
| Combined local regression | 158 passed, 34.197s | JSON/SQLite finance, existing finance/signoffs, authenticated HTTP, SQL store, role/endpoint, provenance and bulk callers |
| Added internal-save-refusal SQLite check | 1 passed, 1.159s | Shared save-refusal error precedence after recovery SELECT failure |
| Actual isolated local SQL Server finance | 18 passed, 87.675s | Includes first four new recovery tests and existing role/OID, rollback, reopen and concurrency |
| Added actual SQL Server save-refusal check | 1 passed, 5.121s | Fifth new recovery path; no second full class rerun |
| Final five SQLite recovery targets | 5 passed, 1.333s | Final helper/error-diagnostic assertions after test formatting |
| Scoped Ruff/format/configured mypy | Passed at closeout | Migrated-source exemptions remain; no universal strict typing |
| Diff/local links/append log/original-memory and original Review preservation | Passed at closeout | No web changes or browser/WCAG acceptance |

Local SQL Server responded to `SELECT 1` before tests. Both loopback containers
were removed by their exact owned IDs, and each harness removed only its own
UUID database. Random credentials stayed process-only, never printed/committed.
Logs remain in session files/finance-cycle2-regression.txt,
finance-cycle2-mssql.txt and finance-cycle2-mssql-refusal.txt.
No private data, real financial commitment, cloud or payment action occurred.
Final documentation check covered 515 existing/changed local link targets,
append-only log, valid state JSON and unchanged original/memory/original Review/
unrelated PR body. The owned local SQL Server container name is absent.

Both authorized coordinator corrections are now used. COORD-002 has local
resolving evidence; the external exact-852b342 verdict remains Revise until
external coordinator closure. Original RPI Review Complete / Not accepted,
JSON correction ONE and their evidence are unchanged. No second full Review,
new critique or independent Pass is claimed. Required closeout: authenticated
noreply normal commit, same-branch push, honest PR #383 update and clean stop.
Actual #84 / PR #382 overlap includes `_discard` and adjacent SQL recovery error
handling; the coordinator must preserve the common helper and both callers
when sequencing integration. No merge/rebase/force push/cherry-pick is performed.

### Correction TWO delivery

Committed and pushed source/evidence
6e75380b7f72bc44b865276615c901045a8c9ce9 with authenticated account's noreply
author/committer, conventional message and required Copilot trailer. Verified
the exact source hash in origin and PR #383, base main. Updated actual PR body
from the committed dated body, explicitly retaining Revise/external closure
pending and actual common-helper overlap. Source checks running/queued at
inspection, not represented as passed.

Worktree was clean after the verified source push. Final evidence-only commit
publishes completed P02 markers and explicit stopped state, followed by normal
same-branch push and clean-head verification. Both authorized corrections used;
no known unresolved local engineering defect, but no independent Pass or
external closure is claimed. No new Review, merge, rebase, force push or child.

## P03-T01: Caller-authorized merged-assessment integration

Subsequent explicit authorization reopens this run-owned topic for integration,
not a third correction or full Review. Clean worktree/branch confirmed at
54ed4451fc6ef38b6361ad5782e0da2e43d9227c; remote and open PR #383 match exactly.
`git fetch origin main` resolves bbbc9243505b606550327c64bf5429243f457f2e,
the merged PR #382 assessment correction. Expected remote lease is fixed to
54ed4451fc6ef38b6361ad5782e0da2e43d9227c, not inferred after rewriting.

Plan/details/state now authorize P03-T01: logically reconcile shared discard/
save guards, all validator hooks and both callers' transient state; preserve
upstream KB exact log prefix plus own entries, run combined local and actual
SQL Server regressions, record conflicts and publish with explicit lease.
Only committed origin/main was inspected; no other worktree read. No
acceptance expansion, dependency invention or repeated critique/Review.

### Rebase and conflict decisions

`GIT_SEQUENCE_EDITOR=true git rebase origin/main` replayed five own commits.
First source conflict combined `stock.validate_sql(self)` with finance's
validator, retaining provenance, bulk and safety/resident/stock validation.
Second source conflict preserved upstream `stock_decision` refusal ownership:
SQL save does not pre-discard an active stock decision, whose scoped caller
owns cleanup, original error and context restoration. For other callers the
finance original-error/logging guard wraps discard. One `_discard(pending=())`
retains upstream cleanup-before-read, committed case/recommendation/document
snapshots and `_seq = -1`; finance adds only optional prior-audit retention.
Upstream `_proc_snap` restoration is kept verbatim, not discarded as duplicate.
Finance's lock-exit original-error guard remains. No helper duplication or
source/test removal. Committed stock/signoffs/Store and their tests match
origin/main; procurement/workflows/provenance/bulk source matches both heads.

KB log conflict was resolved upstream-first, then all finance entries.
Byte-prefix assertion against `git show origin/main:docs/reference/log.md`
passed. Other KB/index/component additions auto-merged and were inspected.
Rebased intermediate head: 389defb; base bbbc924. Publication is still pending
and original expected remote lease 54ed445 remains unchanged.

Initial combined invocation ran 180 with one import error: the upstream
stock API test imports `tests.test_mvp` and needs src/api on the module path.
The other 179 cases passed. Corrected invocation added src/api and ran remaining
stock API/workflows/role/endpoint tests: 54 ran, OK with one existing opt-in
browser skip (53 passed). No dependency install or source workaround; no
unnecessary rerun of the 179 passing cases. Law-store-unavailable fixture
diagnostics remain explicit and do not establish regulatory acceptance.

### Integrated validation and command evidence

Initial combined command (179 passed plus one stock API import error):

```bash
PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_finance_match_controls.JsonFinanceChecks test_finance_match_controls.SqlFinanceChecks \
  test_finance_signoffs test_finance_match_api test_stock_reconciliation \
  test_stock_reconciliation_api test_quality_procurement test_sqlstore \
  test_change_provenance test_bulk_edits -q
```

Corrected remaining command: 54 ran in 17.111s, 53 passed and one existing
opt-in rendered stock-browser test skipped. Combined passing total 232, not
counting the initial import error as a test pass.

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_stock_reconciliation_api test_workflows test_role_matrix test_role_endpoint_inventory -q
```

Actual isolated local SQL Server: all 19 inherited finance tests passed
(90.599s), then 18 combined cases passed (19.284s): canonical existing
MssqlStockDecisions' 10 cases and eight selected existing procurement/workflow
cases using only a session-owned MssqlStore adapter. Procurement: package
validation, evidenced committed capacity/headroom, work-order lifecycle and
audit, reopen, two-store synchronization. Workflows: handoff, independent
safety release, chain across handoff/return. No production/test file modified
for that adapter; no stripped or weakened assertions. The harness used existing
`ZF_FINANCE_MSSQL=1` and `ZF_TEST_MSSQL=1`/local `ZF_SQL_*` configuration.
The owned container answered `SELECT 1`, finance tests each owned a UUID database,
and stock/procurement/workflows used one additional created UUID database.
Both database harnesses cleaned only owned databases; exact container
fc75ea2acc75864fa6a4f4edc4a4857eeefd4dbb72d44d8b86e81e96a15a3e29 removed.
Random credentials were process-only and never printed or committed.

Scoped Ruff passed for both integrated paths, and four typed harness format
checks passed. Configured mypy passed for finance/sqlstore/stock and both core
harnesses (5 files). Combined API mypy initially failed only on missing
playwright.sync_api; the existing API manifest already pins the dev dependency.
After that concrete missing-dependency failure,
`.venv/bin/python -m pip install --quiet 'playwright==1.64.0'` restored it;
configured mypy then passed for both API harnesses (2 files). No manifest edit,
browser download or new browser/WCAG claim.

`git range-diff bab4bf3..54ed445 bbbc924..HEAD -- <sqlstore path>` confirms
the source replay differs only to retain stock validation/refusal ownership
and upstream canonical snapshots. Finance source/tests exactly match 54ed445.
Upstream stock/signoffs/Store, stock core/API tests, MSSQL harness and upstream
prototype synthesis exactly match bbbc924. Procurement/workflows/provenance/
bulk source is unchanged from both heads. No unmerged #90 branch imported.

Raw output is in session files/finance-integration-combined.txt,
finance-integration-api-workflows.txt and finance-integration-mssql.txt.
Final integration evidence commit and explicit-lease publication remain;
external coordinator independent closure is next, not a new full RPI Review.

Final `git diff --check`, valid state JSON, all exact source/test parity and
upstream log-prefix/original-finance-tail assertions passed. Link review covered
520 local targets, retaining the repository-root-relative tracking-path
convention in the unchanged original critique. An initial relative-only checker
misread those historical tracking links; corrected convention-aware check
passed without editing the critique or original Review. Exact owned container
name is absent. Latest remote main remains bbbc924 and topic remains exact
54ed445 before publication. Temporary session SQL runner removed; raw results
retained, no credentials written to it.
