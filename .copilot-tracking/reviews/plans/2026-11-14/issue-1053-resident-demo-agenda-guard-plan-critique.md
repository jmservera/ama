<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue 1053 Resident Demo Callback Agenda Availability Guard

## Metadata

* Task ID: issue-1053
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Issue #1053 (`fix(resident-demo): signed-in page invites callback booking but live agenda returns 503`) on branch `feat/ux-1053-agenda-guard-2235` targeting `feat/demo-233-same-home-tensions-0825`. Surface callback agenda connectivity in `/demo/view` and `/demo/session`, update client rendering (`web/demo.js`, `web/assistant.js`) and chat suggestions (`chat.py`) so unconfigured instances (`app.agenda is None`) never invite callback booking, hide or disable dead callback controls with an honest upfront notice, preserve explicit fail-closed `503` behavior on `POST /demo/agenda`, leave Issue #1054 bulkhead concurrency controls untouched (`MAX_CONCURRENT`, `RETRY_AFTER_SECONDS`, `BUSY`, `app.slots`, `_route` in `app.py:53-79`, `app.py:286-292`, and `loadView` `503` backoff in `demo.js:742-750`), and validate in `src/api` with `mypy`, `ruff check .`, `ruff format --check .`, `web-design-guidelines`, and `resident_demo` plus continuity unit tests.
* Research and evidence considered: `.copilot-tracking/research/2026-11-14/issue-1053-resident-demo-agenda-guard-research.md` (`C1` through `C17`, `W1`), `.copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md`, `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md`, `src/api/src/zava_forward/api/resident_demo/app.py`, `src/api/src/zava_forward/api/resident_demo/chat.py`, `src/api/src/zava_forward/api/resident_demo/web/demo.js`, `src/api/src/zava_forward/api/resident_demo/web/assistant.js`, `src/api/src/zava_forward/api/resident_demo/web/index.html`, `src/api/src/zava_forward/api/web/chat-widget.js`, `src/core/src/zava_forward/core/resident_showcase.py`, `src/api/tests/test_resident_demo_api.py`, `src/api/tests/test_resident_chat_api.py`, `src/api/tests/test_resident_callbacks_page.py`, `src/api/tests/test_epic149_manual_fallback_continuity.py`, `src/api/tests/test_resident_demo_script.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_accessibility_baseline.py`, and `src/api/checks/resident_demo_browser_check.py`.
* Decisions, dependencies, and acceptance criteria considered: `FR-01` through `FR-04`, `NFR-01` through `NFR-03`, `AC-01` through `AC-05`, sequential dependencies `P01` (`P01-T01`) -> `P02` (`P02-T01` -> `P02-T02`) -> `P03` (`P03-T01`), Focused validation tier classification (owner decision D4 / Issue #1294), Epic #149 static source invariants (`C14`), plain-language and WCAG constraints (`C15`, `C16`), and Issue #1054 bulkhead non-interference (`NFR-01`).
* Assessment boundary: Evaluates plan and phase-detail completeness, code-path accuracy, boundary locks, static/runtime test invariants, and validation coverage against current workspace sources without modifying plan, phase details, or codebase files, and without querying live Azure deployments beyond `W1` recorded in the research artifact.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `FR-01`, `AC-01`, `C1`..`C3`, `C6` | Covered | `P01-T01` adds `agenda_available` and `callbacks_available` booleans (`app.agenda is not None`) to `GET /demo/session` (`app.py:322-335`) matching `ResidentDemo.view_for()` (`app.py:194-202`) while keeping `POST /demo/agenda` fail-closed `503` (`app.py:556-567`) untouched. |
| `FR-02`, `AC-02`, `C5`, `C10`, `C11`, `P01`, `P01-T01` | Covered | `P01-T01` adds `callbacks_available: bool = True` to `chat.suggestions()` and `chat.answer()` (`chat.py:606-617`, `632-729`), honors `view.get("agenda_available")` when `answer()` is called directly with a `view` dict, and explicitly passes `callbacks_available=app.agenda is not None` at both `chat.answer(...)` call sites in `app.py:_assistant()` (`app.py:474`, `491`) where `rs.showcase_view(...)` lacks `agenda_available`. |
| `FR-03`, `AC-02`, `C8`, `C9`, `C14`, `P02-T01` | Partial | `P02-T01` preserves Epic #149 literals in `web/assistant.js` (`lines 185, 224`), updates `#assistant-notice`, hides the dead button, and renders an upfront plain-language notice when disconnected, but does not preserve `agendaAvailable` when `setSession(signedIn)` is called without a boolean second argument (`PC-001`) or clear hidden `callbacksOffNote.textContent` when `agendaAvailable` becomes `true` (`PC-003`). |
| `FR-04`, `AC-03`, `C4`, `C12`, `C13`, `P02-T02` | Partial | `P02-T02` adds the disabled `"Synthetic callbacks"` item in `#sec-unavailable` (`demo.js:673-687`) and guards optional `assistant` methods, but `start()` -> `showSignin()` -> `clearPersonal()` resets `/demo/session` `agenda_available: true` back to `false` (`PC-001`), and `actionsSection(view)` (`demo.js:552-573`) is omitted from `P02-T02` boundaries so `callbacks_available`-only payloads omit `"Book a synthetic callback"` (`PC-002`). |
| `NFR-01` (Issue #1054 bulkhead isolation) | Covered | Target ranges in `app.py` (`322-335`, `467-498`) and `demo.js` (`24-81`, `552-573`, `633-706`, `714-729`, `760-791`) are completely disjoint from `MAX_CONCURRENT`, `BUSY`, `RETRY_AFTER_SECONDS`, `_route` (`app.py:53-79`, `285-292`), and `loadView` `503` retry backoff (`demo.js:740-758`). |
| `NFR-02`, `AC-04`, `C14`..`C17`, `P03`, `P03-T01` | Partial | Planned copy avoids banned register terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) and colour words (`red`, `green`, `amber`), and Python test selectors are accurate, but `test_resident_callbacks_page.py` currently stubs `mountResidentAssistant` and lacks `document.body`/`getClientRects()` for real `assistant.js` execution (`PC-003`), and `P02`/`P03-T01` omit explicit `web-design-guidelines` pre-edit load/fetch and post-edit `file:line` review steps (`PC-004`). |
| `NFR-03`, `AC-05` | Covered | Commit, branch, privacy-safe `gh api user` author/committer email, no-push boundary, and four-artifact `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` deliverables match caller constraints. |

## Verdict

* Verdict: Revise
* Rationale: Architecture, server API/chat wiring (`P01-T01`), Epic #149 continuity preservation, and Issue #1054 bulkhead isolation are sound, but four concrete task-detail gaps across `P02` and `P03` (`PC-001` through `PC-004`) would cause signed-out sessions to lose `/demo/session` `agenda_available: true`, break `callbacks_available`-only fallback parity in `actionsSection(view)`, leak hidden `"not connected"` text or leave `assistant.js` stubbed in `test_resident_callbacks_page.py`, and under-specify mandatory `web-design-guidelines` execution steps. All four are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Signed-out and sign-out clearPersonal() flow in demo.js overwrites GET /demo/session agenda_available: true back to false

* Related IDs: `FR-01`, `FR-03`, `FR-04`, `AC-01`, `AC-03`, `C6`, `C9`, `C13`, `P02`, `P02-T01`, `P02-T02`
* Evidence: `src/api/src/zava_forward/api/resident_demo/web/demo.js:73-81`, `714-729`, `769-781`; `src/api/src/zava_forward/api/resident_demo/web/assistant.js:303-319`; `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md:174-184`, `208-224`
* Concern: In `demo.js:769-781`, when `GET /demo/session` returns `{ signed_in: false, agenda_available: true }`, `start()` invokes `showSignin(pendingNotice || undefined)` (`line 779`), which invokes `clearPersonal()` (`line 715`), which invokes `assistant.setSession(false)` (`line 77`). The same `showSignin(...)` -> `clearPersonal()` path runs on sign-out, `401` session expiry, and `BroadcastChannel` tab changes (`demo.js:88-90`). Neither `P02-T01` nor `P02-T02` specifies preserving the known server `agendaAvailable` flag across `clearPersonal()` or ignoring `undefined` `agendaValue` in `assistant.setSession(value, agendaValue)`. If `start()` syncs `/demo/session` before `showSignin()` and `clearPersonal()` resets `agendaAvailable` to `false` (or calls `setSession(false)` where `Boolean(undefined)` becomes `false`), `showSignin()` immediately clobbers `agenda_available: true` back to `false` on every signed-out load.
* Impact: Signed-out visitors on a connected showcase (`app.agenda` configured, where `"Use the manual callback form"` legitimately focuses `#email` via `assistant.js:235`) would see the chat drawer falsely hide the button and report `"Synthetic callback booking is not connected in this showcase"`, defeating `FR-01` for signed-out sessions.
* Smallest useful change: Specify in `P02-T01` that `assistant.setSession(value, agendaValue)` only updates `agendaAvailable` when `typeof agendaValue === "boolean"` (defaulting initial module state to `false` until synced), and specify in `P02-T02` (including `clearPersonal` in `P02`/`P02-T02` boundaries) that `demo.js` retains module-scoped `var agendaAvailable = false;` updated from `/demo/session` (before `showSignin`) and `/demo/view`, with `clearPersonal()` calling `syncAssistant(false, agendaAvailable)`.
* Action owner: `planning_parent`
* Exact resolving evidence: Updated `P02`, `P02-T01`, and `P02-T02` specifications in `.copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md` and `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md` explicitly preserving `agendaAvailable` across `clearPersonal()`/`showSignin()` and guarding `typeof agendaValue === "boolean"` in `assistant.setSession`, paired with a signed-out `agenda_available: true` assertion in `P03-T01`.
* Decision route: `direct_planner_correction`

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: P02 and P02-T02 omit actionsSection(view) in demo.js, breaking callbacks_available fallback parity on #sec-actions

* Related IDs: `FR-04`, `AC-03`, `C4`, `P02`, `P02-T02`
* Evidence: `src/api/src/zava_forward/api/resident_demo/web/demo.js:552-573` (`if (view.agenda_available)` at `line 564`), `641`, `652`, `683`, `690`; `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md:150`, `208-235`
* Concern: `P02` and `P02-T02` require `isAgendaAvailable(payload)` to honor `agenda_available` with fallback to `callbacks_available` (`FR-04`) and explicitly expect `callbacks_available`-only payloads to pass validation (`phase-details.md:235`), yet `P02` (`line 150`) and `P02-T02` (`line 223`) restrict `demo.js` boundaries to `isAgendaAvailable, syncAssistant, showSignin, render, and start`, omitting `actionsSection(view)` (`demo.js:552-573`). `actionsSection(view)` is a separate top-level helper that checks `if (view.agenda_available)` directly (`demo.js:564`) to emit the `"Book a synthetic callback"` anchor (`bookingLinks`).
* Impact: For a `callbacks_available: true` fallback payload lacking `agenda_available`, `render(view)` mounts the callback section while `actionsSection(view)` omits `"Book a synthetic callback"` (`bookingLinks === 0`), producing an inconsistent signed-in page and failing `FR-04` / `P02-T02` fallback validation.
* Smallest useful change: Include `actionsSection` in `P02` and `P02-T02` `demo.js` boundaries and specify replacing direct `view.agenda_available` reads in both `actionsSection(view)` (`line 564`) and `render(view)` (`lines 641, 683, 690`) with `isAgendaAvailable(view)`.
* Action owner: `planning_parent`
* Exact resolving evidence: Updated `P02` and `P02-T02` boundaries and description in `.copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md` and `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md` covering `actionsSection(view)` alongside `render(view)`.
* Decision route: `direct_planner_correction`

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Hidden callbacksOffNote textContent leakage and stubbed mountResidentAssistant harness in test_resident_callbacks_page.py

* Related IDs: `FR-03`, `FR-04`, `AC-02`, `AC-03`, `AC-04`, `C8`, `C9`, `C13`, `C17`, `P02-T01`, `P03-T01`
* Evidence: `src/api/tests/test_resident_callbacks_page.py:21-58`; `src/api/src/zava_forward/api/web/chat-widget.js:57`; `src/api/src/zava_forward/api/resident_demo/web/assistant.js:224-239`, `276`; `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md:174-200`, `270-297`
* Concern: Two coupled DOM/test-harness details are underspecified between `P02-T01` and `P03-T01`:
  1. Both standard browser `Node.textContent` and `Node_.textContent` in `test_resident_callbacks_page.py:26` (`this._text + this.children.map(c => c.textContent).join("")`) include text inside `hidden = true` children. If `P02-T01` sets static text on `callbacksOffNote` at mount time and `applyAgendaState()` only toggles `callbacksOffNote.hidden = agendaAvailable`, then `ui.intro.textContent` still contains `"not connected"` when `agendaAvailable === true`, contradicting `FR-03` (`no 'not connected' text when agenda_available=True`). In addition, `assistant.js:276` checks `if (response.body.action === "appointments")` without a defensive `&& agendaAvailable` client guard.
  2. `test_resident_callbacks_page.py:49-58` currently stubs `window.mountResidentAssistant = () => ({setSession() {}})` without loading `chat-widget.js` or `assistant.js`, and its fake DOM omits `document.body` (required by `chat-widget.js:57`) and `Node_.getClientRects()` (required by `assistant.js:237`), while mocking `/demo/session` without `agenda_available`.
* Impact: Without clearing `callbacksOffNote.textContent` when `agendaAvailable === true` and specifying how `test_resident_callbacks_page.py` tests both the legacy `{setSession() {}}` stub and real `chat-widget.js` + `assistant.js` execution, `P03-T01` will either fail `textContent` / `TypeError` checks under Node or leave `assistant.js` unexercised behind the existing stub.
* Smallest useful change: In `P02-T01`, specify that `applyAgendaState()` sets both `callbacksOffNote.hidden = agendaAvailable` and `callbacksOffNote.textContent = agendaAvailable ? "" : "Synthetic callback booking is not connected in this showcase. Use the contact routes on this page."`, plus `if (response.body.action === "appointments" && agendaAvailable)` at `assistant.js:276`. In `P03-T01`, specify keeping existing `demo.js` tests against the `{setSession() {}}` stub (proving `FR-04` optional-method compatibility) and adding a dedicated helper in `test_resident_callbacks_page.py` that provides `document.body` and `getClientRects()` on `Node_` and loads `chat-widget.js` + `assistant.js` to assert `#assistant-notice`, button `hidden` state, and `callbacksOffNote` across `agendaAvailable` `false` and `true` (signed-out and signed-in).
* Action owner: `planning_parent`
* Exact resolving evidence: Updated `P02-T01` and `P03-T01` details in `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md` specifying dynamic `callbacksOffNote.textContent` clearing, defensive `action === "appointments" && agendaAvailable` guarding, and fake-DOM harness wiring for real `chat-widget.js` + `assistant.js` alongside the legacy `{setSession() {}}` stub test.
* Decision route: `direct_planner_correction`

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Task execution and P03-T01 validation steps omit mandatory web-design-guidelines pre-edit load/fetch and post-edit file:line review evidence

* Related IDs: `NFR-02`, `AC-04`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`
* Evidence: `.copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md:107-108`, `184-208`; `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md:162`, `245`, `259-297`; `.github/copilot-instructions.md` (`Web Development Guidance`)
* Concern: Repository `Web Development Guidance` and caller requirements mandate loading the `web-design-guidelines` skill and fetching its current source before editing web files (`web/assistant.js`, `web/demo.js`), then refreshing and reviewing the changed web files against all fetched rules in `file:line` format (or explicitly disclosing any failed/unavailable fetch without claiming conformance). Although `NFR-02`, `P02` (`line 162`), and `P03` Intent (`line 245`) mention `web-design-guidelines`, `P02-T01`, `P02-T02`, `P03` Validation Expectations (`lines 259-263`), and `P03-T01` (`lines 270-297`) omit the pre-edit skill/source load and the post-edit `file:line` audit artifact step.
* Impact: An implementer following `P02-T01` -> `P02-T02` -> `P03-T01` task-by-task could edit `assistant.js` and `demo.js` before loading `web-design-guidelines` or omit the refreshed `file:line` audit evidence from `.copilot-tracking/changes/2026-11-14/issue-1053-resident-demo-agenda-guard-changes.md`, failing repository review expectations.
* Smallest useful change: Add explicit pre-edit `web-design-guidelines` skill activation and source fetch to `P02` / `P02-T01` prerequisites, and add refreshed `web-design-guidelines` review of `src/api/src/zava_forward/api/resident_demo/web/assistant.js` and `src/api/src/zava_forward/api/resident_demo/web/demo.js` with `file:line` findings (or explicit fetch-blocker disclosure) to `P03` and `P03-T01` Validation Expectations.
* Action owner: `planning_parent`
* Exact resolving evidence: Updated `P02`/`P02-T01` and `P03`/`P03-T01` steps in `.copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md` and `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md` specifying pre-edit `web-design-guidelines` load/fetch and post-edit `file:line` audit recording.
* Decision route: `direct_planner_correction`

## Strengths and Residual Risk

* Strong ancestry awareness and minimal blast radius: The plan accurately recognizes what commits `be809739c` and `8c943c9b1` already guard (`ResidentDemo.view_for()`, `POST /demo/agenda` `503`, `POST /demo/assistant` `appointments` topic refusal, and main signed-in card/nav/lede guards in `demo.js`) and targets only the four remaining surfaces (`/demo/session`, `chat.py` unrouted suggestions, `assistant.js` drawer intro/notice, and `demo.js` `#sec-unavailable` + session sync).
* Accurate server-to-chat dataflow catch: `P01-T01` correctly identifies that `app.py:_assistant()` builds `view` from `rs.showcase_view(row, app.now())` (`app.py:445`) rather than `app.view_for(...)`, and therefore passes `callbacks_available=app.agenda is not None` explicitly at both `chat.answer(...)` call sites (`app.py:474`, `491`).
* Continuity, content-standard, and bulkhead safety: Preserving `"Use the manual callback form"` (`assistant.js:224`) and the `Chat could not load.` alert literal (`assistant.js:185`) satisfies `test_epic149_manual_fallback_continuity.py` (`C14`), all proposed strings avoid banned register terms and colour words (`C15`, `C16`), and all planned edit hunks are disjoint from Issue #1054 bulkhead semaphore/retry ranges (`NFR-01`).
* Accepted residual risk: When `window.ChatWidget?.create` itself fails to load (`assistant.js:184-189`), the static fallback alert string retains `"The manual callback form is still available."` verbatim in source to satisfy `test_epic149_manual_fallback_continuity.py:67-72`; this narrow script-load-failure edge is documented in `C14` and `P02-T01` Boundaries.

## Questions or Blocking Evidence Gaps

* None. All four findings are deterministic code-contract and validation-specification gaps resolvable directly by the planning parent from workspace evidence without user input.

## Limitations

* Live deployed `ca-resident-demo` behavior (`W1`) was evaluated from the recorded research evidence rather than re-probing Azure during read-only plan critique.
* Full local RPI receipt (`tools/rpi-checks.py --all`) and Playwright browser runs were not executed during plan critique; Focused-tier classification is verified against repository instructions (`D4` / Issue #1294) because the scoped edits touch only resident showcase session/chat/UI presentation without altering schemas, auth/session crypto, bulkhead limits, Dockerfiles, dependencies, workflows, or security gates.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Apply direct planner revisions for `PC-001`, `PC-002`, `PC-003`, and `PC-004` to `.copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md` and `.copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md`, then finalize the plan as `Ready` without another critique pass.
* User response required: no
