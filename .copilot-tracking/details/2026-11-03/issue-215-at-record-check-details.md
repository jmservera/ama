---
title: Issue 215 AT record check details
ms.date: 2026-11-03
---

* Input: JSON list of {session, role, mode, tool, chat_available, result, barrier, workaround}. Roles are the seven kit audiences; modes are keyboard-only and screen-reader; results are pass, fail, blocked.
* Exit 0 only when every role has both modes, screen-reader records name tool and version, non-pass results state a barrier, and every chat-bearing role has a chat-unavailable run. Non-pass results are listed as findings to route.
* Fluent 2, WCAG baseline, plain-language standard, human approval and consent boundaries preserved; no UI change.
