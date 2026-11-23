---
title: Issue 2201 live9 research
ms.date: 2026-11-23
---

Research disposition: executed (code reading; Azure read-only, nothing changed). Planning Readiness: Ready.

## Findings

* #2308 (live8) records `callback_error_type` for an unexpected failure inside `on_event` and prints it from `live_receiver.run_window`. A unit test covers the recording; no test covers the `run_window` print.
* Remaining blind spots in `src/api/src/zava_forward/api/iot_stream.py` (`HubReceiver.run`): the SDK `on_error` callback sets `IOT_RECEIVE_FAILED` and discards the exception, and the outer `except Exception` re-raises `IOT_RECEIVE_FAILED` with `from None`. Authentication, AMQP link and transport failures therefore log one fixed code, so a future Failed execution of job-live-receiver cannot be told apart.
* All #2201 acceptance criteria are ticked; live7 and live8 recorded the cause of the 23 Nov 09:30 to 11:30 failures as unproven.

## Decision

Record only the exception class (messages may carry connection detail) as `receive_error_type` in `on_error` and in the outer handler, print `receive_error_type=<Class>` to stderr in `run_window`, and add tests for both paths.

## Criteria for the demo

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded | Unproven for 23 Nov 09:30 to 11:30 | class not logged before; this change adds the evidence channel |
| Fix merged and deployed | Not newly provable | change is local, undeployed |
| Three consecutive Succeeded runs | Not re-probed | no new Azure read this task |
| Readings in store and map | Not re-proven | demo-proven earlier (live7) |
