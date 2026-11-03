---
title: "Changes: #432 resident adapter usage sink"
ms.date: 2026-11-03
---

* Changed `api/resident_demo/assistant.py`: optional counts-only `record_usage` sink. Added two tests to `test_resident_assistant_provider.py`.
* No knowledge-base, log.md, price, budget, ledger wiring or activation change; no figure or cost introduced.
* Validation (focused tier): 39 tests (resident provider, API, aoai) and 31 tests in test_ai_consumption pass; ruff check and format and mypy (cache /tmp/mypy-432) clean on the changed files. Tests ran with PYTHONPATH pointing at this worktree's src because the shared pip environment installs another worktree. Not run: tools/rpi-checks.py gate, benchmarks, full suites, live Azure calls. No security, infrastructure, SQL or deployment code touched.
