---
title: Issue 86 focused-tier plan critique
description: One independent read-only critique of the focused-tier research, plan and details, with dispositions
ms.date: 2026-11-08
---

Scope: issue #86 only. Reviewer: rubber-duck agent, read-only, one pass. Verdict as returned: Revise.

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | SQL setup omits `CREATE DATABASE rpi_disposable` and `ZF_SQL_PASSWORD` | Accepted; plan amended |
| 2 | Blocking | Owned-endpoint checks (container ID, label, running, loopback port) and lock held through cleanup not required | Accepted; plan amended |
| 3 | Blocking | Skips could hide missing SQL coverage; pass criteria needed | Accepted; plan amended |
| 4 | Non-blocking | Resident complaint HTTP tests use SQLite; MSSQL ranking/export API paths not shown | Accepted as an explicit non-claim |
| 5 | Non-blocking | Hash-locked requirements and driver probe missing | Accepted; plan amended |
| 6 | Non-blocking | Currency failure instruction conflicts | Accepted; stop and re-plan |

Reusing same-head receipt groups as historical same-code observations was judged sound with the currency proof; it is not a passing FULL.
