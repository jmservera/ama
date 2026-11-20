---
title: Details for issue 217
ms.date: 2026-11-17
---

Phase 1: after test_sql_new_statements_are_portable_and_append_only, add a test that runs the engine, then for each table in rule_engine.TABLES asserts UPDATE raises sqlite3.IntegrityError and the row count is unchanged. No source change; no store change.
