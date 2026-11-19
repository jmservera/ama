---
title: Issue 120 live research (staff time capture gate)
date: 2026-11-19
task_id: issue-120-live
---

## Scope

Issue #120 has two ticked criteria and one unticked: "Staff notice approved and enabling action audited". Demo owner decisions of 2026-11-18 apply (synthetic demo, desktop only, live Azure authorised, production items deferred).

## Findings

* Code for notice approval (`ZF_TIME_NOTICE_APPROVED` plus `ZF_TIME_NOTICE_VERSION`), separated request and enable actions, and audit entries (`time_capture_enable_requested`, `time_capture_enabled`, `time_notice_acknowledged`) exists in `src/api/src/zava_forward/api/timecapture.py` and `server.py`; 38 targeted tests pass locally (5 skipped).
* Live proof against `ca-cutover-test-demo-api` (signed in with the staff test account, credentials unprinted): `GET /api/time/status` returns HTTP 500 and `POST /api/time/enable` returns 403. Container logs show `ProgrammingError` on `/api/time/status`.
* Reproduced inside the live container (`az containerapp exec`, read-only call of `TimeCapture.status`): `_ensure` runs `ALTER TABLE ... ADD notice_version NVARCHAR(50) NOT NULL DEFAULT N''` and Azure SQL refuses it: "Only nullable columns without a default value WITH VALUES can be added to ledger tables."
* Consequence: on a database whose `time_request`/`time_enabled` tables predate `notice_version`, the gate cannot even report status, so the enabling action cannot be taken or audited. This is a real unmet-in-live defect, not a production-only item.
* Direct SQL access from the workstation is denied (public network access disabled); no firewall change was made.

## Planning readiness

Ready: change the MSSQL upgrade to add a nullable column and read it with `COALESCE`.
