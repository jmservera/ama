# Changes

* src/api/tests/test_assistant_restart_non_replenishment.py: `MssqlRevocationAndSuspension` (skipped unless ZF_TEST_MSSQL=1) runs the revocation, suspension and old-image change-path tests on actual SQL Server.
* src/api/tests/test_assistants.py: `MssqlFixture` now drops `assistant_releases`; before, stale release rows leaked between tests (first run: 2 failures, `['active','revoked']`; a fixture gap, not a product defect).

## Validation (FOCUSED, test-only)

* Throwaway local container mcr.microsoft.com/mssql/server:2022-latest on 127.0.0.1 with a generated password: `test_assistant_restart_non_replenishment` 19 tests OK (29 s, includes the MSSQL class). First run before the fixture fix: 19 tests, 2 failures. Container removed, password file deleted.
* SQLite: `test_assistant_restart_non_replenishment test_assistants`: 158 tests OK, 65 skipped (MSSQL gated).
* ruff check: pass. mypy in src/api: 7 errors, all in src/core/tests/telemetry_support.py (missing opentelemetry stubs), none in changed files; pre-existing.
* Not run: full gate, Azure SQL (owner: no drills), revision restart on Azure.

## Per-criterion table (epic 104)

| Criterion | Status | Basis |
| --- | --- | --- |
| #440 stabilization checkpoint | Unproven | Needs #440 closed and owner pivot/defer decisions |
| All child features closed or deferred | Unproven | #107, #108, #164, #216 open; no owner deferral |
| AI never approves/executes/ranks/mutates | Proven (ticked) | Prior audit 2026-11-18, invariant suite |
| #432 complete or gap recorded | Proven (ticked) | Prior audit |
| No capability beyond exercise without limits | Proven (ticked) | Prior audit |
| Child #107: old images cannot restore revoked approval (SQL) | Proven locally on SQL Server 2022 this run; Azure SQL unproven | This change |
