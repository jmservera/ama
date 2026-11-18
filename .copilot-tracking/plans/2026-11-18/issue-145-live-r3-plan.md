---
title: Issue 145 live run 3 plan
ms.date: 2026-11-18
---

* [x] PITR restore `retrofit` to a throwaway database (S0, Local), point 15 minutes before start.
* [x] Run a throwaway job with the existing orchestrator image and managed identity; the read-only probe compares restored copy and source, verifies the chain and tries native ledger verification.
* [x] Retain redacted raw output in `docs/reference/research/issue-145-live-r3-raw-probe-2026-11-18.txt`; record the research note with the per-criterion table (ledger, retention vs #121, reconciliation, resurrection).
* [x] Delete job and database, confirm absence.
* [x] Update index and log, commit locally. No src change, so focused tier. The coordinator publishes.

Details: [details](../../details/2026-11-18/issue-145-live-r3-details.md).
