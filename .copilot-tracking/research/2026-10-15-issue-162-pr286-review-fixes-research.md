---
title: PR 286 review fixes research
description: Evidence for five review findings on chat isolation after the #285 memory lifecycle merge
ms.date: 2026-10-15
---

## Disposition

Research executed (code read). Planning Readiness: Ready.

## Findings and evidence

* ChatIsolation.memory_for read chat_repo.memories directly, bypassing opt-in, global and per-task switches and labelling. `ChatPrivacy.prompt_memory(user, task)` in `mvp/zavaforward_mvp/chat_privacy.py` is the gated source.
* `POST /api/chat/memory` called `add_memory(user, content)`; #285 made `task` keyword-required and opt-in mandatory. Lifecycle methods exist: opt_in, opt_out, edit_memory, delete_memory, set_global, set_task, list_memory, memory_status.
* `turn()` stored the model reply unredacted via `store.chat_add_message`; `redact()` is the shared pass.
* `build_prompt` received the raw question; only the stored copy was masked.
* `_chat` mapped ChatForbidden to 403 and ChatNotFound to 404; an unavailable case raised ChatForbidden, so case existence could be probed.

## Decision

Role denial and break-glass refusal stay 403 (no case information). Case-out-of-scope becomes ChatNotFound (404).

## Open items (unchanged)

Admin/break-glass content policy (BRD OD-46), contractor chat, live-model prompt-injection evaluation (OD-49).
