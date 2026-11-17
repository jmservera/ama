<!-- markdownlint-disable-file -->
# RPI Changes: Issue #1053 Resident Demo Callback Agenda Guard

## Metadata

* Task ID: issue-1053
* Related plan: .copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: All planned backend, client, test, static, lint, formatting, and refreshed `web-design-guidelines` checks completed and passed in `src/api`.

## Execution Summary

Completed full-plan implementation (`P01`, `P02`, `P03`) for Issue #1053 on `feat/ux-1053-agenda-guard-2235`. `GET /demo/session` now exposes `agenda_available` and `callbacks_available` matching `GET /demo/view`; `POST /demo/assistant` passes `callbacks_available=app.agenda is not None` at both `chat.answer(...)` call sites so unrouted questions omit `"Can I find a callback time?"` when the callback agenda is unconfigured while preserving `POST /demo/agenda` fail-closed `503` behavior. On the client, `web/assistant.js` defaults fail-closed (`agendaAvailable = false`), hides the dead `"Use the manual callback form"` button and `"Find callback times in the manual form"` action button when disconnected, displays an upfront plain-language notice, and preserves all Epic #149 continuity string literals; `web/demo.js` resolves `isAgendaAvailable(payload)` defensively across `actionsSection(view)`, `render(view)`, `start()`, `clearPersonal()`, and cross-tab session checks, and adds a disabled `"Synthetic callbacks"` item in `#sec-unavailable` when disconnected. Zero Issue #1054 bulkhead lines were touched.

## Completed Work

### P01 (`P01-T01`): Server Agenda Readiness & Chat Suggestion Guard

* Files modified:
  * `src/api/src/zava_forward/api/resident_demo/app.py`
  * `src/api/src/zava_forward/api/resident_demo/chat.py`
* Evidence:
  * Added `agenda_available=app.agenda is not None` and `callbacks_available=app.agenda is not None` to the `GET /demo/session` response payload in `make_handler`.
  * Passed `callbacks_available=app.agenda is not None` at both `chat.answer(...)` call sites inside `_assistant()`.
  * Updated `chat.suggestions(question, *, callbacks_available=True)` and `chat.answer(..., *, callbacks_available=None)` to exclude the `"appointments"` example (`"Can I find a callback time?"`) when `callbacks_available` is `False` (or `view["agenda_available"]` is `False`), while preserving explicit not-connected advice and `action=None` on direct `"appointments"` questions and leaving `POST /demo/agenda` `503` untouched.

### P02 (`P02-T01`, `P02-T02`): Client Page & Chat Widget Fail-Closed Agenda Guard

* Files modified:
  * `src/api/src/zava_forward/api/resident_demo/web/assistant.js`
  * `src/api/src/zava_forward/api/resident_demo/web/demo.js`
