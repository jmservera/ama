---
title: Details for issue 2245 (2026-11-25 live run)
ms.date: 2026-11-25
---

* `src/agents/src/zava_forward/agents/chat.py`: add `SPEND_HELD = "spend-held"`; when `outcome == "financial-held"` and the reason is not a budget limit, raise outcome `spend-held`.
* `src/core/src/zava_forward/core/chat_panel.py`: add `SPEND_HELD_FALLBACK` and `SPEND_HELD_NOTE`; map outcome `spend-held` in the fallback selection and in the rules-note lookup; include the new fallback text in the grounded-rules replacement tuple.
* Tests: update the existing mapping test (liability-unknown now `spend-held`); add a panel test beside `test_budget_hold_reply_names_the_allowance_not_unavailability`.
