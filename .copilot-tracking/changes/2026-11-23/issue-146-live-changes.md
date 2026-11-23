---
title: Issue 146 live changes (2026-11-23)
ms.date: 2026-11-23
---

Refs #146. Tier: focused (infra JSON and test; no src, permission, secret or control change). Hosted CI not observed.

Changes: infra/monitoring-workbook.json (split extend in ai-variance-by-period, fixes Log Analytics SEM0100); infra/tests/test_ai_observability_workbook_budget.py (new test, fails on old query, 20 workbook tests pass); docs/reference/research/issue-146-live6-monitoring-2026-11-23.md, README index, log.

Throwaway: storage account sttmp14627989-style (tag tmp146-delete) created and deleted; no tmp146 resource remains.

## Per-criterion result

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts: job failures, poison queue, ledger digest, IoT ingestion | Partly proven, unproven as a whole | Ledger digest enabled; job, poison, IoT disabled pending named-human approval; no firing or notification observed; poison PutMessage shape unverifiable (no logs; throwaway account blocked by policy) |
| Dashboard/workbook: availability, errors, latency, cost vs budget | Partly proven, unproven as a whole | Cost, AI usage, variance (after fix), limits tiles execute live; availability, errors, latency empty because Application Insights is not workspace-based; no Portal render; fixed workbook not redeployed |
| Each alert has runbook entry with owner | Unproven | Owners are proposed roles; naming people is a human decision |
| Tokenomics dashboard: AI usage by capability beside Azure cost, variance visible | Proven for the demo, with limit | Usage and unreconciled variance shown; Azure cost record Unknown by owner exclusion |

No box ticked.
