---
title: Issue 2314 saved query and emitter contract, round 2
description: Evidence that the AI usage saved query matches the emitted AI_USAGE line
ms.date: 2026-11-23
---

## Evidence

* The saved search in `infra/modules/operationalMonitoring.bicep` and the workbook panel `ai-usage-by-capability` both parse `AI_USAGE capability=... period=... calls=... tokens=... usage=... outcome=...`.
* `src/core/src/zava_forward/core/ai_consumption.py` emits that line. A new infra test compares the three.
* Read-only `az` check on 2026-11-23 (resource group `ama`, workspace `log-cutover-test`): alert rules for ledger digest, poison queue and AI limits exist; the saved search is not deployed. Deployment stays owner-authorised.
* Unproven for the demo: named human owners (roles are proposed) and execution of the query on live data.
