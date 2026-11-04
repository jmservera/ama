---
title: Issue 134 slice 4 details
ms.date: 2026-11-04
---

## Phase 1

`src/core/src/zava_forward/core/perspective_walkthroughs.py`: `EVIDENCE` maps eleven manifest profile IDs to five elements; `register()` marks cells `partial` or `unmet`; `check(root)` blocks profile/PRD mismatch, missing cells, invalid status, missing reason, missing evidence files. Read-only, no store, clock or network.

## Phase 2

`src/core/tests/test_perspective_walkthroughs.py`, four tests.
