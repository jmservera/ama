<!-- markdownlint-disable-file -->
# RPI Changes: Rebase and Verify Issue #220 Non-Retaliation Guard onto PR #1641

## Metadata

* Task ID: 220-no-retaliation-rebase-1641
* Related plan: .copilot-tracking/plans/2026-11-15/220-no-retaliation-rebase-1641-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01` through `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: None
* Status basis: Rebased `feat/ai-220-no-retaliation` onto latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`697b00c0a` -> `135bd2a3e`, `5803323ad`), added `no_retaliation_guard.py` and `test_no_retaliation_guard_220.py`, preserved held `form_review` isolation in `resident_decisions.py`, passed full `src-ci.yml` Focused Tier validation across `src/core` and `src/api` plus the post-cleanup bare-`python3` caller Task 2 check, and committed `src/` in `fb950840a`.

## Execution Summary

Rebased Issue `#220` (`b67bd2a94`, `1a626f1c1`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`697b00c0a`, incorporating sibling merges `#1775`..`#1788` -> rebased `#220` commits `135bd2a3e` and `5803323ad`), added the 18-symbol typed `zava_forward.core.no_retaliation_guard` facade and `test_no_retaliation_guard_220.py` test selector with `load_tests` discovery deduplication, updated both `#220` anchors in `src/core/README.md`, and fixed a held `form_review` (`finance_decision_holds` `status == "Held"`) catalog isolation leak in `src/core/src/zava_forward/core/resident_decisions.py` uncovered by full `src/api` `unittest discover` (`PC-001`).

## Completed Work

### P01 (`P01-T01`, `P01-T02`): Parent Rebase onto `PR #1641` (`697b00c0a`) and Scratch Environment Isolation

* Configured repository-local privacy-safe git identity (`Juan Manuel Servera <8036360+jmservera@users.noreply.github.com>`) resolved dynamically via `gh api user`.
* Fetched `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` initially, then updated tip `697b00c0a` after sibling PRs `#1785`, `#1781`, and `#1788` landed) and rebased `feat/ai-220-no-retaliation` (`135bd2a3e`, `5803323ad`).
* Verified `git range-diff`, clean `git diff --check HEAD`, untouched `src/api/src/zava_forward/api/web/role-screens.js`, intact `#1778` `monitoring_status` + `#117` `is_available_case_document` + `#220` `Assistants.challenge` in `src/core/src/zava_forward/core/assistants.py`, and intact `#1782` + `#115` + `#117` + `#220` sections in `src/core/README.md`.
* Provisioned ephemeral workspace-local `.venv-220-rebase` (`zzz_user_site_fallback.pth`, editable `--no-deps` `src/core[dev]`, `src/agents`, `src/api[dev]`, plus `azure-iot-hub==2.7.0` / `six==1.17.0` inside `.venv-220-rebase` only) without modifying shared `~/.local`.

### P02 (`P02-T01`): `no_retaliation_guard` Facade, `test_no_retaliation_guard_220` Selector, and Held `form_review` Isolation

* Created `src/core/src/zava_forward/core/no_retaliation_guard.py` re-exporting all 18 public non-underscore symbols of `zava_forward.core.challenges` (`ACCESSIBLE_ROUTE`, `FORBIDDEN_ADVERSE_FIELDS`, `NON_DIGITAL_CHANNELS`, `NOT_INFERRED`, `PROTECTION`, `RESOLVED`, `ROUTES`, `SAFEGUARDS`, `STATUSES`, `SUBJECT_KINDS`, `SUBMITTER_KINDS`, `ChallengeRegister`, `ChallengeSafeguardError`, `Node`, `Record`, `assert_no_adverse_challenge_effects`, `build_non_retaliation_assurance`, and `reject_adverse_mapping`).
* Created `src/core/tests/test_no_retaliation_guard_220.py` re-exporting `ChallengeRegisterNoRetaliationTests`, `StoreAndSqlStoreNoRetaliationLifecycleTests`, and `AssistantsProposalChallengeNoRetaliationTests` from `test_challenge_no_retaliation_220` plus `NoRetaliationGuardFacadeTests` (18-symbol set/identity parity + held `form_review` catalog isolation test) and `load_tests` discovery deduplication.
* Updated both `#220` verification/documentation anchors in `src/core/README.md`.
* Updated `_form_staging_records` in `src/core/src/zava_forward/core/resident_decisions.py` to exclude drafts actively held in `finance_decision_holds` (`status == "Held"`) from `linked_batches` and `verified_by` resolution so unapproved held working reviews remain isolated from `/api/cases/<cid>` (`detail()`).

### P02 (`P02-T02`): Full `src-ci.yml` Focused Tier Validation, `.venv-220-rebase` Cleanup, Bare Caller Check, and Clean Local Commits

