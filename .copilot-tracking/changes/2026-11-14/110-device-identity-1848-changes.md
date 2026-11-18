---
title: Issue 110 device identity hardening changes
ms.date: 2026-11-14
---

* `src/core/src/zava_forward/core/synthetic/device_identity.py`: added `CANONICAL_SLOT`; `verify_envelope` rejects non-canonical `observed_at` with `READING_ID_MISMATCH`.
* `src/core/tests/test_iot_device_identity_schema.py`: added three non-canonical timestamp cases and a null schema version case.

Validation (from `src/core`): `python3 -m ruff check .` passed; `python3 -m ruff format --line-length 100 --check .` passed; `PYTHONPATH=src:tests python3 -m unittest` for the identity, sensor consumer and live readings tests: 67 passed. From `src/api`: `test_iot*` 66 passed.

Not done: no push, no live Hub or Azure SQL run, no complete gate.
