---
title: Issue 189 simulator-admin HTTP test-clock changes (C5)
ms.date: 2026-11-10
task_id: 189-expiry-c5-1110
---

## Status

Implementation complete 2026-11-10 (started after plan-done with clean source). Base HEAD `d38bad4b76e4aec40c247086a22078e885f5b2c2` (parent test/demo-session-opacity-1373-1110, PR1375). This is correction C5 of five for #189: 5/5, zero further automatic corrections; the four earlier corrections are preserved unchanged.

## Changed product file (only one)

`src/api/tests/test_simulator_admin.py` (+77/-3), sha256 `bb92944e3740c28615df76df816781d11e75021ccd28539147fc5e12c0ef80c3` at implement-done.

* `SimulatorClock(datetime)` overrides only `now` (typed `Self`, `fromtimestamp` of the scoped instant); `scoped_clock(moment)` returns a per-test subclass; an `EXPIRY` constant is added.
* `AdminHttpTests.setUp` creates the scoped clock and calls `bind_clock()` BEFORE the server thread starts. `bind_clock` patches only `simulator_admin.datetime` and registers its restore. The thread is kept and `join_server` (join 5 s, assert not alive) is registered before `server_close` and `shutdown`, so cleanup runs `shutdown`, `server_close`, join, clock restore, env restore, temp-dir cleanup (LIFO).
* The round-trip method asserts `code == 200` with the body as the message before indexing `started["changed"]` (diagnostic only; not the repair).
* New tests (real HTTP, App, provider, lock, file and audit): `test_fixture_clock_replaces_only_the_module_now_and_keeps_datetime_behaviour`; `test_expiry_boundary_is_valid_before_expired_at_and_refuses_a_start` (one second before expiry valid and GET `send`; at exactly expiry GET `expired` with 0 remaining seconds; an expired Start returns 400 `CONTROL_WINDOW_INVALID` with unchanged bytes and unchanged audit entries); `test_start_after_the_expiry_writes_no_control_and_no_audit` (clock at the CI instant 2026-11-10T10:04:47Z).
* Untouched: view-only 403 before module, CSRF, wrong-role, boundary matrix, owner/reference/cap/maximum-window and direct explicit-`now` tests.

## Unchanged

Production source, `live_control`, auth, session, server, project configs and shared helpers are byte-identical to the parent: `git diff d38bad4b7 -- src ':!src/api/tests/test_simulator_admin.py'` plus toml and workflow paths is empty; the changed-file list is the single test file plus `.copilot-tracking`.

## Evidence (external, outside the repository, in the Root C5 evidence directory `proof/`)

Commands ran from `src/api` with `PYTHONPATH` set to this worktree's `src/api/src`, `src/core/src`, `src/agents/src`, `src/core/tests`, `src/agents/tests`, `src/api/tests`; module origins were printed and checked to be this worktree. No raw CI token was copied.

| Check | Result |
| --- | --- |
| RED original file, real clock 10:19Z | exit 1; `KeyError: 'changed'` at 636 and `400 != 200` at 593 (`red-original-realclock-1110.log`) |
| RED original file, ONLY `simulator_admin.datetime` at 2026-11-10T10:04:47Z (external runner) | exit 1; same two failures; probe: HTTP 400, `CONTROL_WINDOW_INVALID`, no `changed`, no control file, 0 start audit entries (`red-original-ambient-1004-1110.log`) |
| GREEN fixture binding intact, same ambient 10:04:47Z, the two original methods over HTTP | exit 0, both ok (`green-original-methods-ambient-1004-1110.log`) |
| RED fixture binding removed (`bind_clock` no-op only), ambient 10:04:47Z | exit 1; both fail again; the round trip now reports `400 != 200` with the `CONTROL_WINDOW_INVALID` body; probe unchanged 400 (`red-binding-removed-ambient-1004-1110.log`) |
| GREEN whole `test_simulator_admin` plus `test_live_control`, real clock (past the deadline) | 64 tests OK, exit 0 (`green-targeted-realclock-1110.log`); `test_simulator_admin` alone: 30 OK |
| Configured static, owned venv `/tmp/venv-189-c5-1110` (mypy 2.4.0, ruff 0.17.1; the user-level tools were 2.4.1 and 0.17.3, not the pinned versions) | `ruff check .` exit 0; `ruff format --check .` exit 0 (136 files); project `mypy` exit 0 (213 source files) (`green-static-1110.log`) |

During implementation a single-file mypy run flagged `simulator_admin.datetime` as not exported under strict implicit re-export; the contract test now reads the module global through `__dict__` as `Any`. The configured project mypy passes.

## Amendments and divergences

* Critique amendment applied: the installer is the single method `bind_clock`, so the external negative control neutralizes only the fixture binding.
* The first test-file edit was made with a one-off Python heredoc rather than the edit tool, contrary to the file-change rule; the resulting diff was reviewed and `ruff format` applied. Later edits used the edit tool.
* No other divergence. No skips, retries or weakened assertions.

## Not run (by tier)

Full or `--changed` gate, SQL, browser, cloud and model calls, private or default working data, hosted CI. Hosted PR1374, PR1375 and PR1376 results are separate observations and are not claimed.
