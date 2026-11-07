---
title: Changes for SQL wiring of the unleased revocation test (#107)
description: Actual delta, commands, exits and skips for the continuation; actual SQL still not run
ms.date: 2026-11-07
---

Plan: [plan](../plans/2026-11-07-assistant-unleased-sql-revocation-107-sql-wiring-plan.md). Prospective records were committed first (`3126ad3d6`). Earlier changes and Review records are unchanged.

## Actual delta

* Source commit `6685263711dedfc1a01799729a2b55ecabff00ce`: `tools/rpi-checks.py` appends `test_assistant_release.MssqlUnleasedRevocation` to `SQL_SELECTORS`; `tools/test_rpi_checks.py` asserts membership; `src/api/tests/test_assistant_release.py` gains a mixin `setUp` that deletes non-`fx-` release rows after base setup (critique finding) and a release assertion filtered to `fx-CAP`; only the added block was formatted.
* One normal merge `b0df5abeec71c2a377ff1e279c3cb7d5a24f76e4` (tree `5356a286b09e70cf612fa3099fd01f82f7fb96d5`) of main `a1d265340ba7d6f14b24e028362b2d5f4bb80126` (PR 1252). Parents: first `6685263711...`, second `a1d265340...`. Incoming delta is the 15 files of 1252 (tools/backlog-sync.py, its test and 1251 records); the three edited blobs are identical before and after; `git diff --check` exit 0. No rebase, force or retarget. Local ref `backup/issue-107-sql-wiring-pre-merge-HEAD` preserves the pre-merge head. The earlier candidate `3a9523a88` remains an ancestor.
* Main may still gain a score-only descendant; a further normal merge is then needed before FULL.

## Generated metadata

The three ignored egg-info folders (PKG-INFO, SOURCES.txt, dependency_links.txt, requires.txt, top_level.txt, created by this task's pip install at 14:21 UTC, owner azureuser) were moved by explicit path, with sha256 lists, to `/mnt/ama-gates/g107-sql-wiring-preparation-1107/egg-info-relocated/`. Afterwards `zava_forward.core`, `zava_forward.agents` and `zava_forward.api` resolve under this worktree, `pip list` shows editable worktree locations, `pip check` exit 0 and `git status --short --ignored` is empty.

## Commands and results (own venv `/mnt/ama-gates/g107-unleased-preparation-1107`, external caches, PYTHONDONTWRITEBYTECODE=1, exits unmasked)

* `python -m unittest test_rpi_checks test_backlog_sync` from `tools`: exit 0, 103 tests.
* Tool lint as the runner configures it (`ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check`) on both tool files: exit 0. A bare `ruff check` without that configuration reports pre-existing EXE001 and ISC004 findings; this is not the canonical configuration and was not acted on.
* From `src/api`: `ruff check .` exit 0; `mypy` exit 0 (188 files); new classes `SqliteUnleasedRevocation` ok and `MssqlUnleasedRevocation` skipped ("needs disposable SQL Server (ZF_TEST_MSSQL=1)"), exit 0; `test_assistant_release test_assistants test_continuity` exit 0, 190 tests, 59 skipped, all SQL Server opt-in.
* Format qualifier preserved: `ruff format --check tests/test_assistant_release.py` still exits 1 because the file is excluded by the canonical configuration; the baseline file shows 51 diff hunks and the new file shows the same 51, and the added block alone checks clean.

## SQL disposition

Implemented and wired, unverified. The runner's SQL group now selects the class with `ZF_TEST_MSSQL=1` and the owned loopback container, so it would run unskipped; nothing was run on SQL here and the SQLite pass is only a proxy. Hosted CI (`src-ci.yml`) is not extended.
