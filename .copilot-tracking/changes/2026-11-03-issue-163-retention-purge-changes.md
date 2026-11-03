---
title: "Issue 163 retention purge changes (2026-11-03)"
ms.date: 2026-11-03
---
* Changed: `src/core/src/zava_forward/core/chatthreads.py`, `chat_privacy.py`, `src/core/tests/test_chat_privacy.py`, the demo storage approval record, `docs/reference/log.md`.
* Divergence: none. Amendments: a stray no-op test line was removed.
* Validation run: `pip install -e src/core` in a /tmp venv; `python -m unittest discover -s tests -p "test_chat_*.py"` 99 OK; ruff check clean; mypy (cache /tmp/mypy-163) clean on the two modules.
* Not run: complete gate, full suites, benchmarks, Azure SQL, any scheduler. `ruff format --check` reports the touched files unformatted, as before this change (not enforced).
