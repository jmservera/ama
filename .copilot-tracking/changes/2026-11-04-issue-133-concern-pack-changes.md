---
title: "Issue 133 concern pack changes (2026-11-04)"
ms.date: 2026-11-04
---
* Changed: `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/ai_registry.py`, `src/core/tests/test_aftercare.py`, `src/core/README.md`, `docs/reference/log.md`.
* Amendment: the first registry entry was enabled and broke `assistants.registry` (legacy binding KeyError, 2 failures in `test_assistant_release`); changed to disabled as the chat task is. No other divergence.
* Validation run: `test_aftercare` and `test_challenges` (33 OK); core `test_rai_release*` (12 OK) and `test_funding_automation_boundary` (8 OK); api `test_ai_tasks` (69 OK), `test_assistant_release` (45 OK) and `test_chat_panel` (52 OK, 1 skipped); ruff check and format; mypy with `--cache-dir=/tmp/mypy-530`. Tests used `PYTHONPATH` to this worktree's `src` trees because the editable installs point at another worktree.
* Not run: complete gate, benchmarks, full suites, browser checks. Focused tier; no security, infrastructure, SQL or deployment change.
