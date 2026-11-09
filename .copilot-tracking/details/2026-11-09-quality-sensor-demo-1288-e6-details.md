# Details: issue 1288 E6

Plan: `.copilot-tracking/plans/2026-11-09-quality-sensor-demo-1288-e6-plan.md`.

## P2 F1 mechanism

* `assistants.py`: `CallTicket.send_fence(timeout)` calls `Assistants.fence_send(attempt, capability, timeout)`; raises `ai_consumption.DispatchWithdrawn` on refusal. `fence_send` is one `self.transaction()`: select the attempt row; require outcome in (`reserved`, `sending`) and `active_until > now`; require `self.disabled(db, capability)` is None; `UPDATE assistant_attempts SET outcome='sending', active_until=now+timeout+HOLD_GRACE`. `CallTicket` records the capability.
* `ai_consumption.py`: `SEND_FENCE` ContextVar and `send_fence(callable)` context manager, like `sealed_simulation`.
* `ai.py`: `Ai.send_fence_supported = True`. In `_request`, when a fence is set, use a private opener with a connection subclass; `send()` runs `fence(timeout)` once after `connect()`, measures elapsed monotonic time and raises `DispatchWithdrawn` if it exceeds the margin (2 s) or the fence refuses; a `threading.Timer(timeout)` closes the socket; the opener is not cached. No fence set: unchanged `urlopen`.
* `simulation_lane.py`: `Ticket` Protocol gains `send_fence`; `Lane.request` refuses (held, manual route, no seal) when `getattr(ai, "send_fence_supported", False)` is not true; sets `ai_consumption.send_fence(ticket.send_fence)` around `ai.evidence`.
* `server.py`: no wiring change beyond what `Admission` already carries.
* Outcomes: `DispatchWithdrawn` maps to `suspended-before-dispatch` (existing); the durable slot is released, the reservation stays as finite liability.

## P2 tests (failing first, in `test_quality_simulation_lane.py` plus a worker module)

* `src/api/tests/two_process_worker.py`: opens the same working SQLite file, builds `Assistants` and a real `Ai` pointed at the shared loopback TLS peer with a counting file meter, admits a call, sleeps until told, then runs the production send path; prints a JSON result.
* Test 1 short-lease stall: `active_calls=1`, lease 2 s. Process A admits and stalls past the lease; the parent (process B) admits and sends while the peer holds the reply; A resumes while B is still in flight and must be refused. Peer counts: one accept, one body. Allowance: two calls used, token liability finite.
* Test 2 authority expiry before send: admit, wait until `ZF_ASSIST_EXPIRES` passes, then send: no accept, no meter-to-socket, token counter zero.
* Test 3 valid bounded call still completes; slots released.
* Test 4 fail-closed: an `Ai` without `send_fence_supported` is refused before admission.

## P3

* `test_role_endpoint_inventory.py`: add the GET and two POST routes with the public-fixture payload and the per-role status expectations established by the existing dedicated role test; run discovery unchanged.

## P4 types

* Measure post-merge with `mypy` in `src/core` and `src/api` (pinned 2.4.0 profile). Annotate; reuse existing typed helpers; no suppression, cast, stub or override.
