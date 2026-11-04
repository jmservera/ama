<!-- markdownlint-disable-file -->
---
title: Issue 164 held-out freeze gate plan
description: Add chat_heldout gate and behavioural tests
ms.date: 2026-11-04
---

## Plan

* [x] Phase 1: add `src/agents/src/zava_forward/agents/chat_heldout.py` (digest, labeller, date, critical errors, bindings, leak checks, scripted scoring).
* [x] Phase 2: add `src/agents/tests/test_chat_heldout.py`.
* [x] Phase 3: run focused tests, ruff and mypy.

Details: [chat-heldout-freeze-164-details.md](../details/2026-11-04/chat-heldout-freeze-164-details.md). Critique: executed once by the implementing agent; compatible findings (reject same-person labeller, include system prompt in leak check) applied directly. Validation tier: focused; no security, infrastructure, SQL or deployment change.
