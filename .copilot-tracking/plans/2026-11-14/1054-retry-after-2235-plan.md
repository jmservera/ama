<!-- markdownlint-disable-file -->
# RPI Plan: Resident Demo 503 Retry-After and Accessible Retry Guidance (Issue #1054)

## Task Metadata

* Task ID: 1054-retry-after-2235
* Task slug: 1054-retry-after-2235
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/1054-retry-after-2235-plan-critique.md

## Executive Summary

When more than `MAX_CONCURRENT = 8` concurrent requests reach the single-replica resident showcase (`resident_demo/app.py`), excess signed-in `GET /demo/view` requests are shed intentionally with HTTP `503` rather than queuing against Azure SQL. Earlier partial slices added an initial semaphore and retry stub, but left `RETRY_AFTER_SECONDS` non-configurable at `2`, allowed `demo.js` to misclassify permanent `503` states (such as an ended showcase) as concurrent-viewer traffic, crashed `api()` on non-JSON `503` bodies, allowed the 4-second sign-in slow timer to overwrite the retry status banner, and lacked client-side `"try again in a few seconds"` fallback guidance.

This plan completes Issue #1054 cleanly across `resident_demo/app.py`, `resident_demo/web/demo.js`, and `src/api/tests/`: it preserves the 8-slot bulkhead, makes `retry_after_seconds` configurable and bounded (`1..10` seconds, default `RETRY_AFTER_SECONDS = 3`) in both `Retry-After` and JSON, hardens `demo.js` so only retry-hinted `503`s auto-retry with accessible polite `role="status"` and `aria-busy` announcements, and ensures every shed `503` displays plain-language `"try again in a few seconds"` guidance.

### User Decisions and Requirements Highlights

* **Preserve `MAX_CONCURRENT = 8` bulkhead**: Excess concurrent requests keep shedding fast with `503` instead of hanging or exhausting the `0.25 vCPU` / `0.5 GiB` container replica.
* **Explicit bounded `Retry-After` and JSON guidance**: Shed responses emit `Retry-After` (default `3`, clamped to `1..10` seconds) alongside `retry_after_seconds` and plain-language `BUSY` copy reassuring the viewer nothing is wrong with their case.
* **Client-side accessible retry guidance**: `demo.js` honors `Retry-After` / `retry_after_seconds` for one bounded retry on `/demo/view`, keeps `aria-busy` and polite status announcements coherent, and guarantees `"try again in a few seconds"` copy even when an upstream or repeated `503` omits custom JSON error prose.
* **Focused local validation and local-only commit**: Validate in `src/api` with `mypy`, `ruff check`, `ruff format --check`, and `resident_demo` unit tests, then commit cleanly on `feat/ux-1054-retry-after-2235` without pushing.

### What You May Not Know

* **`app.py` emits non-bulkhead `503`s without `Retry-After`**: Ended showcases (`app.expired`) and unhandled reader failures also return HTTP `503`. Gating `demo.js` busy retry behavior on a positive retry hint (`Retry-After` header or `retry_after_seconds` field) prevents ended showcases from falsely claiming concurrent viewer traffic and stalling 3 seconds before displaying `"This synthetic showcase has ended."`.
* **4-second `loadingTimer` race after sign-in**: Submitting `#signin-form` starts a 4-second `SLOW_COPY` timer (`"Still signing you in..."`). Without clearing `loadingTimer` when `loadView()` enters a `Retry-After` wait, `SLOW_COPY` overwrites the polite retry status mid-wait.
* **Web Development Guidance applies to `demo.js`**: Repository instructions require loading `web-design-guidelines` and fetching its current rule source before editing `demo.js`, then refreshing and auditing `demo.js` with `file:line` findings during Review.

### Unresolved Decisions or Blockers

