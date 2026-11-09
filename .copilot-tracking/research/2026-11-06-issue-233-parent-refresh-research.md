---
title: "Research: refresh PR 1224 onto the advanced parent 149"
description: Prospective research for a bounded merge of the declared parent into the published issue 233 branch
author: Copilot
ms.date: 2026-11-06
ms.topic: reference
---

Written on 2026-11-06 before any merge or repair. This is maintenance of published PR 1224, not new feature work. Issue 233 pauses new implementation for dependencies and UX acceptance. Original late artifacts (checker 13:09Z before Research 13:12Z and Plan 13:13Z on 2026-11-05), corrections 1 to 3, correction 4 and the 2026-11-05 forward recovery records are retained and do not cure that history.

## Trigger and identities

* PR 1224 head `1addf9c3535700bb76a8b79fe3f18bd3ac54d270` (tree `c82e05379490c542f9006e17d4f2488bf8cc9f62`), base `test/ux-evidence-149`, is now `CONFLICTING` after PR 1237 merged into the parent at `c66f2cdd1bd3f841cd61d8487791931e8762a53c` (2026-11-06T20:28:10Z).
* Fresh fetch: `origin/main` is `56eec736906774ef56d8c9a66ed7f3f9c1e520c6`; `origin/test/ux-evidence-149` is `c66f2cdd`; the merge base with the branch is `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. The parent is not main and stays the target.
* Isolated worktree `/tmp/a233f`, branch `fix/atlas-tensions-233-parent-refresh`, clean including ignored files at the published head. The original issue worktree and its six ignored caches are untouched.

## Overlap evidence (read only)

* Parent changed 13 files since the base: 7 RPI records for issue 153, `docs/reference/README.md`, `docs/reference/log.md`, `docs/reference/research/ux/content-standard.md`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_document_controls.py`, `src/core/src/zava_forward/core/doc_controls.py`.
* This branch changed `docs/reference/README.md`, `docs/reference/log.md`, `docs/reference/research/ux/atlas-screen-trace.md`, the checker, its test, `test_role_screens_conformance.py`, `src/api/README.md` and 2026-11-05 RPI records. Shared files: `docs/reference/README.md` (one index row edit here, a new paragraph elsewhere in the parent) and `docs/reference/log.md` (both append at the end).
* A read-only `git merge-tree` dry run reports no textual conflict, while GitHub reports CONFLICTING. The likely cause is the shared end of `log.md`. The real merge will confirm.
* No runtime, checker, test or static JavaScript file is shared. Parent runtime changes (`doc_controls.py`, document-control tests) are unrelated to the checker.

## Boundaries and unknowns

* Resolve only knowledge base conflicts by keeping both sides, with earlier log entries unrewritten and in context. Stop for a handoff if a conflict needs runtime, test, checker or UX intent changes, or if the parent moved.
* The 2026-11-05 receipt `/tmp/r233j/receipt.json` and the 194-PASS Chromium run are historical after this merge. No browser, gate, SQL or heavy lane runs here because issue 86 owns the sole full lane. No native receipt is claimed.
* C2 engineering only; C4, C5, WCAG, AT and user acceptance remain unmet. Planning readiness: Ready.
