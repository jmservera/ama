---
title: Issue 1231 r29 details, final reconciliation
description: Phase acceptance for the final root and main reconciliation
ms.date: 2026-11-07
---

* Phase 2 acceptance: ranking helper, runner, Store, server, README and the two ranking test files equal the child's 5630fb25 blobs; `.copilot-tracking` gains only added files; `docs/reference/log.md` has no deleted lines and holds the main, root and child entries; UI source, UI tests and the score JSON equal root d99e6901.
* Phase 3: record exact commands and exits; run the `Config` class at `test_exception_register.py:163` explicitly.
* Phase 4: FULL only on exact main f0af and clean root and child; no source write after the runner starts.
