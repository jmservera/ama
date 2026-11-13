---
title: Issue 152 changes
ms.date: 2026-11-13
---

* Added `test_ac043_manifest_declares_slice_coverage_and_unavailable` and `test_ac034_scope_reset_checks_follow_default_manifest` to `src/api/tests/test_workbench.py`.
* No manifest or design-system change: widths already aligned.
* Refreshed the `navigation-tests` sha256 in `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`.
* Validation: test_workbench and test_design_system OK; browser check passed against worktree sources (system Chromium 156); scenario manifest, needs inventory, cutover audit OK; ruff (src/api) and mypy clean. Full tier not claimed; AC-034/043 remain partial.
