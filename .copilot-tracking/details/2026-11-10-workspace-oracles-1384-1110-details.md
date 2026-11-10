---
title: Issue 1384 workspace exhaustion oracles details
description: Phase details, interfaces, exact transformations and acceptance for the two workspace exhaustion oracles
ms.date: 2026-11-10
ms.topic: reference
---

## Phase 1: `src/api/checks/script_retry.py`

* `APP_JS`: `src/zava_forward/api/web/app.js` resolved relative to the module.
* `parse_retry_delays(source: str) -> tuple[int, ...]`: finds the declaration with the anchored multiline pattern for `const SCRIPT_RETRY_DELAYS = [...];`. Raises `ValueError` with a precise message when there is not exactly one declaration, the list is empty, or any item is not a positive decimal integer literal (trailing comma, zero, strings and identifiers are malformed).
* `retry_delays() -> tuple[int, ...]`: parse of the real `app.js` (read at call time).
* `exhausted_requests() -> int`: `1 + len(retry_delays())`.
* `MISSING_GLOBAL_REQUESTS = 2`: initial load plus the single retry that evaluates without the global and stops the recovery; kept separate from the exhaustion total.
* `Mutation = Literal["extra", "early", "reset", "continue"]` and `mutate_app(source: str, kind: Mutation) -> str`:
  * `extra`: appends one more 250 ms delay to the declaration; refuses (`ValueError`) when the resulting schedule would leave less than one second of margin below Playwright's 5 s `expect` timeout, so no timeout is relaxed.
  * `early`: removes the last delay (a single declared delay becomes an empty schedule, which is valid and gives zero retries).
  * `reset`: replaces the single `return workspaceScriptLoads.get(path);` with a version that deletes the memo when the promise settles, so a revisit starts a fresh budget.
  * `continue`: removes the single `if (outcome !== "error") break;` so a successful evaluation or timeout no longer stops recovery; refuses (`ValueError`) when the schedule has fewer than two delays because the control would then be indistinguishable from the contract.
  * Every replacement must match exactly once, otherwise `ValueError`.
* `serve_mutated_app(page: Page, base: str, kind: Mutation) -> None`: routes `asset_url("/app.js", base)`, fetches the real response and fulfils it with `mutate_app(response.text(), kind)`, the JavaScript content type, a recomputed `content-length`, no `etag` and `cache-control: no-store`, so no stale validator or immutable caching applies.
* `assert_requests(observed: int, expected: int, message: str) -> None`: raises `AssertionError(f"{message}: expected {expected}, observed {observed}")`. Used by both oracles so the failure text carries the counts.
* `expect_detected(run: Callable[[], None], message: str, expected: int, observed: int, label: str) -> None`: runs a control; it passes only when `run` raises exactly the `assert_requests` text for the given message, the oracle's expected count and the observed count that the changed loader must produce (derived from the contract and the transformation, never from a measured run). A pass, another assertion or a different count fails the control.

## Phase 2: `workspace_scripts_browser_check.py`

* `exhaustion(browser, base, missing_global=False, mutation=None)`: when `mutation` is given, call `serve_mutated_app` before sign-in. `count = MISSING_GLOBAL_REQUESTS if missing_global else exhausted_requests()`. The terminal assertion carries the message `Terminal attempts must equal one load plus every declared retry` plus the expected and observed numbers; the revisit assertion keeps its existing message `Route revisit must not reset the retry budget`.
* `exhaustion_controls(browser, base)`: runs `extra`, `early` and `reset` on the repeated-abort scenario and `continue` on the missing-global scenario. Required outcomes with `n = len(retry_delays())` and `T = exhausted_requests()`: extra gives terminal message, expected `T`, observed `T + 1`; early gives expected `T`, observed `T - 1`; reset gives the revisit message, expected `T`, observed `T + n` (a fresh budget after the revisit); continue on the missing-global scenario gives the terminal message, expected `MISSING_GLOBAL_REQUESTS`, observed `T`. A scenario that passes, fails on another assertion or with another count fails the control. Prints one PASS line per control.
* `run_browser` calls the controls after the two real exhaustion scenarios.

## Phase 3: `employee_workspace_browser_check.py`

* `missing_ops_recovery(browser, base, mutation=None)` serves the transformed `app.js` when `mutation` is given and asserts `original_ops == exhausted_requests()` with the existing message (module constant `EXHAUSTION`).
* `missing_ops_controls(browser, base)`: `extra` (expected `T`, observed `T + 1`) and `early` (observed `T - 1`) must raise exactly the `assert_requests` text for `EXHAUSTION`; anything else, including no failure, fails the control.
* `run_browser` runs the controls after the real scenario.

## Phase 4: tests in `src/api/tests/test_workspace_scripts.py`

* Helper: `assert_requests` text and `expect_detected` acceptance and rejection (pass-through, wrong message, wrong count, no failure).
* Strict parser: valid declaration returns the tuple; absent, duplicate, empty, trailing comma, zero, string and identifier items each raise `ValueError`.
* Real loader in the Node VM: with every load erroring, the retry request count equals `exhausted_requests() - 1`; with the first retry evaluating, it equals `MISSING_GLOBAL_REQUESTS - 1`; a second call after completion adds none.
* Each transformation changes the real loader as intended: extra gives one more retry than derived, early one fewer, reset adds requests on a second call, continue adds requests after a successful first retry. This proves the browser controls are not vacuous.
* Existing tests stay unchanged.

## Acceptance

* Unmodified-assertion red reproduced before edits (research evidence); after the change both served checks exit 0 with the control PASS lines.
* No change to production files; `git diff --stat` shows only the two checks, the helper, the test file and tracking evidence.
* ruff, mypy and `node --check app.js` pass.
