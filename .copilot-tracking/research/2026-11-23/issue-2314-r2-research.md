---
title: Research issue 2314 round 2
ms.date: 2026-11-23
---

## Findings

* Criteria 1, 2 and 4 are already satisfied in main (PR 2325); criterion 3 has a saved search `zava-ai-usage-by-capability-and-period`.
* Gap: no test ties the saved query's `parse` pattern to the `AI_USAGE` line that `ai_consumption.py` emits, so a format change would silently empty the saved query.
* Read-only Azure check (resource group `ama`, workspace `log-cutover-test`): scheduled query rules for ledger digest, poison and AI limits exist; the AI usage saved search is not deployed. Nothing was changed.

## Planning Readiness

Ready. Research disposition: executed.
