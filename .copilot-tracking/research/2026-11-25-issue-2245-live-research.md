---
title: Research for issue 2245 (2026-11-25 live run)
ms.date: 2026-11-25
---

## Scope

The issue has no checkboxes; its four asks are: (1) thread creation does not 500, (2) a model-answerable question shows "Model calls: 1", (3) the banner is plain when answers are rule-based, (4) which skills and routes call the model and why none did.

## Prior evidence reused

* The 2026-11-24 note proved (4) and thread creation 8/8 on revisions 0000060 and 0000066, and found the allowance-hold wording defect, fixed in tree (`allowance-used` in `chat.py`, `chat_panel.py`).
* Live revision is now 0000076 (created 2026-11-25T22:27Z). Whether it contains the wording fix, and whether today's 20-call allowance is spent, is unknown before probing.

## Investigation to do

Re-run the Playwright probe at runtime credentials on 0000076, check `/api/chat/status`, and read container logs for `AI_LIMIT_BREACH` or model-call lines.

Disposition: reused for (4); executed for (1), (2), (3). Planning Readiness: Ready.
