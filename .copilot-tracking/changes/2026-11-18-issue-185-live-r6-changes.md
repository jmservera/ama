---
title: Issue 185 live r6 changes
ms.date: 2026-11-18
---

Refs #185. Tier: FULL applies (src/core changed); full receipt NOT run by this worker (brief forbids `rpi-checks.py --all`). Focused checks below.

## Files

* `src/core/src/zava_forward/core/synthetic/device_registry_azure.py`: `SasEnrollment`, `Enrollment` union, SAS branch in `create` (type `sas`, no key, DISABLED, marker, create-only).
* `src/core/tests/test_device_registry_azure.py`: simulator returns fake Hub-generated keys for SAS identities; `SasEnrollmentTests` (4 tests).
* `docs/reference/research/issue-185-live-r6-sas-adapter-2026-11-18.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* `.copilot-tracking/` research, plan, details, critique, this file, review, state.

## Process deviations (kept)

* A draft source edit preceded the `implement-start` witness; it was reverted, saved aside, and reapplied after the witness (critique C4). Witness seq 2 to 4 are in order for the final edit.
* A mistaken `ruff format` over `src` reformatted 35 unrelated files; all were reverted with `git checkout`, leaving only the two intended source files.
* Baseline 39 tests fail on system Python (no `azure-iot-hub`); a venv with `azure-iot-hub==2.7.0`, `six==1.17.0` was used.

## Validation

| Command | Result |
| --- | --- |
| `PYTHONPATH=src:tests python -m unittest test_device_registry_azure` (venv) | 43 OK |
| same for `test_device_identity test_device_provision test_live_provisioning test_iot_device_identity_enforcement` | 125 OK in total |
| `src/api` `test_iot_credential_hygiene` | 12 OK |
| `python -m mypy` in `src/core` | no issues, 396 files |
| `ruff check`; `ruff format --isolated --line-length 100 --check` on changed files | pass |
| Azure | no resource created or changed; no live run of the new code |

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Approach decided with credential owner (ticked) | Already ticked | Owner decision 2026-11-18 |
| Home maps to one device identity and stock home ID (ticked) | Already ticked | Prior live run 3 and source tests |
| Credentials issued and stored without appearing in source or logs | Issuance and no-leak proven (live r1 to r3; adapter in simulator tests); durable storage UNPROVEN | [r6 note](../../docs/reference/research/issue-185-live-r6-sas-adapter-2026-11-18.md) |
| Teardown removes all simulated identities | Proven live on the demo hub (in-job delete and zero count); adapter delete proven in simulator only | r5 and r6 notes |

Unmet: durable secret store and rotation, X.509, N-home scale, live run of the new adapter, FULL receipt, independent review, hosted CI.
