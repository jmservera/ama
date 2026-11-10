---
title: Issue 1388 delayed-companion route-delivery changes
ms.date: 2026-11-10
task_id: 1388-delayed-route-1110
---

## Status

Implemented 2026-11-10 from HEAD `83503b74e0e5f555382436c0ae27f64cd200971f` (implement started with source clean; the changes record was registered first). Source change is two files. Production code, retry policy, other checkers and README are unchanged (`git diff --name-only 83503b74e -- src` lists only these two files). Zero corrections were spent.

## Source change

* `src/api/checks/workspace_scripts_browser_check.py` (+10, -1): adds `from time import monotonic` and `ROUTE_DELIVERY_DEADLINE_S = 5.0`. After the existing DOM-ready `wait_for_function`, `delayed_companion` loops `page.wait_for_timeout(10)` while `pending` is empty and the monotonic clock is under the deadline, then asserts `len(pending) == 1` with a message naming the deadline and the observed count. No `time.sleep`, no `>= 1`, no first-wins, no longer `expect` timeout. First-abort, saved callback lifecycle, variant branches and `finally: context.close()` are untouched.
* `src/api/tests/test_browser_asset_urls.py` (+149, -1): new `DelayedCompanionRouteDelivery` class drives the real `delayed_companion` with test-local browser, context, page and route doubles. The retry route reaches the routine's own `intercept` callback only on a `wait_for_timeout` pump (or inside `wait_for_function` for the prompt case). `expect`, `sign_in`, `observe_companion` and `monotonic` are patched on the checker module; the fake clock advances only inside the pump. The page double raises a sentinel on the first interaction after DOM-ready, so the real routine stops right after its count assertion. Each case runs over the four real variants.

## Actual delayed variants (names and commands)

| Call | Printed scenario |
| --- | --- |
| `delayed_companion(browser, base)` | navigation |
| `delayed_companion(browser, base, timed_out=True)` | timeout and late load |
| `delayed_companion(browser, base, sign_out=True)` | sign-out |
| `delayed_companion(browser, base, session_ended=True)` | same-document 401/login |

Whole checker: `python3 -m checks.workspace_scripts_browser_check` from `src/api`. The isolated variants ran through an inline driver calling those four real calls inside the existing `main(run, synthetic_data)` harness, optionally after the three `recovery` calls.

## Red before, green after (deterministic)

* Red on the original checker (own venv, raw log `p1-red-original.log` in the coordinator session `checks-1388-initial-1110/`): `DelayedCompanionRouteDelivery` ran 4 tests with 16 failures. Eight are the race itself: DOM-ready before delivery makes the original routine raise `AssertionError` at `assert len(pending) == 1` for all four variants at pump 1 and pump 3. Eight are control messages: zero delivery and double delivery fail on the original with an empty message, so the explicit `saw 0` and `saw 2` expectations are red. The prompt-delivery test passed on the original, as expected.
* Green after: 4 tests OK. Delayed delivery (pump 1 and 3) passes for all four variants with event order `dom-ready` then `deliver`, the first route aborted once, the held retry untouched and the context closed once. Prompt delivery uses zero pumps. Zero delivery fails with `saw 0` after a fake clock of 5.0 s (within 0.011 s). Double delivery fails with `saw 2`, not first-wins.

## Validation (focused demo tier; own venv `ama-venv-1388-delayed-route-1110`, pinned playwright 1.64.0, ruff 0.17.1, mypy 2.4.0, Python 3.12.3)

* Selectors `test_browser_asset_urls test_static_assets test_workspace_scripts test_loading_feedback`: 24 tests OK.
* `ruff check .` passed; `ruff format --check .` 139 files formatted; configured `mypy` no issues in 219 files.
* Adverse intermediate result retained: the first `ruff format --check .` failed (`s2-ruff-format.log`) because one `patch.object` call in my new test was wrapped over three lines instead of one; I joined it before the final run, and the final logs (`f-*.log`) pass. Not a review correction.
* Real browser, one non-queued `flock -n /tmp/ama-rpi-heavy.lock` acquisition, no HOLD, each run once on the final source (checker sha256 `2e08370aa06c134fca43ca6916ea70419bc1cc212b03cebae514fff40f2ea979`):
  * Four variants isolated (13:32:31Z): all four PASS.
  * Three `recovery` calls then the four variants without `exhaustion` (13:32:41Z): all four PASS. This is the preceding-sequence shape that failed in the diagnosis.
  * Whole checker (13:32:54Z): exit 1 at the existing `exhaustion` oracle (`assert len(requests) == count`, line 150), after the three recovery passes and before any delayed variant. This is the independently owned #1384 failure, recorded raw and not called green; the delayed coverage above is the separate execution of the four variants.

## Original adverse evidence preserved

* Diagnosis (coordinator, summarized in the research): DOM-ready before Python delivery, main 65c 1 of 12 and candidate 3f1fa48 2 of 12 failures without controls.
* This task's original-source baseline (13:27:52Z): whole checker exit 1 at the same exhaustion oracle (line 148 before the edit); the isolated four variants gave one failure (`sign_out`, empty `AssertionError`, traceback not captured by the driver) and three passes. These small samples are not rates; the new-source runs above passed all eight delayed calls but are corroboration only, not proof of absence.

## Residuals

* Not run: hosted CI, the full or `--changed` gate, JS static check (JS unchanged), the independent exact-head review. #1384 must still pass BOTH browser checks after adopting this fix.
* The deterministic regression proves duplicates delivered before the check fail; it does not claim no future request can occur.
* README is unchanged; names and commands of the four variants are recorded here.
