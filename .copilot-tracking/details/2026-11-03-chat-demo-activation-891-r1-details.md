---
title: Issue 891 round 1 details
ms.date: 2026-11-03
---

1. `src/core/.../ai_registry.py`: `DEMO_ACTIVATION` record; `demo_activation_honoured(task, env)`; `authorizes_live(task, env=None)` true only via the exact switch value plus `ZF_DEPLOYMENT_PROFILE=demo`, chat task only.
2. `src/api/.../server.py`: `/api/chat/status` adds `demo_activation` and `demo_disclaimer`; `chat_admission` unchanged (still needs `store.ai.gate`).
3. `src/api/.../web/chat.js`: disclaimer paragraph (role note, described-by), model-generated label.
4. `src/api/tests/test_chat_panel.py`: default deny, switch on, wrong values, provider failure fallback, refusal before model, web assertions.
5. Docs: demo storage approval note section; `docs/reference/log.md`.
