# Issue 115 plan

* [x] Phase 1: `digest_blob.py` publish and verify with alert marker and exit code.
* [x] Phase 2: unit tests with an immutable-container fake over the synthetic store.
* [x] Phase 3: Bicep container, retention policy, daily job, log alert.
* [x] Phase 4: README, ADR status row, knowledge-base log.

Critique (single pass): never anchor a broken chain; verify from the container only; lock is an owner step. Applied directly.

## Follow-up 2026-10-15 (PR 268 review)

* Added a `LEDGER_DIGEST_OK` heartbeat and `alert-*-ledger-verify-missing` (no success in 26h) so a job that fails to run alerts; documented the `--publish` trust-on-first-use gap and that the owner must choose the retention period before locking; Log Analytics table/column names (`ContainerAppConsoleLogs_CL`, `ContainerJobName_s`) stated as unconfirmed open items.
* Merged origin/main (log.md kept both sides). Unit suite 530 OK; SQL Server run not possible locally (Docker socket permission denied), left to the mssql CI job. No SQL added by this change.
