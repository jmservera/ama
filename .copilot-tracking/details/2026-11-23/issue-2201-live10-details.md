---
title: Issue 2201 live10 details
ms.date: 2026-11-23
---

Phase 1: the class name of a plain `Exception` is not sensitive; the message may carry connection detail, so it is never printed. Phase 2: patch `rx.persistence` to raise `RuntimeError("secret-host")` with a valid control file and assert the output contains `error_type=RuntimeError` and not `secret-host`. Phase 3: from `src/api`, `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests.test_live_control -q`, `PYTHONPATH=../core/src:../agents/src python3 -m mypy`, `ruff check` and `ruff format --isolated --line-length 100 --check`.
