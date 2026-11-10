---
title: Changes - quality sensor demo, issue 1288 E4
---

# Changes, issue 1288 E4 (sealed public synthetic simulation lane, CANDIDATE not approved)

Base: `ebb08e21d` (E3 head merged with `origin/main` `ad679b96b`). Start `7e88abb58`.

## Added

* `src/core/src/zava_forward/core/simulation_lane.py`: dedicated simulation store (separate SQLite `SqlStore`), separate 0600 key, bundled public fixture, trusted composer, single-use sealed capability, explicit unavailable states.
* `src/api/tests/test_quality_simulation_lane.py`: 7 own tests (byte-equal sealed request through a real `Ai` client and loopback TLS peer, refusals before meter/token/socket, single use, existing guards, unavailable, store and key separation, role gate).
* UI `simulationPanel()` in `web/ops.js`, wired in `web/app.js`.

## Modified

* `ai_consumption.py`: `SimulationRefused`, `SIMULATION_SEAL`, `sealed_simulation`.
* `ai.py`: `Ai.provider_body` (single serializer), `simulation_verifier`, seal verified on the exact bytes before data hold, meter, token and socket; refusal reported as `simulation-refused`.
* `assistants.py`: `authorize_user`, `dispatch_hold`.
* `server.py`: lane composition and three routes.
* `test_quality_sensors_e2.py`: `TlsPeer` records bodies and accepts a reply callable.
* `checks/quality_sensors_browser_check.py`: simulation panel checks (synthetic label, UI readings equal stored readings, unapproved proposal, no accept control, axe).
* `pyproject.toml` (core and api): the typed new modules are added to the existing `disallow_untyped_calls = false` overrides, as chat_panel and the sensor tests already are. No `ignore_errors`, cast, stub or ignore comment.
* `src/api/README.md`: CANDIDATE note.

## Validation actually run (SQLite)

* API modules (lane, quality_sensors, assistants, e1, c7, e2, call-site inventory): 509 OK, 217 skipped.
* Core (input bounds, sensor consumer, live): 53 OK.
* Browser and axe 4.10.3: 23 checks passed, no serious or critical.
* Ruff check and format on changed new files clean. mypy normalised: core 63 baseline, 0 new; api 675 baseline, 0 new.

## Divergences and limits

* Not solved: atomic last-check suspension race; in-process key holder; separate SQL Server login. Private captured-data route stays off.
* No live, Azure, model or financial call; no private data read.
