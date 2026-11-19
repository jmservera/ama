---
title: Issue 1818 sensor_register receiver fix and criterion proof, 2026-11-18
description: Candidate fix so accepted live readings write their sensor_register row, focused test evidence, and a per-criterion table for issue 1818 (synthetic demo, desktop only)
ms.date: 2026-11-18
---

## Scope and status

Refs #1818. Synthetic demo, desktop only. The candidate ports held commit `7bde5f149` onto `origin/main` `2cd131da5`: `SensorConsumer.process` inserts the sensor's `sensor_register` row (insert-if-absent, same transaction) for an accepted live reading, the consumer DDL set creates `sensor_register`, and the receiver grant list and `infra/README.md` gain `SELECT, INSERT ON dbo.sensor_register`. Without it, live-only sensors have readings but no register row, so the resident view and map join do not see them (round 5 and 6 findings in the [round 7 evidence](./issue-1818-live-iot-map-walkthrough-evidence-2026-11-18.md)).

The change touches SQL and receiver permissions, so the tier is FULL. `/tmp/ama-rpi-heavy.lock` was held on 2026-11-18, so the full gate was not run and no verified receipt exists. The extra `INSERT` grant on the production receiver is a deploy-time change that needs human approval.

## Focused validation (this worktree)

| Command | Result |
| --- | --- |
| `src/core`: `PYTHONPATH=src:tests python3 -m unittest tests.test_sensor_consumer -q` | 38 tests OK, including `test_accepted_reading_writes_register_row_once` |
| `src/api`: `python3 -m unittest tests.test_live_receiver_sql -q` (src-ci path set) | 2 tests skipped: no SQL Server available here, so the minimum-grant proof is not re-run (it passed 74 tests against SQL Server in round 6) |
| `python3 -m mypy` in `src/core` and `src/api` | no issues (396 and 347 files) |
| `python3 -m ruff check` on the changed core files | passed |

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 `/api/map` sensor summary | Proven (demo) | Round 7: fresh 3, restricted 97, not-loaded 343 in one response ([evidence](./issue-1818-live-iot-map-walkthrough-evidence-2026-11-18.md)) |
| 2 Employee map, card, accessible list, filter | Proven (demo) | Round 7: cards, list lines and stale filter 0 then 3 of 443 |
| 3 Resident `#sec-sensors` | Proven (demo) | Round 7: fresh and stale text, no other home id |
| 4 Tests and browser checks on exact HEAD | Partly proven | New and existing core tests, mypy and ruff pass on this HEAD. `map_fullscreen_browser_check.py`, `resident_sensors_browser_check.py` and axe were not re-run (no web change; ticked earlier by #1826). SQL Server grant test and full gate not run |
| 5 Live Hub to SQL to UI walkthrough | Proven (demo), not re-run | Round 7 run used the deployed round 6 image carrying this fix; no new live traffic was sent in this session, and the live run did not exercise the receiver minimum-grant path |

Unmet for merge: the full gate and independent review, the grant approval for the production receiver, and Playwright re-runs on this exact HEAD.
