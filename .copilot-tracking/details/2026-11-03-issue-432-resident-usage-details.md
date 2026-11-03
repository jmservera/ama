---
title: "Details: #432 resident adapter usage sink"
ms.date: 2026-11-03
---

* Source: `src/api/src/zava_forward/api/resident_demo/assistant.py`. New optional constructor argument `record_usage: Callable[[dict[str, int | None] | None], None] | None`, default None (behaviour unchanged).
* After the reply is parsed and before it is validated, `_record` reads `usage` through `zava_forward.core.ai_consumption.usage` (non-negative bounded ints, total equals prompt plus completion, optional cached tokens) and calls the sink with the counts or None when absent or invalid. Usage is therefore kept for a reply that is later rejected as invalid.
* Any sink exception is swallowed so the resident outcome and manual or rules path are unchanged.
* Tests: `src/api/tests/test_resident_assistant_provider.py`.
