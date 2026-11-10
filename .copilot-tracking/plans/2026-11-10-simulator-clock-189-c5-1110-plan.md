---
title: Issue 189 simulator-admin HTTP test-clock plan (C5)
ms.date: 2026-11-10
task_id: 189-expiry-c5-1110
---

## Plan (authored 2026-11-10 after research-open, before any source edit)

Objective: make the simulator-admin HTTP fixture independent of the real wall clock by binding only `simulator_admin.datetime` to a cleanup-managed, advanceable test clock, so the two failing methods exercise the same real HTTP, App, provider, lock, file and audit path at the fixture's `NOW`, and add focused expiry regressions. Only `src/api/tests/test_simulator_admin.py` changes.

* [ ] Phase 1: Add `SimulatorClock(datetime)` (overrides `now` only), a per-test factory, and install it in `AdminHttpTests.setUp` before the server thread; reorder cleanups so shutdown, close and thread join precede the clock restore.
* [ ] Phase 2: Add real-HTTP regressions: clock/type contract of the scoped binding, just-before expiry valid, exact expiry reads expired, expired Start 400 `CONTROL_WINDOW_INVALID` with unchanged bytes and audit, expired Start with no file writes nothing. Assert status before indexing `started["changed"]`.
* [ ] Phase 3: Prove green with the fixture, and re-prove red by removing only the fixture clock installer under the external ambient 10:04:47Z runner; run the two original methods under the ambient post-deadline clock.
* [ ] Phase 4: Targeted tier: whole `test_simulator_admin`, `test_live_control`, configured API `mypy` 2.4.0, `ruff` 0.17.1 check and format; production-source-unchanged diff; changes record, one Review, freeze commit, handoff.

Done means: both original methods pass over HTTP with the real clock past the deadline and under an ambient 10:04:47Z clock; they fail again when only the fixture binding is removed; the new regressions pass; targeted checks have exit 0; production source and configs are byte-identical to parent.

Out of scope: production code, clock/auth/session/live_control policy, global time freeze, year-2099 expiry, retries, skips, weakened assertions, mocking `handle`, `_start`, `check_window`, provider, authorization, persistence or audit, other test files, shared helpers, project configs, full or `--changed` gate, SQL, browser, cloud, models, push, PR, issue edits, primary checkout changes, other time-bombed fixtures.

Gates: this C5 is the last allowed correction (5/5); no further automatic correction. Independent exact-head review by Root precedes publication. Stacked under `test/demo-session-opacity-1373-1110` at `d38bad4b76e4aec40c247086a22078e885f5b2c2` (PR1375), not main. `Refs #189`, `#1373`, `#80`, `#129` only; no closing keyword; no whole-#189, live owned-run or budget-alert acceptance.
