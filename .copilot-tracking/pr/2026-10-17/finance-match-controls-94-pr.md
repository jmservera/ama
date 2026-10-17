---
title: Finance match controls 94 pull request
ms.date: 2026-10-17
---

Recorded exact #94 acceptance evidence and corrected demonstrated line-level,
identity and stale-match gaps. Finance remained record-only, with no banking
integration, payment execution or new authority/currency model.

## Changes

* Attached all match exceptions to affected invoice lines and refused unknown/
  ambiguous commitments. Rechecked matching at acceptance; a newly received
  duplicate now blocks the original until explicitly resolved.
* Enforced current registered staff and preparer independence by email, staff
  code and optional OID, including transaction-time SQL checks. Preserved holds,
  independent disposition and external-payment status as notes only.
* Added finance-owned semantic/HTTP tests and failure recovery, scoped existing
  mypy settings, and updated existing component guides/Finance synthesis/index/log.
  Committed dated Research, Plan, details, critique, changes, Review, state and
  phase-execution evidence.

## Exact criterion evidence

| #94 criterion | Actual proof |
| --- | --- |
| Nothing paid by product | Closed action set has no execution adapter; external-status notes leave approved budgets, commitments and grant/cash unchanged through reopen |
| Match exceptions line-level | Actual zero-based line IDs for scope/quantity/milestone and aggregate/duplicate/ambiguous blockers, authenticated HTTP and Finance queue |
| Preparer cannot approve | Same person/code/OID aliases refused, distinct same-role people succeed; fresh role/OID checks and SQL transaction-time independence |

Evidence: `src/core/tests/test_finance_match_controls.py`,
`src/core/tests/test_finance_signoffs.py`,
`src/api/tests/test_finance_match_api.py`.

## Validation and Review

Baseline 29 passed; failing-first controls ran 22 with 18 failures/5 errors
(subtest cascades included). Post-correction focused finance/JSON/SQLite/HTTP:
55 passed for JSON correction ONE. Existing SQL/role/endpoint regression: 47
passed at that stage. Original isolated local SQL Server: 14 passed, including reopen, rollback, fresh role/OID and
simultaneous writers. Initial cleanup-only pooled-connection errors were fixed
for each uniquely created test database.

Changed-file Ruff, new-harness format, configured mypy (3 core + 1 API),
diff/local-link checks and append-only history preservation passed. Existing
migrated-source exemptions remain; no universal strict-typing claim.

Exactly one critique and one independent Review ran. Review execution:
Complete; original outcome: Not accepted, High RV-001. Coordinator correction
ONE reproduced persistent primitive save failure, decoupled ledger rollback
from state restoration and passed focused checks. Original verdict retained,
no second full Review or invented independent pass. RV-001 has objective
coordinator resolving evidence, distinct from subsequent SQL finding COORD-002.

## Coordinator correction TWO: COORD-002

External independent review of exact `852b3421c5b5a2dd09944fa39ee609cc2efcf811`
returned **Revise**: failed SQL audit INSERT followed by early `_discard` SELECT
failure allowed outer lock exit to flush a false approval although the budget
remained Proposed. This is a blocking finding, not a deferred future item.

* Fixed canonical `_discard(pending=())`: failed audit/touched/validation state
  is quarantined before fallible recovery I/O, snapshots restore and sync cache
  invalidates for the next healthy persisted refresh. Finance retains only its
  pre-operation legitimate audit prefix.
* Preserved original operation errors through finance, save-refusal and lock-exit
  recovery, with explicit exception notes and error logging. A legitimate prefix
  that cannot flush remains for healthy retry, never replaced with failed success.
* Added five finance-owned inherited regressions for first/persistent recovery
  read failure, prior audit preservation, failed lock-exit retry and internal
  save-refusal recovery. They assert state at first recovery I/O, original error
  identity/diagnostics, rollback/reopen, no false approval, cross-thread lock
  release and healthy subsequent approval/chain.

First three SQLite tests failed before production edits. After correction,
158 combined local finance/HTTP/SQL/role/provenance/bulk tests passed plus the
added refusal test separately. Actual isolated local SQL Server passed 18
finance cases plus the added refusal test. Both owned loopback containers
responded before testing and were removed by exact ID; no shared cleanup.
Scoped Ruff/format/configured mypy and documentation preservation checks passed.

