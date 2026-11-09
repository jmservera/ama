---
title: Details - issue 1288 E5
---

# Phase details: issue 1288 E5

Plan: [plan](../plans/2026-11-09-quality-sensor-demo-1288-e5-plan.md). CANDIDATE, not approved.

## P1 failing-first tests

* `src/api/tests/test_quality_simulation_lane.py`: a `service(**cfg)` helper builds a real `Assistants` over the same store from `config()` overrides and restores the counting meter; tests POST through HTTP and call `nothing_left(peer)`:
  * missing authority, invalid allowance (`call_allowance=0`), expired (`expires` in the past), schema error, SQL unavailable.
  * exhausted calls (`call_allowance=1`, second POST) and exhausted tokens (`token_allowance` just above the reservation, unknown usage keeps the liability).
  * parallel: `active_calls=1`, first call blocked in the meter `before` hook, concurrent POSTs decline with zero extra meter, token, socket; after release a new POST succeeds.
  * valid: one proposal, `used_calls` and `reserved_tokens` recorded, active slot freed; provider failure (peer closes): outcome recorded, slot behaviour as ordinary tasks.
  * the "existing guards" test uses a real suspension rather than a patched `dispatch_hold` for the first hold.
* F3 in the same file: forced `PermissionError` on the key `open` and an invalid `sim_meta` through `App(...)`; assert `simulation is None`, explicit reason, partial store closed (spy on `SqlStore`), ordinary `/api/assistants` route still 200.
* `src/api/checks/quality_sensors_browser_check.py`: seed `sim_proposals` rows (one of 12 cited, source:home only, empty findings), render the panel, assert wording and counts, rotate readings and assert the supplied list is unchanged; axe unchanged.

## P2 F1 core

* `assistants.py`: `_reserve(db, now, attempt_id, task_id, fence)` returns `None`, `"active"` or `"pool"` (active-call count, pool upsert and min, exhaustion; on success charge and insert attempt). `_settle(db, attempt_id, envelope)` returns `(actual, reserved)`. `claim` and `complete` call them with unchanged behaviour. `begin_call(capability, chars, call_id)`: one `transaction()`: `disabled(db, capability)`, input bound, `_reserve`; then non-blocking `call_slots.acquire`, compensating the reservation in a second transaction on failure; event `sim-claimed`. `end_call(call_id, envelope)`: `_settle` with the same lease and uncertainty rules, event `sim-completed`, always releases `call_slots`.
* `simulation_lane.py`: `Admission` dataclass; `Lane.request(ai, admission)` order: model configured, compose, no readings, `admission.begin`, mint, call, `admission.end` in `finally`, late `hold`, validate, store.
* `server.py`: `simulation_act` builds the `Admission` from `self.assistants`.

## P3 F3 core

* `_read_key`: `OSError` on open or read to `Unavailable("key-unreadable")`, a short read to `key-unsafe`.
* `Lane.open`: probe connect inside the `try`; `SqlStore` construction `(sqlite3.Error, OSError)` to `store-unavailable`; `Lane.__init__` `sqlite3.Error` to `store-not-simulation`; any `Unavailable` after a store exists closes `store.db` first.

## P4 F2 UI

* `Lane.last_proposal`: `cited` derived from stored `output.findings[*].citations` intersected with the stored `readings` keys (`sensor_view.key_of`); `readings` stays the supplied set.
* `ops.js` `simulationPanel`: "Supplied with N stored readings. Cited M of them." plus the cited list, "It cited no sensor readings." when zero, "The model gave no findings." when the findings list is empty, supplied readings in a native `details`.

## Critique amendments (applied before implementation)

* `begin_call` acquires the physical `call_slots` first (non-blocking), then runs one transaction (`disabled`, input bound, `_reserve`); failure releases the slot, so no compensation. It returns an idempotent ticket; `_settle` only settles an attempt still `reserved`. `store.dberror` fails closed with a manual-route reason.
* `Admission.bounds()` supplies `min(600, limits.output_tokens)` and `limits.timeout`; body, seal and call use them.
* `last_proposal` rebuilds citation keys as `sensor:{SENSOR_ID}:{reading_id}` from the stored triples.
* Residual, disclosed: a stall before dispatch longer than the lease can free the durable slot (same as ordinary tasks).

## Validation commands

`cd src/api && PYTHONPATH=../core/tests:../agents/tests:tests ../../.venv-1288/bin/python -m unittest ...` for the targeted modules; browser check `python3 checks/quality_sensors_browser_check.py` (with axe); ruff and same-tool mypy comparison against the E4 baseline.
