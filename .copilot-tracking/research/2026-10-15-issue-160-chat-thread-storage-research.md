---
title: Issue 160 chat thread storage research
ms.date: 2026-10-15
---

* Task: issue #160 (parent #157). Research disposition: executed. Planning readiness: Ready.
* Sources: ADR 0004 decision 3 (accepted; threads in Azure SQL behind Store, owner key, content separate from ledger), ADR 0002 decisions 1 and 2, ADR 0003 decision 1, ADR 0005 (labelled synthetic fixtures only).
* Code evidence: `store.py` (JSON in-memory Store, `ConflictError`, `audit`), `sqlstore.py` (SQLite schema, `dblock`, BEGIN IMMEDIATE pattern, `audit`), `mssqlstore.py` (`TABLES`, `_indexes`, collation), `test_mssqlstore.py` (portability test pattern, `wipe`).
* Findings: no thread or message tables existed; shared SQL must avoid INSERT OR REPLACE/IGNORE, AUTOINCREMENT and PRAGMA outside dialect hooks; row versions are the Store concurrency convention.
* Owner decisions applied: uksouth, Azure only, ADR 0004 accepted, retention unlocked (legal lock deferred), existing Entra sign-in.
* Open (not invented): retention period and deletion schedule (#163, OD-46), break-glass access (#162), live Azure SQL run (no server here; MSSQL suite is gated by ZF_TEST_MSSQL=1), AI model calls (panel #159).
