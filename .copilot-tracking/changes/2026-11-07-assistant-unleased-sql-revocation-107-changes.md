---
title: Changes for unleased SQL revocation coverage (#107)
description: Actual delta, commands, exits and skips for the bounded test
ms.date: 2026-11-07
---

Plan: [plan](../plans/2026-11-07-assistant-unleased-sql-revocation-107-plan.md). Planning commit d60d46b23 precedes the source edit.

## Delta

Only `src/api/tests/test_assistant_release.py`: imports `os` and `MssqlFixture`; mixin `UnleasedRevocation` with one test; `SqliteUnleasedRevocation` (local proxy) and `MssqlUnleasedRevocation` (gated on `ZF_TEST_MSSQL=1`). No production, schema, approval or attestation change.

## Commands (from `src/api`, own-worktree venv in `/mnt/ama-gates/g107-unleased-preparation-1107`, external caches, PYTHONDONTWRITEBYTECODE=1)

* Import origin: `zava_forward.core.assistants` and `zava_forward.api` resolve under this worktree.
* `python -m unittest test_assistant_release.SqliteUnleasedRevocation test_assistant_release.MssqlUnleasedRevocation` with `PYTHONPATH=tests:../core/tests:../agents/tests`: exit 0, 2 tests, 1 skipped (the MSSQL class, needs `ZF_TEST_MSSQL=1`).
* Selector `test_assistant_release test_assistants test_continuity`: exit 0, 190 tests, 59 skipped, all SQL Server opt-in skips.
* `ruff check .`: exit 0. `mypy`: exit 0, 188 files.
* `ruff format --check tests/test_assistant_release.py`: exit 1 on both the base file and the new file; the file is excluded in the canonical configuration, so this is a baseline diagnostic and no unrelated code was reformatted.

## SQL disposition

Implemented-unverified. The SQLite pass is a proxy, not SQL acceptance. The MSSQL class has not run.

## Future admission

Run `ZF_TEST_MSSQL=1 ZF_SQL_SERVER=localhost python -m unittest test_assistant_release.MssqlUnleasedRevocation -v` from `src/api`, then FULL on the frozen head after a normal merge of the then-current main (1252 pending), under one nonqueued lock with stdin /dev/null and a new external output directory.
