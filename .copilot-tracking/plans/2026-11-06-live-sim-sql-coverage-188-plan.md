---
title: Plan for #188 real-SQL coverage correction
ms.date: 2026-11-06
---

* Goal: make the existing maintained sensor SQL route run the already-implemented weather, live-envelope and live-consumer regression classes against the task-owned SQL Server, with proof of the actual backend, without a new wrapper or framework.
* Change 1, `src/api/checks/sensor_sql_check.py`: extend the one `unittest` argument list with `test_sensor_consistency.WeatherContinuityTests`, `test_sensor_consistency.LiveEnvelopeReplayTests` and `test_sensor_consumer_live`. Keep the container, loopback, memory and CPU bounds, random password and `finally` cleanup unchanged. Replace the unchecked `check=True` on `docker rm` and the `-q` run only if needed for truthful reporting; otherwise leave them alone. The container-name and database-name constants stay.
* Change 2, `src/api/tests/test_sensor_consistency.py` and `src/core/tests/test_sensor_consumer_live.py`: add one assertion per class setUp or `seeded()` that the store backend equals the requested one (`isinstance(store, MssqlStore)` exactly when `ZF_SENSOR_MSSQL == "1"`), mirroring the `SqlHandoverTests` assertion. This is the real-backend proof; no constant-only test.
* Change 3, docs: the api README sensor SQL sections (about lines 1872 and 2068) and the core README if it lists the route: state the extended selector set, that the complete gate still does not include it, and that results are constructed local evidence only.
* Acceptance:
  * SQLite default discovery still passes for the touched modules, with the new backend assertions satisfied on SQLite.
  * With `ZF_SENSOR_MSSQL=1` against a task-owned endpoint, the extended selector set runs with zero skips, exit 0, and the reported run count equals the sum of the selected classes (weather 5, plus envelope, live, ingestion, handover method).
  * Refusal controls still pass: unsupported live-sim weather windows refuse `HANDOVER_SCHEMA_UNSUPPORTED` before statistics or replay writes; mixed or mismatched version, channel or unit is rejected; `HANDOVER_TOLERANCE_NOT_APPLICABLE` holds.
  * Idempotence controls still pass: replay twice leaves the store unchanged; duplicate delivery gives replay receipts.
  * Legacy-only handover behaviour is unchanged (existing legacy tests, same results).
  * `retained_envelopes` lossless replay and indoor `observed_series` exclusion unchanged.
* Source proof: worktree import proof with explicit `PYTHONPATH` for `src/api/src`, `src/core/src`, `src/agents/src` and the test directories (never `mvp`), because installed distributions resolve elsewhere.
* Owned disposable endpoint constraints: loopback only, random port and password held only in process environment, a unique name, resource bounds as in the helper, `ZF_SENSOR_MSSQL` set only in that subprocess, `store_at(reset=True)` allowed only against that freshly created database, exact-name removal in `finally`, nothing foreign touched, no pruning.
* Lock: the existing README route holds `/tmp/ama-rpi-heavy.lock` through the queuing `flock -w 600`. This plan does not queue or run anything; #185 holds the sole heavy admission and the lock decision belongs to the coordinator.
* Selected tier: FULL (ingestion, SQL, runtime). Pending gates, none run in this continuation:
  * Light and focused, after implementation: touched unittest modules on SQLite, Ruff check and format (no cache), mypy with external caches, `python3 tools/rpi-checks.py --changed`, `PYTHONDONTWRITEBYTECODE=1`.
  * Admitted heavy: the extended sensor SQL helper run, then the maintained `tools/rpi-checks.py --all` FULL gate on the final frozen head, independent exact-head review and hosted checks.
* Exclusions: schema, consent, calibration, thresholds, new APIs or UI, new wrappers, edits to `tools/rpi-checks.py`, architecture refactoring, weather-to-indoor conversion, live send, deployment, spending, cleanup of existing evidence.
* Sequence: root assesses this plan and admits the bounded correction; implementation starts only then, with tests (backend assertions) before the helper change; a dedicated Review follows implementation. This continuation writes records only.
* [ ] Human review required and left unchecked.
