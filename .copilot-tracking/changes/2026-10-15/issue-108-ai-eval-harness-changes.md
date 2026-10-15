---
title: Issue 108 AI evaluation harness changes
ms.date: 2026-10-15
---

* `mvp/zavaforward_mvp/ai_eval.py`: `OPEN_ITEMS`, `evidence_gate`, critical-miss gate, CLI output.
* `mvp/tests/test_ai_eval.py`: two new tests.
* `mvp/README.md`, `docs/reference/log.md`: documentation.
* Validation: `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` (see PR).
