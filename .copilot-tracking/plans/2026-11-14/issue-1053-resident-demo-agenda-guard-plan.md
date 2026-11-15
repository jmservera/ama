<!-- markdownlint-disable-file -->
# RPI Plan: Issue #1053 Resident Demo Callback Agenda Guard

## Task Metadata

* Task ID: issue-1053
* Task slug: issue-1053-resident-demo-agenda-guard
* Planning status: Ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan-critique.md

## Executive Summary

Complete fail-closed callback agenda availability signaling and honest upfront UX across `ca-resident-demo` (`src/api/src/zava_forward/api/resident_demo/`) so residents and reviewers are never invited to book a synthetic callback or offered a dead callback button when no local callback agenda is connected (`app.agenda is None`). While ancestry commits (`be809739c`, `8c943c9b1`) guarded `/demo/view` and the main-page callback card, four surfaces remain unguarded or incomplete: `GET /demo/session` omits `agenda_available`/`callbacks_available`, the chat widget (`web/assistant.js`) still renders `"Callback booking needs your separate confirmation."` and an active `"Use the manual callback form"` button that silently closes chat onto no target when disconnected, `chat.py` unrouted `suggestions()` still suggests `"Can I find a callback time?"`, and `#sec-unavailable` ("Not available in this showcase") omits a disabled `"Synthetic callbacks"` item when disconnected. Following one-pass plan critique (`PC-001`..`PC-004` applied directly), this plan preserves module-scoped `agendaAvailable` across `clearPersonal()`/`showSignin()`, applies `isAgendaAvailable(view)` across both `actionsSection(view)` and `render(view)`, clears hidden `callbacksOffNote.textContent` when `agendaAvailable` is `true`, passes `callbacks_available=app.agenda is not None` at both `chat.answer(...)` call sites in `app.py`, enforces pre-edit and post-edit `web-design-guidelines` checks, preserves explicit fail-closed `503` behavior on `POST /demo/agenda`, stays completely isolated from Issue #1054 bulkhead concurrency code, and locks focused unit and real `assistant.js` + stub Node fake-DOM tests.

### User Decisions and Requirements Highlights

* Surface callback agenda availability (`agenda_available` / `callbacks_available`) cleanly across `/demo/view` and `/demo/session`, and ensure the client does not invite callback booking (`"You can try synthetic callback booking below"`) or leave dead callback controls active when unconfigured.
* Preserve explicit fail-closed `503` (`"The local callback agenda is not connected."`) on `POST /demo/agenda` when `app.agenda is None`, rather than silently creating an ephemeral SQLite database in HTTP startup.
* Do not touch Issue #1054 bulkhead concurrency code (`MAX_CONCURRENT`, `RETRY_AFTER_SECONDS`, `retryWait` in `app.py:53-79`, `app.py:286-292`, and `demo.js:742-750`).
* Validate in `src/api` under the Focused tier (`mypy`, `ruff check`, `ruff format --check`, `web-design-guidelines` audit, and `resident_demo` + continuity unit suites) and commit cleanly on `feat/ux-1053-agenda-guard-2235` without pushing.

### What You May Not Know

