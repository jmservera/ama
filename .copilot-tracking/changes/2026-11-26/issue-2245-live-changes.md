---
title: Changes for issue 2245 (2026-11-26 live run)
ms.date: 2026-11-26
---

## Changes

* `src/core/src/zava_forward/core/chat_demo_meter.py`: one synthetic authority per UTC hour instead of per day (same caps per slot); test in `src/api/tests/test_continuity.py`.
* `src/agents/.../chat.py`, `src/core/.../chat_panel.py` and tests: `spend-held` outcome and plain wording for non-budget ledger holds (carried from the unmerged 2026-11-25 branch).
* Evidence: `docs/reference/research/issue-2245-live-2026-11-26.md` and folder; index and log entries; the 2026-11-25 run artifacts are carried unchanged.

## Classification

FULL tier (src change). Local checks: api `test_continuity`, `test_chat_panel`, `test_content_standard` and agents `test_chat_model` (153 OK, 1 skipped). `rpi-checks.py --all` not run (coordinator gate). Not pushed, not deployed.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Thread creation does not 500 | Proven (8/8 on 0000079; 24/24 over two days). 2026-11-22 cause unproven: Log Analytics denied | probe JSON |
| Model-answerable question shows "Model calls: 1" | Proven in the widget on 0000079 (draft rejected by source check, said so) | screenshot, `AI_USAGE` log |
| Banner plain when answers are rule-based | Fixed and unit tested; unproven live until deployed | tests |
| Which skills and routes call the model, why none did | Proven (rules-first skip; held ledger forces rules; day-wide budget on 2026-11-25) | source, logs |
| Why reservations go unsettled | Unproven: needs SQL lock inspection, unavailable | note |
