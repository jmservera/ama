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
