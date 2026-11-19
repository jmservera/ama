<!-- markdownlint-disable-file -->
# Issue 1818 live8 changes log (Refs #1818)

Started 2026-11-18. Applies the diff of held commit `7bde5f149` (source, tests, `infra/README.md` grant text) onto `origin/main` `2cd131da5`.

Files: `src/core/src/zava_forward/core/sensor_consumer.py`, `src/core/tests/test_sensor_consumer.py`, `src/api/tests/test_live_receiver_sql.py`, `infra/README.md`, research note, index and log.

## Validation (focused; FULL tier gate not run, `/tmp/ama-rpi-heavy.lock` held)

* `src/core` sensor consumer tests: 38 OK. `src/api` receiver SQL test: 2 skipped (no SQL Server). mypy core and api: clean. ruff check: clean.

## Per-criterion table (issue 1818)

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 `/api/map` sensor summary | Proven (demo) | round 7 live evidence |
| 2 Employee map, card, list, filter | Proven (demo) | round 7 live evidence |
| 3 Resident `#sec-sensors` | Proven (demo) | round 7 live evidence |
| 4 Tests and browser checks on exact HEAD | Partly proven | unit, mypy, ruff pass; browser checks, axe, SQL grant test and full gate not run |
| 5 Live walkthrough | Proven (demo), not re-run | round 7 run on deployed fix image; no new traffic this session |

No Azure action was taken in this session; no resource was created.
