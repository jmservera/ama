<!-- markdownlint-disable-file -->
# RPI Changes: Capacity SQL reopen correction

## Metadata

* Task ID: pr-605-capacity-sql-reopen-correction
* Task slug: capacity-sql-reopen-correction
* Related plan: .copilot-tracking/plans/2026-10-31/capacity-sql-reopen-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/capacity-sql-reopen-correction-phase-details.md
* Implementation date: 2026-10-31

## Execution Status

* Status: Complete (implementation and one independent Review).
* Declared scope: Full plan implementation.
* Completed markers: P01-T01, P01-T02, P01.
* Remaining active implementation markers: none.
* Publication: final evidence-only commit and explicitly authorized non-force push follow this closeout.

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
P01-T01 checked immediately after focused validation; P01-T02 and P01 checked
after the single independent Review completed. Plan/details and changes agree
on the assessed source boundary and outstanding hosted/human gates.

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
| Independent rpi-review | Implementation HEAD 183c4ca3df7e39d6f7c83b617ca680883bd049e7 | Complete / Conformant | Zero substantive findings; original canonical Review preserved |

SQL runner uses only session-created ama_605_reopen_20261031_0845339f database
on protected ama-350-feedback-sql. No secret is stored in evidence.
Protected container identity after validation:
793cb3650397532c73fd27a46e4e7c600c03a7198d76832942c733a30ca32ae8,
running the protected 2022-latest image. No image/container removal or restart.
The original adverse SQL baseline and corrected file-selector invocation are
preserved in research, not rewritten as successful runs.
After Review, removed only session-created database
ama_605_reopen_20261031_0845339f. Protected container/image remain untouched.

## Pre-Review Reconciliation

* Plan/details/changes: current; P01-T01 completed and P01-T02 validation complete before Review; all markers now checked after the original Review.
* Completed-work evidence: three-file test/documentation correction and tool counts above.
* Blockers: none for bounded Review; hosted/human approval remains pending.
* Follow-ups: none invented.
* Original Review: .copilot-tracking/reviews/logs/2026-10-31/capacity-sql-reopen-correction-review.md, Complete / Conformant; AC7 final evidence commit/push remain subsequent authorized publication actions.

## Blockers

None for implementation.

## Remaining Work

No remaining source implementation or routed findings. Commit final dated
evidence and push; corrected hosted CI and human merge approval remain pending.

## Follow-Up Items

None.

## Return-to-Caller State

Automatic RPI task's Research, Plan, Implement and single Review are complete.
No source changes after assessed implementation HEAD
183c4ca3df7e39d6f7c83b617ca680883bd049e7; only closeout evidence follows.
Review source hashes are checked immediately before non-force push. No
complete local-gate receipt, hosted success, rubric score, issue closure or
merge approval is claimed. Automatic session remains running at Follow-up,
with CI/human approval as the supported next action and no new child task.
