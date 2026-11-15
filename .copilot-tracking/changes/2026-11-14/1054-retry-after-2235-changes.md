<!-- markdownlint-disable-file -->
# RPI Changes: Resident Demo 503 Retry-After and Accessible Retry Guidance (Issue #1054)

## Metadata

* Task ID: 1054-retry-after-2235
* Related plan: .copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: Every phase and task in the approved full plan has direct code, test, and focused-tier validation evidence (`mypy`, `ruff check`, `ruff format --check`, and `341` passing unit/VM/UX tests).

## Execution Summary

Completed `P01`, `P02`, and `P03` in plan order to resolve Issue #1054 cleanly:
* Preserved the `MAX_CONCURRENT = 8` semaphore bulkhead in `src/api/src/zava_forward/api/resident_demo/app.py` while adding `MIN_RETRY_AFTER_SECONDS = 1`, `MAX_RETRY_AFTER_SECONDS = 10`, `RETRY_AFTER_SECONDS = 3`, `clamp_retry_after(seconds: object) -> int`, and configurable `ResidentDemo(..., retry_after_seconds: int = RETRY_AFTER_SECONDS)` emitted in both `Retry-After` header and `retry_after_seconds` JSON field exclusively on bulkhead shedding.
* Loaded `web-design-guidelines` and fetched its live rule source prior to editing `src/api/src/zava_forward/api/resident_demo/web/demo.js`; updated `api()`, `retryWaitSeconds()`, `busyErrorCopy()`, `loadView()`, `start()`, and `#signin-form` submission so `!r.ok` non-JSON error responses are tolerated without swallowing `2xx` parse errors, only retry-signaled `503`s trigger one `1..10s` bounded automatic retry, `loadingTimer !== null` is cleared safely, `aria-busy="true"` and the returned retry `Promise` chain stay intact, and second-person `"try again in a few seconds"` guidance appears in both transient `#status` and terminal `#error` / `#signin-error` UI states.
* Added `5` focused regression and semantic tests (`0` removals) across `src/api/tests/test_resident_demo_api.py` (`2` tests) and `src/api/tests/test_resident_demo_script.py` (`3` tests) and passed all static and behavioral checks in `src/api`.

## Completed Work

### Bounded Configurable Server `Retry-After` on Bulkhead Shedding

* Related phase or task: `P01`, `P01-T01`
* Files: src/api/src/zava_forward/api/resident_demo/app.py
* What changed and why: Defined `MIN_RETRY_AFTER_SECONDS = 1`, `MAX_RETRY_AFTER_SECONDS = 10`, `RETRY_AFTER_SECONDS = 3`, and `clamp_retry_after(seconds: object) -> int` (rejecting `bool` and non-`int` inputs with `ValueError`, clamping integers into `[1, 10]`); added `retry_after_seconds: int = RETRY_AFTER_SECONDS` to `ResidentDemo.__init__`; and emitted `app.retry_after_seconds` in `Handler._route` when `app.slots.acquire(blocking=False)` fails while leaving non-bulkhead `503` paths header-free.
* Completion evidence: Diff in `src/api/src/zava_forward/api/resident_demo/app.py` and passing `AbuseAndHardeningTests` in `src/api/tests/test_resident_demo_api.py`.
* Validation: Passed (`mypy` `0` issues; `ruff check` & `ruff format --check` passed; `test_resident_demo_api.py` passed).

### Resilient Accessible Client Retry Classification and Copy in `demo.js`