Both authorized coordinator corrections are used. COORD-002 has local resolving
evidence; **external independent closure remains pending**. The original single
RPI Review remains Complete / Not accepted and exact-852b342 coordinator verdict
remains Revise until external closure. No new full Review or independent Pass.
Separate evidence: `.copilot-tracking/changes/2026-10-17/finance-match-controls-94-changes.md#coord-002-resolving-evidence`.

## Authorized integration on merged assessment main

After correction/publication completed at `54ed4451fc6ef38b6361ad5782e0da2e43d9227c`,
the coordinator explicitly authorized rebasing only this run-owned topic onto
latest `origin/main`: **`bbbc9243505b606550327c64bf5429243f457f2e`**, merged
#84 / PR #382. The rebase is not a new correction cycle or independent Review.

Conflict decisions retain both intents:

* Keep stock, finance, provenance, bulk and safety/resident/stock transaction
  checks in the same writer transaction.
* Keep upstream active-`stock_decision` refusal ownership and scoped actor
  restoration. For other callers retain original-error notes/logging around
  save-refusal recovery.
* Keep one canonical `_discard(pending=())`, cleanup before recovery reads,
  committed case/recommendation/checked-document snapshots and watermark reset;
  finance optionally retains its prior legitimate pending audit prefix.
* Keep finance lock-exit original-error handling, every existing test, both KB
  routes/syntheses, and upstream KB log as an exact byte prefix plus own entries.

Post-integration validation: **232 local passes, one existing opt-in browser
skip**. Initial combined run had 179 passing cases and one stock API import
error; rerunning the remaining API/workflow/role selection with required
`src/api` on the module path passed 53 with that one browser skip. No source
workaround or repeated broad suite.

**Actual isolated local SQL Server: 37 passed**: all 19 finance tests plus
10 canonical stock and 8 selected procurement/workflow tests. Includes early/
persistent recovery faults, original error identity/logs, rollback/reopen,
current authority, independent sign-offs, capacity, work-order versions,
cross-store changes, handoff and safety controls. Ready via `SELECT 1`, exact
owned container/UUID database removed; no shared service cleanup.

Combined scoped Ruff/format and configured mypy passed (5 core and 2 API files).
API mypy initially lacked the declared Playwright dev package; restored pinned
`playwright==1.64.0` after that failure, then passed. No browser binary download
or browser-conformance claim. Finance production/tests have exact pre-rebase
content; upstream stock/signoffs/Store and tests remain exact main content.
Procurement/workflows/provenance/bulk source unchanged. Existing dated RPI
plan/details/changes/state/phase execution record commands and conflict choices.

Publication is topic-only with `--force-with-lease` pinned to exact previous
remote `54ed4451fc6ef38b6361ad5782e0da2e43d9227c`; never unconditional force or
main. **External coordinator independent closure of the integrated pushed head
is the next gate; no new independent Pass is claimed.**

## Related Issues

Refs #94. #93 is parent hierarchy; declared dependencies: none. Concurrent
#90 procurement/capacity and #84 signoffs are not inferred dependencies.
Shared SQL edits: finance validator, canonical `_discard` and minimal
save-refusal/lock-exit error preservation. Actual overlap with merged #84 /
PR #382 is integrated through authorized latest-main rebase as described above,
not cherry-pick or foreign dirty-worktree inspection. Store/server and signoff
production code match upstream main; no new #94 edit to them. Concurrent #90's
unmerged work is not imported or weakened.

## Limits

PRD FR-018/AC-021/042 informed the audit, not complete PRD acceptance.
Current BRD FR-018/RULE-003 concern handoff/hazards; stale issue numbering was
explicitly recorded, not silently relabelled. Supplied milestone references do
not establish actual acceptance authority. JSON separate files do not promise
abrupt-crash atomicity; failed state restoration explicitly reports a potentially
unknown durable outcome and requires persisted readback before retry.

Tiny fictional local fixtures only: no private data, real provider/financial
commitment, payment, paid AI or Azure action. No web assets changed or new
browser/WCAG, real delegation or live-platform acceptance claimed. Hosted checks
remain pending; merge remains owner-controlled.
