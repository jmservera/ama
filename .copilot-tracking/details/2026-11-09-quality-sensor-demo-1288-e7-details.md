# Details: issue 1288 E7

Plan: `.copilot-tracking/plans/2026-11-09-quality-sensor-demo-1288-e7-plan.md`.

## P1 route disabled

* `ai.py`: `send_fence_supported = False` with a comment that the physical send cannot be fenced against an expired owner.
* `simulation_lane.py`: replace the `getattr(ai, "send_fence_supported", False)` refusal reason with `real-provider-route-unavailable`; the check stays before `compose` and `admission.begin`. Keep the `ai_consumption.send_fence(ticket.send_fence)` wrapper only for scripted plumbing that sets the capability.
* Tests (`test_quality_simulation_lane.py`): `tls_ai` helper sets `ai.send_fence_supported = True` on the instance, labelled scripted plumbing over a local peer. New regression `test_real_ai_route_is_refused_before_credential_reservation_and_socket`: production `App`, unmodified real `Ai`, counting meter and credential, local peer with zero accepts; expects status unavailable, reason as above, counters zero, manual route present, and no `sim_seals` row. New source test: no production source line assigns `send_fence_supported` True.
* The two-process worker sets the instance capability the same way (scripted plumbing label).

## P2 deadline ownership (`ai_transport.py`) (amended by the critique)

* `Window`: lock-guarded `adopted`, `done`, `expired`. `arm(sock)` at first byte stores the connected socket object and starts the timer; the callback, if not done, sets `expired` and shuts the stored socket (never `self.sock`). `finish()` sets `done` and cancels the timer.
* Each connection class sets `response_class` to a partial of `OwnedResponse(HTTPResponse)` bound to its window. `OwnedResponse.__init__` adopts the window; `_close_conn` and `close` call `finish()`; `read` raises `TimeoutError` when the window expired even if shutdown produced EOF. No proxy.
* Connection `close()` calls `finish()` only when no response adopted the window (pre-handoff failure). `ai.py` closes an `HTTPError` in its failure path.
* Tests (`test_ai_transport_deadline.py`, real loopback TLS peer, public synthetic bodies): Connection: close trickle; persistent Content-Length trickle; valid JSON prefix then trickle; normal completion; non-2xx; send failure; malformed header. Each asserts timeout or result as expected, no live window timer thread and no open socket afterwards.

## P1 amendment

* The refusal is also in `Ai._request` in the `seal is not None` branch (`SimulationRefused("real-provider-route-unavailable")`) before the verifier, data hold, meter, token or socket. Scripted tests use a labelled `ScriptedPlumbingAi` subclass; tests also cover a plain subclass without the capability and a delegating `store.ai`.
* Source regression: no non-test source assigns `send_fence_supported` True.


## P3 lint

* `sensor_consumer.py` lines 471 and 484 wrapped; format diff resolved.

## P4 profile commands

* API: from `src/api`, `../../.venv-1288/bin/ruff check .`, `ruff format --check .`, `mypy`.
* Core SDK-free: owned `mktemp -d` venv, `pip install -e src/core[dev]` only, then from `src/core` the same three commands.

## P5 validation set

API: `test_quality_simulation_lane`, `test_role_endpoint_inventory`, `test_ai_call_site_inventory`, `test_ai_consumption_api`, `test_assistants`, `test_assistants_dispatch`, `test_assistant_release`, `test_ai_transport_deadline`. Core: `test_ai_consumption*`, `test_ai_input_bounds`, `test_sensor_consumer*`. SQL decision by diff qualification of `assistants.py` against `5827ebede` as in the research.
