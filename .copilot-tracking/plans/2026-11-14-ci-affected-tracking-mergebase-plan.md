---
title: ci-affected tracking paths and merge-base diff plan
ms.date: 2026-11-14
---

## Phases

* [ ] Phase 1: add `is_inert_path` and skip it in `select`; update docstring.
* [ ] Phase 2: switch `changed_files` to `base...head`.
* [ ] Phase 3: unit tests for tracking/docs paths, watched docs paths, and `changed_files` (arg construction, non-zero exit, empty base).
* [ ] Phase 4: run focused validation (unittest, ruff check and format check), commit.

Critique: executed once inline; verdict compatible, risk is that docs non-Markdown and watched paths must still widen (covered by tests).
