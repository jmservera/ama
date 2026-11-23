---
title: Issue 184 live research (run b)
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready.

Prior run (2026-11-23, [recheck note](../../docs/reference/research/issue-184-live-recheck-2026-11-23.md)) left one element unproven: secret absence in live Event Hubs message bodies. All three issue criteria are already ticked, so no unticked criterion remains. The CLI identity holds Owner on the subscription, so a temporary, narrowly scoped Event Hubs Data Receiver assignment on `eh-iot-cutover-test-rzsrg` (resource group `ama`) is possible and is deleted after the read. Plan: read a bounded sample of events, scan bodies for secret patterns without printing bodies, record counts only.

## Result

Temporary Event Hubs Data Receiver role (user principal, scoped to `sensor-readings`) was created and later deleted. Two reads (load-balanced and per-partition) returned 0 events: the namespace has `publicNetworkAccess` Disabled and local auth disabled (`eh-network.json`), so the CLI host cannot open the AMQP connection (CBS token authentication failed). Live body secret absence therefore cannot be proven from outside the network. Jobs remain healthy (`sim-executions.txt`, `receiver-executions.txt`).
