---
title: Issue 146 research (live 20261119T160746Z)
ms.date: 2026-11-19
---

Refs #146. Research disposition: executed (read-only). Planning Readiness: Ready.

Live inventory (az CLI, -g ama, 2026-11-19T16:10Z): 4 metric alerts and 4 scheduled-query alerts enabled (Foundry throttle, SQL CPU, API 5xx, API restarts, KV secret expiry, KV denied access, ledger digest mismatch, ledger verify missing); 0 workbooks; no tmp146 resource.

Unticked criteria: C1 alerts (job failure, poison, IoT unbuilt/disabled; job-failure Total aggregation is an infra edit); C2 workbook (not installed, private link blocks rendering); C3 owners (named people are a human decision); T2 AI usage vs Azure cost (billing reconciliation out of demo scope). Existing offline tests already cover workbook, alert coverage and runbook ownership. Each remaining item is infra/FULL-tier, production-only or human.
