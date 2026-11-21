---
title: Issue 2201 changes
ms.date: 2026-11-21
---

## Changes

* `src/api/src/zava_forward/api/iot_stream.py`: `HubReceiver.run(bounded_window=)`, `rejected` tally.
* `src/api/src/zava_forward/api/live_receiver.py`: uses the bounded window and reports rejected counts.
* `src/api/tests/test_iot_stream.py`, `test_live_control.py`: regression tests and fake signature.
* `src/api/README.md`, `docs/reference/research/issue-2201-live-receiver-failure-2026-11-21.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

Tier FULL (src change) classified by the coordinator-owned gate; only targeted checks ran here: 102 unit tests in `test_iot_stream`, `test_live_control`, `test_live_receiver_sql` pass; `ruff check`, `ruff format --check`, `mypy` (src/api) clean. `rpi-checks.py --all` not run.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Partly proven | Deadline defect proven from source plus test; production exit code and non-cohort event unproven (workspace NSP blocks logs) |
| Fix merged and deployed | Unproven | Local commit only; no push or Azure write |
| Three consecutive scheduled runs Succeeded | Unproven | Needs deployment; latest runs still Failed |
| Readings from IoT Hub in store and employee map with timestamps | Unproven | Not queried; no map screenshot |
