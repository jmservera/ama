<!-- markdownlint-disable-file -->
# RPI Phase Details: Resident Demo 503 Retry-After and Accessible Retry Guidance (Issue #1054)

## Metadata

* Task ID: 1054-retry-after-2235
* Task slug: 1054-retry-after-2235
* Related plan: .copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/1054-retry-after-2235-research.md (`C1`-`C12`), src/api/src/zava_forward/api/resident_demo/app.py, src/api/src/zava_forward/api/resident_demo/web/demo.js, src/api/src/zava_forward/api/resident_demo/web/index.html, src/api/tests/test_resident_demo_api.py, src/api/tests/test_resident_demo_script.py

## Phase Index

| Phase ID | Name                                                      | Status   | Detail sections |
|----------|-----------------------------------------------------------|----------|-----------------|
| P01      | Bounded Server `Retry-After` and Bulkhead Shedding Contract | complete | P01, P01-T01    |
| P02      | Resilient Accessible Client Retry Guidance in `demo.js`   | complete | P02, P02-T01    |
| P03      | Focused Unit, VM, Accessibility, and Static Validation    | complete | P03, P03-T01    |

<!-- rpi:phase id=P01 -->
## P01: Bounded Server `Retry-After` and Bulkhead Shedding Contract

### Context

`src/api/src/zava_forward/api/resident_demo/app.py` guards the single-replica resident showcase with `MAX_CONCURRENT = 8` (`self.slots = threading.BoundedSemaphore(MAX_CONCURRENT)`) inside `Handler._route` (`C1`, `C3`, `C12`). Currently `RETRY_AFTER_SECONDS = 2` is a fixed module constant with no instance configurability or range clamping (`C2`), while six other `503` responses in `app.py` (`UNAVAILABLE` unhandled exception, `/healthz` not-ready, `app.expired`, `_assistant` unavailable, and two `_agenda` database failures) intentionally omit `Retry-After` (`C4`). Existing tests in `src/api/tests/test_resident_demo_api.py` reference `demo.MAX_CONCURRENT`, `demo.BUSY`, and `demo.RETRY_AFTER_SECONDS` symbolically (`C10`).

### Intent

Provide a default `RETRY_AFTER_SECONDS = 3` and bounded configurable `retry_after_seconds` (`1..10` integer seconds) on `ResidentDemo`, emitting the bounded integer value in both `Retry-After` and JSON `retry_after_seconds` exclusively when the `MAX_CONCURRENT` bulkhead sheds a request.

### Boundaries

* Included: `MIN_RETRY_AFTER_SECONDS = 1`, `MAX_RETRY_AFTER_SECONDS = 10`, `RETRY_AFTER_SECONDS = 3`, `clamp_retry_after(seconds: object) -> int`, `ResidentDemo.__init__(..., retry_after_seconds: int = RETRY_AFTER_SECONDS)`, and `Handler._route` bulkhead `503` emission using `app.retry_after_seconds`.
* Excluded: Changing `MAX_CONCURRENT = 8`, altering route slot ownership, modifying `src/core/`, or adding `Retry-After` to non-bulkhead `503` paths (`expired`, `/healthz`, unhandled exceptions, assistant/agenda backend errors).

### Likely Targets

* src/api/src/zava_forward/api/resident_demo/app.py: Define retry-after bounds/clamping helper, store `self.retry_after_seconds` on `ResidentDemo`, and emit `str(app.retry_after_seconds)` + `retry_after_seconds=app.retry_after_seconds` on bulkhead shedding.

### Dependencies

* None.

### Validation Expectations

* `python3 -m mypy` and `python3 -m ruff check . && python3 -m ruff format --check .` in `src/api` pass with `0` issues.
* Existing and new bulkhead tests in `src/api/tests/test_resident_demo_api.py` pass.

### Completion Evidence

* Updated `src/api/src/zava_forward/api/resident_demo/app.py` diff and passing `test_resident_demo_api` run.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add bounded `retry_after_seconds` configuration and emission in `resident_demo/app.py`

