---
title: SQL Entra auditing Bicep changes (issue 143)
ms.date: 2026-11-14
---

## Changes

* Added infra/tests/test_sql_entra_auditing_bicep.py (7 tests): Entra-only auth, no password or SQL login literals, TLS 1.2, public access disabled, no firewall rules, auditing, diagnostics, main.bicep wiring.

## Validation (focused tier)

* python3 -m unittest on the new file: 7 passed.
* ruff check/format --isolated and mypy with /tmp cache dirs: clean.
* Full gate not run (focused tier by instruction); hosted CI not observed.
