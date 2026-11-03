<!-- markdownlint-disable-file -->
---
title: Issue 159 panel limits and consumption visibility changes
description: Changes and validation evidence
ms.date: 2026-11-03
---

## Changes

* `src/api/src/zava_forward/api/web/chat.js`: `limitsNote`, `usageNote`, intro paragraph `chat-limits`, consumption note in each reply detail.
* `src/api/tests/test_chat_widget_focus.py`: one new test.

## Validation (focused tier)

* Run: `test_chat_widget_focus` (10 OK, new test fails without the change), `test_chat_panel` (45 OK, 1 skipped), `test_chat_isolation` (32 OK), `test_chat_fixture_roles`, `test_accessibility_baseline` (8 OK); ruff check and format check on the changed test; mypy with `--cache-dir=/tmp/mypy-159` on the changed test.
* Modules run with source paths on PYTHONPATH because the distributions are not pip-installed in this worktree. Not run: gate, benchmarks, full suites, browser, screen reader. No knowledge-base file changed, so no log.md entry.