* Executed full `src-ci.yml` discovery, lint, format, and strict type checks in `src/core` and `src/api` inside `.venv-220-rebase` (all exiting `0`).
* Deleted `.venv-220-rebase` and temporary `*.egg-info`, then verified the exact caller Task 2 command (`cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`) and `env -u PYTHONPATH python3 -m mypy` (`exit=0`).
* Committed `src/core/src/zava_forward/core/no_retaliation_guard.py`, `src/core/tests/test_no_retaliation_guard_220.py`, `src/core/src/zava_forward/core/resident_decisions.py`, and `src/core/README.md` as `fb950840a` (`Refs #220` + Copilot trailer, zero `.copilot-tracking/` strings), followed by the reconciled pre-Review `.copilot-tracking/` commit.

## Implementation-Time Plan and Detail Updates

* **Immediately relevant current-state update (`P02-T01` / `P02-T02`, held `form_review` isolation)**: Full `src/api` `unittest discover` (`PC-001`) exposed `test_form_staging_api.FormApi.test_working_field_review_and_manifest_are_held_and_isolated`, where saving a held working field review (`POST /api/cases/ZF-1/form-review`, `reviewed_ready == False`, `finance_decision_holds` `status == "Held"`) caused `#220`'s `_form_staging_records` (`src/core/src/zava_forward/core/resident_decisions.py`) to link the staged batch into `/api/cases/ZF-1` (`challenge_targets`). Updated `_form_staging_records` to skip drafts held in `finance_decision_holds` (`status == "Held"`), added `test_held_form_review_drafts_remain_isolated_from_challenge_catalog` in `src/core/tests/test_no_retaliation_guard_220.py`, and recorded the target update in `plan.md` and `phase-details.md`.
* **Immediately relevant current-state update (`P01-T01`, parent `PR #1641` tip advance)**: During execution, `origin/feat/demo-164-chat-grounding-provenance-0900` advanced from `ad005cd5f` to `697b00c0a` (`#1785`, `#1781`, `#1788`). Fetched and rebased cleanly onto `697b00c0a` (`git merge-tree` `exit=0`, `git range-diff` verified) before running final `src/core` and `src/api` suites.

## Validation Record

| Check | Scope | Status | Evidence or reason |
| --- | --- | --- | --- |
| Rebase ancestry & `git range-diff` | `origin/feat/demo-164-chat-grounding-provenance-0900` (`697b00c0a`) .. `HEAD` (`fb950840a`) | Passed | `135bd2a3e` + `5803323ad` + `fb950840a` atop `697b00c0a`; `web/role-screens.js` untouched; `git diff --check HEAD` clean |
| Caller Task 2 bare-`python3` check (post-cleanup) | `src/core`: `PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy` (+ `env -u PYTHONPATH python3 -m mypy`) | Passed | `Ran 7 tests in 0.510s OK`; `All checks passed!`; `303 files already formatted`; `Success: no issues found in 357 source files` |
| Full `src-ci.yml` `src/core` suite | `python -m unittest discover -s tests -q`, `ruff check .`, `ruff format --check .`, `env -u PYTHONPATH mypy` | Passed | `Ran 3685 tests in 808.262s OK (skipped=420)`; `304 files already formatted`; `Success: no issues found in 357 source files` |
| Full `src-ci.yml` `src/api` suite | `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q`, `ruff check .`, `ruff format --check .`, `env -u PYTHONPATH mypy`, `node --check src/zava_forward/api/web/panels.js` | Passed | `Ran 3772 tests in 2071.256s OK (skipped=635)` (including `test_form_staging_api`, `test_challenge_no_retaliation_api_220`, `test_content_standard`, `test_resident_api`, `test_assistants`); `214 files already formatted`; `Success: no issues found in 298 source files` |
| Hosted CI & live SQL Server container | Remote GitHub Actions / Docker `mssql` | Skipped | Caller Task 3 explicitly forbids `git push` ("Leave a clean worktree without pushing") |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]` with completion evidence)
* Completed-work evidence and handoff prose: Reconciled (`135bd2a3e`, `5803323ad`, `fb950840a` recorded)
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining work items)
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/220-no-retaliation-rebase-1641-plan.md, `## Follow-Up Items`
* Extend `src/api/checks/challenge_browser_check.py` with interactive Playwright + axe-core 4.10.3 assertions clicking `#challenge-reopen-<id>` and toggling representative/safety-concern fields.
* Run live native SQL Server `_priority_correction_rows` verification and Issue `#220` human RAI/legal governance + assistive-technology comprehension sign-off (`RV-001`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`, `P02`); completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: None
* Validation coverage: Post-cleanup caller Task 2 check (`7` tests + `ruff` + `ruff format --check` + `mypy` `357` files), full `src/core` `src-ci.yml` suite (`3,685` tests + `ruff` + `mypy`), full `src/api` `src-ci.yml` suite (`3,772` tests + `ruff` + `mypy` + `node --check`); remote CI skipped per no-push requirement
* Blockers: None
* Current plan and detail updates: Recorded rebase onto updated `origin/feat/demo-164-chat-grounding-provenance-0900` (`697b00c0a`) and `resident_decisions.py` held `form_review` (`finance_decision_holds` `status == "Held"`) catalog isolation guard
* Planning and critique state: Complete (`PC-001`..`PC-004` resolved and verified)
* Follow-up items: 2 follow-up items preserved from plan
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