* Evidence:
  * Loaded `web-design-guidelines` prior to editing and refreshed live rules (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`) before review.
  * Updated `mountResidentAssistant` (`web/assistant.js`) to default `agendaAvailable = false`, toggle `callbacks.hidden = !agendaAvailable` and `#assistant-callbacks-note` (`callbacksOffNote.textContent` cleared to `""` when `true` so `textContent` never leaks `"not connected"`), omit `"Callback booking needs your separate confirmation."` when disconnected, guard `response.body.action === "appointments" && agendaAvailable`, support `setSession(value, agendaValue)` (updating `agendaAvailable` only when `typeof agendaValue === "boolean"`) plus `setAgendaAvailable(value)`, and preserve Epic #149 continuity literals verbatim.
  * Updated `web/demo.js` with module-scoped `agendaAvailable = false`, `isAgendaAvailable(payload)` (`agenda_available` boolean, fallback `Boolean(callbacks_available)`, default `false`), `syncAssistant(signedIn, available)` compatible with legacy `{setSession() {}}` stubs, preservation of `agendaAvailable` across `clearPersonal()` / `showSignin()` after `/demo/session`, consistent `isAgendaAvailable(view)` gating in `actionsSection(view)` and `render(view)`, and a disabled `<button type="button" disabled aria-disabled="true">Synthetic callbacks</button>` entry in `#sec-unavailable` when `!agendaAvailable`.

### P03 (`P03-T01`): Focused Regression Tests & Validation Gate

* Files modified:
  * `src/api/tests/test_resident_demo_api.py` (`+1` test method, `0` removals)
  * `src/api/tests/test_resident_chat_api.py` (`+1` test method, `0` removals)
  * `src/api/tests/test_resident_callbacks_page.py` (`+3` test methods, `0` removals)
* Evidence:
  * Added 5 focused test methods total (`0` removals) verifying `/demo/session` + `/demo/view` readiness parity and `/demo/agenda` fail-closed `503`, rules + advisor-configured `/demo/assistant` unrouted suggestion filtering, real `chat-widget.js` + `assistant.js` + `demo.js` DOM behavior in both disconnected and connected (signed-in and signed-out) states, `#sec-unavailable` disabled `"Synthetic callbacks"` item, and `callbacks_available`-only fallback behavior while retaining existing `{setSession() {}}` stub tests.

## Implementation-Time Plan and Detail Updates

* Local judgment (`test_resident_chat_api.py`): Confirmed `app.py:_assistant()` routes `topic == "unknown"` directly to the `else` branch without calling `assistant_advisor.answer_question(...)` even when `assistant_advisor` is configured; locked `advisor.answer_question.assert_not_called()` plus direct `chat.answer("unknown", {"agenda_available": False}, question)` coverage in the test. No plan or scope change required.

## Validation Record

* Validation tier classification: Focused tier (owner decision D4, 2026-11-01, refined by issue #1294). Basis: bounded UX/readiness bug fix in `resident_demo` (`app.py`, `chat.py`, `web/assistant.js`, `web/demo.js`) and 3 unit test files; zero infrastructure, Bicep, deployment, SQL, Dockerfile, workflow, dependency-manifest, or security-control changes. Hosted CI has not run locally because this branch has not been pushed per caller instructions.

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/api` (282 files) | Passed | `Success: no issues found in 282 source files` |
| `python3 -m ruff check .` | `src/api` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/api` (198 files) | Passed | `198 files already formatted` |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests python3 -m unittest test_resident_demo_api test_resident_chat_api test_resident_chat_agenda test_resident_callbacks_page test_resident_demo_script test_epic149_manual_fallback_continuity test_content_standard test_accessibility_baseline -v` | `src/api/tests` (171 tests) | Passed | `Ran 171 tests in 88.046s — OK` |
| Extended `resident_*` unit suite (`test_resident_demo_check`, `test_resident_assistant_api`, `test_resident_assistant_provider`, `test_resident_aoai`, `test_resident_screen_wcag`) | `src/api/tests` | Passed | Passed in 227-test batch (8 opt-in local SQL Server tests skipped as expected) |
| Refreshed `web-design-guidelines` review (`file:line`) | `web/assistant.js`, `web/demo.js` | Passed | `src/api/src/zava_forward/api/resident_demo/web/assistant.js`: `✓ pass`; `src/api/src/zava_forward/api/resident_demo/web/demo.js`: `✓ pass` (zero findings across accessibility, focus, forms, typography, performance, copy, and anti-patterns) |
| Issue #1054 scope isolation (`git diff`) | `src/api` | Passed | Zero lines modified in `app.py:53-79`, `app.py:286-292`, or `demo.js:742-750` |

## Pre-Review Reconciliation

* Plan markers and phase details: All phases (`P01`, `P02`, `P03`) and tasks (`P01-T01`, `P02-T01`, `P02-T02`, `P03-T01`) are checked off in `.copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md` and match `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md`.
* Completed-work evidence and handoff prose: Reconciled across all 7 modified source/test files (`4` source files, `3` test files, `+5` test methods, `0` removals).
* Validation, blockers, remaining work, and follow-up items: All Focused-tier local checks passed; zero blockers; zero remaining active-plan markers; Issue #1054 remains tracked outside scope.
* Review readiness: Ready for `rpi-review`.

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md, `## Follow-Up Items`
* Issue #1054 (`MAX_CONCURRENT = 8` / `Retry-After` contention on `GET /demo/view` in `ca-resident-demo`): explicitly out of scope per caller instructions; untouched in diff.
* Optional future wiring of a synthetic callback agenda (such as an isolated ephemeral SQLite `Agenda` when `ZF_RESIDENT_AGENDA_PATH` is explicitly configured in demo deployments): product/deployment choice noted in Issue #1053 owner comment (2026-11-05); current showcase defaults fail-closed with honest upfront UX.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` complete; `none` remaining)
* Validation coverage: Focused tier complete (`mypy`, `ruff check`, `ruff format --check`, 171+ `resident_demo`/continuity/content/WCAG unit tests, refreshed `web-design-guidelines` `file:line` review, `#1054` diff check)
* Blockers: none
* Current plan and detail updates: All plan checklist items checked off; local judgment on `unknown`-topic advisor non-invocation recorded
* Planning and critique state: Ready (`PC-001`..`PC-004` resolved directly)
* Follow-up items: Issue #1054 (`GET /demo/view` bulkhead contention) and optional deployment-time synthetic agenda provisioning
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: confirmed automatic RPI Agent parent
