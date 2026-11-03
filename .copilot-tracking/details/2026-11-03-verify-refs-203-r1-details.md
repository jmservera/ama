---
title: Issue 203 round 1 details
ms.date: 2026-11-03
---

## Phase 1: link regression test

* Walk `*.md` under the repository root, skipping `.git`, `.copilot-tracking`, `support`, `docs/capstone/` and `docs/reference/log.md`.
* Ignore fenced code, external URLs, anchors, templated targets.
* Assert every relative target exists. Success: 0 unresolved.
