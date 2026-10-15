---
title: Issue 160 chat thread storage review
ms.date: 2026-10-15
---

* Review executed once. Outcome: conformant for the storage slice.
* Criteria: migration additive and idempotent (met); list, resume, archive, delete by owner (met); content apart from ledger, metadata only (met, tested); row versions via ConflictError (met); in-memory and SQL parity (met; Azure SQL suite written but not run, no server available).
* Routed follow-ups: run `ZF_TEST_MSSQL=1` suite in CI against SQL Server; retention and deletion schedule (#163); HTTP endpoints and panel (#159); case-scope authorisation per turn (#162).
