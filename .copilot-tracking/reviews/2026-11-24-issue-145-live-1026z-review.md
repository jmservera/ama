---
title: Issue 145 live review (2026-11-24 10:26Z run)
ms.date: 2026-11-24
---

Executed once. Outcome: conformant for scope.

* The fix is fail closed, idempotent and touches only the allowance table; admission code is unchanged. Test covers headroom, exhausted and repeat cases.
* Findings routed to later work: (1) call `close_allowance_after_restore` from an automated post-restore sequence and test it on a disposable SQL Server (needs drill authority); (2) wire long-term retention after the #121 decision (#1906).
* Residual: lower-tier SQLite evidence only; C4, R1 to R2 partial, R5 remain unproven as tabled.
