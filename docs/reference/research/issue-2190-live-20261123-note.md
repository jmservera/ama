---
title: "Issue 2190 gate flakes: regression tests for flakes 2 and 3 and a tighter result rule"
description: Closes the review gaps on the three gate flake fixes (a behavioural slow-server test, a deterministic settle wait for the chat late_success check and a stricter _region_passed) with recorded evidence and a per-criterion verdict.
ms.date: 2026-11-23
---

Scope: issue #2190, review finding D6, D7 and D9 from the gate-speed review. Synthetic DEMO, desktop only. No Azure resource was read or changed; the flakes are local gate behaviour. Earlier reproductions: [2026-11-21 note](./issue-2190-live-20261121-2026-11-21.md) and [2026-11-22 re-verification](./issue-2190-live-20261122-note.md). Evidence files: [issue-2190-live-20261123-evidence](./issue-2190-live-20261123-evidence/).

## Changes

* `_region_passed` (`tools/rpi-checks.py`): the result is a line that is exactly `ok`, or `ok` glued to an unterminated log fragment such as `status=503ok`. A log line that ends in a separate word or value `ok` (`http-response status ok`, `... status=200 ok`, `state=ok`) no longer counts. Failing patterns are unchanged. Three new rejected shapes were added to `test_log_noise_never_hides_a_failed_skipped_or_missing_result`; before the change the first two added were accepted (`GateError not raised`, two subtest failures), after it all are rejected and the 129 gate tests pass ([result](./issue-2190-live-20261123-evidence/gate-tests-after.txt)).
* Flake 3 (`test_rai_release_readiness_api_218.py`): the test that only compared a constant with a patched `urlopen` argument is replaced by a behavioural one. A local HTTP server delays its reply by 0.8 s; the module budget returns the reply, and a budget of 0.2 s raises `TimeoutError`, the failure the issue reports. Deterministic, under one second of waiting ([result](./issue-2190-live-20261123-evidence/api-tests-after.txt)).
* Flake 2 (`employee_chat_browser_check.py`): a new `settle_route` waits for `#workspace-status` to start with `Perspective:` when the route destination is `#/`, then for `networkidle`. The list route reads facets and then its cases, and the status is written when the second read ends, so `networkidle` alone could pass in the gap between the reads under load. New deterministic tests: `test_employee_chat_settle.py` pins the order and predicate with a recording page double, and the existing AST test in `tools/test_rpi_checks.py` now pins `settle_route` before the baseline snapshot.

## Evidence

* 14 busy-loop processes on 8 cores: 6 of 6 runs of `checks.employee_chat_browser_check` passed ([first run](./issue-2190-live-20261123-evidence/chat-check-loaded-and-first.txt), [five more](./issue-2190-live-20261123-evidence/chat-check-loaded-runs.txt)). Before the 2026-11-21 fix 1 of 15 failed, so six passes alone are consistent with, not proof of, the removal of the race.
* `python3 -m unittest tools.test_rpi_checks`: 129 tests OK. `tests.test_employee_chat_settle` and `tests.test_rai_release_readiness_api_218` from `src/api`: 7 tests OK. mypy in `src/api` clean; ruff check and the 100-column format check pass on the changed `src/api` files; `ruff check` on the `tools` files reports the same 20 findings as before the change.
* The scenario manifest recipe does not list `employee_chat_browser_check.py`, so no SHA update was needed.

## Limits

* The original flake 2 gap is client-side CPU stall between two fetches, and requests in flight are already awaited by `networkidle`, so no request-level reproduction is deterministic. The ordering and predicate are tested; the race itself remains evidenced by repeat runs under load.
* A log line shaped like a test header (`name (a.b) ... `) still starts a region; the failing-pattern scan and the `Ran N` plus final `OK` checks remain the backstop.
* Not run: the complete local gate (`rpi-checks.py --all`), owned by the coordinator, and hosted CI for the exact head. Tier FULL applies because `src/api` code changed.

## Per-criterion verdict

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Each flake reproduced or explained | Proven | Earlier notes; unchanged |
| Fixed with a regression test | Proven for flakes 1 and 3; flake 2 proven for the fix ordering, unproven as a deterministic race reproduction | Tests above; the race itself is not reproducible deterministically (see Limits) |
| No check relaxed | Proven | `_region_passed` is now stricter than before; failing patterns, snapshot comparison and the 91-scan expectation are unchanged; the 218 timeout of 120 s is retained and now exercised by a test |
