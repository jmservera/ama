---
title: "Issue 163 age-based retention changes (2026-11-03)"
ms.date: 2026-11-03
---
* Changed: `src/core/src/zava_forward/core/chatthreads.py`, `chat_privacy.py`, `src/core/tests/test_chat_privacy.py`, the demo storage approval record (plus disclaimer), `docs/reference/log.md`.
* Divergence: none.
* Run: focused `test_chat_*.py` 99 OK (JSON store and SQL store variants); ruff clean; mypy (cache /tmp/mypy-163) clean on the two modules.
* Not run: complete gate, full suites, benchmarks, Azure SQL. Touches the SQL repository, so the gate is for the coordinator.
