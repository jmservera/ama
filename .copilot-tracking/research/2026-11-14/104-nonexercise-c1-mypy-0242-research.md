---
title: C1 mypy correction Research
ms.date: 2026-11-14
---

Refs #104, PR #1602. CI `src-api` mypy reported 6 `no-any-return` errors in `src/core/tests/test_ai_consumption.py` because `src/api/tests/test_nonexercise_capability_bounds.py` imported it and `src/api` sets `warn_return_any`. Open PR #1608 edits the core test file, so it must not be touched. `pyproject.toml` and `docs/reference/log.md` are also out of bounds. Planning readiness: Ready.
