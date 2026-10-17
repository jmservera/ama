---
title: Finance match controls 94 plan
ms.date: 2026-10-17
---

## Task Metadata

Task ID: 94. Slug: finance-match-controls-94. Parent: 93, hierarchy only.
Status: Independent Review Complete, original outcome Not accepted; sole RV-001
resolved by coordinator correction ONE and 55 passing focused checks. Delivery
pending. No repeated full Review or conformant reassessment claimed.
Details: .copilot-tracking/details/2026-10-17/finance-match-controls-94-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-17/finance-match-controls-94-plan-critique.md.

## Executive Summary

Retain existing record-only finance and repair demonstrated line-level, identity
and stale-write gaps. No product payment, banking or authority model is added.
Most edits stay in finance and finance-owned tests; one SqlStore.save validator
hook is the sole planned shared touchpoint. Existing API/screens already render
line indices and refusals. BRD numbering in the issue is stale: current FR-018
and RULE-003 are handoff/hazard controls, not finance.
No unresolved engineering decision; no human operational approval is claimed.

## User Decisions and Requirements

* Execute full ordered RPI and commit dated phase evidence; push main-targeted PR Refs #94.
* Exact criteria: nothing paid; line-level match exceptions; preparer cannot approve.
* Prove actual humans, same/different staff and OID, not role-only denial.
* Unknown inputs refuse match; preserve budgets, commitments and held record-only disposition.
* Use tiny fictional local fixtures, src only, focused checks and no paid/cloud/private activity.
* Correct blocking review findings before handoff, at most two coordinator corrections.
* #90/#84 are concurrent, not inferred dependencies; disclose actual shared overlap.

## Goals

* Prove the three issue criteria across durable finance writes and HTTP entry.
* Preserve existing lifecycle while preventing identity aliases and stale acceptance.

## Scope and Non-Goals

Finance module/tests, one SQL validator hook, component guides, existing Finance
journey synthesis, reference index and append-only log. No web edits, new
authorization/currency/payment model, schema change, real providers, commitments,
Azure or AI. Do not alter original, memory or source requirement numbering.

## Functional Requirements

* Every emitted match exception names its affected zero-based line.
* Missing/ambiguous commitment, budget or milestone input blocks a clean match.
* Finance uses current registered named staff; approval rejects equal email,
  stable staff code or nonempty OID even across email aliases and role changes.
* New preparer snapshots retain stable identity; legacy records resolve their
  named preparer or refuse unknown identity.
* Acceptance rechecks current match inputs; holds and record-only statuses persist.

## Non-Functional Requirements

* SQL case/audit commit or roll back together; no success audit leaks on failure.
* Recheck authority and independence under SQL writer transaction; retain
  rowversion conflicts and test two writers with separate connections.
* JSON restores failed in-memory writes; disclose separate-file crash limitations.
* No dependency or shared Store/server expansion except the isolated SQL hook.

## Acceptance Criteria

1. External payment status remains a note; no execution call or cash/grant mutation.
2. All exception records refer to actual invoice lines; unknown inputs cannot pass.
3. Same human by email/code/OID cannot approve budget, commitment, invoice
   disposition, hold release or record their own disposition's external payment.
4. Different humans with the same permitted role can prepare/approve.
5. Reopen/rollback/concurrency/fresh-authority tests prove affected writes.

## Sources

Research C1-C8/W1-W2 in
.copilot-tracking/research/2026-10-17/finance-match-controls-94-research.md;
PRD FR-018/AC-021/042; exact issue 94; core/API guides.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Demonstrate and repair exact finance gaps

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Failing-first finance-owned regression tests

Add exact identity, line, stale-match and transaction cases before production
edits. JSON save/audit failures, including after completed writes, must preserve
in-memory/reopened finance, remove failed-operation success events and preserve
subsequent chain integrity; abrupt-crash atomicity remains excluded.
Payment note transitions must preserve budget/commitment/grant/cash records;
held refusals and Keep on hold must persist their hold/disposition through reopen.
Use fail-on-call external seams if any exist; do not invent a payment adapter.
Save baseline failure evidence. Tests own behavioral semantics, not source
string assertions. Existing suite keeps broader signoff/grant/resident regression.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Minimal finance and SQL hook corrections

Reuse change_provenance actor validation without its unrelated metadata contract.
Keep finance identity snapshots/checks private to finance. Aggregate blockers
attach to all affected lines; reject ambiguous commitment instead of first wins.
Revalidate match at acceptance, and roll back staged SQL success audit on errors.

<!-- rpi:phase id=P02 -->
### [ ] P02: Verify and publish criterion evidence

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Focused persistence/API checks and documentation

Run finance-owned tests and existing finance/signoffs, relevant SQL/role regression,
targeted ruff/format/mypy. Exercise local MSSQL using existing CI guide if
available. No application/Azure acceptance claim. Update existing KB synthesis,
index/log and core guide; record exact evidence and limitations.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Independent Review and delivery

One canonical Review; correct actual blockers before delivery within caller's
two coordinator-correction limit. Record execution/outcome separately. Commit
with authenticated privacy-safe identity and Copilot trailer; push, create PR
targeting main, leave checks/merge to owner and stop after final push.

## Test Ownership and Change Budget

Canonical tests: src/core/tests/test_finance_match_controls.py (new),
src/api/tests/test_finance_match_api.py (new), existing test_finance_signoffs.py.
Maximum two new test files, no removals, no generated tests or fixture datasets.
Modify obsolete null-line assertion and the directly affected duplicate
regression: current-match acceptance intentionally refuses a newly duplicated
original until the duplicate is independently rejected.
Semantic acceptance: runtime state/HTTP/persisted audit, not role-only proxies.
Regression: existing finance/signoff and focused SQL/role suites.
Canonical production: finance.py and one SQL save hook. Generated targets: none.
Scoped existing mypy configuration includes the two typed test harnesses'
calls into migrated untyped boundaries and the reused fixture import; no new
ignore_errors, dependency or broad strictness change.

## Dependencies

None declared. #93 parent only. Actual shared SqlStore.save hook may overlap #90;
avoid Store/server/shared helper edits and retain their existing validations.

## Critique Disposition

One final-candidate critique executed: Revise. Direct compatible corrections:
PC-001 resolved by explicit JSON ordinary-exception durable state/audit matrix
in P01-T01 and details; PC-002 resolved by explicit ledger/held invariance and
HTTP/reopen evidence. No user decision needed, no repeat critique.

## Follow-Up Items

* Broader PRD contract/home allocation and accepted-evidence authority are not
  established by this exact issue audit; no unsupported full PRD acceptance.

## Handoff

One Review found RV-001: persistent primitive save failure could prevent audit
rollback. Caller-authorized coordinator correction ONE proved primitive-level
recovery and explicit uncertain outcome if state restoration fails; no unresolved
finding remains. Original Review verdict retained with separate changes evidence.

Changes: .copilot-tracking/changes/2026-10-17/finance-match-controls-94-changes.md.
Proceed P01 only after critique disposition; no unresolved engineering blocker.
