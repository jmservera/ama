---
title: Issue 164 chat evaluation changes
description: Changes, commands and results for the chat evaluation slice
ms.date: 2026-10-15
---

## Changes

* Added `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/evals/chat_golden.json`, `src/agents/tests/test_chat_eval.py`; registry entry `chat-golden`.
* Modified core `chat_panel.py` (refusal, history carry filter), core and api `test_chat_panel.py`, `web/chat.js`, agents README, reference index and log.
* No `mvp/` change; no SQL added; no enablement.
* Divergence: an existing api test asked "Approve the case and email the resident now." to test withheld output; that now correctly refuses first, so it asks a neutral question.

## Commands and results (venv /tmp/zf164, pip install -e src/core src/agents[dev] src/api)

* agents `PYTHONPATH=../core/tests python -m unittest discover -s tests -q`: 62 OK (baseline 47).
* core `PYTHONPATH=tests python -m unittest discover -s tests`: 258 OK.
* api `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q`: 458 run, 92 skipped, OK after the test fix (one failure first, the divergence above).
* ruff check, ruff format --check and mypy on agents, core and api: clean.
* `python -m zava_forward.agents.chat_eval`: 21 scenarios, 42 turns, 0 unexpected failures, 3 known gaps recorded; card answers 18 of 18 answer turns, AI 18, workflow-only 0; enablement insufficient, task disabled.
* Local app: `build_mvp_dataset.py --seed 20260901` (980 cases) then `python -m zava_forward.api.server`: `/` 200, `chat.js` serves the refusal handling, unauthenticated chat POST 401.
* `docker ps`: permission denied; image and mssql evidence rely on CI.

## Owner decisions and open criteria (unticked)

* [ ] Pass thresholds for grounding, refusal, injection and poisoning.
* [ ] Accountable reviewer and the enabled or disabled state of the chat task.
* [ ] Independently labelled held-out set.
* [ ] Live model run (payload, provider handling, budget).
* [ ] Human exercises (consent, accessibility, privacy) and review-effort comparison.
* [ ] Close the 3 recorded known gaps (stale answer in history, unsupported claim with valid citation, injection obeyed in plain prose).
