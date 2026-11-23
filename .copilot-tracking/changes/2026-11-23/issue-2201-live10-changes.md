---
title: Issue 2201 live10 changes
ms.date: 2026-11-23
---

Full tier (src change). Azure read-only; no resource created. Status: in progress.

## Files

* `src/api/src/zava_forward/api/live_receiver.py`: `main` prints `error_type=<class>` for an unexpected failure.
* `src/api/tests/test_live_control.py`: regression test.

Status update: implemented.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Proven (earlier notes `docs/reference/research/issue-2201-live-receiver-failure-2026-11-21.md`, `-logs-2026-11-22.md`); not re-read here | prior committed research |
| Fix merged and deployed | Proven for the demo by the live probe below: runs succeed on the deployed job; this task's change is local and undeployed | `az containerapp job execution list` |
| Three consecutive scheduled runs Succeeded | Proven live 2026-11-23 20:24 UTC | 16 consecutive Succeeded since 12:48 UTC (every 30 minutes, `*/30 * * * *`), the 20:00 run still Running; last failure 12:47:30 UTC (manual) |
| Readings from IoT Hub in store and map with timestamps | Unproven here | proven in earlier live notes; not re-probed this task |
| New code angle (goal) | Proven | new test passes: unexpected startup failure prints the class only, exit 4 |

## Validation

* From `src/api`: `unittest` for `test_live_control` and `test_iot_stream` OK; `mypy` clean; `ruff check` and `ruff format --check` clean.
* `rpi-checks.py --all` not run (coordinator). Hosted CI not observed (not pushed).
