# Issue 115 changes

* Added `mvp/zavaforward_mvp/digest_blob.py`, `mvp/tests/test_digest_blob.py`.
* Edited `infra/modules/storage.bicep`, `containerapps.bicep`, `main.bicep`, `mvp/README.md`, ADR 0002 status row, `docs/reference/log.md`.
* Validation: full mvp unittest suite; `az bicep build` of main.bicep.

## Follow-up 2026-10-15 (PR 268 review)

* Added a `LEDGER_DIGEST_OK` heartbeat and `alert-*-ledger-verify-missing` (no success in 26h) so a job that fails to run alerts; documented the `--publish` trust-on-first-use gap and that the owner must choose the retention period before locking; Log Analytics table/column names (`ContainerAppConsoleLogs_CL`, `ContainerJobName_s`) stated as unconfirmed open items.
* Merged origin/main (log.md kept both sides). Unit suite 530 OK; SQL Server run not possible locally (Docker socket permission denied), left to the mssql CI job. No SQL added by this change.