#### Context

Issue #1054 specifies keeping `MAX_CONCURRENT` and emitting an explicit `Retry-After` header (for example `Retry-After: 3` or configurable/bounded seconds) alongside JSON retry guidance (`BUSY` already states `"The showcase is busy because several people are viewing it at once. Nothing is wrong with your case. Try again in a few seconds."`, `C2`). Bounding `retry_after_seconds` to `1..10` seconds matches `demo.js`'s `1..10s` client cap (`C6`) so server hints and client waits agree.

#### Intent

Add `MIN_RETRY_AFTER_SECONDS = 1`, `MAX_RETRY_AFTER_SECONDS = 10`, `RETRY_AFTER_SECONDS = 3`, and `clamp_retry_after(seconds: object) -> int` (rejecting `bool` and non-`int` runtime inputs with `ValueError`, clamping integers to `[1, 10]` in a `mypy`-clean signature), wire `retry_after_seconds: int = RETRY_AFTER_SECONDS` into `ResidentDemo.__init__`, and use `app.retry_after_seconds` in `Handler._route` when `app.slots.acquire(blocking=False)` returns `False`.

#### Boundaries

* Included: `app.py` module constants, `clamp_retry_after`, `ResidentDemo.__init__` keyword-compatible parameter, and `_route` bulkhead `503` payload/header.
* Excluded: Non-bulkhead `503` responses and CLI flags in `__main__.py`.

#### Likely Targets

* src/api/src/zava_forward/api/resident_demo/app.py: Constants, `clamp_retry_after`, `ResidentDemo.__init__`, and `Handler._route`.

#### Dependencies

* None.

#### Validation Expectations

* Verify default `ResidentDemo` emits `Retry-After: 3` and `retry_after_seconds: 3`, clamped values (`0 -> 1`, `99 -> 10`) emit `1` and `10`, `bool`/non-`int` raises `ValueError`, and `expired=True` `503` emits no `Retry-After` header.

#### Completion Evidence

* Clean `mypy` types on `ResidentDemo.__init__` and `clamp_retry_after`, plus green `test_resident_demo_api.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Resilient Accessible Client Retry Guidance in `demo.js`

### Context

`src/api/src/zava_forward/api/resident_demo/web/demo.js` currently has four client gaps identified in Cycle 1 Contrarian analysis (`C4`-`C9`):
1. `api()` calls `r.json()` unconditionally (`C5`), throwing on empty/plain-text `503` responses and losing `r.status` and `Retry-After`.
2. `loadView()` checks `if (res.status === 503 && !retried)` without checking whether `Retry-After` or `retry_after_seconds` was sent (`C4`, `C6`), causing permanent `503` states like `app.expired` (`"This synthetic showcase has ended."`) to falsely announce concurrent-viewer busyness and pause before failing.
3. `demo.js` lacks the explicit `"try again in a few seconds"` client wording requested by Issue #1054 (`C6`, `C7`): its waiting status says `"Trying again in " + wait + " seconds…"` (which also outputs `"1 seconds"` when `wait === 1`), and when a shed `503` carries generic `"The showcase is not available right now."` or an empty body, `fail()`/`start()`/`login` show no retry guidance.
4. During post-login `loadView()`, `beginLoading()`'s 4-second `loadingTimer` remains scheduled and overwrites `#status` with `SLOW_COPY` (`"Still signing you in..."`) during a `Retry-After` wait (`C9`); meanwhile, signed-in `start() -> loadView()` omits `aria-busy="true"` on `#main`.

### Intent

Follow `.github/copilot-instructions.md` Web Development Guidance (`web-design-guidelines` pre-edit load and fetch), then harden `demo.js` so retry-signaled `503`s get safe JSON fallback, accurate classification, clean `aria-busy` / `loadingTimer` coordination, and plain-language `"try again in a few seconds"` guidance in both polite status and alert error states.

### Boundaries

