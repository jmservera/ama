---
title: Issue 135 exception queue research
ms.date: 2026-11-14
---

* Disposition: executed. Planning readiness: Ready.
* `src/core/.../exception_queue.py` already routes failed_import (steward), failed_ai_run, failed_integration and stranded_task (operator) to a named owner, with an audited, human-only `request_recovery`.
* `src/core/.../exception_register.py` feeds refused imports, failed AI runs and stranded tasks into the served register (`src/api`).
* Gap: items did not state `unresolved_eligibility` or an explicit `automatic_replay`/`automatic_release` policy; only `eligibility: "Unknown"` and a post-request `replayed`/`released` pair existed.
