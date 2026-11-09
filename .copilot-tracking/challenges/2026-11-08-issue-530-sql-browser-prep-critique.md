---
title: Issue 530 actual SQL and employee browser preparation critique
ms.date: 2026-11-08
---

* Execution: one independent rubber-duck pass on the final candidate plan, read-only, before the Changes, Review and state records. Verdict: Proceed with changes. Not repeated.
* Verified by the critic: the maintained browser group does not invoke `employee_chat_browser_check`; `--extra-test` cannot carry MSSQL env or run a module check; SQLite proxies are distinct from actual MSSQL; 17 groups and command forms are correct; no lock argument or `--exact-base` is mandatory; assistant ledger tests concern assistant events, not chat cost.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | SQL coverage understated; `MssqlLedgerMigration` chat-memory test exists | Applied directly in research and details; stated as migration only |
| 2 | Axe coverage overstated for design-system check | Applied directly; corrected |
| 3 | Lock admission could poll or wait 600 seconds | Applied directly; `--jobs 1 --lock-timeout 0`, stop on contention |

No finding conflicted with a confirmed decision; no user decision required.
