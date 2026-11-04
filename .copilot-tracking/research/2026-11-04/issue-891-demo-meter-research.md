---
title: Research for #891 demo meter seeding
ms.date: 2026-11-04
---

* Task: issue-891-demo-meter. Research disposition: executed. Planning readiness: Ready.
* Delivered already: #892 (demo activation record and switch), #995 (chat admission skips the legacy SQL release denial). The owner live check on 2026-11-04 (main 16d7a3de2) showed one model call attempted and a rules-only reply.
* Confirmed cause from code: `Consumption.reserve` (`src/core/src/zava_forward/core/ai_consumption.py`) holds the call as `authority-unknown` unless the ledger holds an authority for the exact `(capability, configuration)` and a price for the configured model; `Ai._request` replaces the context configuration with `Ai.configuration(deployment, temperature, max_tokens)`. Nothing in the repo records either (only tests and `ai_consumption_demo.py` do). The held call raises `DispatchHeld`, `Ai.evidence` returns `financial-held`, and the chat panel shows the fallback with Tokens and Cost Unknown. This matches the live footer.
* Second cause found: `reserve(live=True)` also holds any call whose price is `synthetic`, because the endpoint is not loopback. A synthetic demo price therefore cannot admit the call without a narrow, demo-only exception.
* Constraints: authority and price events are append-only and immutable; overlapping authority windows for one configuration are refused; reserved calls per root are capped by `max_calls`.
* Completion check: a completed call with unknown cached tokens records `liability-unknown`, which holds later calls. Azure returns `prompt_tokens_details.cached_tokens`; the test fake does the same.
* Not touched: SQL schema (events use the existing `assistant_events` table), infrastructure, production paths.
* Unknown: the real deployed gpt-4.1-nano response shape (cannot be verified offline), and whether `AI_MODEL_VERSION` is set (default `unattested`, which the seed matches).
