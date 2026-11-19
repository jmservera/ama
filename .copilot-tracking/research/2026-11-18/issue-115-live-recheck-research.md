---
title: Issue 115 live recheck research
date: 2026-11-18
---

Research disposition: reused plus fresh read-only confirmation. Planning Readiness: Ready.

The earlier same-day run ([note](../../../docs/reference/research/digest-verification-alert-live-2026-11-18.md), merged as #1913) already proved the one unticked criterion for the demo. Read-only Azure checks at 10:5x UTC confirmed it still stands:

* Alert rule `alert-cutover-test-ledger-digest-mismatch` enabled, Sev1, hourly, routed to `ag-cutover-test-ops` (one email receiver). Query matches `LEDGER_DIGEST_ALERT` on the ledger-verify job.
* Alert instance fired 2026-11-18T08:18:52Z; monitor condition now Resolved.
* `alert-cutover-test-ledger-verify-missing` enabled (absence of `LEDGER_DIGEST_OK` over 26 h).
* Job `job-cutover-test-ledger-verify` trigger is still Manual; the last cron-driven run was 2026-10-26. Schedule reinstatement remains an infra change, out of scope.
* Log Analytics and the storage account refuse this host's network, so logs and containers cannot be read directly. No network rules were changed.
* `src/orchestrator` digest_blob tests: 31 pass, including mismatch and missing-anchor alert cases.
