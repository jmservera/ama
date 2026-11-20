---
title: Changes for issue 217
ms.date: 2026-11-17
---

* Added test_every_audit_table_refuses_update_and_keeps_rows to src/core/tests/test_rule_engine.py. No source or store change.
* Validation (FOCUSED): test_rule_engine 31 OK; earlier baseline of five core modules 96 OK; mypy src/core clean (327 files); ruff format --isolated --line-length 100 --check clean.
* Not applicable: SQL/browser/full gate (test-only, existing triggers unchanged); src/api suite not touched.
