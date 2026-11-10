---
title: Issue 189 simulator-admin HTTP test-clock research (C5)
ms.date: 2026-11-10
task_id: 189-expiry-c5-1110
---

<!-- markdownlint-disable-file -->

## Disposition and scope

Research executed 2026-11-10 from 10:17Z, before any source edit. Disposition: `executed`. Planning Readiness: Ready.

Scope is the API test file `src/api/tests/test_simulator_admin.py` only: the HTTP fixture `AdminHttpTests.setUp`, the two originally failing methods and focused clock regressions. No production, clock, auth, session or `live_control` policy change. This research grants no whole-#189 acceptance and no live owned-run or budget-alert evidence.

## Authority and ownership (stop rule)

* Root's brief authorizes ONE existing-issue correction (C5) for #189. Retained C4 research (`optional-sdk-189-c4-research.md:30`) and its state and handoff record four of five spent, one remaining; C4 final head `b933c2f606b394469b53f702824b707e6fc3548d`. C5 consumes the last one: 5/5, zero further automatic corrections.
* Root reports freshly fetched current #189 comments with no later consumption or hold (latest is the Nov 9 scoped #1313 merge comment) and no exact issue match for `test_simulator_admin` or `CONTROL_WINDOW_INVALID`. This task did not repeat GitHub searches. No contrary evidence appeared in the repository: `.copilot-tracking` shows no earlier owned attempt at this clock failure.

## Exact input confirmation

* Worktree HEAD is `d38bad4b76e4aec40c247086a22078e885f5b2c2` on `test/demo-simulator-clock-189-c5-1110`, clean at start; the declared parent (PR1375 head), not main.
* The admission source was the older pin `1ee56da3a`. `git diff 1ee56da3a HEAD` over `simulator_admin.py`, `live_control.py`, `test_simulator_admin.py` and `test_live_control.py` is empty, so the relied-on hunks are byte-identical. (`server.py` differs but only in unrelated hunks; the POST dispatch below was re-read at HEAD.)
* Tests were run with `PYTHONPATH` pointing to this worktree's `src` trees; `simulator_admin`, `identity` and `live_control` import from the worktree (origin printed and checked), not from the editable installs that point to the primary checkout.

## Causal chain (read at HEAD)

* `test_simulator_admin.py:29-30`: `NOW` is 2026-11-09T10:00Z; `EXPIRES` is 2026-11-10T10:00Z; `start_body()` always sends that absolute expiry.
* Direct module tests pass `NOW` as the explicit `now` argument, so they remain coherent at any real time.
* `AdminHttpTests.setUp` mounts the real `App`, provider and temporary control file on a `ThreadingHTTPServer`; it pins no clock. Cleanup is LIFO: `shutdown`, `server_close`, then the temp-dir and env patches. The server thread is not joined.
* `server.py:1199-1200` calls `simulator_admin.handle(app.store, u, "POST", url.path, body)` with no `now`; `handle` uses `now or datetime.now(UTC)` through the module-level `datetime` name (`simulator_admin.py:13,303`). That is the only runtime use of the name in the module; elsewhere it is annotation only.
* `_start` takes the file lock, then `live_control.check_window` requires `now < expires_at <= now + 14 days` and raises `CONTROL_WINDOW_INVALID`; `handle` returns it as 400. `decide` independently reports EXPIRED when `now >= expires_at`. Both behaviours are correct and unchanged.

## Observations (actual)

* Real clock 2026-11-10T10:19Z, unmodified file: 27 tests, `FAILED (failures=1, errors=1)`; `KeyError: 'changed'` at line 636 and `AssertionError: 400 != 200` at line 593, the same two shapes as the hosted job 129755471054 (run 42794274166, failed 10:04:47Z). Log: `red-original-realclock-1110.log` (external evidence).
* Deterministic negative control, unmodified file, ONLY `simulator_admin.datetime` bound to 2026-11-10T10:04:47Z by an external runner: same two failures, and a real HTTP probe returned status 400, code `CONTROL_WINDOW_INVALID`, no `changed` key, no control file written, zero `sim_control_start` audit entries. Log: `red-original-ambient-1004-1110.log`.
* Direct explicit-`now` tests, CLI test, boundary matrix and the other HTTP tests pass: only the two start-dependent HTTP methods are time-bombed.

## Options

| Option | Result |
| --- | --- |
| Test-local `simulator_admin.datetime` subclass binding (selected by Root) | Real HTTP, auth, locks, file and audit stay real; only the module-local clock lookup changes; scoped and restorable |
| Year 2099 expiry | Rejected: exceeds the 14-day maximum, so check_window refuses it |
| Patch `handle`, `check_window`, provider or global datetime | Rejected: mocks away the behaviour under test or leaks across clocks |
| Dynamic `expires_at` from the real clock | Rejected for this task: makes the oracle depend on wall time and removes the fixed deterministic scenarios; also not the selected design |
| Retries, skips, weaker assertions | Rejected by the brief |

## Design for the plan

* Module-level `SimulatorClock(datetime)` subclass overriding only `now`, returning the scoped instant with the requested tzinfo via `fromtimestamp` (typed `Self`); all construction, comparison and arithmetic are inherited. A small factory gives each test its own mutable instant so no state is shared between tests.
* Install with `patch.object(simulator_admin, "datetime", clock)` before the server thread starts. Register cleanups so the order of execution is: `shutdown`, `server_close`, thread join, then the clock restore.
* New regressions on the real HTTP path: the CI moment (10:04:47Z on Nov 10) with the fixture clock still lets the two original methods pass; clock at one second before expiry is valid; clock at exactly expiry reports `expired` on GET; an expired Start returns 400 `CONTROL_WINDOW_INVALID` with unchanged bytes and audit; an expired Start with no file writes nothing.
* Assert the status before indexing `started["changed"]` (diagnostic only).

## Proof design

* Negative control with the final fixture: an external runner binds an ambient clock at 10:04:47Z and replaces only the fixture's clock installer with a no-op; the two original methods must fail again. Positive control: the same ambient clock with the fixture binding intact; both pass.
* Targeted tier: whole `test_simulator_admin`, `test_live_control`, configured API `mypy` (2.4.0), `ruff` 0.17.1 check and format in an owned venv, because the user-level tools are 2.4.1 and 0.17.3 and the project pins 2.4.0 and 0.17.1.

## Risks

* A subclass that overrides `now` must return `Self`; `fromtimestamp(...)` of a whole-second instant is exact.
* `shutdown()` before join; join after `server_close` is safe because requests are synchronous.
* Test ordering and other modules are unaffected: the patch is on `simulator_admin.datetime` only and is restored after the thread stops.

## Follow-ups (current)

* Independent exact-head review, then publication under PR1375's stack (Root).
* Hosted CI for PR1374, PR1375 and PR1376 remains a separate observation each; none is claimed fixed here.
* Other time-bombed fixtures, if any, are a separate unadmitted discovery; none is claimed.
