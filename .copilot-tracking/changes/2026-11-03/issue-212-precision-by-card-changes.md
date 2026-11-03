---
title: Issue 212 per-card precision changes
description: Changes record
ms.date: 2026-11-03
---

* Modified `src/core/src/zava_forward/core/rule_engine.py`, `src/core/tests/test_rule_engine.py`,
  `src/core/README.md`.
* Validation: core test_rule_engine 30 OK, test_source_monitor 29 OK, api test_rule_alerts 7 OK,
  ruff check and format clean, mypy clean (`--cache-dir=/tmp/mypy-212`).
* Not run: RPI gate, benchmarks, full suites.
* No divergences from plan.
