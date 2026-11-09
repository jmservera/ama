---
title: "Recovery changes: issue 233 rendered tension checker"
description: Forward recovery changes record written after the planned light validation
author: Copilot
ms.date: 2026-11-05
ms.topic: reference
---

Written after the recovery Research, Plan and light validation, in that order. Plan: `../plans/2026-11-05-issue-233-rendered-tensions-recovery-plan.md`.

## Code retained, not authored now

* No source, test, documentation, CSS, API, auth or SQL file was edited in this recovery. The checker (blob `5e4e2d51b2ad95739a7f89bf070e24eebfa5f846`), its unit test (blob `08151f6f5cab26560d7f83f9c683a0384cb494c8`) and the documentation from HEAD `d540244fe52db2b6ce9bde6b8216639c49eea18f` are retained as they were. Their original authorship stays recorded in the earlier records.
* Added by this recovery: the Research, Plan/details, Changes and Review records dated 2026-11-05 with the `-recovery-` name.

## Validation executed now (light, 2026-11-05 18:48Z to 18:49Z)

* Source identity: HEAD and tree as above, tracked tree clean, blobs matched. Imports resolved to this worktree through `zava_forward.core.store`, `zava_forward.api.server`, `zava_forward.agents.dispatch` and the checker (exit 0).
* `tests.test_atlas_tensions_checker` and `tests.test_role_screens_conformance`: 19 tests OK, 0 skips (exit 0).
* `tests.test_atlas_screen_trace`: 17 tests OK; trace CLI "Atlas trace: complete" (exit 0).
* Ruff check with E,F,I,B,UP, py312, 100 columns, no cache and isolated: pass on both files. Ruff format check at 100 columns: both formatted (exits 0).
* `mypy --strict` on checker and test: no issues in 2 files (exit 0).
* External caches were under `/tmp/r233rec-light.ZRuvMN`. The six original ignored caches are unchanged.
* Not run: maintained gate, Chromium checker, DOM probe, SQL, builds. Another runner owns heavy admission.
