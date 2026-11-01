# Changes: resident AI expiry as data (issue 624)

* `infra/sql/resident-assistant.sql`: `expires_at` column migration, `reserve` reads it, seed insert names columns.
* `src/api/tests/test_resident_aoai_sql.py`: future expiry in setUp, new expiry tests.
* `infra/README.md`: section "Resident AI accounting expiry (issue 624)".

Validation: `tests.test_resident_aoai` and `tests.test_resident_aoai_sql` (24 tests, local SQL Server container, OK); ruff check and format clean; mypy reports no errors in the changed test (repository-wide mypy errors pre-exist from missing optional stubs).
