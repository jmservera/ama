<!-- markdownlint-disable-file -->

# Task Research: 1054-retry-after-2235

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-14                                                               |
| Researcher / agent | rpi-research (RPI Agent)                                                 |
| Status             | Complete                                                                 |
| Artifact path      | .copilot-tracking/research/2026-11-14/1054-retry-after-2235-research.md  |

## Research Brief

* What to research: How `resident_demo/app.py` enforces the `MAX_CONCURRENT` bulkhead on signed-in `GET /demo/view` requests, how HTTP `503` responses are constructed and formatted in `resident_demo/app.py` and across `zava_forward.api`, how `resident_demo/demo.js` handles `503` / `Retry-After` / error UI accessibility and plain-language retry guidance, and how `src/api/tests/` tests `resident_demo`.
* Why it matters: Concurrent signed-in showcase viewers exceeding `MAX_CONCURRENT` currently receive HTTP `503` ("The showcase is not available right now.") with no `Retry-After` header and no retry guidance in JSON or client UI, leaving concurrent demo viewers at a generic error panel dead end (Issue #1054).
* Audience or intended use: Downstream `rpi-plan`, `rpi-implement`, and `rpi-review` phases delivering Issue #1054 on branch `feat/ux-1054-retry-after-2235` targeting `feat/demo-233-same-home-tensions-0825`.
* Scope: `src/api/src/zava_forward/api/resident_demo/` (`app.py`, `demo.js`, HTML/CSS templates and helpers), sibling `Retry-After` / `503` patterns in `src/api/`, UX/content/WCAG baselines in `docs/reference/research/ux/`, and unit/browser tests in `src/api/tests/`.
* Non-goals: Removing the concurrency bulkhead, changing `ca-resident-demo` Azure Container Apps scaling/Bicep configuration, altering authentication/session boundaries, or pushing to remote.
* Criteria: Keep the bulkhead; emit an explicit bounded/configurable `Retry-After` header (e.g., `Retry-After: 3`) on concurrency shedding; provide plain-language retry guidance ("try again in a few seconds") in both the 503 JSON payload and `demo.js` client with accessible error/status semantics; pass `mypy`, `ruff check`, `ruff format --check`, and `resident_demo` unit tests.
* Requested outputs: Converged implementation recommendation with file/line evidence, API/header/UI contract, edge-case analysis (distinguishing concurrency shedding vs other 503 causes if any), and test plan inputs.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                    |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How should `resident_demo` emit `Retry-After` and accessible plain-language retry guidance when concurrent views shed with HTTP `503`?   |
| Codebase scope                       | `src/api/src/zava_forward/api/resident_demo/`, `src/api/src/zava_forward/api/`, `src/api/tests/`, `docs/reference/research/ux/`          |
| External scope                       | RFC 9110 `Retry-After` semantics (if needed); code-first internal scope preferred unless external verification is required                |
| Initial internal candidate areas     | `src/api/src/zava_forward/api/resident_demo/app.py`, `src/api/src/zava_forward/api/resident_demo/demo.js`, `src/api/tests/`              |
| Initial external candidate areas     | none (standard HTTP `Retry-After` delay-seconds integer header is well-defined; verify existing repo conventions first)                  |
| Research posture                     | balanced                                                                                                                                 |
| Posture provenance                   | default (bounded bug fix with named files, plus adjacent 503 error modes, UX/a11y conventions, and existing tests to check)              |
| Explicit limits / deadline           | Do not push; commit locally on `feat/ux-1054-retry-after-2235`                                                                           |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence across `resident_demo`, sibling `Retry-After` conventions, UX rules, and test contracts    |
| Edits allowed during research?       | no, research-only                                                                                                                        |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                     |
| Known constraints / excluded sources | Preserve bulkhead, Fluent 2 / WCAG baseline, plain-language content standard (no banned jargon), no `.copilot-tracking/` refs in code    |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                              | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|---------------------------------------|-------------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches workspace and evidence paths              | Adds UX/WCAG/content-standard rules, validation tier rules, and git safeguards   | Selected: mandatory repository instructions                                               |
| Skill               | `rpi-research`                        | Explicit phase skill for RPI loop step 1                          | Owns three-wave research artifact and readiness handoff                          | Selected: active phase skill                                                              |
| Skill               | `web-design-guidelines`               | Matches web UI edits (`demo.js`) in repository instructions       | Guides web implementation and post-edit `file:line` review                       | Deferred to Implement/Review per repo guidance ("Before web edits, load...")              |
| Skill               | `redesign-existing-projects`          | Existing-app design improvements                                  | Audits visual design                                                             | Skipped: task is targeted error-copy/retry-guidance bug fix, not a visual redesign        |
| Skill               | `accessibility`                       | Accessibility conformance audit                                   | WCAG 2.2 check patterns                                                          | Skipped for Research: local `wcag-conformance-baseline.md` and DOM inspection cover scope |
| Research specialist | `hve-core-all:rpi-researcher`         | General delegated research lane worker                            | Independent subagent lane artifact                                               | Skipped (inline): tightly coupled 2-3 file target (`resident_demo/app.py`, `demo.js`)     |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                          |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with explicit caller acceptance criteria, branch, validation commands, and artifact paths.     | Not asked            | Proceed with `balanced` posture and `convergence` output mode under caller constraints.  |
| Direction change | Prior commits (`#1115`, `#1185`, `#1670`) partially addressed `#1054`, leaving concrete boundedness, 503-classification, client fallback copy, JSON parse resilience, and loading-state accessibility gaps within caller scope. | Not asked | Keep scope focused on completing and hardening `app.py`, `demo.js`, and `src/api/tests/` for `#1054`. |
| Convergence      | All five research questions answered from repository code and tests with zero unresolved blockers.                     | Not asked            | Mark Planning Readiness `Ready` and proceed in confirmed automatic RPI session to `Plan`. |

## Scope and Success Criteria

* Scope: `src/api/src/zava_forward/api/resident_demo/` (`app.py`, `demo.js`, and static assets), related tests in `src/api/tests/`, and sibling `Retry-After` / error patterns in `src/api/`.
* Assumptions:
  * `resident_demo` may emit `503` for more than one reason (for example, bulkhead shedding vs missing fixture/startup failure or disabled demo), which must be verified so `Retry-After` and transient retry wording are applied accurately.
  * Existing tests in `src/api/tests/` assert specific 503 status/body/DOM structures for `resident_demo` that must be inspected before planning changes.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Keep `MAX_CONCURRENT` bulkhead in `resident_demo/app.py`; emit explicit `Retry-After` header (e.g., `Retry-After: 3` or configurable/bounded seconds) on concurrent `GET /demo/view` shedding; include retry guidance ("try again in a few seconds") in 503 JSON payload and `demo.js` client with clear, accessible retry guidance; validate with `mypy`, `ruff`, and `unittest`.
* Inferred research questions:
  * Which routes and conditions in `resident_demo/app.py` use `MAX_CONCURRENT` or return HTTP `503`?
  * Does `zava_forward.api` already define a `Retry-After` convention, header helper, or JSON error envelope?
  * How does `demo.js` parse HTTP error responses, read headers/JSON fields, render error states, expose ARIA live/alert semantics, and offer a retry action (if any)?
  * Is `MAX_CONCURRENT = 8` appropriate to keep as-is for single-replica scale-to-zero demo, or configurable?
  * Which existing unit, content-standard, or accessibility tests cover `resident_demo`?
* Caller constraints and non-goals: Convergence for Issue #1054 implementation; keep bulkhead; commit locally on `feat/ux-1054-retry-after-2235`; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                 | Source / checkpoint | Effect on active brief, evidence, or revalidation                         |
|----------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------|
| narrow                                                   | Keep the `MAX_CONCURRENT` bulkhead; add `Retry-After` + JSON/client retry guidance    | Caller intake       | Excludes removing bulkhead; focuses alternatives on header/payload/UX     |
| exclude                                                  | Do not push to remote; commit cleanly on `feat/ux-1054-retry-after-2235`              | Caller intake       | Constrains Implement/Review closeout to local commit only                 |

## Research Questions

|  # | Sub-question                                                                                                      | Type            | Priority | Status   |
|---:|-------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | How does `resident_demo/app.py` implement `MAX_CONCURRENT` and what other `503` paths exist in `resident_demo`?    | depth           | H        | answered |
| Q2 | What `Retry-After` and JSON error payload conventions already exist across `src/api/`?                             | breadth         | M        | answered |
| Q3 | How does `resident_demo/demo.js` (and HTML/CSS) fetch `/demo/view`, parse errors, and present accessible UI copy?  | depth           | H        | answered |
| Q4 | Should `MAX_CONCURRENT = 8` remain 8, and should `Retry-After` seconds be constant or bounded/configurable?       | depth           | M        | answered |
| Q5 | Which tests in `src/api/tests/` cover `resident_demo`, content standards, and accessibility contracts?            | straightforward | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/content-standard.md`, `.copilot-tracking/research/2026-11-14-resident-demo-retry-after-research.md`, `.copilot-tracking/reviews/2026-11-14-resident-demo-retry-after-review.md`, GitHub Issue #1054 and its comments.
* Reused (verified) findings:
  * Content standard (`docs/reference/research/ux/content-standard.md`) requires plain-language error messages stating what happened and what to do next ("Never leave a person at a dead end"), plain ASCII punctuation, no em dashes, and bans internal jargon (`gate`, `hold`, `provenance`, `trace`, `envelope`, `snapshot`).
  * Design system and WCAG baseline (`docs/reference/research/ux/design-system.md`, `wcag-conformance-baseline.md`) require native HTML controls, `aria-busy` during loading states, non-colour status signals, visible focus, and `role="status"` / `role="alert"` live regions.
* Superseded / stale: Issue #1054's initial description predated partial slices `#1067`, `#1115`, `#1185`, `#1331`, and `#1670`. Direct source inspection on `feat/ux-1054-retry-after-2235` verified what those slices already landed and isolated the remaining server/client/accessibility defects.

## Research Cycle Log

### Cycle 1

* Active direction controls: `narrow` (preserve `MAX_CONCURRENT` bulkhead; emit bounded/configurable `Retry-After` and JSON/client retry guidance), `exclude` (commit locally only; do not push).
* Active research posture and completion basis: `balanced`; balanced scope coverage and adequate evidence across `resident_demo`, sibling `Retry-After` conventions, UX rules, and test contracts.
* Explicit limits or deadline effect: None on research depth; write scope limited to `.copilot-tracking/`.

#### Wave 1: Wider

* Plan and independent lanes: Inline breadth sweep across `src/api/src/zava_forward/api/resident_demo/`, `src/api/`, `src/api/tests/`, and `infra/` for `MAX_CONCURRENT`, `Retry-After`, `retry_after`, `/demo/view`, and `resident-demo` hosting configuration.
* Worker evidence relationships or inline fallback: Inline fallback (tightly coupled single-package target; delegation would duplicate small file reads). Mapped Q1/Q2/Q4/Q5 -> `resident_demo/app.py`, `resident_demo/web/demo.js`, `infra/README.md`, `test_resident_demo_api.py`, `test_resident_demo_script.py` (`C1`, `C2`, `C6`, `C10`, `C11`, `C12`).
* Reflection: `ca-resident-demo` runs as a single scale-to-zero replica (`0.25 vCPU`, `0.5 GiB`, `min 0 / max 1`), confirming `MAX_CONCURRENT = 8` should stay at 8 (`C1`, `C12`). Earlier slices added initial `Retry-After` and single-retry scaffolding, so Wave 2 must inspect every `503` branch in `app.py`, `demo.js`, `index.html`, and existing test assertions in detail.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact `503` emission sites in `app.py`, `ResidentDemo` constructor/configuration bounds, `demo.js` `api()`/`loadView()`/`fail()`/`beginLoading()`/`start()` flows, `index.html` live regions and focus targets, and test contracts in `test_resident_demo_api.py`, `test_resident_demo_script.py`, `test_content_standard.py`, and `test_epic149_manual_fallback_continuity.py`.
* Plan and independent lanes: Inline full reads of `resident_demo/app.py`, `resident_demo/ __main__.py`, `resident_demo/web/demo.js`, `resident_demo/web/index.html`, `resident_demo/web/demo.css`, `resident_demo/web/assistant.js`, and resident demo test modules.
* Worker evidence relationships or inline fallback: Inline execution (`C1`-`C11`). Verified seven distinct `503` paths in `app.py` (`_route` bulkhead, `_route` unhandled exception, `/healthz` not ready, `app.expired`, `_assistant` `AssistantUnavailable`, `_agenda` disconnected, `_agenda` `sqlite3.Error`) and traced `demo.js` DOM/focus/live-region transitions.
* Reflection: `app.py` currently hardcodes `RETRY_AFTER_SECONDS = 2` with no configurable/bounded instance setting on `ResidentDemo` (`C2`). In `demo.js`, `#status` (`role="status" aria-live="polite"`) and `#error` (`role="alert"`, `#error-title` focused, `#retry` native button) provide accessible containers (`C8`), but Wave 3 contrarian testing is needed to challenge failure modes when non-bulkhead `503`s, non-JSON `503`s, repeated `503`s, or slow-login timers overlap.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge the assumption that existing `#1670` changes already satisfy `#1054` cleanly across concurrent signed-in `GET /demo/view` bursts, non-bulkhead `503`s, degraded payloads, and accessible status announcements.
* Plan and independent lanes: Inline adversarial trace of `demo.js` timer, header, payload, and status interactions against all `app.py` `503` responses and existing unit/Node tests.
* Worker evidence relationships or inline fallback: Inline execution uncovered five concrete defects weakening the assumption that current code is complete:
  1. Non-bulkhead `503` misclassification (`C4`, `C6`): `demo.js:763` treats *every* first `503` on `/demo/view` as bulkhead busyness, even when `app.expired` returns `503 {"error": "This synthetic showcase has ended."}` or an unhandled reader exception returns `UNAVAILABLE` with no `Retry-After` header and no `retry_after_seconds` field.
  2. Missing client-side `"try again in a few seconds"` guidance (`C6`, `C7`): `demo.js` no longer contains `"try again in a few seconds"` in its waiting banner or fallback error handling; if a shed `503` carries `Retry-After` with generic `"The showcase is not available right now."` or an empty/non-JSON body (for example from ingress/older revision), `fail()` renders no retry guidance, and `1` second produces `"1 seconds"`.
  3. Unhandled non-JSON `503` body in `api()` (`C5`): `r.json()` in `demo.js:752` rejects on empty or plain-text `503` responses, discarding `r.status` and `Retry-After` and causing `start()` to misreport `"Check your connection"`.
  4. Loading-timer clobber and missing `aria-busy` on signed-in reload (`C6`, `C9`): During post-login `loadView`, `loadingTimer` (4000ms `SLOW_COPY` `"Still signing you in..."`) stays active during a `Retry-After` wait and overwrites the busy retry status at 4s; conversely, on an already signed-in `start() -> loadView()` or `#retry`, `mainEl` never sets `aria-busy="true"`.
  5. Unbounded/non-configurable server `Retry-After` (`C2`, `C3`): `ResidentDemo` does not expose a bounded configurable `retry_after_seconds` parameter (`[1, 10]`, default `3`), and `c9d420402` dropped backward-compatible `retry_after` key support while changing `RETRY_AFTER_SECONDS` to `2`.
* Reflection: Fixing all five issues inside `resident_demo/app.py` and `resident_demo/web/demo.js` with targeted unit and Node behavioral tests in `test_resident_demo_api.py` and `test_resident_demo_script.py` resolves every acceptance criterion without changing bulkhead semantics or unrelated endpoints.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|----------------------------|
| Keep `MAX_CONCURRENT = 8` semaphore bulkhead in `resident_demo/app.py` | `C1`, `C10`, `C12` | accepted | Explicit caller requirement; matches single-replica `0.25 vCPU` / `0.5 GiB` container profile and existing slot-ownership tests | Selected recommendation |
| Add bounded configurable `retry_after_seconds` (`[1, 10]`, default `3`) on `ResidentDemo` and emit `Retry-After` header + `retry_after_seconds` + `BUSY` copy on bulkhead shedding | `C2`, `C3`, `C10` | accepted | Satisfies explicit `Retry-After: 3` / configurable bounded seconds requirement while preserving existing `demo.RETRY_AFTER_SECONDS` test contract | Selected recommendation |
| Gate `demo.js` automatic single retry and busy copy on positive retry signal (`Retry-After` header or `retry_after_seconds` field), not bare `status === 503` | `C4`, `C6`, `C11` | accepted | Prevents `app.expired` ("This synthetic showcase has ended.") and unhinted `503` failures from falsely claiming concurrent-viewer busyness | Selected recommendation |
| Harden `demo.js` `api()`, waiting banner, `aria-busy`, `loadingTimer` cleanup, singular/plural grammar, and client fallback `"try again in a few seconds"` copy on shed `503`s | `C5`, `C6`, `C7`, `C8`, `C9`, `C11` | accepted | Ensures resilient, accessible `role="status"` / `role="alert"` retry guidance even on repeated shedding, post-login shedding, or bodyless `503`s | Selected recommendation |
| Retry multiple times with exponential backoff in `demo.js` | `C1`, `C6`, `C11` | rejected | Multiplies burst pressure against an 8-slot single replica and breaks the deliberate single-retry contract tested in `test_resident_demo_script.py` | Rejected alternative |
| Move semaphore acquisition from `_route()` into `/demo/view` only | `C3`, `C10` | rejected | Weakens server-wide thread/memory protection and breaks `test_concurrency_cap_returns_503_not_a_hang` on `/healthz` | Rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Scope covered with high-confidence primary codebase evidence (`C1`-`C12`); contrarian findings are fully resolved within existing files and require no external sources or scope expansion.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: inline: bounded 2-source-file and 2-test-file scope in `src/api`; inline inspection avoided subagent round-trip overhead without losing depth.

### Codebase Evidence

| ID  | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|-----|-----------------|------------------------|------|------------|-------|
| C1  | `MAX_CONCURRENT = 8` bounds `ResidentDemo.slots = threading.BoundedSemaphore(MAX_CONCURRENT)` with recorded `#1054` rationale | `src/api/src/zava_forward/api/resident_demo/app.py:62-64` | view | high | Also `app.py:135` |
| C2  | `BUSY` message states concurrent-viewer reason, case safety reassurance, and `"Try again in a few seconds."`; `RETRY_AFTER_SECONDS` is module constant `2` with no configurable/bounded `ResidentDemo` parameter | `src/api/src/zava_forward/api/resident_demo/app.py:80-85` | view | high | Constructor at `app.py:113-143` |
| C3  | `Handler._route` sheds non-blocking slot acquisition failures with HTTP `503`, JSON `{"error": BUSY, "retry_after_seconds": ...}`, and `Retry-After` header | `src/api/src/zava_forward/api/resident_demo/app.py:306-315` | view | high | Unhandled exceptions emit `503 {"error": UNAVAILABLE}` without `Retry-After` at `app.py:319-321` |
| C4  | Non-bulkhead `503` responses in `app.py` omit `Retry-After` and `retry_after_seconds`, including `app.expired` (`"This synthetic showcase has ended."`), `/healthz` not-ready, `_assistant`, and `_agenda` | `src/api/src/zava_forward/api/resident_demo/app.py:329-338` | view | high | Also `app.py:512-519`, `591-593`, `630-638` |
| C5  | `demo.js` `api()` parses `r.json()` unconditionally before reading `Retry-After`, throwing on empty/non-JSON `503` bodies | `src/api/src/zava_forward/api/resident_demo/web/demo.js:750-756` | view | high | Discards HTTP status and `Retry-After` header on parse error |
| C6  | `demo.js` `loadView()` retries once on *any* `res.status === 503 && !retried` regardless of retry hint, clamps `wait` to `1..10`, and lacks `"try again in a few seconds"` wording and `1 second` singular grammar | `src/api/src/zava_forward/api/resident_demo/web/demo.js:759-776` | view | high | Falls through to `fail(res.body.error || "Something went wrong.")` |
| C7  | `demo.js` `start()` and `signin-form` submit handlers pass `res.body.error` directly without client-side retry guidance if a shed `503` lacks retry text | `src/api/src/zava_forward/api/resident_demo/web/demo.js:792-793` | view | high | Login fallback at `demo.js:859` |
| C8  | `resident_demo/web/index.html` provides `#status` (`role="status" aria-live="polite"`) and `#error` (`role="alert"`, focusable `h2#error-title`, manual assist copy, and `<button type="button" id="retry">Try again</button>`) | `src/api/src/zava_forward/api/resident_demo/web/index.html:33-53` | view | high | `#retry` calls `start` (`demo.js:890`), which preserves the HttpOnly session cookie |
| C9  | `beginLoading()` sets `mainEl` `aria-busy="true"` and starts a 4000ms `loadingTimer` writing `SLOW_COPY` (`"Still signing you in..."`), which is not cleared when `loadView()` enters a `Retry-After` delay; signed-in `loadView()` without `beginLoading()` omits `aria-busy="true"` | `src/api/src/zava_forward/api/resident_demo/web/demo.js:49-68` | view | high | Interacts with `loadView()` at `demo.js:759-771` |
| C10 | `test_resident_demo_api.py` asserts `demo.MAX_CONCURRENT`, `demo.BUSY`, `"Try again in a few seconds"`, `body["retry_after_seconds"] == demo.RETRY_AFTER_SECONDS`, and `Retry-After` header on `/healthz` and signed-in `/demo/view` | `src/api/tests/test_resident_demo_api.py:713-755` | view | high | Uses `demo.RETRY_AFTER_SECONDS` symbolically, not literal `2` |
| C11 | `test_resident_demo_script.py` runs `demo.js` in Node VM and asserts `busy` scenario (`Retry-After: "3"` without `retry_after_seconds` in body) announces `"busy"`, schedules one `3000ms` timer, retries `/demo/view`, and surfaces `"Try again in a few seconds"` in `errorText` | `src/api/tests/test_resident_demo_script.py:113-131` | view | high | Assertion at `test_resident_demo_script.py:208-215` |
| C12 | `infra/README.md` documents `ca-resident-demo` as `0.25 vCPU`, `0.5 GiB`, `minimum 0`, `maximum 1` replica, matching the deliberate single-replica `MAX_CONCURRENT = 8` bulkhead | `infra/README.md:4340-4342` | grep | high | Deployment context for Issue #1054 |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `app.py` enforces `MAX_CONCURRENT = 8` via `BoundedSemaphore` in `Handler._route` and emits six other non-bulkhead `503` responses without `Retry-After` (`UNAVAILABLE`, `/healthz`, `expired`, assistant, and two agenda errors). | `C1`, `C3`, `C4` | high | Client retry/busy logic must inspect `Retry-After` / `retry_after_seconds` so non-bulkhead `503`s (especially `expired`) are not mislabelled as concurrent-viewer shedding. |
| Q2 | `resident_demo/app.py` is the only HTTP `Retry-After` emitter in `src/api`; it sends integer delay-seconds in header `Retry-After` and JSON `{"error": BUSY, "retry_after_seconds": <int>}`. | `C2`, `C3`, `C10` | high | Keep integer delay-seconds header + `retry_after_seconds` JSON field; default `RETRY_AFTER_SECONDS = 3` and clamp configurable values on `ResidentDemo` to `[1, 10]`. |
| Q3 | `demo.js` uses `#status` (`role="status" aria-live="polite"`) for polite retry progress and `#error` (`role="alert"`, focused `#error-title`, `#retry` button) for terminal failure, but needs safe JSON fallback, explicit `"try again in a few seconds"` wording, `loadingTimer` cleanup, and `aria-busy` management. | `C5`, `C6`, `C7`, `C8`, `C9` | high | Update `demo.js` `api()`, retry-hint helpers, and `loadView()`/`start()`/`login` 503 handling while keeping native controls and plain-language rules. |
| Q4 | `MAX_CONCURRENT = 8` remains right for the `0.25 vCPU` / `0.5 GiB` single-replica showcase; `retry_after_seconds` should default to `3` seconds and be bounded to `1..10` seconds on both server (`ResidentDemo`) and client (`demo.js`). | `C1`, `C2`, `C6`, `C12` | high | Add `MIN_RETRY_AFTER_SECONDS = 1`, `MAX_RETRY_AFTER_SECONDS = 10`, `RETRY_AFTER_SECONDS = 3`, and bounded `retry_after_seconds` parameter on `ResidentDemo`. |
| Q5 | `test_resident_demo_api.py` and `test_resident_demo_script.py` directly test bulkhead `503` and `demo.js` retry behavior; `test_epic149_manual_fallback_continuity.py` checks no colour-only cues in `demo.js`. | `C10`, `C11` | high | Extend `test_resident_demo_api.py` and `test_resident_demo_script.py` with bounded `Retry-After`, non-bulkhead `503`, non-JSON/generic `503` fallback copy, and post-login slow-timer interaction tests. |

## Key Discoveries

* Partial `#1054` commits (`#1067`, `#1115`, `#1185`, `#1331`, `#1670`) already established the semaphore bulkhead, `Retry-After` header, and one-shot client retry, so our implementation must preserve existing symbol contracts (`MAX_CONCURRENT`, `BUSY`, `RETRY_AFTER_SECONDS`, `retry_after_seconds`) while closing the five remaining edge-case and UX gaps (`C1`-`C11`).
* Distinguishing retryable bulkhead `503`s (positive `Retry-After` header or `retry_after_seconds` body hint) from unhinted `503`s prevents expired-showcase or database-failure responses from misleadingly announcing concurrent-viewer traffic and stalling 2-3 seconds (`C4`, `C6`).
* Clearing `loadingTimer` on retry wait and setting `aria-busy="true"` during `loadView()` fixes a real race where `"Still signing you in..."` overwrites the polite `Retry-After` announcement 4 seconds after form submission (`C6`, `C8`, `C9`).

### Complete Examples

```python
MIN_RETRY_AFTER_SECONDS = 1
MAX_RETRY_AFTER_SECONDS = 10
RETRY_AFTER_SECONDS = 3


def clamp_retry_after(seconds: int) -> int:
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        raise ValueError("retry_after_seconds must be an integer")
    return max(MIN_RETRY_AFTER_SECONDS, min(MAX_RETRY_AFTER_SECONDS, seconds))
```

```javascript
function retryHintSeconds(res) {
  var bodyHint = Number(res.body && res.body.retry_after_seconds);
  if (bodyHint > 0) return Math.min(10, Math.max(1, Math.round(bodyHint)));
  if (res.retryAfter > 0) return Math.min(10, Math.max(1, Math.round(res.retryAfter)));
  return 0;
}
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Keep `MAX_CONCURRENT = 8` in `resident_demo/app.py`; set `RETRY_AFTER_SECONDS = 3` with bounded `MIN_RETRY_AFTER_SECONDS = 1` and `MAX_RETRY_AFTER_SECONDS = 10` via an optional `retry_after_seconds: int = RETRY_AFTER_SECONDS` parameter on `ResidentDemo`; emit `Retry-After: <bounded>` and `{"error": BUSY, "retry_after_seconds": <bounded>}` when `app.slots.acquire(blocking=False)` sheds a request; and update `resident_demo/web/demo.js` to safely parse non-JSON error responses, gate automatic one-shot `/demo/view` retry on a positive retry hint (`retry_after_seconds` or `Retry-After`), maintain `aria-busy="true"` without `loadingTimer` clobbering, announce polite `"try again in a few seconds"` copy with singular/plural second formatting, and guarantee retry guidance in terminal shed `503` errors across `/demo/view`, `/demo/session`, and `/demo/login`.
* Rationale: Directly satisfies every acceptance criterion of Issue #1054, aligns server and client retry bounds (`1..10s`, default `3s`), preserves existing test contracts, prevents false busy announcements on expired/broken showcases, and meets repository plain-language and WCAG live-region/focus conventions.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`
* Implementation impact: `src/api/src/zava_forward/api/resident_demo/app.py`, `src/api/src/zava_forward/api/resident_demo/web/demo.js`, `src/api/tests/test_resident_demo_api.py`, `src/api/tests/test_resident_demo_script.py`.
* Confidence: high: all code paths and test harnesses are local, deterministic, and directly verified.

File tree:

```text
src/api/
├── src/zava_forward/api/resident_demo/
│   ├── app.py          (modified: bounded configurable retry_after_seconds, default 3s)
│   └── web/
│       └── demo.js     (modified: safe JSON parse, retry-hint gating, accessible busy/retry copy, timer/aria-busy fix)
└── tests/
    ├── test_resident_demo_api.py     (modified: configurable/bounded Retry-After and signed-in concurrent burst tests)
    └── test_resident_demo_script.py  (modified: non-bulkhead 503, generic/bodyless 503 retry guidance, post-login timer race, aria-busy tests)
```

### Alternative: Multi-attempt client exponential backoff with jitter

* Approach: Automatically retry `GET /demo/view` 3-4 times in `demo.js` with increasing delays before surfacing `#error`.
* Trade-offs: Higher chance of eventual automatic render under prolonged bursts, but multiplies request load against a 0.25 vCPU single replica and leaves a viewer waiting 10-20s without manual control.
* Evidence refs: `C1`, `C6`, `C8`, `C11`, `C12`
* Rejection rationale: Contradicts the established single-retry design (`test_resident_demo_script.py` asserts `fetches == 3` across session + view + one retry) and delays reaching the manual assistance notice and `#retry` button.

### Alternative: Apply `MAX_CONCURRENT` semaphore only to `/demo/view`, `/demo/assistant`, and `/demo/agenda`

* Approach: Bypass `app.slots` for `/healthz`, `/demo/session`, and static assets so only SQL/model routes consume slots.
* Trade-offs: Keeps `/healthz` and `/demo/session` unthrottled under synthetic slot exhaustion, but weakens process-wide handler protection and breaks `test_concurrency_cap_returns_503_not_a_hang` which explicitly tests bulkhead shedding via `/healthz`.
* Evidence refs: `C3`, `C10`
* Rejection rationale: Issue #1054 explicitly notes `/demo/session`, `/demo.js`, and `/healthz` already stayed 120/120 in live burst testing and asks to keep the bulkhead, not narrow its route coverage.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: `none`
* Important: Live deployed authenticated burst verification against `ca-resident-demo` remains an operational check outside local offline unit validation (noted in Issue #1054 owner comments).
* Follow-up: Hosted CI and independent exact-head review remain required when opening/updating a PR, after local commit.
* Residual uncertainty: Actual Azure SQL latency variance under >30 simultaneous viewers in `ca-resident-demo` is not re-measured locally because local tests use deterministic in-memory `FakeReader` and synchronization primitives.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Keep `MAX_CONCURRENT = 8` bulkhead in `resident_demo/app.py` | confirmed | user | Explicit Issue #1054 and caller requirement matching single-replica showcase limits | `C1`, `C10`, `C12` | Semaphore cap and `_route()` placement remain unchanged |
| Default `RETRY_AFTER_SECONDS = 3` and clamp `ResidentDemo.retry_after_seconds` to `1..10` seconds | proposed | evidence | Aligns server header/JSON delay with client `1..10s` clamp and caller `Retry-After: 3` / bounded seconds specification | `C2`, `C3`, `C6`, `C10` | `ResidentDemo` accepts optional `retry_after_seconds: int = RETRY_AFTER_SECONDS` |
| Gate automatic `/demo/view` retry and busy banner on positive `Retry-After` / `retry_after_seconds` hint, and supply client `"try again in a few seconds"` guidance | proposed | evidence | Avoids false busy messages on expired/broken `503`s while guaranteeing accessible retry copy on shed `503`s | `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C11` | `demo.js` cleanly separates transient shedding from permanent `503` states |
| Focused validation tier (`mypy`, `ruff check`, `ruff format --check`, `resident_demo` unit tests) and local commit without push | confirmed | user | Small targeted bug fix in non-gate application code; caller explicitly specified validation commands and `Do NOT push` | `C10`, `C11` | Run all requested checks in `src/api` and commit locally on `feat/ux-1054-retry-after-2235` |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Live deployed authenticated burst verification on `ca-resident-demo` | Post-deployment burst run against updated container digest in Azure | owner | Required before closing GitHub Issue #1054 completely | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Measure post-deploy `ca-resident-demo` 30-viewer burst recovery rate with `Retry-After: 3` | Confirms live end-to-end retry success rate over Azure SQL | Owner deploys new `zava-resident-demo` image digest | deferred | Q4; `C1`, `C12` |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected with high confidence.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`
* Preconditions met: Target files, existing partial changes, edge-case defects, UX/WCAG/content-standard rules, and test harnesses verified.
* Blockers: `none`
* Smallest action to change readiness: `none`

## Closeout Record

| Field                            | Record                                                                                                        |
|----------------------------------|---------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                      |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                                                     |
| Lane evidence or inline fallback | Inline fallback across Cycle 1 waves (bounded 2-file source scope; subagent dispatch unnecessary)             |
| Research disposition             | executed                                                                                                      |
| Planning Readiness               | Ready (`C1`-`C12`)                                                                                            |
| Blockers                         | none                                                                                                          |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic transition to `Plan`                                                 |

## Advisory Next Step

| Field                            | Record                                                                                                        |
|----------------------------------|---------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                      |
| Planning Readiness               | Ready (`C1`-`C12`)                                                                                            |
| Output mode and planning support | `convergence`; yes, selected recommendation is backed by `C1`-`C12` and Planning Readiness is `Ready`         |
| Acting owner                     | confirmed automatic RPI Agent                                                                                 |
| Required gates or confirmations  | Research brief, 3-wave cycle, evidence IDs, self-check, and pre-transition state write: passed                |
| Continuation result              | automatic continuation to `Plan` (`rpi-plan`)                                                                 |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/1054-retry-after-2235-research.md                                       |
| Notes for planning or re-entry   | Preserve existing `MAX_CONCURRENT`, `BUSY`, and `RETRY_AFTER_SECONDS` test symbols; load `web-design-guidelines` before editing `demo.js` |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All in-scope server, client, accessibility, and test questions are answered from direct codebase evidence (`C1`-`C12`); further research is immaterial before planning.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry and Provenance, User Participation and Research Decisions, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions and Evidence, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none
