---
title: Issue 120 staff time capture, live ledger-table defect and fix
description: Live evidence that the deployed time capture status endpoint fails on Azure SQL ledger tables, the local fix, and the per-criterion position
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only (owner decisions 2026-11-18). Refs #120.

## Evidence

* Signed in as the staff test user (credentials read at runtime, not printed) on `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000033`: `GET /api/time/status` returned HTTP 500; `POST /api/time/enable` returned 403.
* Container log: `ProgrammingError` on `/api/time/status`.
* Reproduction inside the container with `az containerapp exec` calling `TimeCapture.status()`: `ALTER TABLE ... ADD notice_version NVARCHAR(50) NOT NULL DEFAULT N''` fails with "Only nullable columns without a default value WITH VALUES can be added to ledger tables."
* Direct SQL from the workstation is denied (public network access disabled); no firewall change was made.

## Fix

`timecapture.py` adds `notice_version` as a nullable column and reads `COALESCE(notice_version, '')`, so pre-existing rows never match the current notice version. Focused tests: 69 pass. Not redeployed; post-fix live proof is pending. FULL tier is required before publication because the change touches SQL.

## Per-criterion position

| Criterion | Position |
| --- | --- |
| Capture impossible without recorded DPIA reference | Ticked; tests pass |
| Reports aggregate only with minimum group size | Ticked; tests pass |
| Staff notice approved and enabling action audited | Code and tests prove it locally; live status fails until the fix is deployed; a real notice approval reference is production-only and deferred |
