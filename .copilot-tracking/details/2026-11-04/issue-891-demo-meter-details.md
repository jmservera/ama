---
title: Details for #891 demo meter seeding
ms.date: 2026-11-04
---

* `src/core/src/zava_forward/core/chat_demo_meter.py` (new): `ensure(store, max_tokens, env, now)`; no-op unless `ai_registry.demo_activation_honoured`; window is the current UTC day (start of day to next day, so the records expire); ids derive from `synthetic-demo-chat-<date>` so restarts are idempotent and days adjoin without overlap; price `synthetic=True`, placeholder rates; authority owner `synthetic-demo-owner-jmservera`, `max_calls=1`, `max_depth=1`, budget 20 calls, 100000 tokens, amount 1; configuration from `Ai.configuration(fast, 0, max_tokens)` to match the evidence call; failures are logged by type only.
* `src/core/src/zava_forward/core/ai.py`: `synthetic_price_capabilities` frozenset, default empty; `live` is false for a listed capability.
* `src/api/src/zava_forward/api/server.py`: demo branch of `chat_admission` calls `ensure` with `CHAT_MAX_TOKENS` before the suspension check.
* `src/api/tests/test_continuity.py`: `ChatDemoMeterOnSqlStore` (four tests): demo admits one call and records price, authority, reserved, completed with no alert; second call in one request is held; no switch means nothing seeded and zero transport calls; synthetic price still holds a live call when the exception is not set.
