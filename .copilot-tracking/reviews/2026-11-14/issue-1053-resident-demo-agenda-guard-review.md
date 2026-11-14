<!-- markdownlint-disable-file -->
# Review: Issue #1053 Resident Demo Callback Agenda Guard

## Scope and Evidence

* Task ID: issue-1053
* Review date: 2026-11-14
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: `FR-01`..`FR-04`, `NFR-01`..`NFR-03`, and `AC-01`..`AC-05` covering `GET /demo/session` and `GET /demo/view` callback readiness parity, `POST /demo/assistant` unrouted callback suggestion filtering, `POST /demo/agenda` fail-closed `503` preservation, `web/assistant.js` and `web/demo.js` fail-closed callback UX, Issue #1054 bulkhead non-interference, Focused-tier local validation in `src/api`, and local branch commit hygiene on `feat/ux-1053-agenda-guard-2235`.
* Plan: .copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-1053-resident-demo-agenda-guard-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/issue-1053-resident-demo-agenda-guard-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/issue-1053-resident-demo-agenda-guard-research.md (`C1`-`C17`, `W1`), `git diff` across `src/api/`, refreshed `web-design-guidelines` rules (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`), and local `mypy`, `ruff`, and `unittest` execution outputs.

## Opening Review State

* Interpreted review goal: Verify once against concrete diff, artifact, and test evidence that Issue #1053's implementation closes every unconfigured callback agenda UX invitation across `resident_demo` while preserving connected-mode behavior, fail-closed `POST /demo/agenda` `503`, Epic #149 manual-fallback continuity, UX/WCAG/plain-language rules, and Issue #1054 scope isolation.
* Review scope: full task (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`)
* Evidence readiness: Ready; research, plan, phase details, one-pass plan critique (`PC-001`..`PC-004`), reconciled changes record, and source/test diff are all present and synchronized.
* Acceptance basis: `FR-01`..`FR-04`, `NFR-01`..`NFR-03`, `AC-01`..`AC-05`, critique dispositions `PC-001`..`PC-004`, and Focused-tier validation rules (owner decision D4 / issue #1294).
* First comparison boundary: Plan checklist markers, phase details, critique dispositions, and changes record against `git diff` in `src/api/`; hosted CI and PR human review are outside the local unpushed boundary (`Do NOT push`).
* Active read-only boundaries: Read-only comparison across source, tests, research, plan, details, critique, and changes artifacts; write authority restricted strictly to this canonical review artifact and parent RPI state JSON.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass review on 2026-11-14 across all 7 modified source/test files in `src/api/` and all 5 tracking artifacts for `issue-1053`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | `P01 (P01-T01): Server Agenda Readiness & Chat Suggestion Guard` | Reconciled | Checked off in plan; matches `app.py` (`/demo/session` flags and both `_assistant` `chat.answer` sites) and `chat.py` (`suggestions` + `answer`). |
| `P02` / `P02-T01` | `P02 (P02-T01, P02-T02): Client Page & Chat Widget Fail-Closed Agenda Guard` | Reconciled | Checked off in plan; matches `web/assistant.js` fail-closed `agendaAvailable`, `setSession(value, agendaValue)` / `setAgendaAvailable(value)`, cleared hidden `callbacksOffNote.textContent`, `action === "appointments" && agendaAvailable` guard, and preserved Epic #149 strings. |
| `P02` / `P02-T02` | `P02 (P02-T01, P02-T02): Client Page & Chat Widget Fail-Closed Agenda Guard` | Reconciled | Checked off in plan; matches `web/demo.js` `isAgendaAvailable(payload)`, `actionsSection(view)` + `render(view)` gating, `clearPersonal()` state preservation, and disabled `"Synthetic callbacks"` item in `#sec-unavailable`. |
| `P03` / `P03-T01` | `P03 (P03-T01): Focused Regression Tests & Validation Gate` | Reconciled | Checked off in plan; `+5` focused test methods (`0` removals) across `test_resident_demo_api.py`, `test_resident_chat_api.py`, and `test_resident_callbacks_page.py`, with passing `mypy`, `ruff`, `unittest`, and refreshed `web-design-guidelines` review. |
| `Follow-Up Items` | `Follow-Up Items` (Issue #1054 bulkhead contention; optional synthetic agenda deployment wiring) | Reconciled | Kept outside active `Pxx` / `Pxx-Txx` scope and untouched in `git diff`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/src/zava_forward/api/resident_demo/app.py`, `src/api/src/zava_forward/api/resident_demo/chat.py` | Exposed `agenda_available` and `callbacks_available` on `GET /demo/session`; passed `callbacks_available=app.agenda is not None` at both `_assistant` `chat.answer` call sites; filtered `"appointments"` example out of `chat.suggestions` when disconnected while preserving `POST /demo/agenda` `503`. | `git diff` on `app.py` and `chat.py`; `SignInTests` and `ChatApiTests` assertions. | Passed (`mypy`, `ruff`, `test_resident_demo_api`, `test_resident_chat_api`, `test_resident_chat_agenda`). | Reconciled; satisfies `FR-01`, `FR-02`, `AC-01`, `AC-02`. |
| `P02-T01` | `src/api/src/zava_forward/api/resident_demo/web/assistant.js` | Defaulted `agendaAvailable = false`; hid `"Use the manual callback form"` and `"Find callback times in the manual form"` when disconnected; rendered upfront `#assistant-callbacks-note` (clearing `.textContent` when connected); omitted callback-confirmation sentence from `#assistant-notice` when disconnected; preserved Epic #149 literals. | `git diff` on `web/assistant.js`; real `chat-widget.js` + `assistant.js` Node fake-DOM tests and continuity audit. | Passed (`test_resident_callbacks_page`, `test_epic149_manual_fallback_continuity`, `test_content_standard`, refreshed `web-design-guidelines`). | Reconciled; satisfies `FR-03`, `NFR-02`, `AC-02`, `AC-03`, `PC-001`, `PC-003`, `PC-004`. |
| `P02-T02` | `src/api/src/zava_forward/api/resident_demo/web/demo.js` | Added module-scoped `agendaAvailable` + `isAgendaAvailable(payload)` (`agenda_available` boolean, fallback `Boolean(callbacks_available)`, default `false`); preserved `agendaAvailable` across `clearPersonal()` / `showSignin()` after `/demo/session`; gated `actionsSection(view)` and `render(view)`; rendered disabled `"Synthetic callbacks"` entry in `#sec-unavailable` when disconnected. | `git diff` on `web/demo.js`; legacy stub and real-assistant Node fake-DOM tests. | Passed (`test_resident_callbacks_page`, `test_resident_demo_script`, `test_accessibility_baseline`, refreshed `web-design-guidelines`). | Reconciled; satisfies `FR-04`, `NFR-02`, `NFR-03`, `AC-02`, `AC-03`, `PC-001`, `PC-002`. |
| `P03-T01` | `src/api/tests/test_resident_demo_api.py`, `src/api/tests/test_resident_chat_api.py`, `src/api/tests/test_resident_callbacks_page.py` | Added 5 focused regression/semantic tests (`1` API, `1` chat, `3` Node fake-DOM) with `0` test removals, locking both unconfigured and connected states plus `callbacks_available` fallback. | `git diff` across 3 test files (`+5` test methods, `0` removals) and full Focused-tier test run. | Passed (`171` core resident/continuity/copy/WCAG tests `OK`; `227`-test extended resident run passed with `8` expected SQL skips). | Reconciled; satisfies `NFR-01`..`NFR-03`, `AC-01`..`AC-04`. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P03-T01` (`test_resident_chat_api.py`) | Local judgment in test assertion: verified `advisor.answer_question.assert_not_called()` when `topic == "unknown"` with `assistant_advisor` configured, plus direct `chat.answer("unknown", {"agenda_available": False}, question)` coverage, because `app.py:_assistant()` intentionally restricts `assistant_advisor.answer_question` to routed topics (`Topic`, `"home"`, `"repair"`). | Code inspection of `app.py:_assistant()` and `unittest` execution; no user decision needed because production behavior already matched approved design. | Recorded under `## Implementation-Time Plan and Detail Updates` in changes artifact; both `chat.answer(...)` call sites in `app.py` remain guarded. | Not material; existing plan and one-pass critique (`PC-001`..`PC-004`) remain valid without revision. | Reconciled and intent-preserving. |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four critique findings (`PC-001`..`PC-004`) in `.copilot-tracking/reviews/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan-critique.md` have explicit planner dispositions in `.copilot-tracking/plans/2026-11-14/issue-1053-resident-demo-agenda-guard-plan.md` (`## Critique Disposition`) and are verified in the shipped code and tests:
  * `PC-001`: `demo.js` preserves `agendaAvailable` across `clearPersonal()` / `showSignin()`, and `assistant.js` updates `agendaAvailable` in `setSession` only when `typeof agendaValue === "boolean"`, proven by `test_connected_agenda_enables_assistant_manual_callback_button_even_when_signed_out`.
  * `PC-002`: `actionsSection(view)` uses `isAgendaAvailable(view)`, proven by `test_callbacks_available_fallback_supports_payload_without_agenda_available`.
  * `PC-003`: `assistant.js` clears `callbacksOffNote.textContent = ""` when connected and guards `response.body.action === "appointments" && agendaAvailable`, proven with real `chat-widget.js` + `assistant.js` in `test_resident_callbacks_page.py`.
  * `PC-004`: Both `chat.answer(...)` call sites in `app.py:_assistant()` pass `callbacks_available=app.agenda is not None`, and `web-design-guidelines` was loaded/fetched pre-edit and refreshed pre-review with `file:line` results recorded.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No dependent work required pausing; execution proceeded cleanly in `P01` -> `P02` -> `P03` order.
* Justification assessment: Supported by direct code, diff, and test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Issue #1054: `MAX_CONCURRENT = 8` / `Retry-After` bulkhead contention on `GET /demo/view` in `ca-resident-demo` | Caller explicitly instructed not to touch files/blocks belonging to #1054 (`MAX_CONCURRENT` / `Retry-After` bulkhead logic). | Tracked under Issue #1054 in dedicated workstream. | Open external issue; verified zero lines touched in `app.py:53-79`, `app.py:286-292`, or `demo.js:742-750`; routed as distinct follow-up. |
| Optional deployment-time synthetic SQLite callback agenda (`ZF_RESIDENT_AGENDA_PATH`) in `infra/resident-demo.bicep` | Product/deployment choice noted in Issue #1053 owner comment (2026-11-05); infrastructure/Bicep edits would escalate validation tier and alter live container storage posture beyond the requested UX guard. | Product owner / infra follow-up if interactive synthetic slot booking is desired in live `ca-resident-demo`. | Non-blocking optional enhancement; fail-closed UX contract is complete without it; routed as distinct follow-up. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material or minor implementation defects, decision gaps, or evidence gaps were found within the Issue #1053 task boundary (`0` `RV-xxx` defect entries).

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Hosted CI and PR human review remain post-push gates on `feat/ux-1053-agenda-guard-2235`

* Related scope: `P03` (publication/CI boundary outside local unpushed commit)
* Evidence: `.copilot-tracking/changes/2026-11-14/issue-1053-resident-demo-agenda-guard-changes.md` (`## Validation Record`); caller instruction `Commit all changes cleanly on feat/ux-1053-agenda-guard-2235 ... Do NOT push.`
* Impact: All Focused-tier local checks (`mypy`, `ruff check`, `ruff format --check`, 171+ unit tests, refreshed `web-design-guidelines` review) passed, while hosted GitHub Actions CI and independent PR human review cannot run until the branch is pushed and opened/updated against `feat/demo-233-same-home-tensions-0825`.
* Destination: follow_up (branch push / PR publication owner)
* Smallest useful next action: When ready to publish `feat/ux-1053-agenda-guard-2235` into `feat/demo-233-same-home-tensions-0825`, push the branch, verify applicable hosted CI checks on the exact head, and complete independent PR review.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | Distinct follow-up (post-commit branch publication / hosted CI check) | Coordinator or repository owner when pushing `feat/ux-1053-agenda-guard-2235` | Caller explicitly prohibited `git push` in this run; hosted CI is unobserved locally per issue #1294 validation disclosure rules. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Post-commit branch push, PR creation targeting `feat/demo-233-same-home-tensions-0825`, hosted CI verification on exact head, and human merge review (deferred per explicit `Do NOT push` instruction).
* Issue #1054 (`GET /demo/view` concurrency bulkhead contention) tracked separately outside #1053 scope.

## Blockers and Remaining Work

* Blockers: none for local RPI completion and branch commit (required human review and hosted CI remain unchecked/pending prior to any future PR merge).
* Remaining active work: none (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` all complete; final clean git commit on `feat/ux-1053-agenda-guard-2235` executed at loop closeout).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/api` (282 source files) | Passed | `Success: no issues found in 282 source files` |
| `python3 -m ruff check .` | `src/api` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/api` (198 files) | Passed | `198 files already formatted` |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests python3 -m unittest test_resident_demo_api test_resident_chat_api test_resident_chat_agenda test_resident_callbacks_page test_resident_demo_script test_epic149_manual_fallback_continuity test_content_standard test_accessibility_baseline -v` | `src/api/tests` (171 tests) | Passed | `Ran 171 tests in 88.046s — OK` |
| Extended `resident_*` unit suite (`test_resident_demo_check`, `test_resident_assistant_api`, `test_resident_assistant_provider`, `test_resident_aoai`, `test_resident_aoai_sql`, `test_resident_screen_wcag`) | `src/api/tests` | Passed | Passed in 227-test run (`8` opt-in local SQL Server tests skipped by design) |
| Refreshed `web-design-guidelines` review (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`) | `src/api/src/zava_forward/api/resident_demo/web/assistant.js`, `src/api/src/zava_forward/api/resident_demo/web/demo.js` | Passed | Both files `✓ pass` with zero `file:line` violations |
| Hosted GitHub Actions CI | `feat/ux-1053-agenda-guard-2235` | Unavailable | Unobserved because caller instructed `Do NOT push` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every functional, non-functional, UX/accessibility/plain-language, and scope-isolation requirement (`FR-01`..`FR-04`, `NFR-01`..`NFR-03`, `AC-01`..`AC-05`, and critique dispositions `PC-001`..`PC-004`) is satisfied with passing Focused-tier validation and zero implementation defects.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | Distinct follow-up | Push `feat/ux-1053-agenda-guard-2235` and run hosted CI + PR review against `feat/demo-233-same-home-tensions-0825` when ready; progress Issue #1054 separately |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier local checks passed (`mypy`, `ruff check`, `ruff format --check`, 171+ unit tests, refreshed `web-design-guidelines` review, `#1054` diff isolation); hosted CI unobserved pending future push
* Blockers: none
