---
title: Issue 80 stack integration plan
description: Validate combined parent adbca56e plus current main b8394cd5 without source change
ms.date: 2026-11-11
---

## Objective

Closure-first integration validation of PR1423 (head `adbca56e`) against current main `b8394cd5`. No source edit, no merge commit unless a real conflict appears (none: trial tree `93f5a0c9`).

## Phases

* [ ] Phase 1: run targeted checks on the combined trial-merge tree in the owned scratch worktree and venv: child 13 + 6 (Chromium, no skip, heavy lock) + handoff guidance 9 + `test_handoff_api`, parent journey 31, list-export 11, static 60, role inventory, main-side guards (resident API, core resident decisions, Atlas checker test).
* [ ] Phase 2: Ruff check/format, API mypy, Node syntax for changed JS (`app.js`, `ops.js`) on the combined tree.
* [ ] Phase 3: `app.js` differs from `2cc34027` (child `pendingHandoffs` hunk; `ops.js` and checker unchanged), so the earlier PASS is historical only. Run ONE whole `capacity_browser_check --axe` on the combined tree under the heavy lock; record hashes; no repeat after red (critique PC-001).
* [ ] Phase 4: native review, commit own RPI only, handoff.

## Stop rules

* Any real failure: record first failure, stop for Root, no C6, no source fix. Busy heavy lock: do other work and report the browser check as needed, not passed.
