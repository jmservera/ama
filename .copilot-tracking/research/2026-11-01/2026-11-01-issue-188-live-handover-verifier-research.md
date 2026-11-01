---
title: Issue 188 live handover verifier research
ms.date: 2026-11-01
---

* Task: issue-188-live-handover-verifier. Research disposition: executed (code, tests, README and research plan read; no Azure access).
* Evidence: #587 delivers the local constructed proof (`src/core/.../synthetic/sensor_consistency.py`, `src/core/tests/test_sensor_handover.py`, `src/api/tests/test_sensor_consistency.py`): backfill CSV prefix plus SDK-decoded suffix through the #110 consumer, joint per-home query, inclusive point, mean-step and spread tolerances, 24-row reopened replay.
* Closure audit comment on #188 (2026-10-31) lists all three criteria as unmet only for the actual Azure SQL / live Hub scope.
* Gap: the joint query and unit reattachment exist only inside a test (`queried()`), so an operator with an Azure SQL store (`ZF_STORE=mssql`) has no way to run the statistical check or the window re-run against live-streamed rows.
* Dependencies: #110 is open (device identity criterion); #183 and #186 are closed. Live Hub transport and Azure SQL cannot be exercised here.
* Decision: deliver a store-agnostic read-only query method on the consumer and a small verifier CLI in `src/api` that works on SQLite, local SQL Server and Azure SQL. It supplies demo-ready tooling, not live evidence.
* Out of scope: infra, IoT Hub, mvp/ or prototype/ code, checkbox changes.
* Planning Readiness: Ready.
