---
title: Continuity 122 remaining-criteria record (research)
ms.date: 2026-11-04
---

* Task: continuity-record-122. Research disposition: reused (issue comments, closure audit 2026-10-31).
* Merged delivery: #269 (export, ledger head), #398 (epoch binding, audience-safe reliance, incomplete SQL-unavailable export), #431 (custody and recovery proposal, non-operative), #614 (closure audit; ticks C4, C5, C7, C9).
* Existing behavioural tests: src/api/tests/test_continuity_epoch_export.py (old queued/leased/missing epoch, in-flight completion overlap, review/suspend race, persisted restart, owned-MSSQL opt-in classes) and src/api/tests/test_operator_suspension.py (restart negative matrix, manual hazard drill).
* Unmet, with the blocker for each:
  * C6: enforceable old-image exclusion and restart is unresolved (infrastructure); MSSQL independent-connection tests are opt-in (ZF_CONTINUITY_MSSQL=1) and need an owned SQL instance.
  * C8: needs an actual authorized human restart decision (OQ-017/OD-35 delegation); constructed actors are not authority.
  * C10: needs actual accessibility acceptance of the bundled challenge route.
  * C11: needs a witnessed authorized drill and owned communication responsibility.
* Planning readiness: Ready for a docs-only record. No source slice is available that proves any unmet criterion without human, Azure or legal evidence.
