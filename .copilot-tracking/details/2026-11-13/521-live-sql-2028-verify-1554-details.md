# Details: Live SQL 2028 cutoff (Refs #521)

## Phase 1 probe

* Render: `resident_showcase_sql.render("probe-principal")` batch 3 must contain `'2028-01-01T00:00:00'`.
* Network: `socket.getaddrinfo` and a 5 s TCP connect to `sql-cutover-test-rzsrg.database.windows.net:1433`; record resolved address class (private or public) without the address.
* Auth: token from `az account get-access-token --resource https://database.windows.net/` held in a Python variable; connect via `mssql_python` with the access-token attribute as `resident_showcase_sql.py` does. Databases: list with `az sql db list` (names only) and exclude `master`.
* Read: `SELECT name, definition FROM sys.check_constraints WHERE parent_object_id = OBJECT_ID(N'resident_showcase.allowed_case')`.

## Phase 2 apply

* Execute only the batch containing `DROP CONSTRAINT ck_allowed_case_window` and `ADD CONSTRAINT`, as rendered from the repository SQL. The transaction rolls back on failure (existing rows beyond 2028 would fail the WITH CHECK; that is reported, not worked around).
* Read back the definition and require it to contain `2028-01-01T00:00:00`.

## Phase 3 to 5

* Changes file: [changes](../../changes/2026-11-13/521-live-sql-2028-verify-1554-changes.md), redacted (no token, subscription or tenant id, no IPs).
* Tests: `python3 -m unittest` for `src/core/tests/test_cutover_audit.py`; scrub with grep for token, credential and GUID patterns over the changed files.
