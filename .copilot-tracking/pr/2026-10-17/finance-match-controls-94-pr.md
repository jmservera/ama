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
55 passed. Existing SQL/role/endpoint regression: 47 passed. Actual isolated
local SQL Server: 14 passed, including reopen, rollback, fresh role/OID and
simultaneous writers. Initial cleanup-only pooled-connection errors were fixed
for each uniquely created test database.

Changed-file Ruff, new-harness format, configured mypy (3 core + 1 API),
diff/local-link checks and append-only history preservation passed. Existing
migrated-source exemptions remain; no universal strict-typing claim.

Exactly one critique and one independent Review ran. Review execution:
Complete; original outcome: Not accepted, High RV-001. Coordinator correction
ONE reproduced persistent primitive save failure, decoupled ledger rollback
from state restoration and passed focused checks. Original verdict retained,
no second full Review or invented independent pass; sole blocker resolved by
objective coordinator evidence.

## Related Issues

Refs #94. #93 is parent hierarchy; declared dependencies: none. Concurrent
#90 procurement/capacity and #84 signoffs are not inferred dependencies.
Only shared production edit: two-line `SqlStore.save` finance validator hook.
Shared Store/server and signoff production code remained unchanged.

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
