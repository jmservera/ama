---
title: Issue 2191 capacity research
ms.date: 2026-11-22
---

Research disposition: executed. Planning readiness: Ready.

* Receiver already batched (`ZF_RECEIVER_BATCH_SIZE=10`, lookback 360 s); fresh coverage was a sawtooth (baseline mean 30.8 percent over 5 samples; owner figure 37.7).
* SQL `retrofit` was Standard S0 (10 DTU, no autopause, online) at 100 percent DTU maximum in every 15 minute bucket for 3 hours; no connection failures or deadlocks.
* Simulator schedule, timeout and failure rate are not binding. Receiver logs are unreadable (workspace public access denied; finished executions keep no replica logs).
* Chosen action: raise the SQL objective with az to S3 (about USD 5 a day, inside the USD 700 cap) and sample 30 minutes.
* Evidence: [docs/reference/research/issue-2191-live-sql-capacity-2026-11-22.md](../../../docs/reference/research/issue-2191-live-sql-capacity-2026-11-22.md).
