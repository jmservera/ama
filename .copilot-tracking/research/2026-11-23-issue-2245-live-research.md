---
title: Research for issue 2245 (employee chat 500 and no generative answer)
ms.date: 2026-11-23
---

Task: issue-2245-live. Research disposition: executed. Planning Readiness: Ready.

## Findings

* Model call gate (`src/core/.../chat_panel.py` `_ask`): a model call needs permitted sources, a configured model, not rules-first, and no open AI suspension. Case-fact intents `unblock`, `claim`, `pas2035`, `sensor` (`chat_case_answers.RULES_FIRST`) answer from rules by design with 0 model calls. A thread with no case has no sources and abstains.
* Root cause of "no generative answer" on the live demo: an open all-scope AI suspension recorded 2026-11-18 ("Demo probe: negative test", evidence SYN-221-PROBE, restart null) is read from `GET /api/continuity`. The reply and the widget banner already say so plainly ("AI answers are on hold ... replies use rules only"), proven live 2026-11-23. Restart is a human-authority action; not performed.
* 500 on `POST /api/chat/threads`: not reproduced (8 consecutive creates 200 on revision 0000055; no `http-error` lines in the console tail). Cause unreadable (Log Analytics denied). Candidate: SQL write-lock timeout (SQL error 50002). `_unhandled` maps that to 503 for GET and HEAD only (issue 2237), so a POST thread create still returns the plain 500. Thread creation is one insert then commit, so a lock timeout leaves nothing committed and a retry is safe.

## Evidence

* [probe-chat-result.json](../../docs/reference/research/issue-2245-live-2026-11-23/probe-chat-result.json), [probe-continuity-result.json](../../docs/reference/research/issue-2245-live-2026-11-23/probe-continuity-result.json), [probe-widget-banner.json](../../docs/reference/research/issue-2245-live-2026-11-23/probe-widget-banner.json), screenshots in the same folder.
