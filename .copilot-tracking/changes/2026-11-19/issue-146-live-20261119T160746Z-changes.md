---
title: Issue 146 changes (live 20261119T160746Z)
ms.date: 2026-11-19
---

Refs #146. Docs only; no src, infra or test change. Tier FOCUSED. Added a research note, an index entry and a log entry.

| Criterion | Result | Basis |
| --- | --- | --- |
| C1 Alerts: job failures, poison queue, ledger digest, IoT | Partly proven | Digest alerts installed (2 rules enabled); job-failure Total aggregation is an infra edit (FULL tier); poison and IoT disabled pending named-human approval |
| C2 Workbook: availability, errors, latency, cost vs budget | Unproven | 0 workbooks installed; workspace queries are private-link only |
| C3 Runbook entry with owner per alert | Partly proven | Entries carry proposed roles; naming people is a human decision |
| T2 AI usage beside Azure cost, variance visible | Unproven here | App AI report showed it on 2026-11-18; no Azure cost table; billing reconciliation out of demo scope |

Commands (read-only, `-g ama`): `az monitor metrics alert list` (4 enabled), `az monitor scheduled-query list` (4 enabled), `az resource list` for workbooks (0). No resource created; nothing to delete.
