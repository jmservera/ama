# Issue 115 review (single pass)

Outcome: conformant for built scope; open items routed as follow-ups.

* AC1 immutable container with retention: built in Bicep (policy created unlocked; lock is an owner decision). Not deployed.
* AC2 scheduled verification alerts on mismatch: daily job, `LEDGER_DIGEST_ALERT` marker, log alert; mismatch, empty and unreachable cases tested.
* Validation: 527 tests OK (85 skipped), `az bicep build` ok.
* Follow-ups: legal retention period; lock the policy; deploy and confirm the Log Analytics table name `ContainerAppConsoleLogs_CL`; live Azure run.