* Included: Loading `web-design-guidelines` and fetching its live rules; updating `api()`, retry-hint/error-copy helpers, `loadView()`, `start()`, and `#signin-form` submit `503` handling in `src/api/src/zava_forward/api/resident_demo/web/demo.js`.
* Excluded: Visual restyling (`demo.css`), HTML structure changes (`index.html` already has compliant `#status`, `#error`, `#error-title`, manual assistance copy, and `#retry`), or multi-retry loops.

### Likely Targets

* src/api/src/zava_forward/api/resident_demo/web/demo.js: `api()`, `retryWaitSeconds()`, `shedErrorCopy()`, `loadView()`, `start()`, and `login` submit handler.

### Dependencies

* P01 (`RETRY_AFTER_SECONDS = 3` and `1..10s` server contract).
* `web-design-guidelines` skill + fetched rules source.

### Validation Expectations

* Node VM tests in `src/api/tests/test_resident_demo_script.py` pass for existing `busy` scenario (`Retry-After: "3"`, 3000ms timer, 3 total fetches) and new edge-case scenarios.
* Content standard and fallback continuity tests (`test_content_standard.py`, `test_accessibility_baseline.py`, `test_epic149_manual_fallback_continuity.py`) pass.

### Completion Evidence

* Updated `src/api/src/zava_forward/api/resident_demo/web/demo.js` diff, fetched `web-design-guidelines` compliance check, and green Node VM test output.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Load `web-design-guidelines` and update `resident_demo/web/demo.js` retry and fallback copy

#### Context

In `index.html` (`C8`), `#status` is `<p id="status" class="status" role="status" aria-live="polite"></p>` and `#error` is `<section id="error" ... role="alert" hidden>` with `<h2 id="error-title" tabindex="-1">`, `#error-text`, manual staff help reassurance, and `<button type="button" id="retry">Try again</button>`. `endLoading()` (`demo.js:64-68`) clears `loadingTimer` and removes `aria-busy` from `mainEl`, and is already called by `render()`, `fail()`, and `showSignin()`.

#### Intent

1. Invoke `web-design-guidelines` skill and fetch its current guidelines URL before editing `demo.js`.
2. In `api(path, options)`:
   * Read raw `Retry-After` header string via `r.headers && r.headers.get ? r.headers.get("Retry-After") : null` and compute `hasRetryAfter = rawHeader !== null && String(rawHeader).trim() !== ""`.
   * Parse JSON via `r.json().catch(function (err) { if (r.ok) throw err; return {}; })` and normalize `var safeBody = body && typeof body === "object" ? body : {};` so malformed `2xx` payloads still reject into `.catch()` while empty/HTML `!r.ok` error bodies resolve cleanly to `{ ok: r.ok, status: r.status, retryAfter: hasRetryAfter ? Number(rawHeader) : NaN, hasRetryAfter: hasRetryAfter, body: safeBody }`.
3. Add two small helpers in `demo.js`:
   * `retryWaitSeconds(res)`: returns `0` unless `res.status === 503` and either `res.hasRetryAfter` is true or (`res.body && res.body.retry_after_seconds !== undefined && res.body.retry_after_seconds !== null && typeof res.body.retry_after_seconds !== "boolean"`). When retry-signaled, inspects finite positive numeric body hint first, then `res.retryAfter`; if `Number.isFinite(num) && num > 0`, returns `Math.min(10, Math.max(1, Math.round(num)))` (`"99" -> 10`), and otherwise defaults non-numeric or non-positive retry headers (such as HTTP-date strings or `"0"`) to `3` seconds.
   * `busyErrorCopy(res, fallback)`: if `res.status === 503` and `retryWaitSeconds(res) > 0`:
     * When `res.body && typeof res.body.error === "string" && res.body.error.trim()`: let `trimmed = res.body.error.trim()`; if `/try again in a few seconds/i.test(trimmed)`, return `trimmed` verbatim (preserving `app.py` `BUSY` `"Try again in a few seconds."` and `test_resident_demo_script.py` assertions); otherwise return `trimmed + (/[.!?]$/.test(trimmed) ? "" : ".") + " Please try again in a few seconds."`.
     * When `res.body.error` is absent/empty: return `"The showcase is busy because several people are viewing it at once. Nothing is wrong with your case. Please try again in a few seconds."`.
     * Otherwise (non-bulkhead error): return `(res.body && res.body.error) || fallback`.
