---
title: Changes for #891 demo meter seeding
ms.date: 2026-11-04
---

* Added `chat_demo_meter.py`, `Ai.synthetic_price_capabilities`, the `chat_admission` call and four real-store tests (see details).
* Validation run: `test_continuity`, `test_chat_panel`, `test_assistants` (194 tests OK, 59 skipped) and core `test_ai_consumption*` (40 OK); `ruff check` on changed files; `ruff format` on the new module; `mypy --cache-dir=/tmp/mypy-530` on the new module (clean).
* Not run: complete local gate, benchmarks, full suites, live deployment, live model call. No SQL schema, infrastructure or deployment change.
* Divergence: none from plan.
