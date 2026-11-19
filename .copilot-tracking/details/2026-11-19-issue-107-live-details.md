# Issue 107 live details

Phase 1: copy the existing `MssqlRevocationAndSuspension` pattern (`MssqlFixture` first, then the base class).
Phase 2: for each material variation, after the mismatch revokes the release, an "old image" worker (LARGER allowance config, approver) must fail to reactivate via `change_release(..., "active")`, invoke must stay disabled, provider calls and the allowance pool must be unchanged, and domain records must be unchanged.
Phase 3 validation: targeted unittest module on SQLite; same with ZF_TEST_MSSQL=1, ZF_SQL_SERVER=127.0.0.1 against a throwaway container.
