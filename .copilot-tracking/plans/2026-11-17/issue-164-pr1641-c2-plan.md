---
title: Issue 164 PR 1641 c2 plan
ms.date: 2026-11-17
---

## Plan

* [x] Phase 1: merge origin/main 7de4a8110289 (clean auto-merge, staged).
* [ ] Phase 2: run core, agents, api targeted tests sequentially; mypy per project; ruff check and format.
* [ ] Phase 3: commit merge, record changes and review, freeze.

Critique: single pass; compatible, no conflicts with confirmed decisions (merge not rebase, no push).
