---
title: Issue 221 round 1 details
ms.date: 2026-11-03
---

* Phase 1: run `unittest` on `test_operator_suspension.py` with core, agents and api `src` on PYTHONPATH (installed distributions point at another worktree), ruff check, mypy with `--cache-dir=/tmp/mypy-221`.
* Phase 2: write dated artifacts; clean ignored caches.
