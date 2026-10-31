<!-- markdownlint-disable-file -->
# RPI Phase Details: Capacity SQL reopen correction

## Metadata

* Task ID: pr-605-capacity-sql-reopen-correction
* Task slug: capacity-sql-reopen-correction
* Related plan: .copilot-tracking/plans/2026-10-31/capacity-sql-reopen-correction-plan.md
* Evidence: .copilot-tracking/research/2026-10-31/capacity-sql-reopen-correction-research.md; C1-C6/W1.

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Correct fixture and verify | P01-T01 complete; validation complete; Review pending | P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct fixture and verify

* Context: SQL-specific resetting factory and SQLite-only assertion invalidate the cross-store reopen test.
* Intent: test genuine persisted reopening; no legal or procurement authority expansion.
* Boundaries: external tests and directly related API guide only; no production code.
* Dependencies: completed research, one final-candidate critique, protected SQL resource reuse.
* Completion evidence: focused suites and requested tools, original independent Review.
* Unresolved items: hosted outcome remains future evidence.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Correct and strengthen external reopen regression

* Context: common make_store is initialization, and its SQL override calls wipe. MssqlStore.db_path is state_dir/mssql. FileStore saved live.json allows reopening without seed.
* Intent: introduce common reopen_store returning make_store for SQLite/file and override for SQL without wipe, following MssqlHandoffApi precedent.
* Targets: src/api/tests/test_procurement_api.py and src/api/tests/test_mssqlstore.py; src/api/README.md clarification near contractor capacity.
* Boundaries: two new fixture methods, focused assertions in existing test, no removed test or generated file.
* Expected checks: capture detached nonempty audit before reopen; seed unlink before reopen; same actual type/state marker and independent SQL connection; compare original audit/procurement immediately and after repeated reads and refused action; missing-law 503/unknown safe route; appointment refusal remains 403.
* Dependencies: critique complete; PC-001 accepted in this task detail; PC-002 rejected as a worker-only boundary absent from parent constraints.
* Completion evidence: coherent diff and three-backend regression success.
* Unresolved items: none.
* Completion: common reopen helper, SQL non-wiping override, seed removal, exact type/backend comparison, pre-reopen audit oracle and unknown-law assertions implemented. 40 SQLite/file/law and 13 real SQL HTTP tests pass.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Run requested checks and independent Review

* Context: package lint exemptions and suite reuse are already defined; tests live outside packaged source.
* Intent: prove actual SQL lifecycle, not SQLite-only approximation.
* Targets: existing API tool configuration and unit runners, dated changes/Review artifacts.
* Dependencies: P01-T01.
* Commands from src/api: requested PYTHONPATH, /tmp/mv/bin/python -m ruff check ., -m ruff format --check ., -m mypy; unittest test_procurement_api test_rule_alerts; isolated runtime SQL runner for test_mssqlstore.MssqlProcurementApi.
* Completion evidence: exact exit codes/test counts, one independent rpi-review artifact and unmodified protected resource identity.
* CI publication boundary: do not run or claim the complete local gate, per explicit caller direction; push reviewed correction, no merge.
* Unresolved items: hosted/human approval pending; no fabricated receipt.
* Validation complete: API-wide ruff check and format pass (66 formatted files), mypy passes (125 source files), 40 SQLite/file/law tests and 13 SQL HTTP tests pass with zero skips. Independent Review is the remaining task boundary.