* Related phase or task: `P02`, `P02-T01`
* Files: src/api/src/zava_forward/api/resident_demo/web/demo.js
* What changed and why: Loaded `web-design-guidelines` and fetched `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before editing; hardened `api()` to tolerate empty/non-JSON `!r.ok` responses while rethrowing malformed `2xx` JSON and capturing raw `Retry-After` presence; added `retryWaitSeconds()` (`1..10s` monotonic clamp, `3s` fallback for non-numeric/non-positive retry headers, `0` when no retry hint exists) and `busyErrorCopy()` (preserving `/try again in a few seconds/i` verbatim and appending punctuated `"Please try again in a few seconds."` or `BUSY_FALLBACK` otherwise); updated `loadView()` to set `aria-busy="true"`, clear `loadingTimer !== null`, reset `loading = false`, announce second-person `"try again in a few seconds"` copy with singular/plural seconds, and return the `Promise`-chained single retry guarded by `current === transition`; wired `busyErrorCopy()` into `/demo/view`, `/demo/session`, and `/demo/login`.
* Completion evidence: Diff in `src/api/src/zava_forward/api/resident_demo/web/demo.js` and passing Node VM behavioral tests in `src/api/tests/test_resident_demo_script.py`.
* Validation: Passed (`test_resident_demo_script.py`, `test_content_standard.py`, `test_accessibility_baseline.py`, `test_epic149_manual_fallback_continuity.py`, and `test_static_assets.py` all passed).

### Focused Server and Client Test Additions and `src/api` Validation Suite

* Related phase or task: `P03`, `P03-T01`
* Files: src/api/tests/test_resident_demo_api.py, src/api/tests/test_resident_demo_script.py
* What changed and why: Added `test_retry_after_seconds_is_configurable_and_bounded` and `test_expired_503_omits_retry_after_header` in `test_resident_demo_api.py`, plus `test_expired_503_without_retry_hint_fails_immediately_without_busy_retry`, `test_generic_and_non_json_shed_503_clamp_delay_and_add_retry_guidance`, and `test_login_shed_view_clears_slow_timer_and_keeps_promise_chain` in `test_resident_demo_script.py` (`5` total additions within `<= 6` cap, `0` removals).
* Completion evidence: `284` resident tests (`discover -s tests -p "test_resident*.py"`) and `57` UX/content-standard/accessibility/static-asset tests passed with `0` failures and `0` errors.
* Validation: Passed (`mypy`, `ruff check .`, `ruff format --check .`, and `unittest` suites all exited `0`).

## Implementation-Time Plan and Detail Updates

None required; implementation matched the finalized critique-reconciled plan (`PC-001` through `PC-004`).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `web-design-guidelines` pre-edit rules fetch | `resident_demo/web/demo.js` | Passed | Retrieved `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before web edits |
| `python3 -m mypy` | `src/api` (`282` source files) | Passed | `Success: no issues found in 282 source files` |
| `python3 -m ruff check .` | `src/api` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/api` (`198` files) | Passed | `198 files already formatted` |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest discover -s tests -p "test_resident*.py" -v` | All `resident*` API, demo, script, check, chat, callbacks, and summary UI tests | Passed | `Ran 284 tests in 123.412s — OK (skipped=9)` |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests python3 -m unittest tests.test_content_standard tests.test_accessibility_baseline tests.test_epic149_manual_fallback_continuity tests.test_static_assets -v` | Plain-language, WCAG 2.2 AA baseline, manual fallback continuity, and static asset integrity | Passed | `Ran 57 tests in 4.243s — OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: current (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01` checked `[x]` in plan and marked `complete` in phase details)
* Completed-work evidence and handoff prose: current
* Validation, blockers, remaining work, and follow-up items: current (`0` blockers, `0` remaining active-plan markers, focused validation tier classification recorded: small application/client UX fix with no infra, Bicep, SQL, Dockerfile, workflow, dependency, or security-control weakening)
* Review readiness: ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md, `## Follow-Up Items`
* Live post-deploy 30-viewer authenticated burst verification against `ca-resident-demo`: outside local offline worktree scope (`Do NOT push`); owned by repository owner after merging and publishing the updated `zava-resident-demo` container digest (Issue #1054).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining: none
* Validation coverage: Focused tier passed (`mypy` `0` errors across `282` files, `ruff check .` & `ruff format --check .` clean across `198` files, `284` resident tests + `57` UX/content-standard/accessibility/static-asset tests passed)
* Blockers: none
* Current plan and detail updates: Markers `P01`-`P03` and `P01-T01`-`P03-T01` checked complete; no plan amendments needed
* Planning and critique state: Ready and reconciled (`PC-001` through `PC-004` implemented and verified)
* Follow-up items: Live post-deploy burst verification on `ca-resident-demo` (owner)
* Review readiness or no-handoff reason: Ready for Review
* Continuation owner: confirmed automatic RPI Agent