4. In `loadView(announce, retried)`:
   * Set `mainEl.setAttribute("aria-busy", "true")` while loading `/demo/view` (cleared automatically by `endLoading()` in `render()`, `fail()`, or `showSignin()`).
   * Compute `var wait = retryWaitSeconds(res);`. If `wait > 0 && !retried`: clear `loadingTimer` safely (`if (loadingTimer !== null) { clearTimeout(loadingTimer); loadingTimer = null; }`), reset `loading = false` while keeping `aria-busy="true"`, set `statusEl.textContent = "The showcase is busy because several people are viewing it at once. We will try again in a few seconds (" + wait + (wait === 1 ? " second" : " seconds") + ")\u2026"`, and return `new Promise(function (resolve) { setTimeout(resolve, wait * 1000); }).then(function () { if (current === transition) return loadView(announce, true); })` so caller `.catch()` / `.then()` chains and cross-tab `transition` cancellation remain intact.
   * On non-OK completion without retry: call `fail(busyErrorCopy(res, "Something went wrong."))`.
5. In `start()` (`/demo/session` non-OK) and `#signin-form` submit (`/demo/login` non-OK): pass `busyErrorCopy(res, "The showcase is not available right now.")` and `busyErrorCopy(res, "We could not sign you in.")` respectively so bulkhead-shed session or login requests also receive `"try again in a few seconds"` guidance.

#### Boundaries

* Included: `resident_demo/web/demo.js` logic and plain-language copy.
* Excluded: Changing DOM IDs, CSS classes, or session cookie mechanics.

#### Likely Targets

* src/api/src/zava_forward/api/resident_demo/web/demo.js: Lines around `api`, `loadView`, `start`, and `form.addEventListener("submit", ...)`.

#### Dependencies

* P01-T01 and `web-design-guidelines` skill activation.

#### Validation Expectations

* Existing `test_busy_view_retries_once_after_retry_after_then_shows_the_error` passes unchanged (`"busy"` in waiting status, `1` timer at `3000ms`, `retried == True`, `"Try again in a few seconds"` in `errorText`, `fetches == 3`).
* New VM tests verify non-bulkhead `expired` `503` does not retry, generic/empty-body `503` with `Retry-After` receives `"try again in a few seconds"`, `1` second uses singular `"1 second"`, `aria-busy` toggles cleanly, and post-login `loadingTimer` does not clobber `#status`.

#### Completion Evidence

