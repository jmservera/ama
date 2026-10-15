---
title: "Plan details: conversational assistant panel (#159)"
ms.date: 2026-10-15
---

## Files

| File | Change |
| --- | --- |
| `src/core/src/zava_forward/core/chat_panel.py` | new: `ChatPanel.ask`, `permitted_sources`, `parse_reply`, constants |
| `src/core/tests/test_chat_panel.py` | new: parse and source tests |
| `src/core/pyproject.toml` | narrow mypy override `disallow_untyped_calls=false` for `chat_panel` |
| `src/agents/src/zava_forward/agents/chat.py` | new: `ChatModel` |
| `src/agents/tests/test_chat_model.py` | new |
| `src/api/src/zava_forward/api/server.py` | `App.panel`, `ask` and `proposals` routes |
| `src/api/src/zava_forward/api/web/{chat.js,index.html,app.js,style.css}` | panel UI |
| `src/api/tests/test_chat_panel.py`, `src/api/pyproject.toml` | new tests, exemption for the untyped harness |
| `src/api/README.md`, `docs/reference/{README,log}.md` | docs |

## Behaviour

* Answer kinds: `answer`, `abstain`, `fallback`, `withheld`; label always "AI suggestion, not approved".
* Each turn: `current_user`, `chat_resume` (owner only), `case_context` (projection); failures raise 403 or 404.
* Citations: ids `CASE/path` from projected facts; at most 12; stored as message evidence.
