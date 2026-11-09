---
title: Details - issue 1288 E4
---

# Phase details: issue 1288 E4

Plan: [plan](../plans/2026-11-09-quality-sensor-demo-1288-e4-plan.md). CANDIDATE architecture, not approved.

## P1 core

* `core/sensor_sql.py`: `SensorSqliteConnector(path)`; `assistant_connection()` returns a new `sqlite3` connection (`isolation_level=None`, busy timeout), `dberror = sqlite3.Error`. No DDL, like `SensorMssqlConnector`. `SensorConsumer` accepts it.
* `core/ai_consumption.py`: `SIMULATION_SEAL` ContextVar, `simulation_seal(seal)` context manager, `SimulationRefused(DispatchWithdrawn)` carrying a fixed reason code.
* `core/ai.py`: `Ai.provider_body(system, user, max_tokens, temperature)` static (the single serializer, used by `_request` and by the composer); `Ai.simulation_verifier` (None by default); a captured-readings or sealed request is verified after the body is serialized and before the data hold, input bound, meter, token and socket. Order of reserve, dispatch_check, urlopen, complete is unchanged. `evidence()` reports `outcome="simulation-refused"` with the reason; `run`/`look_at` degrade to template via the existing generic handler.
* `core/simulation_lane.py` (new):
  * Constants: `NAMESPACE`, fixture home `SIM-PUBLIC-1`, one sensor key, fixed public case (address "1 Fixture Row, Exampletown", measure "Loft insulation", one quality record with fixed public evidence text, no documents), fixed exercise policy and control (consent granted, calibration confirmed).
  * `Lane.provision(store_path, key_path)`: trusted one-time setup. Creates the dedicated SQLite file (marker, store id, `cases` row for the fixture home, sensor schema via `SensorConsumer.configure`, seal and proposal tables) and a 32-byte key file with mode 0600. Refuses an existing path, identical paths, or a store path equal to `ZF_DATA`, `ZF_SQLITE` or the working database.
  * `Lane.open(env)`: reads only `ZF_SIM_STORE` and `ZF_SIM_KEY_FILE`. Anything missing, unreadable, group or world readable key, wrong namespace, wrong marker, or the working store file raises `Unavailable(code)`.
  * `observe(now)`: public generator readings through the actual `SensorConsumer.process` into the dedicated store, each 5-minute slot after the latest stored (idempotent).
  * `view(now)`: `sensor_view.view` of the dedicated store for the fixture home (what the UI shows).
  * `compose(now, max_tokens)`: `capture("quality-evidence", FIXTURE, sensors=capture_source(...))`, `build_request`, `Ai.provider_body`; returns system, prompt, body bytes, digest and the cited reading ids and values.
  * `mint`/`verify`: seal = HMAC-SHA256 over canonical (namespace, store id, nonce, body sha256, expiry); nonce stored single-use. `verify(seal, body)` checks mac, namespace, store id, body digest, expiry, then atomically consumes the nonce. Explicit reasons: `missing`, `malformed`, `signature`, `namespace`, `store`, `payload-mismatch`, `expired`, `replayed`, `unknown-nonce`.
  * `request(ai, hold, now)`: compose, check `hold()` (suspension and release), mint, run `ai.evidence` inside `call_context`, `captured_readings(True)` and `simulation_seal`, validate the output with `assistants.validate_output` against the composed snapshot, recheck `hold()` after return (discard on change), store the unapproved proposal. Returns an explicit status for unavailable, held, refused, model failure and ok.

## P2 composition

* `Assistants.dispatch_hold(capability)`: reason string from the existing `suspended` and `admission` reads on the caller's connection, or None.
* `App.__init__`: `self.simulation = lane_or_unavailable(os.environ)`. `store.ai.simulation_verifier` is attached to the lane's verifier only when the carrier is a real `Ai`.
* Routes (roles `REGISTRY["quality-evidence"]["roles"]`): `GET /api/simulation/quality` (state, fixture, view, last request digest and readings, last proposal, labels); `POST /api/simulation/quality/observe`; `POST /api/simulation/quality/request`. Unconfigured returns `state: unavailable` with the manual route. No other route reads the dedicated store.

## P3 UI

`simulationPanel()` in `web/ops.js`, rendered by the existing assistants view for the same roles. Heading "Public synthetic simulation (not a real home)". Native buttons, textual status, readings table (same columns as `sensorTable`), the request digest and the reading ids sent, the proposal text and "Unapproved proposal. Use the ordinary quality check." No accept control.

## P4 tests

New `src/api/tests/test_quality_simulation_lane.py` (reusing the E2 TLS peer, counting meter and token counter):

* sealed lane request reaches the peer once; recorded body parsed: reading ids and values equal `view()` and the API response; digest equals sealed digest; no working-store field present (home address is the fixture, no `PRIVATE-` marker).
* negative at `Ai`, each with peer accepts and bytes, meter reserved and checked, tokens all zero: no seal; forged mac; altered body; wrong namespace; cross-store seal (second lane with its own key); expired; replayed; caller-supplied boolean, digest-only or namespace-only contextvars; captured flag with no seal (the private path); lane unconfigured; key unreadable.
* separation: provisioning refuses `ZF_DATA`/working database and a shared key and store path; opening a working database as a lane is refused.
* guards preserved: release or suspension hold sends nothing; meter held sends nothing.
* routes: role matrix, default deny, unavailable never success, no controlled-domain mutation (domain tables unchanged), proposal state `unapproved`.
* browser check addition: panel text equals API and labels synthetic; unavailable state shows the manual route.

## P5 commands

From `src/api` with `.venv-1288`: `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest test_quality_simulation_lane test_quality_sensors test_assistants test_quality_sensors_e1 test_quality_sensors_c7 test_quality_sensors_e2`; core `test_sensor_consumer test_sensor_consumer_live test_ai_input_bounds test_data_protection`; `test_ai_call_site_inventory`; owned SQL under `flock -n`; browser with the pinned axe; `ruff check`, `ruff format --check`; same-tool `mypy` normalized comparison.
