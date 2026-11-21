---
title: Issue 2201 job-live-receiver failure diagnosis
description: Read-only Azure evidence and source root cause for the failed job-live-receiver runs, with the repository fix and per-criterion status
ms.date: 2026-11-21
---

Demo scope (owner decision 2026-11-18): synthetic data, desktop only, resource group `ama`, read-only `az`. No Azure resource was created or changed.

## Evidence

* `az containerapp job execution list -g ama -n job-live-receiver`: 26 retained executions, all Failed, schedule `*/30 * * * *`. `job-live-simulator` (same image digest, every 5 minutes) is Succeeded.
* Job config: `--seconds 1500 --events 20000`, replica timeout 1620 s, 0.25 vCPU, 0.5Gi, hub `iot-cutover-test-rzsrg`, control document enabled, expires 2026-12-04, 20 homes (non-secret fields only).
* Execution `job-live-receiver-29920980` polled every ~10 s: Running 11:00:01, Failed 11:16:17 UTC, that is about 16 minutes into a 25 minute window. Execution `29920950` also Failed before 10:54.
* Exit code and stderr are not observable: `az monitor log-analytics query` fails with `NspValidationFailedError` (workspace `log-cutover-test` denies this client IP) and `az containerapp job logs show` returns "No replicas found" for finished executions. Relaxing the workspace network rule is an Azure write and was not done.

## Root cause

* Proven from source: `HubReceiver.run` raised `RUN_DEADLINE` when the bounded window ended without reaching the event cap, and `live_receiver.main` turns every `StreamError` into exit 2, so a window that ended on time was a Failed run.
* Probable, not proven by logs: `on_event` made any refused event (for example `IOT_DEVICE_NOT_ALLOWED` from a retained non-cohort device) fatal. The job replays the retained backlog from `starting_position="-1"` every run, so one such event fails every run at the same offset, which fits the repeatable ~16 minute failure.

## Fix (src, branch `test/receiver-fix-live-20261121T102918Z`)

* `HubReceiver.run(..., bounded_window=True)`: the deadline ends the window normally; events refused by `decode` are skipped, never stored, counted by reason code in `HubReceiver.rejected`. SQL, link and cleanup failures stay fatal. The default is unchanged.
* `live_receiver.run_window` uses it and writes `rejected=N reasons=CODE=n` to stderr, so a future log names the cause.
* Tests: `test_iot_stream.py` (`test_bounded_window_ends_on_deadline_and_skips_refused_events`, `test_bounded_window_keeps_sql_failure_fatal`); fakes in `test_live_control.py` updated. 102 tests in `test_iot_stream`, `test_live_control` and `test_live_receiver_sql` pass; ruff and mypy are clean.

## Acceptance criteria

| Criterion | Status | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Partly proven | Deadline defect proven from source and a regression test; the exact production exit code and the non-cohort event are unproven because logs are blocked |
| Fix merged and deployed | Unproven | Local commit only; no push, no image build or job update was authorised in this task |
| Three consecutive scheduled runs Succeeded | Unproven | Depends on deployment; current runs still Failed on the old image |
| Readings from IoT Hub appear in the store and the employee map, with timestamps | Unproven | Not queried; the failing job does not give a reliable store proof, and no map screenshot was taken |
