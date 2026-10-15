---
title: PR 282 CI fix changes
ms.date: 2026-10-15
---

* `mvp/zavaforward_mvp/chatthreads.py`: `SqlRepo.get`, `list` and `messages` hold `store.dblock` while using the shared connection.
* Merged origin/main into the branch.
* Validation: concurrency test 0 of 40 failures (6 of 40 before); full suite OK.