* Diff of `demo.js` and passing `test_resident_demo_script.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Unit, VM, Accessibility, and Static Validation

### Context

Under repository validation policy (owner decision D4 / #1294), this targeted application and client UX fix takes the **focused validation tier**: no Bicep/infra, SQL schema, Dockerfile, workflow, dependency manifest, gate script, or security control is changed. All canonical tests live in `src/api/tests/test_resident_demo_api.py` and `src/api/tests/test_resident_demo_script.py` (`C10`, `C11`), alongside UX/content-standard suites (`test_content_standard.py`, `test_accessibility_baseline.py`, `test_epic149_manual_fallback_continuity.py`, `test_static_assets.py`).

### Intent

Add focused regression and semantic tests (`0` removals, `<= 6` additions across `test_resident_demo_api.py` and `test_resident_demo_script.py`), then run `mypy`, `ruff check .`, `ruff format --check .`, and the `resident_demo` + UX unit test suites in `src/api`.

### Boundaries

* Included: `src/api/tests/test_resident_demo_api.py`, `src/api/tests/test_resident_demo_script.py`, and running validation commands in `src/api`.
* Excluded: Removing or weakening existing assertions, creating standalone ad-hoc test files, or running cloud deployments.

### Likely Targets

* src/api/tests/test_resident_demo_api.py: Server bulkhead `retry_after_seconds` configurability, clamping (`[1, 10]`), type validation, and absence of `Retry-After` on non-bulkhead `expired` `503`.
* src/api/tests/test_resident_demo_script.py: Client non-bulkhead `503` immediate failure, generic/non-JSON shed `503` `"try again in a few seconds"` guidance, singular `1 second` + out-of-range clamp, `aria-busy`, and post-login `loadingTimer` non-clobber.

### Dependencies

* P01, P02.

### Validation Expectations

* `cd src/api && python3 -m mypy` -> `Success: no issues found` (`0` errors).
* `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .` -> `0` errors and clean formatting.
* `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests.test_resident_demo_api tests.test_resident_demo_script tests.test_resident_demo_check tests.test_resident_summary_ai_ui tests.test_content_standard tests.test_accessibility_baseline tests.test_epic149_manual_fallback_continuity tests.test_static_assets -v` -> `OK`.

### Completion Evidence

* Recorded command outputs and test counts in `.copilot-tracking/changes/2026-11-14/1054-retry-after-2235-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Extend `resident_demo` server and client tests and run `src/api` validation suite

#### Context

Before `rpi-plan-critique`, test ownership and bounds are locked:
* Canonical targets: `src/api/tests/test_resident_demo_api.py` and `src/api/tests/test_resident_demo_script.py`.
* Generated targets: `none`.
* Exact test removals: `none`.
* Maximum test additions: `6` focused test methods (`2` in `test_resident_demo_api.py`, up to `4` in `test_resident_demo_script.py`).
* Semantic-versus-regression split:
  * Regression preserved: existing `test_concurrency_cap_returns_503_not_a_hang`, `test_one_slot_below_the_cap_still_admits_a_request`, `test_shed_signed_in_view_carries_retry_guidance`, `test_shed_view_owns_every_slot_despite_delayed_login_release`, and `test_busy_view_retries_once_after_retry_after_then_shows_the_error`.
  * Semantic additions: (1) configurable and clamped `retry_after_seconds` (`1..10`, invalid `Any`-typed non-`int`/bool input raises `ValueError` cleanly under `mypy`) on `ResidentDemo` signed-in `/demo/view` shedding; (2) expired-showcase `503` omits `Retry-After` on server and fails immediately without false busy retry in `demo.js`; (3) generic or non-JSON `503` with `Retry-After` (`1` second -> `"1 second"`, `"99"` -> clamped `"10 seconds"`, HTTP-date -> `"3 seconds"`) preserves status, sets/clears `aria-busy`, and renders `"try again in a few seconds"`; (4) post-login shed `/demo/view` retry status clears timer ID `0`, keeps the returned `Promise` chain active until retry settles, and is not overwritten by the 4000ms `SLOW_COPY` timer.

#### Intent

Implement the focused tests in both canonical test modules and execute the full required `src/api` validation command set.

#### Boundaries

* Included: `test_resident_demo_api.py`, `test_resident_demo_script.py`, and `mypy`/`ruff`/`unittest` execution in `src/api`.
* Excluded: Unrelated API test suites outside resident showcase and UX/content baselines unless a failure requires escalation.

#### Likely Targets

* src/api/tests/test_resident_demo_api.py: Add `test_retry_after_seconds_is_configurable_and_bounded` and `test_expired_503_omits_retry_after_header`.
* src/api/tests/test_resident_demo_script.py: Extend embedded Node scenario runner and add focused methods for unhinted `expired` `503`, generic/non-JSON shed `503` fallback copy + `1 second` / clamp / `aria-busy`, and post-login `loadingTimer` non-clobber.

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* Every command required by the caller exits `0` with zero warnings/errors.

#### Completion Evidence

* Exact test runner and static analyzer outputs captured in `.copilot-tracking/changes/2026-11-14/1054-retry-after-2235-changes.md`.

#### Unresolved Items

* None.
