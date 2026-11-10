---
title: Quality sensor demo 1288 C4 changes
ms.date: 2026-11-08
---

Recorded 2026-11-08T21:48Z after the C4 plan commit `d1edf1b2e` (header fix `391b73cfc`). Source base `699ec528`, tree `37e1775`. Light SQLite only; no heavy process was started (the shared lock belongs to a disk cleanup).

## Finding dispositions

* F1 (High) index proof: new `sensor_consumer_index_state` marker (count and per-home sha256 of sensor ids) written by `configure` and a strict `reconcile_control_home` (parses every control first, raises on a malformed body or invalid home). `sensor_view._controls` withholds consent unless the marker, both counts and the home digest agree. A failed reconcile deletes the marker; `migrate` logs and continues. Residual: an out-of-band edit that restores counts and the home digest is undetectable.
* F2 (High) release, epoch and A-B-A: `_serviced` scopes the schedule to the current release and epoch and compares only the latest task; `_due` is shared by `scan` and `forecast`.
* F3 (High) stale before claim: a task stale with zero attempts does not count as serviced, so it is replaced once; further same-bucket arrivals stay throttled; allowance use stays 1.
* F4 (Medium) dispatch: `_mark_requested` only sets `manual_requested`; it no longer rewrites a leased dispatch. Claim-time trigger is frozen per fence.
* F5 (Medium) wording: `AS_OF_RULE` names the 366-day newest window and the 30-day context window that may be older. UI and model share it; no web edit.

## Files changed

* `src/core/src/zava_forward/core/assistants.py`, `sensor_view.py`, `sensor_consumer.py`, `src/core/README.md`, `src/api/tests/test_quality_sensors.py`.

## Evidence (raw exits)

* Red on committed source (three source files restored from `HEAD`, then re-applied): `/tmp/c4-red-final.txt` exit 1, 11 failures of 66 (intermediate `/tmp/c4-red-1.txt`, `-2.txt` show earlier test-harness bugs I fixed).
* Green: `/tmp/c4-green-final.txt` test_quality_sensors exit 0, 134 run, 67 skipped (MSSQL variants, PENDING). Also exit 0: test_assistants (120, 58 skipped), test_assistant_release (54, 4 skipped), test_sensor_consumer (37), test_sensor_ingestion (47), test_sensor_consistency (38), test_iot_stream (36), test_regulatory_chat_api (9); logs `/tmp/c4-green-<module>.txt`.
* Ruff check/format at line length 100 clean for the changed files; `assistants.py` checked with `--select F,E9`.
* The epoch test patches `continuity` plus `suspended` (a real epoch bump needs the suspend/restart flow); mock provider only, no live AI.

## Source sha256

* assistants.py 55844709d5aa6ebca0d8d73e3d91743bc8f3735e2911d1b0d9063c5e03e8a0cd
* sensor_view.py 2eec4796dc99d1a7b7cd7dfac8a495a5bd57f43ab25dc93634a7495c74890905
* sensor_consumer.py 59dde349ebe570e8d6759682953abcfb4ebb152ea4c4e008284189b9d889286b
* README.md 43ebd442fd2c0b4547948b7089f8ffe51e7d57cc79ecbc0ed252ecfdf5910560
* test_quality_sensors.py 92f7558450a407f44c4fbc4be5ae90e509ee6a9078a3365c5f0129d6e38424fa

## Pending

* Actual SQL Server and query plans, browser/axe, #184 semantic integration, FULL receipt, release and attestation, live walkthrough.
