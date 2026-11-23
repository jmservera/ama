---
title: Issue 2201 live9 changes
ms.date: 2026-11-23
---

Full tier (src change). Azure not touched; no throwaway resource. Status: implemented.

## Files

* `src/api/src/zava_forward/api/iot_stream.py`: `receive_error_type` (exception class only, first wins) set in the SDK `on_error` and the outer handler.
* `src/api/src/zava_forward/api/live_receiver.py`: prints `callback_error_type=` and `receive_error_type=` on a failed window.
* `src/api/tests/test_iot_stream.py` (two tests), `src/api/tests/test_live_control.py` (one test).

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Unproven for 09:30 to 11:30 UTC 23 Nov | no execution log read this task; this change adds the receive-side class so the next failure is attributable |
| Fix merged and deployed | Unproven here | change is local and undeployed |
| Three consecutive scheduled runs Succeeded | Unproven here | no Azure probe this task |
| Readings from IoT Hub in store and map with timestamps | Unproven here | demo-proven in live7; not re-probed |
| New code evidence (goal) | Proven | three new tests pass |

## Validation

* From `src/api`: `unittest` for `test_iot_stream` and `test_live_control` 109 tests OK; `mypy` clean; `ruff check` and `ruff format --check` clean.
* `rpi-checks.py --all` not run (coordinator). Hosted CI not observed (not pushed).
