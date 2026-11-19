# Issue 107 live research (2026-11-19)

Task: issue-107-live. Research disposition: executed. Planning Readiness: Ready.

* Issue 107 has two unticked criteria: (1) independent SQL connection/worker and race tests cover material mismatches, revocation and restart, old images/restarts cannot restore revoked approval or replenish allowances; (2) delivered-build real AI/SQL/Azure acceptance.
* Criterion 1 is the first unmet. Existing coverage in `src/api/tests/test_assistant_restart_non_replenishment.py`: `RevocationAndSuspension` runs on actual SQL Server (`MssqlRevocationAndSuspension`); `Allowance` and `MaterialMismatch` run only on SQLite (no Mssql subclass). No composite test covers an old image after a material-mismatch revocation (change path reactivation + allowance non-refund).
* Gap for code: add Mssql subclasses for `Allowance` and `MaterialMismatch`, and a composite old-image-after-material-mismatch test.
* Criterion 2 needs an approved release (named approver, OQ-017) and real AI; not provable for the demo (prior passes: docs/reference/research/issue-107-live-r3-assistants-evidence-2026-11-18.md).
* Tier: test-only change under src/api/tests; FOCUSED (no src code, SQL schema, infra). Uses a disposable local SQL Server container only, never Azure SQL.
