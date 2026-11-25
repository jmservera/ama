---
title: Issue 146 live changes (2026-11-25)
ms.date: 2026-11-25
---

Refs #146. Tier: focused (documentation only; no src, infra, permission, secret or control change). Hosted CI not observed; independent review outstanding.

Changes: docs/reference/research/issue-146-live8-monitoring-2026-11-25.md (new), docs/reference/README.md (index line), docs/reference/log.md (entry).

Throwaway: rule tmp146p-poison, storage account sttmp146poison (with diagnostic setting and scoped role) and workbook tmp146 created and deleted; no tmp146 resource remains.

## Per-criterion result

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts: job failures, poison queue, ledger digest, IoT ingestion | Unproven as a whole | Digest enabled and fired on 2026-11-18; job, IoT, poison rules installed but disabled pending named-human approval; poison firing blocked by storage policy; receiver job has failures and no installed alert |
| Dashboard/workbook: availability, errors, latency, cost vs budget | Partly proven | Errors and latency tile returns live ingress data; availability has no tests (0 rows); cost shows Unknown/Unreconciled by design; deployed workbook is 12 of 14 items; no Portal render |
| Each alert has runbook entry with owner | Unproven | Demo alerts carry runbook and proposed owner role; four legacy alerts lack descriptions; no person named (human decision) |
| Tokenomics: AI usage by capability beside Azure cost, variance visible | Proven for the demo | Live query: 40 calls, cost Unknown, variance "Unreconciled, not zero"; real billing excluded by owner decision |

No box ticked.
