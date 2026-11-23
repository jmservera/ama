---
title: Issue 2314 saved query on structured logs and live data, round 3
description: Evidence that the AI usage saved query groups real plain and JSON console lines and returns rows on the live workspace
ms.date: 2026-11-23
---

## Evidence

* New test `test_saved_query_groups_real_plain_and_structured_console_lines` turns the saved query `parse` literals into a regex and applies it to the real `AI_USAGE` format, as a plain console line and as the JSON line from `StructuredFormatter` (where the text sits inside `body`). Capability, Period, Calls, Tokens and UsageState group correctly in both; only the unused Outcome column absorbs the JSON tail.
* Read-only run on 2026-11-23 of the saved query text (workspace `log-cutover-test`, resource group `ama`, existing `az` login) returned one row: capability `chat-case-conversation`, period `2026-11`, 16 metered calls, 17833 known tokens, 1 call with unknown usage, cost record `Unknown (billing record not connected)`, variance `Unreconciled, not zero`. This proves the KQL parses and runs on live data. The saved search resource is still not deployed; deployment stays owner-authorised. No resource was created.
* Unproven for the demo: named human owners (roles proposed).
