# Plan: issue 120 live fix

1. Change the MSSQL `ALTER TABLE` in `timecapture._ensure` to add a nullable column.
2. Read `notice_version` via `COALESCE(notice_version, N'')` in `request()` and `activation()`.
3. Add a unit test with a fake MSSQL connection asserting the ALTER is nullable and legacy NULL rows do not satisfy the gate.
4. Run targeted tests, mypy, ruff. Redeploy is out of scope (no production changes without the coordinator); live proof of the defect is recorded.
5. Record per-criterion proven/unproven table.
