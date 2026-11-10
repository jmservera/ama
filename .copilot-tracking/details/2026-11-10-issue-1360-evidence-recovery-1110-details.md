---
title: Issue 1360 evidence recovery details
ms.date: 2026-11-10
task_id: 1360-evidence-recovery-1110
---

Commands use `/tmp/zf-1360-e1/bin` from `src/importer` and `src/core`: `ruff check`, `ruff format --check`, `mypy`, importer unittest discovery, and core `tests.test_import_refusals tests.test_priority_order` with `PYTHONPATH=tests`. Each log has a header with command, cwd, head and the exit code. Module origins are asserted under the worktree. Core format comparison: base is main `6d4cd6247`; its `sqlstore.py` and the current one are copied to a temp dir outside the worktree and checked with the project ruff config. The red diagnostic copies `src/core/src` to a temp dir, restores the old `except RuntimeError` there, and runs the two committed-case importer tests with that copy first on `PYTHONPATH`; it is labelled new, not original.
