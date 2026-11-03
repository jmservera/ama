---
title: Issue 891 round 1 changes
ms.date: 2026-11-03
---

* Changed ai_registry.py, server.py, chat.js, test_chat_panel.py, the demo storage approval note and log.md as in the details file.
* No infra, SQL or deployment file changed.

## Validation

Run: test_chat_panel (50 OK, 1 skipped), test_ai_tasks (67 OK), agents test_chat_eval (35 OK); `ruff check` on changed Python; `mypy --cache-dir=/tmp/mypy-891` on ai_registry and server (clean).

Not run: complete gate, full suites, benchmarks, browser checks, Azure, deployment, live check.
