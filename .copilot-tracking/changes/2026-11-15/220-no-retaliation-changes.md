<!-- markdownlint-disable-file -->
# RPI Changes: Issue #220 Criterion 5 — No Retaliation, Inferred Refusal or Delayed Hazard Response

## Metadata

* Task ID: issue-220-no-retaliation-2026-11-15
* Related plan: .copilot-tracking/plans/2026-11-15/220-no-retaliation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full_plan (`P01`..`P04`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P02-T03`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01`, `P04-T02`, `P04-T03`
* All remaining active-plan markers: None
* Status basis: All four phases (`P01`..`P04`) completed and verified against Focused Tier checks (`test_challenge_no_retaliation_220.py`, `test_challenge_no_retaliation_api_220.py`, `test_content_standard.py`, 661 targeted regression tests across `src/core` and `src/api`, all 5 Playwright + axe 4.10.3 `challenge_browser_check.py` journeys, `ruff check .`, `ruff format --check .`, and `mypy` strict across `src/core` and `src/api`), with `src/api/src/zava_forward/api/web/role-screens.js` untouched.

## Execution Summary

Executing the approved four-phase plan (`P01`..`P04`) to enforce and verify end-to-end non-retaliation, non-refusal, non-closure, zero-hazard-delay, immediate independent hazard intake routing, and machine-checkable `non_retaliation_assurance` / `hazard_clock_preserved` contracts across all challenge and correction entrypoints in `src/core` and `src/api` without modifying `src/api/src/zava_forward/api/web/role-screens.js`.

## Completed Work

### Core Challenge Register, Reopen, Representative Metadata, and Safeguard Contract (`P01`)

* Related phase or task: `P01`, `P01-T01`, `P01-T02`
* Files: `src/core/src/zava_forward/core/challenges.py`
* What changed and why: Added `build_non_retaliation_assurance`, expanded `FORBIDDEN_ADVERSE_FIELDS` and `NOT_INFERRED`, upgraded `assert_no_adverse_challenge_effects` (guarding priority/score/urgent, refusal/no-access/sanction/withdrawn/negative-engagement, unrelated work-item closures, `awaiting_hazard_action`, Awaab's Law 24h/7d/14d and safeguarding clocks, and controlled `allow_new_independent_hazard` verification), added `ChallengeRegister.reopen` and `record_representative` plus `submitted_by`/`representative_ref` across `record_digital`, `record_staff`, `update`, and `reopen`, enriched `hazard_referral` (`independent_intake: True`, `waits_for_challenge_review: False`, `hazard_clock_preserved: True` without resetting `received_on`), and exposed `non_retaliation_assurance` + `hazard_clock_preserved: True` on records and `.view()`.
* Completion evidence: `challenges.py` formatted, linted, type-checked under `mypy --strict`, and verified against existing `test_challenges.py` + `test_issue_220_challenge_route.py` (28 tests passing).
* Validation: Passed (`ruff format --check`, `ruff check`, `mypy`, and 28 existing challenge tests).

### Store-Backed Case Challenge, Reopen, Representative, AI-Task/Form, and Immediate Hazard Routing (`P02`)

* Related phase or task: `P02`, `P02-T01`, `P02-T02`, `P02-T03`
* Files: `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/ai_tasks.py`
* What changed and why: Added `challenge_reopen` to `RESIDENT_ACTIONS` and `FOLLOWUP_ACTIONS`, expanded `CHALLENGE_CHANNELS` with `"Assisted visit"` and `"Trusted intermediary"`, added `submitted_by`/`representative_ref` with read-only `representative_authority_status`, implemented replay-safe `_route_challenge_hazard` (`PC-001`) supporting immediate `hazard_referral` and atomic independent `hazard_intake`, updated `priority_correction_lookup` plus `sqlstore.py` and `mssqlstore.py` (`PC-002`) to preserve correction staleness across reopen via `prior_correction_preserved`, blocked stale acceptance/edit in `ai_tasks.review` (`PC-003`), wrapped challenge/nomination/service actions in runtime `assert_no_adverse_challenge_effects` + `_ranking()` invariance checks, extended `challenge_catalog`/`_priority_record`/`_dependency`/`priority_challenge_state` to `ai_task` and `form_staging` (`form:<id>`) records, and attached `non_retaliation_assurance` + `hazard_clock_preserved: True` to records, `challenge_targets`, and audit details.
* Completion evidence: Passed `ruff check`, `ruff format --check`, `mypy --strict`, and 462 existing tests across `test_challenges.py`, `test_issue_220_challenge_route.py`, and `test_resident_decisions.py`.
* Validation: Passed.

### Assistant Proposal Challenge Route, HTTP API Endpoint, and Plain-Language Workbench (`P03`)

* Related phase or task: `P03`, `P03-T01`, `P03-T02`
* Files: `src/core/src/zava_forward/core/assistants.py`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js`
* What changed and why: Added `Assistants.challenge` supporting `open`, `update`, `reopen`, `escalate`, and `resolve` on SQLite `assistant_tasks` with optimistic `revision` fencing, representative/nominee metadata, immediate `hazard_referral` and independent `hazard_intake` routing via `raise_hazard`, runtime `assert_no_adverse_challenge_effects` + `_ranking()` invariance verification, `"Correction recorded"` staleness (`challenged_stale` preserved across reopen), transient `_view` key stripping and `_withhold_sensors` challenge-note redaction (`PC-004`), and `non_retaliation_assurance` + `hazard_clock_preserved: True` projection; exposed `POST /api/assistants/proposals/<tid>/challenge` in `server.py`; and updated `web/panels.js` (`renderChallengePanel`, without touching `web/role-screens.js`) after loading and fetching `web-design-guidelines` (`✓ pass`) to support `"Assisted visit"` / `"Trusted intermediary"`, `submitted_by` + optional `representative_ref`, `hazard_concern`, `#challenge-reopen-<id>`, and plain-language safeguard confirmation.
* Completion evidence: Passed `ruff check`, `ruff format --check`, `mypy --strict`, `test_content_standard.py`, `test_resident_api.py`, and all 5 Playwright + axe 4.10.3 `challenge_browser_check.py` journeys (`base`, `history`, `navigation`, `refresh-draft`, `pending-draft`).
* Validation: Passed.

### Core & API Test Suites, Module READMEs, and Focused Tier Validation (`P04`)

* Related phase or task: `P04`, `P04-T01`, `P04-T02`, `P04-T03`
* Files: `src/core/tests/test_challenge_no_retaliation_220.py`, `src/api/tests/test_challenge_no_retaliation_api_220.py`, `src/core/README.md`, `src/api/README.md`
* What changed and why: Added `src/core/tests/test_challenge_no_retaliation_220.py` (5 comprehensive test methods proving `ChallengeRegister` digital/staff/representative reopen & hazard-referral persistence, fail-closed `assert_no_adverse_challenge_effects` tamper rejection across every adverse field/clock/closure class, end-to-end JSON `Store` + SQLite `SqlStore` challenge/reopen/nomination/service/hazard-intake lifecycles across priority, `ai_task`, and `form_staging` suggestions including `PC-001`..`PC-003`, and SQLite `Assistants.challenge` including `PC-004` sensor-consent redaction) and `src/api/tests/test_challenge_no_retaliation_api_220.py` (3 comprehensive HTTP integration tests covering `/api/cases/<cid>/resident`, `/api/cases/<cid>/followup`, `/api/assistants/proposals/<tid>/challenge`, `/api/cases/<cid>/hazard-raise`, `/api/cases/<cid>`, `/api/audit`, closed-schema `400`/`403`/`409` rejection, and `web/panels.js` static/content-standard invariants, seeding linked `form_reviews` alongside `form_staging` in `_seed_api_case_invariants`), updated `src/core/README.md` and `src/api/README.md`, and executed Focused Tier verification via `pip`-installed editable distributions.
* Completion evidence: `test_challenge_no_retaliation_220.py` (5 OK), `test_challenge_no_retaliation_api_220.py` (3 OK), `test_content_standard.py` (29 OK), 502 targeted `src/core` regression tests OK, 159 targeted `src/api` regression tests OK, all 5 Playwright + axe 4.10.3 `challenge_browser_check.py` modes OK, `ruff check .` OK, `ruff format --check .` OK (337 core + 197 api files), and `mypy` OK (337 core + 281 api files); `git status --short` confirms `web/role-screens.js` is untouched.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

* Local judgment only: Updated `_seed_api_case_invariants` in `src/api/tests/test_challenge_no_retaliation_api_220.py` to seed a linked `case["form_reviews"]` record alongside `case["form_staging"]` so `challenge_catalog(..., catalog_only=True)` exposes `form:BATCH-API-1` while keeping unlinked `form_staging` batches backward-compatible with `test_form_staging.py` and `test_form_review.py`. No plan or scope change required.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python -m unittest discover -s tests -p "test_challenge_no_retaliation_220.py" -v` | `src/core` | Passed | Ran 5 tests in 0.431s (`OK`) |
| `python -m unittest discover -s tests -p "test_challenge_no_retaliation_api_220.py" -v` | `src/api` | Passed | Ran 3 tests in 0.903s (`OK`) |
| `python -m unittest discover -s tests -p "test_content_standard.py" -v` | `src/api` | Passed | Ran 29 tests in 0.088s (`OK`; zero forbidden phrases/nouns) |
| `ruff check .` and `ruff format --check .` | `src/core` & `src/api` | Passed | All checks passed; 337 (`src/core`) + 197 (`src/api`) files formatted cleanly |
| `mypy` (`strict = true`) | `src/core` & `src/api` | Passed | `Success: no issues found in 337 source files` (`src/core`) and `281 source files` (`src/api`) |
| Targeted challenge/resident/form/assistant regressions | `src/core` & `src/api` | Passed | 502 tests in `src/core` (`test_challenges`, `test_issue_220_challenge_route`, `test_resident_decisions`, `test_form_staging`, `test_form_review`) + 159 tests in `src/api` (`test_resident_api`, `test_assistants`) all `OK` |
| `checks/challenge_browser_check.py` (5 modes + axe 4.10.3) | `src/api` (`web/panels.js`) | Passed | `base`, `--history`, `--navigation`, `--refresh-draft`, and `--pending-draft` all `OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`..`P04` and `P01-T01`..`P04-T03` checked and marked `Complete`)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active tasks)
* Review readiness: Ready (`rpi-review` eligible)

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/220-no-retaliation-plan.md, `## Follow-Up Items`
* None in active engineering scope; human operational/legal/assistive-technology acceptance gates remain external to local engineering tasks per Issue #220 and `src/core/README.md`.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: `full_plan`; completed: `P01`..`P04` (`P01-T01`..`P04-T03`); remaining: None
* Validation coverage: Focused Tier passed (`test_challenge_no_retaliation_220.py`, `test_challenge_no_retaliation_api_220.py`, `test_content_standard.py`, 661 targeted regressions, 5 Playwright + axe 4.10.3 `challenge_browser_check.py` modes, `ruff check .`, `ruff format --check .`, and `mypy` strict across `src/core` and `src/api`)
* Blockers: None
* Current plan and detail updates: Reconciled (`P01`..`P04` complete)
* Planning and critique state: Ready (`PC-001`..`PC-004` resolved and verified in tests)
* Follow-up items: None in active software plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
