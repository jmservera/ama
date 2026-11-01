# Issue 185 changes (2026-11-01)

* Added `src/core/src/zava_forward/core/synthetic/device_identity.py` (plan, provision with rollback, teardown with verification; Registry and CredentialStore protocols).
* Added `src/core/tests/test_device_identity.py` (8 tests, in-memory fakes).
* Added decision paragraph to `docs/reference/research/iot-sensor-analytics-research-plan.md`.
* Validation (src/core): ruff check, ruff format --check, mypy pass; unittest test_device_identity + test_sensor_stock 24 OK.
* All plan items P1-P5 complete; no divergences.

## Review round 1 (Copilot threads on PR 647)

* Registry protocol gained `run_of` and a run-conditional `delete(device_id, run_id)`; teardown rejects ownership mismatches (`TEARDOWN_OWNERSHIP_MISMATCH`) before any deletion or revocation.
* Provision tracks created devices separately from issued credentials and rolls back only those, running cleanup outside the exception handler so the original error is not chained.
* Teardown converts adapter exceptions to fixed `TEARDOWN_FAILED:<n>` codes, continues remaining cleanup, and verifies the same references it revoked.
* Added 6 regression tests (device identity + sensor stock run: 30 OK); ruff and mypy pass.
