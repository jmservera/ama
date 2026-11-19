# Plan: MSSQL old-image revocation test (Refs #104, #107)

* [x] Phase 1: add `MssqlRevocationAndSuspension(MssqlFixture, RevocationAndSuspension)` gated on ZF_TEST_MSSQL=1.
* [x] Phase 2: run against a throwaway local SQL Server 2022 container (127.0.0.1, generated password), plus the SQLite originals; ruff and mypy; delete the container.
Tier: FOCUSED, test-only; no src/ production change, no Azure.
