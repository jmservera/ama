---
title: "Issue 2190: gate flake re-verification and broken-pipe log noise"
description: Re-verification of the three gate flake fixes on head ae73889080, plus a test-handler traceback that polluted the verbose gate log.
ms.date: 2026-11-26
---

Scope: issue #2190, synthetic DEMO, desktop only. No Azure resource was read or changed. Earlier notes: [2026-11-21](./issue-2190-live-20261121-2026-11-21.md), [glued header](./issue-2190-live-20261123T202218Z-glued-header-note.md).

## Evidence

* Flake 1 (`tools/rpi-checks.py` log interleaving): `python3 -m unittest test_rpi_checks` from `tools/`: 133 tests OK.
* Flake 2 (`late_success`, `employee_chat_browser_check.py`): three consecutive runs with Chromium and the pinned axe 4.10.3 (sha256 equals `AXE_SHA256`) all passed, rc 0.
* Flake 3 (218 timeout): `test_rai_release_readiness_api_218` 5 tests OK; the slow-server test asserts a `TimeoutError` at a quarter of the server delay while the real budget (120 s) passes.
* New finding: in verbose output the slow-server handler printed a `BrokenPipeError` traceback into the log when the client timed out on purpose, glued before `ok`. It never failed a run, but it is the same log-noise class as flake 1.

## Change

The slow handler in `src/api/tests/test_rai_release_readiness_api_218.py` now catches `BrokenPipeError` and `ConnectionResetError` around the write. The timeout assertion is unchanged. After the change a verbose run contains no traceback. `ruff format`, `ruff check` and `mypy` (src/api) are clean. Tier FULL because src changed; the complete gate was not run (coordinator-owned).

## Per-criterion verdict

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Each flake reproduced or explained | Proven (explained in earlier notes; flake 3 residual noise reproduced and fixed here) | Notes, test runs above |
| Fixed with a regression test | Proven for flakes 1 and 3; flake 2 by 3 of 3 passing runs and the earlier real-browser test, no deterministic test for a timing race | Runs above |
| No check relaxed | Proven | Assertions and failure patterns unchanged |
| Hosted CI and complete local gate on this head | Unproven | Coordinator-owned; not run, nothing pushed |
