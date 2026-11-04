---
title: Issue 164 call authorization changes
ms.date: 2026-11-04
---

Refs #164. Slice 1.

* Changed `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/tests/test_chat_eval.py`, `src/agents/README.md`, `docs/reference/log.md`.
* Unmet #164 criteria: thresholds approved and reviewer named; held-out frozen set; memory-poisoning and injection assurance on an actual model; human exercises; actual-call evidence under authorisation (the guard exists, no authorisation or call does); price and review effort (cost Unknown).
* Validation run: test_chat_eval (39 OK, run with PYTHONPATH to src dirs), ruff check and format, mypy (cache /tmp/mypy-530). Not run: gate, full suites, benchmarks, rpi-checks. Independent review and hosted CI still required.
