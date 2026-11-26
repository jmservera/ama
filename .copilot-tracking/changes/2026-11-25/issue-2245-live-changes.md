---
title: Changes for issue 2245 (2026-11-25 live run)
ms.date: 2026-11-26
---

## Changes

* `src/agents/src/zava_forward/agents/chat.py`: any `financial-held` reason that is not a budget limit now gives outcome `spend-held` (was `provider-unavailable`).
* `src/core/src/zava_forward/core/chat_panel.py`: `SPEND_HELD_FALLBACK` and `SPEND_HELD_NOTE`; the reply says the demo spending control is holding AI answers and no model was called.
* Tests: `src/agents/tests/test_chat_model.py` (mapping and receipt outcome), `src/api/tests/test_chat_panel.py` (reply wording).
* Evidence: `docs/reference/research/issue-2245-live-2026-11-25.md` and its folder (probe scripts, JSON, screenshots); `docs/reference/README.md` and `log.md` entries.

## Classification

FULL tier (src change). Local checks run: agents `test_chat_model` (18 OK), api `test_chat_panel` (79 OK, 1 skipped), `test_content_standard` (30 OK), core chat tests (117 OK), mypy and ruff for agents and api clean; core mypy has 3 errors identical on the unchanged base (telemetry stubs, device_provision). `rpi-checks.py --all` not run (coordinator gate). Not pushed, not deployed.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Thread creation does not 500 | Proven (16 of 16 API creates 200 on 0000076; occasional 503 `sql-write-lock-busy` with plain message); 2026-11-22 cause unproven | probe JSON, screenshots |
| Model-answerable question shows "Model calls: 1" | Proven in the widget, 2026-11-26 00:14 UTC | `screens/widget-model-call.png`, `AI_USAGE` log |
| Banner plain when answers are rule-based | Fixed and unit tested; unproven live until deployed | tests |
| Which skills and routes call the model, why none did | Proven (rules-first skip model; held ledger forces rules; `liability-unknown` poisoned the 2026-11-25 budget) | source, logs |
| Why the reservation went unsettled | Unproven: needs SQL lock inspection or Log Analytics, unavailable | note |
