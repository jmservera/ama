---
title: Issue 1231 r20 research, local alignment to parent79 0a8ecd50
description: Prospective research for one normal merge of local parent79 0a8ecd50 into the child
ms.date: 2026-11-07
---

Disposition: executed (read-only), committed before the merge. r15 deviation and r16 to r19 records are preserved.

* Child start 120bbccea44d031df41efb5803fff2b92dce54b4 / tree 8e9e29a2, ignored-clean, branch fix/ranking-archive-concurrent-writer-metadata. PR1242 OPEN, base feat/ranking-publication-runner-79.
* Local parent79 0a8ecd50f608964066ce07ae5c13c8f299b8daf7 / tree f185156daae23fe4878b7f00b967f73eceaf6be6, ignored-clean, in issue-79-publisher. Merge-base is prior parent 47de325d. Stale remote parent not used.
* Main c1a164829e77efe45f5f002740bd79699b89b334 (#1255) is an ancestor of the parent; origin/main equals it; nothing fetched or moved.
* Incoming 47de325d..0a8ecd50, outside .copilot-tracking: docs/reference/log.md (append-only), src/api/tests/test_assistant_release.py (received main test, not ranking), tools/rpi-checks.py, tools/test_rpi_checks.py. Production src/*/src unchanged.
* Child owns ranking source, tests, README; no overlap. Dry run clean (tree 9e3f90a6 before planning files).
* Selectors: core 70, API wiring 18, test_assistant_release, tools test_rpi_checks and test_backlog_sync (no service; opt-in SQL class skips are not acceptance), Ruff, format, mypy. Known formatter diagnostic on incoming test files is preserved, not reformatted.
