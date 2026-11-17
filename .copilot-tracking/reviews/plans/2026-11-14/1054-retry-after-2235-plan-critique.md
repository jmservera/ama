<!-- markdownlint-disable-file -->
# RPI Plan Critique: Resident Demo 503 Retry-After and Accessible Retry Guidance (Issue #1054)

## Metadata

* Task ID: 1054-retry-after-2235
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver Issue #1054 on branch `feat/ux-1054-retry-after-2235` targeting `feat/demo-233-same-home-tensions-0825` in worktree `/home/azureuser/source/ama-demo-wt/feat-1054-retry-after-2235`; keep `MAX_CONCURRENT = 8` in `resident_demo/app.py`; emit bounded/configurable `Retry-After` (for example `Retry-After: 3`) and `503` JSON retry guidance on bulkhead shedding; provide accessible `"try again in a few seconds"` client retry guidance in `resident_demo/web/demo.js`; write all 4 dated RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/`; validate in `src/api` with `mypy`, `ruff check`, `ruff format --check`, and `resident_demo` unit tests; commit cleanly with the `Co-authored-by` trailer and do not push.
* Research and evidence considered: .copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md, .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md, .copilot-tracking/research/2026-11-14/1054-retry-after-2235-research.md (`C1`-`C12`), src/api/src/zava_forward/api/resident_demo/app.py, src/api/src/zava_forward/api/resident_demo/web/demo.js, src/api/src/zava_forward/api/resident_demo/web/index.html, src/api/tests/test_resident_demo_api.py, src/api/tests/test_resident_demo_script.py.
* Decisions, dependencies, and acceptance criteria considered: Confirmed preservation of `MAX_CONCURRENT = 8`; proposed bounded `retry_after_seconds` (`1..10`, default `RETRY_AFTER_SECONDS = 3`); positive retry-signal gating (`Retry-After` header or `retry_after_seconds` body field) so non-bulkhead `503` responses (`app.expired`, `UNAVAILABLE`, `/healthz`, `_assistant`, `_agenda`) do not falsely retry; single client auto-retry on `GET /demo/view`; `web-design-guidelines` pre-edit load/fetch and review audit; canonical test lock (`0` removals, `<= 6` additions across `test_resident_demo_api.py` and `test_resident_demo_script.py`); focused validation tier in `src/api`; local commit without push.
* Assessment boundary: Cross-checks every requirement, research claim (`C1`-`C12`), phase, task, helper contract, and test expectation against the supplied source and test files. Does not execute live network fetches for `web-design-guidelines`, run test suites, or observe live Azure `ca-resident-demo` container bursts.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 (`MAX_CONCURRENT = 8`, default `Retry-After: 3`, `BUSY` JSON) | Covered | Grounded in `app.py:62-84,306-315` and symbolic `demo.RETRY_AFTER_SECONDS` assertions in `test_resident_demo_api.py:713-755` (`C1`, `C2`, `C3`, `C10`). |
| FR-2 / P01 / P01-T01 (configurable bounded `retry_after_seconds`, non-bulkhead `503` separation) | Partial | Constructor default compatibility and `[1, 10]` clamping match `app.py:108-143,319-338`, but `clamp_retry_after(seconds: int)` + non-`int` negative test needs `mypy`-safe typing (`PC-004`). |
| FR-3 (`api()` non-JSON HTTP error resilience) | Partial | `P02-T01` catches `r.json()` unconditionally even when `r.ok` is `true`, converting malformed `200 OK` responses into a `TypeError` inside `render()` (`PC-003`). |
| FR-4 / P02 / P02-T01 (single bounded `/demo/view` retry, `loadingTimer`, `aria-busy`, polite copy) | Partial | `P02-T01` drops `loadView()`'s returned retry `Promise` and `current === transition` guard, uses falsy-unsafe `if (loadingTimer)`, and resets `> 10s` hints to `3s` instead of clamping to `10s` (`PC-001`, `PC-002`). |
| FR-5 (non-bulkhead `503` immediate fail; shed `503` `"try again in a few seconds"` fallback) | Partial | Non-bulkhead gating matches `C4`/`C6`, but `busyErrorCopy()` tests `/try again/i` instead of `/try again in a few seconds/i`, letting generic `"try again"` strings omit required timing guidance (`PC-003`). |
| NFR-1 (WCAG 2.2 AA `aria-busy`, polite `#status`, alert `#error`, focus continuity) | Partial | `index.html:33-53` provides compliant live/alert landmarks, but unreturned retry `setTimeout` in `P02-T01` leaks `aria-busy="true"` if the retry fetch rejects (`PC-001`). |
| NFR-2 (plain-language content standard, `web-design-guidelines`, `mypy`, `ruff`) | Covered | Proposed copy avoids banned jargon and colour-only cues; `P02-T01` loads `web-design-guidelines` prior to web edits and `P03-T01` runs `mypy` and `ruff`. |
| P03 / P03-T01 (canonical test targets, `<= 6` additions, focused validation tier) | Partial | Target files and commands match caller scope, but `P03-T01` item (3) encodes `"99" -> "3 seconds"` instead of clamped `"10 seconds"` (`PC-002`) and omits `mypy`-safe typing detail for invalid-type assertions (`PC-004`). |
| Caller RPI artifacts and local-only git closeout | Covered | Plan tracks `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` plus companion artifacts and local commit with `Co-authored-by` trailer without pushing. |