* None for local implementation, validation, review, and commit. Post-deployment live 30-viewer burst confirmation against `ca-resident-demo` is tracked in [Follow-Up Items](#follow-up-items) for owner execution after image publication.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (Research, Plan, Implement, Review) for Issue #1054 (`fix(resident-demo): concurrent signed-in views shed with 503 and no retry guidance`) in worktree `/home/azureuser/source/ama-demo-wt/feat-1054-retry-after-2235` on branch `feat/ux-1054-retry-after-2235` targeting `feat/demo-233-same-home-tensions-0825` (caller prompt).
* Keep the deliberate `MAX_CONCURRENT` bulkhead in `src/api/src/zava_forward/api/resident_demo/app.py` (caller prompt; Issue #1054).
* Emit an explicit `Retry-After` header (for example `Retry-After: 3` or configurable/bounded seconds) and retry guidance in the `503` JSON payload and `demo.js` client (`"try again in a few seconds"`) so a concurrent demo viewer gets clear, accessible retry guidance (caller prompt; Issue #1054).
* Follow Zava North Homes plain-language content standard, Fluent 2 design system rules, WCAG 2.2 AA baseline, and `web-design-guidelines` verification on changed web files (`.github/copilot-instructions.md`; `docs/reference/research/ux/content-standard.md`; `docs/reference/research/ux/design-system.md`).
* Write all four dated RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` for Issue #1054 (caller prompt).
* Validate in `src/api` with `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and relevant `resident_demo` unit tests via `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest ... -v` (caller prompt).
* Commit all changes cleanly on `feat/ux-1054-retry-after-2235` with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer and do NOT push (caller prompt).

## Goals

* Keep `resident_demo` bulkhead shedding deterministic at `MAX_CONCURRENT = 8` while emitting a configurable, bounded integer `Retry-After` delay (`1..10` seconds, default `3`) and plain-language retry guidance in `503` JSON responses.
* Make `resident_demo/web/demo.js` distinguish retry-signaled bulkhead `503` responses from non-bulkhead `503` responses, perform one bounded accessible automatic retry on `GET /demo/view`, and guarantee `"try again in a few seconds"` guidance in both transient status and terminal error UI states.
* Prove server, client, accessibility, and content-standard conformance through targeted unit/VM tests, static checks (`mypy`, `ruff`), and `web-design-guidelines` review.

## Scope and Non-Goals

### In Scope

* `src/api/src/zava_forward/api/resident_demo/app.py`: bounded configurable `retry_after_seconds` (`MIN_RETRY_AFTER_SECONDS = 1`, `MAX_RETRY_AFTER_SECONDS = 10`, `RETRY_AFTER_SECONDS = 3`) on `ResidentDemo` and bulkhead `503` response emission.
* `src/api/src/zava_forward/api/resident_demo/web/demo.js`: resilient `api()` JSON fallback, retry-hint inspection and `1..10s` clamping, accessible `loadView()` single-retry announcement (`aria-busy`, `loadingTimer` clear, singular/plural second phrasing, `"try again in a few seconds"`), and shed `503` client fallback copy across `/demo/view`, `/demo/session`, and `/demo/login`.
* `src/api/tests/test_resident_demo_api.py` and `src/api/tests/test_resident_demo_script.py`: focused semantic and regression tests for server and client retry behavior.
* RPI artifacts under `.copilot-tracking/{research,plans,details,reviews/plans,changes,reviews,rpi-sessions}/2026-11-14/`.

### Non-Goals

* Changing `MAX_CONCURRENT = 8` or bypassing `ResidentDemo.slots` for specific HTTP routes.
* Multi-attempt client retry loops that amplify burst load against the single-replica container.
* Editing `src/core/`, Bicep infrastructure, Dockerfiles, or GitHub Actions workflows.
* Pushing commits to `origin`, opening/updating PRs, or running live cloud burst traffic against `ca-resident-demo`.

## Functional Requirements

* FR-1: When `ResidentDemo.slots.acquire(blocking=False)` fails in `Handler._route`, `app.py` returns HTTP `503` with `Content-Type: application/json; charset=utf-8`, header `Retry-After: <N>`, and JSON `{"error": BUSY, "retry_after_seconds": <N>}`, where `<N>` defaults to `RETRY_AFTER_SECONDS = 3` and `BUSY` includes `"Try again in a few seconds."`.
  * Observable acceptance criteria: Loopback HTTP tests verify concurrent signed-in `GET /demo/view` (and `/healthz`) requests above `MAX_CONCURRENT = 8` return `503`, `Retry-After: 3` by default, `retry_after_seconds == 3`, and `BUSY` copy.
* FR-2: `ResidentDemo` accepts an optional integer `retry_after_seconds: int = RETRY_AFTER_SECONDS` constructor parameter, clamps integer values into `[MIN_RETRY_AFTER_SECONDS, MAX_RETRY_AFTER_SECONDS]` (`[1, 10]`), rejects non-integer/boolean types with `ValueError`, and leaves non-bulkhead `503` responses without `Retry-After`.
  * Observable acceptance criteria: Unit tests verify custom in-range (`5`), below-minimum (`0 -> 1`), and above-maximum (`30 -> 10`) `retry_after_seconds` values govern both header and JSON field, non-int/bool raises `ValueError`, and `app.expired` `503` omits `Retry-After`.
* FR-3: `demo.js` `api()` tolerates empty or non-JSON HTTP error (`!r.ok`) bodies without throwing a `SyntaxError` while still rejecting malformed `2xx` JSON, normalizing `body` to an object and preserving `status`, `retryAfter` (`Number` parsed from `Retry-After`), and raw `hasRetryAfter` header presence.
  * Observable acceptance criteria: Node VM script test verifies a bodyless/plain-text `503` with `Retry-After: 2` triggers the bounded retry path and surfaces retry guidance rather than the network-unreachable catch block.
* FR-4: On first `GET /demo/view` `503` carrying a retry signal (`retry_after_seconds` in body or `Retry-After` header), `demo.js` clears any pending `loadingTimer` (`loadingTimer !== null`) and resets `loading = false`, keeps `aria-busy="true"` on `#main`, announces plain-language busy copy including `"try again in a few seconds"` and grammatically matched delay (`1 second` vs `N seconds`) in `#status` (`role="status" aria-live="polite"`), and returns a `Promise`-chained retry guarded by `current === transition` after clamping finite positive numeric hints into `[1, 10]` seconds (`Math.min(10, Math.max(1, Math.round(num)))`, defaulting non-numeric or non-positive retry headers to `3s`).
  * Observable acceptance criteria: Node VM tests verify single retry timing and returned `Promise` chain, `1 second` vs `3 seconds` vs clamped `10 seconds` (`Retry-After: "99"`) copy, `"try again in a few seconds"` presence in waiting status, `aria-busy="true"` during wait, and non-overwrite at `>= 4000ms` after login even with timer ID `0`.
* FR-5: On a non-bulkhead `503` lacking both `Retry-After` and `retry_after_seconds` (such as `app.expired` `"This synthetic showcase has ended."`), `demo.js` fails immediately without announcing concurrent-viewer busyness or scheduling a retry timer; on terminal retry-signaled `503` responses across `/demo/view`, `/demo/session`, and `/demo/login`, `demo.js` preserves server retry copy verbatim when `/try again in a few seconds/i` matches and appends punctuated `"Please try again in a few seconds."` guidance when server copy omits that timeframe.
  * Observable acceptance criteria: Node VM tests verify immediate failure (`0` retry timers, `2` total fetches) on `expired` `503`, and verify `"try again in a few seconds"` appears in `#error-text` (`role="alert"`) when a shed `503` carries generic `"The showcase is not available right now."` or an empty body.

## Non-Functional Requirements

* NFR-1: Accessibility and focus continuity (`docs/reference/research/ux/wcag-conformance-baseline.md`, `design-system.md`).
  * Objective threshold or evaluation condition: Transient retry wait uses polite `#status` (`role="status" aria-live="polite"`) plus `#main[aria-busy="true"]`; terminal failure clears `aria-busy`, reveals `#error` (`role="alert"`) with native `#retry` button, and moves focus to `#error-title` without removing session state.
  * Operating condition or verification approach, if needed: Verified via Node VM script assertions in `test_resident_demo_script.py` and existing `test_accessibility_baseline.py` / `web-design-guidelines` review.
  * Observable acceptance criteria: Zero `aria-busy` leaks after `render()`, `fail()`, or `showSignin()`, `#error-title` receives focus on terminal `503`, and `#retry` reloads `/demo/session` + `/demo/view` without re-authenticating.
* NFR-2: Plain-language content standard and static quality (`docs/reference/research/ux/content-standard.md`).
  * Objective threshold or evaluation condition: Zero banned internal jargon words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), zero colour-only status cues, plain ASCII source comments, `mypy` `0` errors, `ruff check .` `0` errors, and `ruff format --check .` clean.
  * Operating condition or verification approach, if needed: Run `mypy`, `ruff`, `test_content_standard.py`, and `test_epic149_manual_fallback_continuity.py` in `src/api`.
  * Observable acceptance criteria: All static and unit suites exit `0`.

## Acceptance Criteria

* `MAX_CONCURRENT = 8` bulkhead remains intact in `resident_demo/app.py`.
* Concurrent signed-in `GET /demo/view` requests shed by the bulkhead receive HTTP `503`, `Retry-After: 3` (or configured `1..10` integer seconds), and JSON `{"error": BUSY, "retry_after_seconds": <int>}` containing `"Try again in a few seconds."`.
* `demo.js` honors `Retry-After` / `retry_after_seconds` for a single bounded retry on shed `/demo/view` `503`s, skips false busy retries on non-bulkhead `503`s without retry signals, prevents `loadingTimer` status clobbering, maintains `aria-busy`, and renders `"try again in a few seconds"` guidance in both waiting status and terminal shed `503` errors.
* Test ownership and scope lock: modify only canonical test modules `src/api/tests/test_resident_demo_api.py` and `src/api/tests/test_resident_demo_script.py` (`0` test removals, at most `6` focused test additions, `0` generated targets), covering both regression contracts and newly fixed edge cases.
* Focused validation tier passes in `src/api`: `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and `resident_demo` + UX/content-standard unit tests.
* All four required RPI artifacts exist under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` (with companion phase details, critique, and state artifacts), and all changes are committed cleanly on `feat/ux-1054-retry-after-2235` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/1054-retry-after-2235-plan.md                                                                         |
| Phase details                    | .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md                                                              |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/1054-retry-after-2235-plan-critique.md with `Revise` verdict (`PC-001`–`PC-004` all resolved directly by planner) |
| Relevant research                | .copilot-tracking/research/2026-11-14/1054-retry-after-2235-research.md (`C1`-`C12`)                                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/1054-retry-after-2235-changes.md is created or continued by implementation as its evidence record   |
| Planning execution and readiness | Complete; implementation-ready after resolving `PC-001` through `PC-004`                                                                 |
| Continuation context             | Confirmed automatic RPI Agent session; parent transitions automatically to `Implement` (`P01`)                                           |

## Sources

* .copilot-tracking/research/2026-11-14/1054-retry-after-2235-research.md: Primary Cycle 1 Wider/Deeper/Contrarian evidence (`C1`-`C12`), selected recommendation, and rejected alternatives.
* src/api/src/zava_forward/api/resident_demo/app.py: Current `MAX_CONCURRENT`, `BUSY`, `RETRY_AFTER_SECONDS`, `ResidentDemo`, and seven `503` paths.
* src/api/src/zava_forward/api/resident_demo/web/demo.js: Current `beginLoading`/`endLoading`, `api()`, `loadView()`, `start()`, `login`, and `fail()` behavior.
* src/api/src/zava_forward/api/resident_demo/web/index.html: Live-region `#status`, alert `#error`, `#error-title` focus target, and `#retry` button markup.
* src/api/tests/test_resident_demo_api.py and src/api/tests/test_resident_demo_script.py: Canonical loopback HTTP and Node VM behavioral test suites.
* docs/reference/research/ux/content-standard.md, docs/reference/research/ux/design-system.md, docs/reference/research/ux/wcag-conformance-baseline.md: Plain-language, `aria-busy`, focus, and non-colour status requirements.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Bounded Server `Retry-After` and Bulkhead Shedding Contract

* Intent: Expose bounded configurable `retry_after_seconds` (`1..10`, default `3`) on `ResidentDemo` and emit consistent `Retry-After` headers and JSON retry guidance on bulkhead `503` shedding while keeping `MAX_CONCURRENT = 8`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add bounded `retry_after_seconds` configuration and emission in `resident_demo/app.py`

* Requirement and evidence: FR-1, FR-2; research `C1`, `C2`, `C3`, `C4`, `C10`.
* Expected result: `MIN_RETRY_AFTER_SECONDS = 1`, `MAX_RETRY_AFTER_SECONDS = 10`, `RETRY_AFTER_SECONDS = 3`, `clamp_retry_after()`, `ResidentDemo(..., retry_after_seconds: int = RETRY_AFTER_SECONDS)` storing `self.retry_after_seconds`, and `Handler._route` emitting `app.retry_after_seconds` in both `Retry-After` header and `retry_after_seconds` JSON field on slot exhaustion only.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Resilient Accessible Client Retry Guidance in `demo.js`

* Intent: Load `web-design-guidelines`, harden `demo.js` `503` parsing and retry-signal classification, fix `loadingTimer` / `aria-busy` coordination, and guarantee plain-language `"try again in a few seconds"` guidance in both polite status and alert error states.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Load `web-design-guidelines` and update `resident_demo/web/demo.js` retry and fallback copy

* Requirement and evidence: FR-3, FR-4, FR-5, NFR-1, NFR-2; research `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C11`; `.github/copilot-instructions.md` Web Development Guidance.
* Expected result: `web-design-guidelines` current source fetched before edits; `api()` tolerates non-JSON `!r.ok` error responses while rethrowing malformed `2xx` JSON and preserving `Retry-After`; `retryWaitSeconds(res)` clamps finite positive numeric hints into `1..10` seconds (`Math.min(10, Math.max(1, Math.round(num)))`, defaulting non-numeric/non-positive retry headers to `3`) and returns `0` when no retry hint exists; `loadView()` clears `loadingTimer !== null`, resets `loading = false`, sets `aria-busy="true"`, announces `"try again in a few seconds"` with singular/plural seconds in `#status`, and returns a `Promise`-chained single retry guarded by `current === transition` only on retry-signaled `503`s; terminal shed `503`s across `/demo/view`, `/demo/session`, and `/demo/login` always include punctuated `"try again in a few seconds"` guidance.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Unit, VM, Accessibility, and Static Validation

* Intent: Lock regression and semantic coverage in `test_resident_demo_api.py` and `test_resident_demo_script.py` and pass focused-tier checks (`mypy`, `ruff`, `unittest`).
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Extend `resident_demo` server and client tests and run `src/api` validation suite

* Requirement and evidence: FR-1 through FR-5, NFR-1, NFR-2; research `C10`, `C11`; focused validation tier (`.github/copilot-instructions.md` D4 / #1294).
* Expected result: Up to `6` focused test additions (`0` removals) in `src/api/tests/test_resident_demo_api.py` and `src/api/tests/test_resident_demo_script.py` proving configurable/bounded `retry_after_seconds`, non-bulkhead `503` non-retry, generic/non-JSON `503` retry copy fallback, singular `1 second` phrasing, `aria-busy` lifecycle, and post-login `loadingTimer` non-clobber; `mypy`, `ruff check .`, `ruff format --check .`, and all `resident_demo` + UX baseline tests pass with `0` errors.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/1054-retry-after-2235-phase-details.md

## Dependencies

* Python toolchain (`mypy`, `ruff`, `unittest`) and Node.js (`node`, required by `test_resident_demo_script.py` VM harness): local runtime prerequisites in `src/api`.
* `web-design-guidelines` skill and remote guideline rules URL: required by `.github/copilot-instructions.md` before web edits and before Review; any network failure must be disclosed explicitly if encountered.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [High]    | resolved    | Updated `FR-4` and `P02-T01` so `loadView()` returns the `Promise`-chained retry guarded by `current === transition`, clears `loadingTimer !== null` (0-safe), and resets `loading = false` while preserving `aria-busy="true"`. |
| Run 1 `PC-002` [Medium]  | resolved    | Aligned `FR-4`, `P02-T01`, and `P03-T01` so finite positive numeric retry hints clamp monotonically via `Math.min(10, Math.max(1, Math.round(num)))` (`"99" -> 10s`), reserving `3s` for non-numeric or non-positive retry headers. |
| Run 1 `PC-003` [Medium]  | resolved    | Restricted `api()` `{}` JSON fallback to `!r.ok` (with object guard) so malformed `2xx` JSON still triggers `.catch()`, and tightened `busyErrorCopy()` to check `/try again in a few seconds/i` with sentence-ending punctuation normalization. |
| Run 1 `PC-004` [Low]     | resolved    | Specified `clamp_retry_after(seconds: object) -> int` in `P01-T01` and `Any`-typed negative test inputs in `P03-T01` so runtime non-`int` guards remain `mypy`-clean (`0` errors). |

## Follow-Up Items

* Live post-deploy 30-viewer authenticated burst verification against `ca-resident-demo`: outside local offline worktree scope (`Do NOT push`); owned by repository owner after merging and publishing the updated `zava-resident-demo` container digest (Issue #1054).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/1054-retry-after-2235-changes.md
* Ready phase or task: Complete (`P01`, `P02`, `P03` checked and validated); ready for `Review`
* Remaining provisional question or blocker: none
