---
title: Issue 164 chat evaluation phase details
description: File-level detail for each phase
ms.date: 2026-10-15
---

## Phase 1

* `src/core/.../chat_panel.py`: `OUT_OF_SCOPE`, `out_of_scope()`, `REFUSED`, `_carry()`; refusal happens before any model call and is stored as an assistant message.
* Tests: `src/core/tests/test_chat_panel.py`, `src/api/tests/test_chat_panel.py`.

## Phase 2

* `src/agents/.../chat_eval.py` (`--json`, `--record PATH`); `src/agents/evals/chat_golden.json` (21 scenarios, 3 known gaps recorded as failures); `registry.json` entry; `tests/test_chat_eval.py`.

## Phase 3

* `web/chat.js`, `src/agents/README.md`, `docs/reference/README.md`, `docs/reference/log.md`.
