<!-- markdownlint-disable-file -->
# Critique: issue 1238 outcome retry plan (recovery 1109)

Executed once, 2026-11-09, by an independent read-only rubber-duck subagent
against the final-candidate plan, details and research. Verdict: Revise.
Critique is not repeated for this task.

| ID | Severity | Finding | Disposition (applied directly, compatible) |
| --- | --- | --- | --- |
| PC-001 | Blocking | On SQL, `mark_committed` sets `persisted` right after COMMIT, so a later failure is a known-committed `ResidentCommittedError`, re-raised and never retried. A "save then raise" success test would fail on SQL. | Accepted. Known-committed stays terminal (receipt is persisted). The ambiguous case is a lost commit acknowledgement with `persisted` unset; the test simulates it by clearing `persisted` after the real save, so JSON and SQL each follow their actual recovery (restore or reload). |
| PC-002 | Blocking | A recovery-note check can miss unverified recovery, and a retry could hide it. | Accepted for the noted boundaries: any error carrying a recovery or restoration failure note is not retried and not reconciled; it fails closed with the receipt logged. The unmarked JSON audit-truncate `OSError` replacing the error is a pre-existing path of `_operation`; it is recorded as a limit, not widened here. |
| PC-003 | Blocking | Reconciliation lock or read failure could bypass logging and the explicit error. | Accepted. Reconciliation is wrapped; failure is treated as unknown and the same log and `ResidentCommittedError` follow. |
| PC-004 | Non-blocking | The message says the attempt shows Pending even when state is unknown. | Accepted. Wording asks to reload and reconcile with the receiver, without asserting the state. No test or API depends on the old text (searched). |

F3 deferral is supported by the recorded Q6 decision and stays open. No user
decision was required; no critique advice conflicted with a confirmed decision.
