---
title: Issue 950 plan
ms.date: 2026-11-04
---

* [ ] Phase 1: add `SEED_PROPOSER` and set it on each seed constraint (details: `.copilot-tracking/details/2026-11-04/issue-950-details.md`).
* [ ] Phase 2: test, ruff, mypy strict.
* Critique (one pass, direct): a named source constant is preferred over validating non-empty at construction, because it does not change the `Constraint` API used by other callers. Compatible; applied.
