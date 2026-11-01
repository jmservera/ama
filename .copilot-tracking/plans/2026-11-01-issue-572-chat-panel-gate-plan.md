---
title: Issue 572 chat-panel gate plan
ms.date: 2026-11-01
---

Research: [research](../research/2026-11-01-issue-572-chat-panel-gate-research.md)

* [x] Phase 1: Verify main already satisfies criteria 1 to 3 (focused gate tests, ruff on touched files).
* [x] Phase 2: Record RPI evidence only; no source change, to avoid broadening the skip allowlist or inventing new code.
* [ ] Phase 3 (out of scope): fresh complete exact-head gate with browser and MSSQL groups, run by the owner or CI on the final head.

Critique: executed once; verdict accepted. Any source change would duplicate merged work, so none is made.
