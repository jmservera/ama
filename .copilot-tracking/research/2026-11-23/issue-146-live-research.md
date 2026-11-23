---
title: Issue 146 live research (2026-11-23)
ms.date: 2026-11-23
---

Refs #146. Research disposition: executed. Planning readiness: Ready.

Findings (read-only unless stated; full note will be docs/reference/research/issue-146-live6-monitoring-2026-11-23.md):

* Workspace log-cutover-test now has publicNetworkAccessForQuery Enabled, so workbook queries can be executed with az monitor log-analytics query (earlier passes: private only).
* Of 7 workbook KQL tiles, 6 execute; ai-variance-by-period fails with SEM0100 because Log Analytics does not allow an extend to reference a column defined in the same extend (isolated with a print probe). Real defect in infra/monitoring-workbook.json line 105; deployed workbook carries it.
* appi-cutover-test is not workspace-based and has query disabled, so request, availability and latency tiles cannot have data.
* StorageQueueLogs on the demo storage shows no PutMessage in 7 days; the poison candidate query shape is unverified. A throwaway storage account (tag purpose=tmp146-delete) with queue diagnostics got a synthetic poison-queue message to check ObjectKey; must be deleted.
* Inventory unchanged from 2026-11-22: job, poison, IoT, AI-limit candidates disabled.