* `test_epic149_manual_fallback_continuity.py` enforces static lexical assertions on `resident_demo/web/assistant.js`, requiring the exact source literals `"Use the manual callback form"` and `"Chat could not load. ... The manual callback form is still available."` and forbidding colour words (`red`, `green`, `amber`) on lines containing `unavailable` or `manual`. Toggling DOM `.hidden` and `.textContent` dynamically while preserving those literals satisfies both runtime honesty and Epic #149 continuity checks.
* Existing Node fake-DOM tests (`test_resident_demo_script.py`, `test_resident_callbacks_page.py`) stub `mountResidentAssistant: () => ({setSession() {}})`, so `demo.js` must pass `agendaAvailable` backward-compatibly via `assistant.setSession(signedIn, agendaAvailable)` and guard any optional `assistant.setAgendaAvailable` call.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Fix Issue #1053 (`fix(resident-demo): signed-in page invites callback booking but live agenda returns 503`) in worktree `/home/azureuser/source/ama-demo-wt/feat-1053-agenda-guard-2235` on branch `feat/ux-1053-agenda-guard-2235` targeting `feat/demo-233-same-home-tensions-0825` (Caller prompt; Issue #1053).
* Surface whether the callback agenda is connected in `/demo/view` and `/demo/session` and update client rendering (`demo.js` / `assistant.js`) so when unconfigured, the page never invites callback booking (`"You can try synthetic callback booking below"`) and hides/disables dead callback controls with an honest upfront notice (Caller prompt; Issue #1053; 2026-11-05 owner closure-review comment).
* Preserve explicit fail-closed `503` behavior on `POST /demo/agenda` when `app.agenda is None`; never implicitly call operator-only `Agenda.create` from HTTP startup (Caller prompt; `agenda.py:52`).
* Avoid touching Issue #1054 bulkhead lines (`MAX_CONCURRENT` / `Retry-After`) in `app.py` and `demo.js` (Caller prompt; Issue #1054).
* Write all four dated RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/`, validate with `mypy`, `ruff check .`, `ruff format --check .`, and `resident_demo` unit tests in `src/api`, and commit cleanly with the Copilot `Co-authored-by` trailer without pushing (Caller prompt).

## Goals

* Ensure `GET /demo/session` and `GET /demo/view` consistently expose boolean `agenda_available` and `callbacks_available` reflecting `app.agenda is not None` without exposing PII.
* Eliminate every remaining unconfigured callback invitation and dead interactive callback control across `web/demo.js`, `web/assistant.js`, and `chat.py` while keeping connected-agenda behavior intact.
* Preserve fail-closed `POST /demo/agenda` (`503`), Epic #149 manual-continuity literals, plain-language vocabulary rules, WCAG 2.2 baseline semantics, and zero diff overlap with Issue #1054 bulkhead code.

## Scope and Non-Goals

### In Scope

* `src/api/src/zava_forward/api/resident_demo/app.py`: include `agenda_available` and `callbacks_available` in `GET /demo/session`; pass `callbacks_available=app.agenda is not None` to `chat.answer(...)` in `POST /demo/assistant`.
* `src/api/src/zava_forward/api/resident_demo/chat.py`: parameterize `suggestions()` and `answer()` with `callbacks_available: bool = True` so `"Can I find a callback time?"` is omitted when `callbacks_available` is `False`.
* `src/api/src/zava_forward/api/resident_demo/web/assistant.js`: default `agendaAvailable = false` (fail-closed) in `mountResidentAssistant`, accept `agendaAvailable` in `setSession(value, agendaValue)` and `setAgendaAvailable(value)`, hide the `"Use the manual callback form"` button and show an upfront plain-language notice in `ui.intro` when `agendaAvailable === false`, and omit the callback-confirmation sentence from `#assistant-notice` when `agendaAvailable === false`.
* `src/api/src/zava_forward/api/resident_demo/web/demo.js`: add `isAgendaAvailable(payload)` (`agenda_available` boolean with fallback to `callbacks_available`, default `false`), sync `assistant` from `/demo/session`, `/demo/view`, and sign-out/sign-in fallback, and render a disabled `"Synthetic callbacks"` item in `#sec-unavailable` ("Not available in this showcase") when `!agendaAvailable`.
* Focused unit and Node fake-DOM tests in `src/api/tests/test_resident_demo_api.py`, `src/api/tests/test_resident_chat_api.py`, and `src/api/tests/test_resident_callbacks_page.py`.

### Non-Goals

* Modifying `MAX_CONCURRENT`, `RETRY_AFTER_SECONDS`, `BUSY`, `_SLOTS`, or `retryWait` bulkhead logic belonging to Issue #1054 (`app.py:53-79`, `app.py:286-292`, `demo.js:742-750`).
* Provisioning cloud storage or changing `infra/resident-demo.bicep`, `Dockerfile`, dependency manifests, SQL views, or GitHub workflows.
* Pushing commits to `origin` or opening/updating a pull request.

## Functional Requirements

* FR-01: `GET /demo/session` returns `"agenda_available": bool` and `"callbacks_available": bool` equal to `app.agenda is not None` for both signed-out and signed-in sessions, matching `GET /demo/view`.
  * Observable acceptance criteria: `test_resident_demo_api.py` verifies `/demo/session` and `/demo/view` return `agenda_available is False` / `callbacks_available is False` when `agenda=None`, and `True` when an `Agenda` instance is wired, while `POST /demo/agenda` still returns `503` when `agenda=None`.
* FR-02: `POST /demo/assistant` and `chat.answer()` / `chat.suggestions()` omit `"Can I find a callback time?"` from unrouted closest-topic suggestions when `callbacks_available` is `False`, while keeping it when `callbacks_available` is `True`.
  * Observable acceptance criteria: `test_resident_chat_api.py` verifies an unrouted visit/time question does not suggest `"Can I find a callback time?"` when `agenda=None`, and still answers direct `"appointments"` topic requests with the explicit not-connected message and `action=None`.
* FR-03: `mountResidentAssistant` in `web/assistant.js` defaults fail-closed (`agendaAvailable = false`), hides the `"Use the manual callback form"` button when `agendaAvailable` is `false`, renders an honest plain-language notice (`"Synthetic callback booking is not connected in this showcase. Use the contact routes on this page."`) in `ui.intro`, updates `#assistant-notice` so it does not imply callback booking is available when disconnected, and restores the button and callback-confirmation notice when `agendaAvailable` is `true`.
  * Observable acceptance criteria: Node fake-DOM tests in `test_resident_callbacks_page.py` verify the chat intro button is hidden and the honest notice is visible when `agenda_available=False`, and the button is visible with no `"not connected"` text when `agenda_available=True`.
* FR-04: `web/demo.js` resolves agenda availability defensively (`agenda_available` boolean, else `Boolean(callbacks_available)`, else `false`), syncs `assistant` on `/demo/session` and `/demo/view` without breaking `{setSession() {}}` stubs, keeps the signed-in lede free of `"You can try synthetic callback booking below"` when disconnected, skips mounting `mountResidentAppointments`, and adds a disabled `"Synthetic callbacks"` item in `#sec-unavailable` explaining that the local callback agenda is not connected and directing the resident to the contact routes above.
  * Observable acceptance criteria: `test_resident_callbacks_page.py` verifies `lede`, `mounts == 0`, `callbackSections == 0`, `bookingLinks == 0`, disabled `"Synthetic callbacks"` button in `#sec-unavailable`, and `callbacks_available`-only fallback behavior.

## Non-Functional Requirements

* NFR-01: Static type safety, lint cleanliness, and formatting compliance in `src/api`.
  * Objective threshold or evaluation condition: `0` mypy errors, `0` ruff lint errors, `0` formatting diffs.
  * Operating condition or verification approach: Run `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/api` against worktree source.
  * Observable acceptance criteria: All three commands exit `0`.
* NFR-02: UX, accessibility, and plain-language content standard conformance.
  * Objective threshold or evaluation condition: Zero violations in `test_epic149_manual_fallback_continuity.py`, `test_content_standard.py`, `test_accessibility_baseline.py`, and `web-design-guidelines` review (`file:line`).
  * Operating condition or verification approach: Preserve Epic #149 source literals in `assistant.js`, avoid colour-only cues and banned glossary terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), keep disabled buttons properly marked (`disabled` + `aria-disabled="true"`), and audit changed JS files against fetched `web-design-guidelines`.
  * Observable acceptance criteria: Continuity/copy/accessibility unit suites exit `0` and `web-design-guidelines` review passes with zero open findings.
* NFR-03: Surgical scope isolation and test discipline.
  * Objective threshold or evaluation condition: Zero modified lines in Issue #1054 bulkhead blocks (`app.py:53-79`, `app.py:286-292`, `demo.js:742-750`); exact test removals `none`; maximum `5` focused test methods added across existing test files; canonical handwritten targets only (zero generated files).
  * Operating condition or verification approach: Verify via `git diff` and targeted `unittest` execution.
  * Observable acceptance criteria: `git diff` touches only planned `resident_demo` and test lines, and all `resident_demo` unit tests pass.

## Acceptance Criteria

* AC-01: `GET /demo/session` and `GET /demo/view` both report `agenda_available: false` and `callbacks_available: false` when `app.agenda is None`, and `true` when `app.agenda` is connected; `POST /demo/agenda` continues to fail closed with `503` (`"The local callback agenda is not connected."`) when `app.agenda is None`.
* AC-02: When `agenda_available` is `false`, the signed-in page does not invite the user with `"You can try synthetic callback booking below"`, does not mount the `"Synthetic callbacks"` form or booking action link, shows honest upfront notices in `#sec-help` and `#sec-unavailable` (disabled `"Synthetic callbacks"` item), hides the dead `"Use the manual callback form"` button inside `#resident-chat`, and does not suggest `"Can I find a callback time?"` on unrouted chat questions.
* AC-03: When `agenda_available` is `true`, the signed-in lede, `"Synthetic callbacks"` form, booking action link, chat `"Use the manual callback form"` button, and callback chat topic work unchanged with no `"is not connected"` copy shown.
* AC-04: Issue #1054 bulkhead concurrency code is untouched; `mypy`, `ruff check .`, `ruff format --check .`, `web-design-guidelines`, and all `resident_demo` + continuity unit tests pass in `src/api`.
* AC-05: All four RPI artifacts exist under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` and all changes are cleanly committed on `feat/ux-1053-agenda-guard-2235` with the Copilot `Co-authored-by` trailer and not pushed.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md                                                         |
| Phase details                    | .copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md                                              |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan-critique.md with Revise disposition (`PC-001`..`PC-004` resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-14/issue-1053-resident-demo-agenda-guard-research.md                                                  |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/issue-1053-resident-demo-agenda-guard-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation                                                                                                    |
| Continuation context             | Confirmed automatic RPI Agent parent return; transitions automatically to `rpi-implement`                                                |

## Sources

* `.copilot-tracking/research/2026-11-14/issue-1053-resident-demo-agenda-guard-research.md`: Primary three-wave research synthesis and evidence log (`C1`-`C17`, `W1`).
* `src/api/src/zava_forward/api/resident_demo/app.py`, `chat.py`, `agenda.py`: Server endpoints (`/demo/session`, `/demo/view`, `/demo/assistant`, `/demo/agenda`) and fail-closed `Agenda` contract.
* `src/api/src/zava_forward/api/resident_demo/web/demo.js`, `web/assistant.js`, `web/index.html`: Client page rendering and chat drawer manual-callback controls.
* `src/api/tests/test_resident_demo_api.py`, `test_resident_callbacks_page.py`, `test_resident_chat_api.py`, `test_epic149_manual_fallback_continuity.py`: Existing HTTP, Node fake-DOM, and static continuity test suites.
* `docs/reference/research/ux/design-system.md`, `wcag-conformance-baseline.md`, `content-standard.md`, and Vercel Web Interface Guidelines (`W1`): UX, accessibility, and plain-language rules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Server Agenda Readiness & Chat Suggestion Guard

* Intent: Expose `agenda_available` and `callbacks_available` consistently on `GET /demo/session` (matching `GET /demo/view`), filter callback search suggestions in `chat.py` when `callbacks_available` is `False`, and preserve fail-closed `503` on `POST /demo/agenda`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Surface `agenda_available` and `callbacks_available` in `GET /demo/session` and guard `chat.py` unrouted suggestions

* Requirement and evidence: FR-01, FR-02 (`C4`, `C5`, `C6`, `C7`, `C9`, `C11`)
* Expected result: `GET /demo/session` includes boolean `agenda_available` and `callbacks_available` (`app.agenda is not None`); `POST /demo/assistant` passes `callbacks_available=app.agenda is not None` at both `chat.answer(...)` call sites (`app.py:474, 491`) so `chat.suggestions()` omits `"Can I find a callback time?"` when disconnected; `POST /demo/agenda` `503` and Issue #1054 bulkhead lines remain untouched.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Client Page & Chat Widget Fail-Closed Agenda Guard

* Intent: Load `web-design-guidelines` and fetch its live rule source before web edits, then propagate agenda availability across `web/demo.js` and `web/assistant.js` (preserving `agendaAvailable` across `clearPersonal()`/`showSignin()` and covering `actionsSection(view)`) so no dead callback buttons or misleading invitations appear when `agenda_available` is `false`, while preserving Epic #149 continuity literals and connected-mode UX.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Guard `mountResidentAssistant` manual callback button and notice on `agendaAvailable` in `web/assistant.js`

* Requirement and evidence: FR-03, NFR-02 (`C10`, `C14`, `C16`, `C17`, `W1`, `PC-001`, `PC-003`, `PC-004`)
* Expected result: With `web-design-guidelines` loaded and fetched prior to edits, `mountResidentAssistant` defaults `agendaAvailable = false`, updates `agendaAvailable` in `setSession(signedIn, agendaValue)` only when `typeof agendaValue === "boolean"` and via `setAgendaAvailable(agendaValue)`, hides `"Use the manual callback form"` and sets `callbacksOffNote.textContent` when `agendaAvailable` is `false` while clearing `callbacksOffNote.textContent = ""` when `true`, guards `response.body.action === "appointments" && agendaAvailable`, omits `"Callback booking needs your separate confirmation."` from `#assistant-notice` when `false`, and preserves all Epic #149 static string literals.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Add defensive `isAgendaAvailable` sync and disabled `#sec-unavailable` item in `web/demo.js`

* Requirement and evidence: FR-04, NFR-02 (`C8`, `C9`, `C13`, `C15`, `W1`, `PC-001`, `PC-002`)
* Expected result: `demo.js` maintains module-scoped `var agendaAvailable = false;` updated from `/demo/session` (before `showSignin`) and `/demo/view` via `isAgendaAvailable(payload)` (`agenda_available` boolean, fallback `Boolean(callbacks_available)`, default `false`), preserves `agendaAvailable` inside `clearPersonal()` (`syncAssistant(false, agendaAvailable)`) without breaking `{setSession() {}}` stubs, uses `isAgendaAvailable(view)` in both `actionsSection(view)` and `render(view)`, renders a disabled `"Synthetic callbacks"` item in `#sec-unavailable` when `!agendaAvailable`, and leaves `api()` / `loadView()` bulkhead retry lines untouched.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Regression Tests & Validation Gate

* Intent: Lock semantic and regression coverage across API, chat, and Node fake-DOM suites (exercising both legacy `{setSession() {}}` stubs and real `chat-widget.js` + `assistant.js` DOM behavior) and pass Focused-tier static, lint, refreshed `web-design-guidelines` (`file:line`), and unit checks in `src/api`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add focused API, chat, and fake-DOM tests and run `mypy`, `ruff`, `web-design-guidelines`, and `unittest` validation

* Requirement and evidence: FR-01..FR-04, NFR-01..NFR-03, AC-01..AC-04 (`C12`, `C13`, `C14`, `C15`, `C16`, `C17`, `PC-001`, `PC-003`, `PC-004`)
* Expected result: Up to 5 focused test additions across `test_resident_demo_api.py`, `test_resident_chat_api.py`, and `test_resident_callbacks_page.py` (`0` removals, including real `chat-widget.js` + `assistant.js` fake-DOM execution with `document.body` and `getClientRects()` plus signed-out `agenda_available: true` preservation) fail without the fix and pass with it; refreshed `web-design-guidelines` `file:line` review of `web/assistant.js` and `web/demo.js`, `mypy`, `ruff check .`, `ruff format --check .`, and all `resident_demo` + continuity/copy/accessibility unit suites pass cleanly.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md

## Dependencies

* Python 3.12 toolchain (`mypy`, `ruff`, `unittest`) and Node.js (`node -e` fake-DOM harness already used by `test_resident_demo_script.py` and `test_resident_callbacks_page.py`): required for local Focused-tier verification in `src/api`.
* `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src`: required when running `unittest` (and `MYPYPATH` / `src tests` target check) inside the git worktree so worktree edits in `src/api/src` take precedence over the main checkout's editable install.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 (`Revise`): `PC-001` (Medium) — `clearPersonal()` overwriting `/demo/session` `agenda_available: true` | resolved | Updated `P02`, `P02-T01`, `P02-T02`, and `P03-T01`: `demo.js` retains module-scoped `var agendaAvailable = false;` across `clearPersonal()` (`syncAssistant(false, agendaAvailable)`), and `assistant.setSession(value, agendaValue)` updates `agendaAvailable` only when `typeof agendaValue === "boolean"`. |
| Run 1 (`Revise`): `PC-002` (Medium) — `actionsSection(view)` omitted from `P02-T02` `isAgendaAvailable(view)` scope | resolved | Updated `P02` and `P02-T02` boundaries to include `actionsSection(view)` (`demo.js:552-573`) using `isAgendaAvailable(view)` so `callbacks_available`-only payloads preserve `"Book a synthetic callback"` parity. |
| Run 1 (`Revise`): `PC-003` (Low) — hidden `callbacksOffNote.textContent` leakage and stubbed `assistant.js` in `test_resident_callbacks_page.py` | resolved | Updated `P02-T01` to clear `callbacksOffNote.textContent = ""` when `agendaAvailable` is `true` and guard `action === "appointments" && agendaAvailable`; updated `P03-T01` to wire `document.body` and `getClientRects()` in a dedicated real `chat-widget.js` + `assistant.js` fake-DOM test helper alongside the existing `{setSession() {}}` stub test. |
| Run 1 (`Revise`): `PC-004` (Low) — explicit `web-design-guidelines` pre-edit load/fetch and post-edit `file:line` review steps | resolved | Updated `P02`/`P02-T01` with pre-edit `web-design-guidelines` skill/source requirement and `P03`/`P03-T01` with refreshed post-edit `file:line` review recorded in the changes artifact. |
| Residual risk: static missing-`ChatWidget` fallback string (`assistant.js:185`) | accepted with risk | Kept verbatim (`"The manual callback form is still available."`) to satisfy `test_epic149_manual_fallback_continuity.py:67-72`; affects only catastrophic script-bundle load failure prior to JS initialization. |

## Follow-Up Items

* Issue #1054 (`MAX_CONCURRENT = 8` / `Retry-After` contention on `GET /demo/view` in `ca-resident-demo`): explicitly out of scope per caller instructions; tracked separately on its dedicated branch/issue.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/issue-1053-resident-demo-agenda-guard-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none
