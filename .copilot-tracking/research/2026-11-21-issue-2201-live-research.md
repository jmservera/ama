---
title: Issue 2201 job-live-receiver research
ms.date: 2026-11-21
---

## Scope

Why does `job-live-receiver` (rg `ama`, env `cae-cutover-test-demo`) end Failed on every run? Read-only `az` and repo source only.

## Evidence (read-only az, 2026-11-21)

* `az containerapp job execution list`: 26 retained executions all Failed (cron `*/30 * * * *`), including 10:00 and 10:30 UTC; the simulator job (same image digest `sha256:899670a1...`, every 5 minutes) is Succeeded.
* Job config: args `--seconds 1500 --events 20000`, `replicaTimeout` 1620, 0.25 cpu / 0.5Gi, identity `id-cutover-test-api`, 41 secret-volume files, control document enabled and unexpired (expires 2026-12-04, 20 homes; only non-secret fields read).
* Execution 29920980 (start 11:00:00) polled every ~10 s: Running until 11:16:17, then Failed. It failed about 16 minutes in, before the 1500 s window ended. Execution 29920950 also Failed before 10:54.
* Console logs are not retrievable: `az monitor log-analytics query` returns `NspValidationFailedError` (workspace `log-cutover-test` denies this client IP); `az containerapp job logs show` returns "No replicas found" for finished executions. The exit code and stderr line are therefore not observable; this is a recorded evidence gap.

## Source findings

* `live_receiver.main` maps any `StreamError` to exit 2 and any other exception to exit 4; Container Apps reports both as Failed.
* `HubReceiver.run` (`iot_stream.py`) returns normally only when `max_events` receipts are reached. When the window deadline passes it raises `StreamError("RUN_DEADLINE")`. A finite receive window that ends on time is therefore always a Failed run (certain, from code).
* `on_event` turns any `decode()` refusal (`IOT_DEVICE_NOT_ALLOWED`, `IOT_ORIGIN_REQUIRED`, `IOT_DEVICE_BINDING_MISMATCH`, bad envelope) into a fatal `failure`. The receiver starts at `starting_position="-1"` and replays the retained backlog on each run, so one retained event from a device outside the 20-home cohort stops every run at the same offset. This fits the repeatable ~16 minute failure but is a hypothesis; the logs that would confirm it are blocked.

## Root cause (recorded confidence)

* Proven from code: deadline expiry of the bounded window is raised as an error.
* Probable, unproven: a retained non-cohort or malformed event is fatal on replay.

Both are fixed in the receiver without weakening ingestion: rejected events are never stored, only counted by reason code.

## Planning readiness

Ready.
