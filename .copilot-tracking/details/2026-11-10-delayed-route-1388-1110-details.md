---
title: Issue 1388 delayed-companion route-delivery details
ms.date: 2026-11-10
task_id: 1388-delayed-route-1110
---

## Phase 1: regression doubles and cases

* File: `src/api/tests/test_browser_asset_urls.py`, new class `DelayedCompanionRouteDelivery`, strict-mypy typed (doubles typed `Any`).
* Doubles: a browser whose `new_context` returns a context (records `close`), a page that captures the routine's own `intercept` handler on the first `route`, and routes recording `abort`, `continue_` and `fulfill`. `wait_for_function` is the DOM-ready signal: it first delivers the first-attempt route (the routine aborts it), marks `ready` and appends `dom-ready` to an event log. Retry delivery happens only where the case says: inside `wait_for_function` (prompt) or on the Nth `wait_for_timeout` pump (delayed). After `ready`, any `locator`, `get_by_role` or `evaluate` raises a test sentinel, so the real routine stops right after its count assertion.
* Collaborators patched on the checker module: `expect` (Mock), `sign_in`, `observe_companion` (return Mock), and `monotonic` with `create=True` so the original source still reaches its assertion and fails there; the clock advances only inside the fake `wait_for_timeout` (ms / 1000), so no real time passes.
* Cases, each over the four real variants (`{}`, `timed_out=True`, `sign_out=True`, `session_ended=True`) via `subTest`:
  * Delayed delivery on the next dispatcher turn (pump 1) and on pump 3: expect the sentinel (routine passed the count). Assert event order `dom-ready` before `deliver`, the first route aborted exactly once, the held retry route untouched (no abort, continue or fulfill), and `context.close` called once.
  * Prompt delivery inside `wait_for_function`: passes with zero pumps.
  * Zero delivery: `AssertionError` mentioning `saw 0`; clock never beyond the 5 s deadline plus one slice; context closed.
  * Double delivery (two retry routes at pump 1): `AssertionError` mentioning `saw 2`; not first-wins; context closed.

## Phase 2: checker edit

* Add `from time import monotonic` and `ROUTE_DELIVERY_DEADLINE_S = 5.0` next to `LEAFLET`.
* In `delayed_companion` replace the bare `assert len(pending) == 1` with `deadline = monotonic() + ROUTE_DELIVERY_DEADLINE_S`, `while not pending and monotonic() < deadline: page.wait_for_timeout(10)`, then `assert len(pending) == 1, <message naming the deadline and the observed count>`. Nothing else in the routine changes (first-abort, saved callback lifecycle, variant branches, `finally: context.close()`).

## Phase 3 and 4: validation

* Commands and failure handling are in the plan. Raw outputs go outside the repository in the coordinator session `checks-1388-initial-1110/`; durable summaries go into the changes record.
* Real-browser corroboration is not acceptance of a failure rate; the deterministic regression is the proof of the race fix.

## Dependencies

None on #1384 or #132. Shared checker file ordering: only `delayed_companion` is edited here; #1384 owns exhaustion, count, parser and employee changes and adopts this fix mechanically after it reaches main.
