# Issue 115 review (single pass)

Outcome: conformant for built scope; open items routed as follow-ups.

* AC1 immutable container with retention: built in Bicep (policy created unlocked; lock is an owner decision). Not deployed.
* AC2 scheduled verification alerts on mismatch: daily job, `LEDGER_DIGEST_ALERT` marker, log alert; mismatch, empty and unreachable cases tested.
* Validation: 527 tests OK (85 skipped), `az bicep build` ok.
* Follow-ups: legal retention period; lock the policy; deploy and confirm the Log Analytics table name `ContainerAppConsoleLogs_CL`; live Azure run.

## Follow-up 2026-10-15 (PR 268 review)

* Added a `LEDGER_DIGEST_OK` heartbeat and `alert-*-ledger-verify-missing` (no success in 26h) so a job that fails to run alerts; documented the `--publish` trust-on-first-use gap and that the owner must choose the retention period before locking; Log Analytics table/column names (`ContainerAppConsoleLogs_CL`, `ContainerJobName_s`) stated as unconfirmed open items.
* Merged origin/main (log.md kept both sides). Unit suite 530 OK; SQL Server run not possible locally (Docker socket permission denied), left to the mssql CI job. No SQL added by this change.
