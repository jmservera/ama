---
title: Issue 470 core suite timeout details and critique
ms.date: 2026-11-17
---

* Critique: shard-core alternative rejected (changes receipt shapes, `SHARDED_PROJECTS`, partition rules; larger risk). Timeout is an upper bound; a hang still fails closed with exit 124, only later. Receipt `timeout_seconds` identity check is retained, so a receipt made with the old 1800 s core value no longer verifies; this is intended and noted.
* Verdict: proceed; no conflicts with confirmed decisions.
