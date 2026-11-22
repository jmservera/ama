# Issue 115 live research (2026-11-22)

Both acceptance criteria of #115 are already ticked (first deferred to production by #1908, owner decision 2026-11-18; second ticked). No unticked criterion remains. Task: verify scheduled verification against merged code, tests and live read-only state, and record an evidence note.

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* `src/core` `test_ledger_digest_blob`: 22 tests OK. `src/orchestrator` `test_digest_blob`: 31 tests OK.
* Live (resource group ama, read-only): job `job-cutover-test-demo-audit` runs `zava_forward.orchestrator.digest_blob --publish` on cron `0 2 * * *`; latest execution 2026-11-22T02:00 Succeeded (an earlier manual run on 2026-11-21T19:23 Failed, the next Succeeded).
* Container `ledger-digests` shows hasImmutabilityPolicy true, immutableStorageWithVersioning false; policy 365 days, state Unlocked. Locking is irreversible and owner-deferred (#1908).
* Job env `ZF_DIGEST_REQUIRE_RETENTION_LOCK=false` on the demo, consistent with the unlocked policy; min retention 365.
* Alerts `alert-cutover-test-demo-ledger-digest-mismatch` (enabled, severity 1, hourly, matches `LEDGER_DIGEST_ALERT` in job logs) and `...ledger-verify-missing` enabled.
* Storage account has public blob access disabled.

## Gap assessment

No unticked criterion. No smallest code gap found: the lock requirement is a deliberate production switch. A mismatch drill was not run (owner: no drills).
