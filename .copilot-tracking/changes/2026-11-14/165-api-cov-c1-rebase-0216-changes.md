---
title: 165-api-cov-c1-rebase-0216 changes
ms.date: 2026-11-14
---

Cycle 1 rebase of edb19fade onto origin/main ac70acafac (PR #1599). Refs #165. Original 165-api-cov-floor-0038 artifacts are preserved.

* Research: only conflict was the mypy override module list in src/api/pyproject.toml; PR #1599 added test_assistant_restart_non_replenishment, edb19fade added test_auth_branch_floor.
* Plan and details: keep both entries in the list; no other file changed.
* Changes: conflict resolved with both entries; rebase completed; no push.
* Review: tomllib parse OK; ruff check and format --check clean on both new test files; agents tests.test_branch_floor 9 tests OK; api tests.test_auth_branch_floor plus tests.test_assistant_restart_non_replenishment 23 tests OK. The brief's PYTHONPATH lacks tests/ so the restart test cannot import test_assistant_release; adding :tests passes. Focused tier; no hosted CI observed, no full gate run.
