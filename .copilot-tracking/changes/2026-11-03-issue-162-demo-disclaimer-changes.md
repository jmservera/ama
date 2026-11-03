---
title: Issue 162 demo-only disclaimer changes
ms.date: 2026-11-03
---

* Code: disclaimer constants, `basis` in audit details, `disclaimer` in the granted response.
* Test: asserts `basis` on all break-glass audit entries and the disclaimer text.
* Docs: new policy record, DPIA update, core README, index, log entry.

Validation (focused tier, worktree sources via PYTHONPATH because the installed editable packages point at another worktree): `test_chat_isolation` 32 OK; `ruff check` and `ruff format --check` clean for src/core and src/api; mypy (`--cache-dir=/tmp/mypy-162`) clean for src/core, and for src/api only 2 unused-ignore errors in tests/test_ai_consumption_api.py, identical without my change.
Not run: local gate, benchmarks, full suites, live Azure or model checks. Deployment setting `CHAT_BREAKGLASS_REF` not changed.
