---
title: Issue 80 round 4 details
description: Phase details
ms.date: 2026-11-05
---

* Phase 1: `git merge --no-ff -m ... bb3a3b03c` on the child; verify the parents, that child-owned paths are unchanged and that no file conflicts.
* Phase 2: with `PYTHONDONTWRITEBYTECODE=1`, external `RUFF_CACHE_DIR` and `--no-cache`, `mypy --cache-dir` outside the checkout. Print `zava_forward.*` module `__file__` first. Selectors: api `test_list_export_api`, `test_role_endpoint_inventory`, `test_loading_feedback`; core `test_list_export`. Ruff and mypy on api and core.
* Phase 3: write r4 changes and review, then the state file; commit.
