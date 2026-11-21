# Research 2026-11-21: issue 350 legacy-body repair crash

* Disposition: executed. Planning Readiness: Ready.
* Gate run14 failure: `test_mssqlstore.MssqlLedgerMigration.test_previous_schema_migrates_in_a_ledger_database` raises `KeyError: 'appointments'` from `SqlStore._repair_identity_columns` -> `SqlStore._row`.
* Cause: commit 4a282143e's repair calls `_row` on every body; `_row` needs fields (appointments, resident, home, wave, owner_code, contacts, funding, contractor, ...) that legacy-schema bodies lack. Repair runs during migration, so it must never raise.
* Fix: skip, and leave untouched, any body for which `_row` raises KeyError/TypeError/ValueError/IndexError (or the JSON is invalid).
* Acceptance criteria of #350 need live multi-role proof; see changes record for per-criterion status.
