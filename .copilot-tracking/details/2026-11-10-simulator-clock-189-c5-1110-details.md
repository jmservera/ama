---
title: Issue 189 simulator-admin HTTP test-clock details
ms.date: 2026-11-10
task_id: 189-expiry-c5-1110
---

## Phase 1 details

* Imports: add `tzinfo` to `from datetime import UTC, datetime` and `ClassVar, Self` to the `typing` import.
* `class SimulatorClock(datetime)` with `current: ClassVar[datetime] = NOW` and `@classmethod now(cls, tz: tzinfo | None = None) -> Self` returning `cls.fromtimestamp(cls.current.timestamp(), tz)`. Nothing else is overridden, so construction, comparison, arithmetic and `isinstance` behave as for `datetime`.
* `scoped_clock(moment) -> type[SimulatorClock]`: returns a fresh subclass with its own `current`, so no state is shared between tests; tests move time with `self.clock.current = ...`.
* `AdminHttpTests.setUp`: after the env patch, `self.clock = scoped_clock(NOW)` and `self.bind_clock()`, a method that starts `patch.object(simulator_admin, "datetime", self.clock)` and registers its stop, all BEFORE the server thread is created (amendment: a single method so the external negative control can neutralize exactly the fixture binding). Keep the thread in `self.server_thread`; register cleanups in this order so they run LIFO as `shutdown`, `server_close`, `server_thread.join(timeout=5)`, clock restore, env restore, temp-dir cleanup: temp-dir, env, clock, join, close, shutdown. The thread-stopped check (`assertFalse(server_thread.is_alive())`) is made after join in the cleanup sequence.
* Only the module-local name changes: global `datetime`, `live_control`, auth and server clocks stay real.

## Phase 2 details

Helpers: `status(self)` does an authorized GET; `start_over_http(self, **changes)` posts a real start with roles ADMIN and STAFF; both reuse `request`.

* `test_fixture_clock_replaces_only_the_module_now_and_keeps_datetime_behaviour`: `simulator_admin.datetime.now(UTC) == NOW` and carries UTC; `simulator_admin.datetime(2026, 1, 2, tzinfo=UTC)` is a `datetime` equal to the plain constructor result; the global `datetime.now` is not the fixture class.
* `test_expiry_boundary_valid_before_expired_at_and_start_refused`: clock EXPIRES minus 1 s: status 200 then start succeeds (200, changed, `state` send via GET); clock exactly EXPIRES: GET state is `expired`; record `digest(self.file)` and audit count; a fresh start with the same expiry and `expected_revision` equal to the digest returns 400 `CONTROL_WINDOW_INVALID`, no `changed`, digest and audit count unchanged.
* `test_expired_start_with_no_control_writes_nothing`: clock at 2026-11-10T10:04:47Z (the CI instant); start returns 400 `CONTROL_WINDOW_INVALID`, the control file does not exist and no `sim_control_start` audit entry exists.
* Round-trip method: `self.assertEqual(code, 200)` before `started["changed"]`, then the existing assertions.
* Existing view-only, CSRF, wrong-role, owner/reference/cap and maximum-window, and direct explicit-`now` tests are untouched.

## Phase 3 details

External runner (`proof/ambient_clock_runner.py`, outside the repository): binds `simulator_admin.datetime` to a fixed instant ambiently; `--no-fixture-binding` replaces the fixture's `bind_clock` with a no-op. Because setUp installs the clock inline, the fixture will expose it as a method `AdminHttpTests.bind_clock(self)` called from `setUp` so the runner can neutralize exactly the fixture binding. Commands recorded in the changes record with exits.

## Phase 4 details

From `src/api` with `PYTHONPATH` set to this worktree's `src/api/src`, `src/core/src`, `src/agents/src`, `src/core/tests`, `src/agents/tests`, `src/api/tests`: `python3 -m unittest test_simulator_admin test_live_control`; owned venv `/tmp/venv-189-c5-1110` (system site packages plus `ruff==0.17.1` and `mypy==2.4.0`): `mypy` (project config), `ruff check`, `ruff format --check` on the changed test file and project-wide per config. Production check: `git diff d38bad4b7 -- src ':!src/api/tests/test_simulator_admin.py'` empty and `git diff --name-only` limited to the test file plus `.copilot-tracking`.
