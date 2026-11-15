<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #1053 Resident Demo Callback Agenda Guard

## Metadata

* Task ID: issue-1053
* Task slug: issue-1053-resident-demo-agenda-guard
* Related plan: .copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/issue-1053-resident-demo-agenda-guard-research.md (`C1`-`C17`, `W1`)

## Phase Index

| Phase ID | Name                                                  | Status | Detail sections          |
|----------|-------------------------------------------------------|--------|--------------------------|
| P01      | Server Agenda Readiness & Chat Suggestion Guard       | ready  | P01, P01-T01             |
| P02      | Client Page & Chat Widget Fail-Closed Agenda Guard    | ready  | P02, P02-T01, P02-T02    |
| P03      | Focused Regression Tests & Validation Gate            | ready  | P03, P03-T01             |

## Test & Target Ownership Lock

* Canonical handwritten production targets:
  * `src/api/src/zava_forward/api/resident_demo/app.py`
  * `src/api/src/zava_forward/api/resident_demo/chat.py`
  * `src/api/src/zava_forward/api/resident_demo/web/assistant.js`
  * `src/api/src/zava_forward/api/resident_demo/web/demo.js`
* Generated targets: `none`
* Canonical test targets (existing files only; `0` new test files):
  * `src/api/tests/test_resident_demo_api.py` (owner of `/demo/session`, `/demo/view`, and `/demo/agenda` HTTP contract coverage)
  * `src/api/tests/test_resident_chat_api.py` (owner of `/demo/assistant` and `chat.py` routing/suggestion coverage)
  * `src/api/tests/test_resident_callbacks_page.py` (owner of Node fake-DOM coverage for `demo.js` and `assistant.js` callback agenda states)
* Exact test removals: `none`
* Maximum test additions: `5` focused test methods total (`<=1` in `test_resident_demo_api.py`, `<=1` in `test_resident_chat_api.py`, `<=3` in `test_resident_callbacks_page.py`)
* Semantic vs regression coverage:
  * Semantic coverage (new behavior that fails without this fix): `/demo/session` `agenda_available`/`callbacks_available` booleans (`True` and `False`); `chat.suggestions()` omitting `"Can I find a callback time?"` when `agenda=None`; `assistant.js` hiding `"Use the manual callback form"` and updating intro/notice copy when `agenda_available=False` while showing it when `True`; `demo.js` rendering disabled `"Synthetic callbacks"` in `#sec-unavailable` when disconnected and honoring `callbacks_available` fallback.
  * Regression coverage (existing suites kept green): `POST /demo/agenda` returning `503` when `agenda=None`; `test_epic149_manual_fallback_continuity.py`; `test_content_standard.py`; `test_accessibility_baseline.py`; `test_resident_demo_script.py`; `test_resident_chat_agenda.py`; `test_resident_demo_check.py`.