## Verdict

* Verdict: Revise
* Rationale: Server bulkhead framing, `503` path separation, and validation scope are well-grounded in `C1`-`C12`, but `P02-T01` and `P03-T01` contain three substantive client defects (broken retry `Promise` chain / missing `transition` cancellation / falsy timer-ID check in `loadView()`, inconsistent `> 10s` client clamping vs `FR-4` and `P01`, and `200 OK` JSON parse swallowing plus loose `/try again/i` matching) along with one low-severity `mypy` typing detail in `P01-T01`. All four findings are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `P02-T01` replaces `loadView()`'s returned retry `Promise` and `transition` guard with an unchained `setTimeout`, breaking error recovery, cross-tab cancellation, and `0`-indexed timer clearing

* Related IDs: FR-4, NFR-1, C6, C9, C11, P02, P02-T01, P03-T01
* Evidence: .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md (`P02-T01` Intent item 4), src/api/src/zava_forward/api/resident_demo/web/demo.js (lines 49-90, 759-810, 838-863), src/api/tests/test_resident_demo_script.py (line 55)
* Concern: Existing `demo.js:767-769` returns `new Promise(function (resolve) { setTimeout(resolve, wait * 1000); }).then(function () { if (current === transition) return loadView(announce, true); });`. `P02-T01` item 4 replaces that with bare `setTimeout(function () { loadView(announce, true); }, wait * 1000)` and `if (loadingTimer) { clearTimeout(loadingTimer); loadingTimer = null; }` without resetting `loading = false`.
* Impact: First, `loadView()` resolves `undefined` as soon as the initial `503` arrives; if the retry `fetch("/demo/view")` rejects on a network drop, neither `start()`'s `.catch()` (`demo.js:808`) nor `#signin-form`'s `.catch()` (`demo.js:859`) catches the rejection, leaving `#main` stuck with `aria-busy="true"` and no `#error` alert (`NFR-1` violation) while `#signin-form` re-enables `signinButton` mid-retry. Second, omitting `if (current === transition)` lets a sign-out or cross-tab session change (`clearPersonal()`) during the wait still fire `loadView(announce, true)`, setting `aria-busy="true"` over `#signin` and overwriting `"Your sign-in changed in another tab. Please sign in again."`. Third, `if (loadingTimer)` fails to clear timer ID `0` in `0`-based timer stubs (`test_resident_demo_script.py:55`, unlike `endLoading()`'s `if (loadingTimer !== null)` at `demo.js:65`), and leaving `loading === true` suppresses `"Loading your progress..."` when the retry leg begins.
* Smallest useful change: Update `P02-T01` item 4 to keep returning `new Promise(function (resolve) { setTimeout(resolve, wait * 1000); }).then(function () { if (current === transition) return loadView(announce, true); })`, clear `loadingTimer` using `if (loadingTimer !== null) { clearTimeout(loadingTimer); loadingTimer = null; }` while setting `loading = false` on retry wait entry, and cover post-login retry completion cleanly in `P03-T01`.
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md` (`P02-T01`) specifies returning the `Promise`-chained retry guarded by `current === transition`, null-safe `loadingTimer !== null` clearing, and `loading = false` reset before retry wait.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Client `retryWaitSeconds()` resets `Retry-After` values above `10` down to `3` seconds instead of clamping to `10` seconds

* Related IDs: FR-4, C2, C6, P01-T01, P02-T01, P03, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md (Scope line 54, `FR-4` line 77, `P02-T01` line 144), .copilot-tracking/research/2026-11-14/1054-retry-after-2235-research.md (lines 206, 219-225), .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md (`P01-T01` line 69, `P02-T01` line 133, `P03` line 177, `P03-T01` line 206)
* Concern: Research (`retryHintSeconds`, lines 219-225) and `P01-T01` (`clamp_retry_after`: `0 -> 1`, `99 -> 10`) clamp positive values above `10` to `10` seconds (`Math.min(10, Math.max(1, Math.round(...)))`), and Plan Scope / `P03` call this behavior an out-of-range `1..10s` clamp. However, `P02-T01` item 3 specifies `raw > 0 && raw <= 10 ? Math.max(1, Math.round(raw)) : 3` and `P03-T01` item (3) expects `Retry-After: "99"` to format `"3 seconds"`. In addition, `Number(res.body && res.body.retry_after_seconds)` converts boolean `true` to `1` if `typeof !== "boolean"` is not guarded.
* Impact: Under `P02-T01`, client backoff is non-monotonic when an upstream proxy or server signals heavier overload: `Retry-After: 10` backs off for `10` seconds, whereas `Retry-After: 15` or `"99"` retries in `3` seconds (3.3x faster), contradicting `P01`'s upper clamp and Research's selected design.
* Smallest useful change: Update `FR-4`, `P02-T01` item 3, and `P03-T01` item (3) so finite positive numeric hints (`typeof val !== "boolean"`, `Number.isFinite(num) && num > 0`) clamp via `Math.min(10, Math.max(1, Math.round(num)))` (`"99" -> 10 seconds`), while non-numeric, non-finite, or non-positive retry signals (such as HTTP-date headers or `"0"`) default to `3` seconds.
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md` (`FR-4`, `P02-T01`) and `.copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md` (`P02-T01`, `P03-T01`) consistently specify `Math.min(10, Math.max(1, Math.round(...)))` clamping (`"99" -> 10 seconds`) and `3`-second fallback only for non-positive/non-numeric retry headers.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `P02-T01` `api()` swallows invalid JSON on `200 OK` responses and `busyErrorCopy()` allows bare `"try again"` strings to bypass `"try again in a few seconds"` guidance

* Related IDs: FR-3, FR-5, C5, C6, C7, P02-T01
* Evidence: .copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md (`FR-3` line 73, `FR-5` line 80), .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md (`P02-T01` items 2-3, lines 128-137), src/api/src/zava_forward/api/resident_demo/web/demo.js (lines 409-415, 660-715, 750-756)
* Concern: First, `FR-3` scopes non-JSON tolerance to HTTP error bodies, but `P02-T01` item 2 uses `r.json().catch(function () { return {}; })` even when `r.ok` is `true`, and only normalizes `b || {}` (leaving non-null JSON primitives truthy). On a truncated `200 OK` from `/demo/view`, `loadView()` calls `render({}, announce)`, where `summarySection()` dereferences `view.summary.sources` (`demo.js:410,415`) and throws an unhandled `TypeError` instead of entering `.catch()` error recovery. Second, `busyErrorCopy()` checks `/try again/i.test(res.body.error)`, so an upstream shed `503` returning `"Service unavailable. Please try again later."` or `"Please reload the page and try again."` returns verbatim without `"try again in a few seconds"`, and appending `" Please try again in a few seconds."` to a periodless error string creates a run-on sentence.
* Impact: Corrupt `2xx` responses crash `render()` instead of surfacing the existing connection-recovery panel, and upstream shed `503` messages mentioning `"try again"` without a timeframe fail `FR-5` and caller `"try again in a few seconds"` requirements.
* Smallest useful change: In `P02-T01` item 2, rethrow JSON parse failures when `r.ok` is `true` (`r.json().catch(function (err) { if (r.ok) throw err; return {}; })`) and normalize `body` with `b && typeof b === "object" ? b : {}`. In `P02-T01` item 3, match `/try again in a few seconds/i.test(res.body.error)` (which still preserves `app.py` `BUSY` and `test_resident_demo_script.py` `"busy"` copy verbatim) and append `"."` if `trimmed` lacks `[.!?]$` before `" Please try again in a few seconds."`.
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md` (`P02-T01` items 2-3) restricts `{}` JSON fallback to `!r.ok` (with object guard) and checks `/try again in a few seconds/i` with sentence-ending punctuation normalization.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: `clamp_retry_after(seconds: int)` runtime non-`int` guard and negative unit test need explicit `mypy`-compatible typing

* Related IDs: FR-2, NFR-2, P01-T01, P03-T01
* Evidence: .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md (`P01-T01` lines 55, 69-73; `P03-T01` lines 182, 206), src/api/src/zava_forward/api/resident_demo/app.py (lines 108-143, 159), src/api/tests/test_resident_demo_api.py (lines 136-163, 713-755)
* Concern: `P01-T01` specifies `clamp_retry_after(seconds: int) -> int` with `isinstance(seconds, bool) or not isinstance(seconds, int)` raising `ValueError`, while `P03-T01` tests non-`int` inputs inside fully annotated `-> None` test methods in `test_resident_demo_api.py` and requires `python3 -m mypy` to pass with `0` issues. Depending on `mypy` reachability and argument-type checks, `not isinstance(seconds, int)` on `seconds: int` and passing `"3"` or `1.5` directly to an `int`-typed parameter in a typed test method can raise `[unreachable]` or `[arg-type]` errors.
* Impact: Avoidable `mypy` failure during `P01`/`P03` validation if the parameter annotation and negative test call site are not typed intentionally.
* Smallest useful change: Specify in `P01-T01` and `P03-T01` that `clamp_retry_after(seconds: object) -> int` (or `Any`, matching `app.py:159`) validates runtime types while `ResidentDemo.__init__` keeps `retry_after_seconds: int = RETRY_AFTER_SECONDS`, and negative non-`int` tests in `test_resident_demo_api.py` pass an `Any`-typed value when exercising `ResidentDemo` runtime validation.
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md` (`P01-T01`, `P03-T01`) documents `mypy`-clean annotations for `clamp_retry_after` and negative runtime type assertions.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Preserving `MAX_CONCURRENT = 8` on `ResidentDemo.slots` in `Handler._route` (`C1`, `C3`, `C12`) honors caller constraints, container memory limits (`0.25 vCPU`, `0.5 GiB`, single replica), and existing `/healthz` and `/demo/view` slot-ownership tests in `test_resident_demo_api.py`.
* Separating retry-signaled bulkhead `503` responses from the six non-bulkhead `503` paths in `app.py` (`C4`) eliminates false concurrent-viewer stalls on ended showcases (`app.expired`) and database failures (`UNAVAILABLE`).
* Test scope and ownership are tightly bounded (`0` removals, `<= 6` focused additions in canonical `test_resident_demo_api.py` and `test_resident_demo_script.py`, `0` generated files), and Web Development Guidance (`web-design-guidelines` pre-edit load/fetch and review audit) is explicitly integrated.
* Accepted residual risk and closeout reminder: live 30-viewer authenticated burst testing against `ca-resident-demo` is appropriately deferred as a post-deploy owner follow-up because remote push/deployment is out of scope; during local commit closeout, remember `.github/copilot-instructions.md` requires configuring repository-local `user.email` to `{id}+{login}@users.noreply.github.com` from `gh api user`.

## Questions or Blocking Evidence Gaps

* none

## Limitations

* Read-only plan critique evaluated static alignment across the plan, phase details, research (`C1`-`C12`), and target source/test files; it did not execute `mypy`, `ruff`, `unittest`, Node VM runs, or live `web-design-guidelines` retrieval.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md` and `.copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md` to apply `PC-001` through `PC-004`, record critique dispositions, and finalize the plan for `P01` implementation without another critique pass.
* User response required: no
