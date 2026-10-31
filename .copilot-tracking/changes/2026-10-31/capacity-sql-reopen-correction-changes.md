<!-- markdownlint-disable-file -->
# RPI Changes: Capacity SQL reopen correction

## Metadata

* Task ID: pr-605-capacity-sql-reopen-correction
* Task slug: capacity-sql-reopen-correction
* Related plan: .copilot-tracking/plans/2026-10-31/capacity-sql-reopen-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/capacity-sql-reopen-correction-phase-details.md
* Implementation date: 2026-10-31

## Execution Status

* Status: In progress.
* Declared scope: Full plan implementation.
* Completed markers: P01-T01.
* Remaining: P01-T02 (independent Review only), P01.
* Validation complete; source boundary ready for Review.

## Execution Summary

Correct SQL test setup, not production law loading. Original critique Revise
is preserved; PC-001 accepted for pre-reopen audit proof and PC-002 rejected
as a worker-only execution restriction not applicable to this parent.

## Completed Work

### Genuine non-destructive reopening and audit oracle

* Related marker: P01-T01.
* Files: src/api/tests/test_procurement_api.py, src/api/tests/test_mssqlstore.py.
* Added a common reopen_store and a SQL override that does not invoke wipe.
* Replaced hardcoded SQLite db_path expectation with comparison to the original actual state marker; exact original type and separate SQL connection adapter are checked.
* Removed only the temporary synthetic seed before reopen. Missing seed and unchanged original procurement prove SQL cannot reset/reseed.
* Captured detached nonempty audit before reopen (PC-001); checked immediately, after each repeated read and after denied appointment.
* Repeated reads preserve null contract version, resident bindings and Unknown appointment status. Missing application law remains 503/unknown with a human safe route; forbidden appointment mutation remains 403.
* src/api/README.md clarifies the test lifecycle and unchanged unavailable-law semantics.
* No production code, dependency, UI, regulatory snapshot or knowledge-base file changed.
* Completion evidence: coherent 28-addition/5-deletion source diff and all focused suites passing.

## Implementation-Time Plan and Detail Updates

No implementation divergence. Plan Ready after direct critique dispositions.
P01-T01 checked immediately after focused validation; P01-T02 records passed
validation and remains open only for the one independent Review. Plan/details
and changes agree on the assessed source boundary and outstanding hosted gates.

## Validation Record

All commands run from src/api with
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Existing interpreter /tmp/mv/bin/python used; required packages were already
installed, so no pip install or dependency change was necessary.

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| python -m ruff check . | API-wide | Passed | All checks passed; exit 0 |
| python -m ruff format --check . | API-wide | Passed | 66 files already formatted; exit 0 |
| python -m mypy | API-wide | Passed | No issues in 125 source files; exit 0 |
| python -m unittest test_procurement_api test_rule_alerts -q | SQLite/file procurement and law boundaries | Passed | 40 tests, 42.516s, zero skips; exit 0 |
| Runtime SQL runner, test_mssqlstore.MssqlProcurementApi -q | Real SQL HTTP procurement, including exact failed regression | Passed | 13 tests, 33.305s, zero skips; exit 0 |
| git diff --check | Changed files | Passed | exit 0 |
| Complete local gate | Publication | Not run | Explicit caller says CI is the gate |

SQL runner uses only session-created ama_605_reopen_20261031_0845339f database
on protected ama-350-feedback-sql. No secret is stored in evidence.
Protected container identity after validation:
793cb3650397532c73fd27a46e4e7c600c03a7198d76832942c733a30ca32ae8,
running the protected 2022-latest image. No image/container removal or restart.
The original adverse SQL baseline and corrected file-selector invocation are
preserved in research, not rewritten as successful runs.

## Pre-Review Reconciliation

* Plan/details/changes: current; P01-T01 completed, P01-T02 validation complete and Review remaining.
* Completed-work evidence: three-file test/documentation correction and tool counts above.
* Blockers: none for bounded Review; hosted/human approval remains pending.
* Follow-ups: none invented.
* Review readiness: ready for exactly one independent assessment of the implemented source boundary and AC1-AC6; AC7 push remains a subsequent authorized publication action.

## Blockers

None for implementation.

## Remaining Work

P01-T02 independent Review, then commit and push; no remaining source implementation.

## Follow-Up Items

None.

## Return-to-Caller State

Automatic parent continues to one Review. No source changes are planned after
Review; findings, if any, route to later work. Then commit dated evidence and
push the requested branch with CI/human approval explicitly separate.