* Validation classification (owner decision D4 / #1294): **Focused tier** — small bounded `resident_demo` UX/capability-flag bug fix with zero infrastructure, Bicep, Dockerfile, SQL schema, package manifest, workflow, or security-control changes.

<!-- rpi:phase id=P01 -->
## P01: Server Agenda Readiness & Chat Suggestion Guard

### Context

`ResidentDemo.view_for` (`app.py:194-202`) already populates `agenda_available` and `callbacks_available` (`self.agenda is not None`), and `POST /demo/agenda` (`app.py:556-567`) fails closed with `503` when `app.agenda is None` (`C4`, `C6`). However, `GET /demo/session` (`app.py:322-335`) omits `agenda_available` and `callbacks_available` (`C5`), and `POST /demo/assistant` (`app.py:492-505`) calls `chat.answer(...)` without telling `chat.suggestions()` whether callbacks are connected, allowing unrouted questions mentioning `"visit"` or `"time"` to suggest `"Can I find a callback time?"` even when `app.agenda is None` (`C7`, `C11`).

### Intent

Expose `agenda_available` and `callbacks_available` consistently on `GET /demo/session` and suppress unrouted callback search suggestions in `chat.py` when `callbacks_available` is `False`, without touching `POST /demo/agenda` fail-closed `503` logic or Issue #1054 bulkhead concurrency code.

### Boundaries

* Included: `_session` and `_assistant` in `src/api/src/zava_forward/api/resident_demo/app.py`; `suggestions()` and `answer()` in `src/api/src/zava_forward/api/resident_demo/chat.py`.
* Excluded: `MAX_CONCURRENT`, `RETRY_AFTER_SECONDS`, `BUSY`, `_SLOTS`, and `_route` bulkhead lines (`app.py:53-79`, `app.py:286-292`); `Agenda` SQLite storage (`agenda.py`); `infra/resident-demo.bicep`.

* Likely Targets
  * `src/api/src/zava_forward/api/resident_demo/app.py`: add `agenda_available=app.agenda is not None` and `callbacks_available=app.agenda is not None` to `_session` response JSON; pass `callbacks_available=app.agenda is not None` at both `chat.answer(...)` call sites in `_assistant` (`app.py:474, 491`).
* `src/api/src/zava_forward/api/resident_demo/chat.py`: add keyword parameter `callbacks_available: bool = True` to `suggestions()` and `answer()`, filtering `item[0] != "appointments"` when `not callbacks_available` (also honoring `view.get("agenda_available")` when `answer()` is called directly with a `view` dict containing `agenda_available=False`).

### Dependencies

* None.

### Validation Expectations

* `mypy` passes with strict typing on `app.py` and `chat.py`; `/demo/session` returns boolean `agenda_available` and `callbacks_available` without leaking resident email or session internals (`C12`, `C15`).

### Completion Evidence

* Clean diff in `app.py` and `chat.py` verified by HTTP unit tests in `test_resident_demo_api.py` and `test_resident_chat_api.py`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Surface `agenda_available` and `callbacks_available` in `GET /demo/session` and guard `chat.py` unrouted suggestions

#### Context

* In `app.py:326-334`, `_session` returns `dict(csrf=token, signed_in=signed_in, session_id=..., banner=rs.BANNER)`. Adding `agenda_available=app.agenda is not None, callbacks_available=app.agenda is not None` exposes a pure service-capability flag (zero PII) and preserves compatibility with `resident_demo_browser_check.py` (`C5`, `C12`, `C15`).
* In `chat.py:606-617`, `suggestions(question: str, *, callbacks_available: bool = True) -> list[str]` ranks `TOPIC_EXAMPLES`; excluding `"appointments"` when `not callbacks_available` falls back cleanly to `"How is my case going?"`, `"What documents am I missing?"`, and `"What forms do I need?"` (`C11`).

#### Intent

Deliver consistent backend readiness flags on `/demo/session` and `/demo/view` and honest chat fallback suggestions when `app.agenda is None`.

#### Boundaries

* Included: `app.py` `_session` and `_assistant` call site; `chat.py` `suggestions` and `answer`.
* Excluded: `app.py` bulkhead lines (`53-79`, `286-292`) and `_agenda` `503` handler (`556-567`).

#### Likely Targets

* `src/api/src/zava_forward/api/resident_demo/app.py`
* `src/api/src/zava_forward/api/resident_demo/chat.py`

#### Dependencies

* None.

#### Validation Expectations

* `GET /demo/session` returns `agenda_available: False, callbacks_available: False` when `agenda=None` and `True` when `agenda` is configured; `POST /demo/assistant` with `{"question": "When is the next visit time?", "use_record": True}` omits `"Can I find a callback time?"` when `agenda=None`.

#### Completion Evidence

* Passing unit assertions in `test_resident_demo_api.py` and `test_resident_chat_api.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Client Page & Chat Widget Fail-Closed Agenda Guard

### Context

In `web/assistant.js` (`lines 197, 224-239, 302-309`), `mountResidentAssistant` unconditionally displays `"Callback booking needs your separate confirmation."` and an active `"Use the manual callback form"` button inside `ui.intro` (`C10`). When signed in to `ca-resident-demo` (`agenda_available === false`), `#callback-title` is not mounted and `#email`/`#retry` are hidden, so clicking `"Use the manual callback form"` silently closes chat and focuses `#chat-launcher` (`C10`). Meanwhile, `test_epic149_manual_fallback_continuity.py` scans `assistant.js` source for `"Use the manual callback form"` and `r"Chat could not load\.[^\"]*"` containing `"The manual callback form is still available."` (`C14`), and `test_resident_demo_script.py` / `test_resident_callbacks_page.py` stub `mountResidentAssistant: () => ({setSession() {}})` (`C13`). In `web/demo.js` (`lines 673-687`), `#sec-unavailable` renders disabled showcase feature buttons (`ul.unavail`) (`C8`, `C15`).

### Intent

Make both `web/assistant.js` and `web/demo.js` fail-closed on `agenda_available` so disconnected showcases never offer a dead manual-callback button or callback invitation, while surfacing clear plain-language notices and preserving every Epic #149, content-standard, WCAG 2.2, and fake-DOM test invariant.

### Boundaries

* Included: Pre-edit `web-design-guidelines` skill activation and live rules fetch (`PC-004`); `mountResidentAssistant` in `src/api/src/zava_forward/api/resident_demo/web/assistant.js`; `agendaAvailable` state, `isAgendaAvailable`, `syncAssistant`, `clearPersonal`, `actionsSection`, `render()`, `start()`, and `showSignin()` in `src/api/src/zava_forward/api/resident_demo/web/demo.js` (`PC-001`, `PC-002`).
* Excluded: `mountResidentAppointments` slot-booking internals (`assistant.js:28-179`); `api()` / `loadView()` `503` `Retry-After` backoff (`demo.js:742-750`, Issue #1054); CSS visual theme changes.

### Likely Targets

* `src/api/src/zava_forward/api/resident_demo/web/assistant.js`
* `src/api/src/zava_forward/api/resident_demo/web/demo.js`

### Dependencies

* P01 (`/demo/session` returning `agenda_available`).

### Validation Expectations

* Node fake-DOM execution of `assistant.js` and `demo.js` verifies both `agenda_available: false` and `agenda_available: true` states; `test_epic149_manual_fallback_continuity.py` passes with zero lexical regressions; `web-design-guidelines` review reports zero issues.

### Completion Evidence

* Clean diff in `web/assistant.js` and `web/demo.js` verified by Node fake-DOM tests and continuity checks.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Guard `mountResidentAssistant` manual callback button and notice on `agendaAvailable` in `web/assistant.js`

#### Context

`mountResidentAssistant` builds `notice` (`#assistant-notice`), `callbacks` (`<button type="button" class="secondary">Use the manual callback form</button>`), and returns `{setSession: ...}` (`C10`). `test_epic149_manual_fallback_continuity.py` checks exact source presence of `"Use the manual callback form"`, `"Chat could not load. ... The manual callback form is still available."`, and forbids colour words on lines mentioning `unavailable` or `manual` (`C14`).

#### Intent

Hide the dead `"Use the manual callback form"` button and show an upfront plain-language notice in `ui.intro` (and accurate `#assistant-notice` copy) whenever `agendaAvailable` is `false` (including initial fail-closed boot before session/view state arrives), and restore both when `agendaAvailable` is `true`.

#### Boundaries

* Included: Pre-edit `web-design-guidelines` skill/source load (`PC-004`); `mountResidentAssistant` state (`agendaAvailable = false`, `applyAgendaState`), `ui.intro` fallback paragraph (`callbacksOffNote.hidden = agendaAvailable` AND `callbacksOffNote.textContent = agendaAvailable ? "" : "Synthetic callback booking is not connected in this showcase. Use the contact routes on this page."`, `PC-003`), `notice.textContent`, `response.body.action === "appointments" && agendaAvailable` guard (`assistant.js:276`, `PC-003`), and returned controller methods (`setSession(value, agendaValue)` updating `agendaAvailable` only when `typeof agendaValue === "boolean"`, plus `setAgendaAvailable(value)`, `PC-001`).
* Excluded: Line 185 `ChatWidget` missing-script fallback literal (`"Chat could not load. Reload this page to try again, or contact your housing officer using your usual contact details. The manual callback form is still available."`) which must remain verbatim in source for `test_epic149_manual_fallback_continuity.py` (`C14`).

#### Likely Targets

* `src/api/src/zava_forward/api/resident_demo/web/assistant.js`

#### Dependencies

* None.

#### Validation Expectations

* When `agendaAvailable` is `false`: `callbacks.hidden === true`, `callbacksOffNote.hidden === false` with `callbacksOffNote.textContent === "Synthetic callback booking is not connected in this showcase. Use the contact routes on this page."`, and `notice.textContent` is `"Advisory only. Chat cannot submit forms, give consent or make decisions."`
* When `agendaAvailable` is `true`: `callbacks.hidden === false`, `callbacksOffNote.hidden === true`, `callbacksOffNote.textContent === ""` (so `ui.intro.textContent` contains zero `"not connected"` text), and `notice.textContent` includes `"Callback booking needs your separate confirmation."`
* Calling `setSession(false)` without a second boolean argument preserves the previously synced `agendaAvailable` boolean (`PC-001`).
* All words obey `content-standard.md` (no banned terms or colour cues).

#### Completion Evidence

* Passing Node fake-DOM assertions in `test_resident_callbacks_page.py` and passing `test_epic149_manual_fallback_continuity.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Add defensive `isAgendaAvailable` sync and disabled `#sec-unavailable` item in `web/demo.js`

#### Context

`demo.js` mounts `assistant` at startup (`lines 24-27`), checks `/demo/session` in `start()` (`lines 760-780`), and renders the signed-in view in `render(view, announce)` (`lines 633-706`) (`C8`). Fake test stubs in `test_resident_demo_script.py` and `test_resident_callbacks_page.py` return `{setSession() {}}` (`C13`), and `resident_demo_browser_check.py` asserts every `ul.unavail button` is disabled (`C15`).

#### Intent

Maintain module-scoped `var agendaAvailable = false;` in `demo.js`, resolve `isAgendaAvailable(payload)` (`typeof payload.agenda_available === "boolean" ? payload.agenda_available : Boolean(payload.callbacks_available)`), update `agendaAvailable` from `/demo/session` (before `showSignin`) and `/demo/view`, preserve `agendaAvailable` in `clearPersonal()` (`syncAssistant(false, agendaAvailable)`), use `isAgendaAvailable(view)` in both `actionsSection(view)` and `render(view)`, and append a disabled `"Synthetic callbacks"` item in `#sec-unavailable` (`ul.unavail`) when `!agendaAvailable`.

#### Boundaries

* Included: `agendaAvailable`, `isAgendaAvailable`, `syncAssistant`, `clearPersonal`, `actionsSection`, `showSignin`, `render`, and `start` in `web/demo.js` (`PC-001`, `PC-002`).
* Excluded: `api()` / `loadView()` bulkhead `Retry-After` handling (`demo.js:742-750`).

#### Likely Targets

* `src/api/src/zava_forward/api/resident_demo/web/demo.js`

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* `test_resident_callbacks_page.py` confirms `callbackSections == 0`, `bookingLinks == 0`, `mounts == 0`, disabled `"Synthetic callbacks"` button in `#sec-unavailable` when `agenda_available=False`, and `callbackSections == 1` with zero `"is not connected"` text when `agenda_available=True` (including `callbacks_available`-only fallback).

#### Completion Evidence

* Passing `test_resident_callbacks_page.py` and `test_resident_demo_script.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Regression Tests & Validation Gate

### Context

Repository validation instructions classify small bounded UX/readiness fixes without infra, Dockerfile, manifest, SQL, or workflow changes under the **Focused tier** (owner decision D4 / #1294). Because the worktree shares the environment's editable install pointing at the main checkout, test and typecheck commands in `src/api` must explicitly resolve worktree `src` (`PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src`).

### Intent

Add minimal, high-signal tests that fail without the P01/P02 fixes and verify full Focused-tier compliance (`mypy`, `ruff check`, `ruff format --check`, `web-design-guidelines`, and unit tests).

### Boundaries

* Included: `src/api/tests/test_resident_demo_api.py`, `src/api/tests/test_resident_chat_api.py`, `src/api/tests/test_resident_callbacks_page.py`, and Focused-tier verification commands.
* Excluded: Adding new test files, testing framework/constants trivially, or touching unrelated suites.

### Likely Targets

* `src/api/tests/test_resident_demo_api.py`
* `src/api/tests/test_resident_chat_api.py`
* `src/api/tests/test_resident_callbacks_page.py`

### Dependencies

* P01, P02.

### Validation Expectations

* Refreshed `web-design-guidelines` source review of `src/api/src/zava_forward/api/resident_demo/web/assistant.js` and `src/api/src/zava_forward/api/resident_demo/web/demo.js` reports zero open findings in `file:line` format (`PC-004`).
* `python3 -m mypy` (and `MYPYPATH=../core/src:../agents/src:src python3 -m mypy src tests`) reports `0` issues.
* `python3 -m ruff check . && python3 -m ruff format --check .` exits `0`.
* `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest discover -s tests -p 'test_resident*.py' -v` and continuity/copy/accessibility tests (`test_epic149_manual_fallback_continuity`, `test_content_standard`, `test_accessibility_baseline`) all exit `0`.

### Completion Evidence

* Recorded command outputs, refreshed `web-design-guidelines` `file:line` audit, and zero-error exit statuses in `.copilot-tracking/changes/2026-11-14/issue-1053-resident-demo-agenda-guard-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add focused API, chat, and fake-DOM tests and run `mypy`, `ruff`, `web-design-guidelines`, and `unittest` validation

#### Context

Existing tests in `test_resident_demo_api.py`, `test_resident_chat_api.py`, and `test_resident_callbacks_page.py` already construct real local `ResidentDemo` HTTP instances (with `agenda=None` and `agenda=Agenda(...)`) and execute `demo.js` under Node fake DOM (`C12`, `C13`). Keep existing `demo.js` tests against the `{setSession() {}}` stub to prove backward-compatible stub tolerance, and add a dedicated fake-DOM helper in `test_resident_callbacks_page.py` supplying `document.body` and `getClientRects()` to load real `chat-widget.js` + `assistant.js` + `demo.js` (`PC-003`).

#### Intent

Add `<=5` focused assertions/methods covering `/demo/session` `agenda_available` (signed-out and signed-in), unrouted chat `suggestions()` with `agenda=None`, real `mountResidentAssistant` disconnected vs connected DOM state (including signed-out `agenda_available: true` surviving `showSignin()`/`clearPersonal()`, `PC-001`, `PC-003`), and `demo.js` disabled `#sec-unavailable` item + `callbacks_available`-only fallback across `#sec-actions` and `#sec-help` (`PC-002`), then execute refreshed `web-design-guidelines` (`file:line`), `mypy`, `ruff`, and `unittest` gates (`PC-004`).

#### Boundaries

* Included: Up to 5 focused test additions (`0` removals) in the three existing resident-demo test modules; running `mypy`, `ruff`, and `unittest`.
* Excluded: Creating standalone test files or altering unrelated test fixtures.

#### Likely Targets

* `src/api/tests/test_resident_demo_api.py`
* `src/api/tests/test_resident_chat_api.py`
* `src/api/tests/test_resident_callbacks_page.py`

#### Dependencies

* P01-T01, P02-T01, P02-T02.

#### Validation Expectations

* Every added test case directly exercises new behavior from FR-01..FR-04 and passes alongside all existing resident_demo, continuity, copy, and accessibility suites.

#### Completion Evidence

* Clean test run logs and static analysis checks recorded in the changes artifact.

#### Unresolved Items

* None.
