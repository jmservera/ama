---
title: Issue 80 stack integration critique
description: One independent critique (rubber-duck subagent) of the integration plan
ms.date: 2026-11-11
---

Executed once on the final candidate plan by an independent read-only subagent (not the author). Verdict: Revise.

| ID | Finding | Disposition |
| --- | --- | --- |
| PC-001 | Whole capacity browser PASS cannot be carried by hash: `app.js` differs from `2cc34027` (child hunk in `pendingHandoffs`, no capacity or checker change; `ops.js` and the checker are unchanged). | Accepted. Plan amended: run ONE whole `capacity_browser_check --axe` on the combined tree under the nonqueued heavy lock; the earlier PASS stays historical, qualified evidence. A red result is reported as first failure, no repeat and no C6. |
| PC-002 | Tested SHAs and tree may differ from the final candidate. | Accepted. Record parent `adbca56e`, main `b8394cd5`, trial tree `93f5a0c9`; Root must run hosted checks on the real merge candidate and revalidate if either tip moves. Own RPI commit changes only tracking files. |
| PC-003 | `test_handoff_api` (existing JSON route) missing from targeted suite. | Accepted. Added to the plan. |

No conflict with a confirmed Root decision.
