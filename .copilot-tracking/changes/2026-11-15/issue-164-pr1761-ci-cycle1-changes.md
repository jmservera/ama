<!-- markdownlint-disable-file -->
# RPI Changes: Issue #164 PR #1761 Cycle 1 Hosted CI `src-api` Fix

## Metadata

* Task ID: issue-164-pr1761-ci-cycle1
* Related plan: .copilot-tracking/plans/2026-11-15/issue-164-pr1761-ci-cycle1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-164-pr1761-ci-cycle1-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01` / `P01-T01`)
* Completed scope markers: `P01`, `P01-T01`
* All remaining active-plan markers: none
* Status basis: `P01-T01` implemented in `src/api/tests/test_ai_consumption_api.py` and verified green against `unittest` (`tests/test_ai_consumption_api.py`, `tests/test_ai_tasks.py`), `ruff check src tests`, `ruff format --check src tests`, `mypy tests/test_ai_consumption_api.py`, and full `mypy src tests` in `src/api`.

## Execution Summary

Updated `test_manager_report_local_http_and_bad_period` in `src/api/tests/test_ai_consumption_api.py` to expect `"chat_evaluation"` in `set(held)` when `GET /api/ai/report` returns under `"meter-capacity-reached"` or `"meter-evidence-invalid"` consumption holds, and added parity assertions verifying `set(held["chat_evaluation"]) == set(result["chat_evaluation"])`, `held["chat_evaluation"]["version"] == result["chat_evaluation"]["version"]`, and `held["chat_evaluation"]["enablement"]["state"] == "disabled"`.

## Completed Work

### P01: Align Held Manager Report Test Contract and Validate `src/api` (`P01-T01`)

* Modified `src/api/tests/test_ai_consumption_api.py` (`P01-T01`):
  * Added `"chat_evaluation"` to the expected top-level key set `set(held)` in `test_manager_report_local_http_and_bad_period` for both consumption-hold subtests (`"meter-capacity-reached"` and `"meter-evidence-invalid"`).
  * Added parity assertions on `held["chat_evaluation"]` (`set(held["chat_evaluation"]) == set(result["chat_evaluation"])`, `version` equality, and `enablement["state"] == "disabled"`), matching the existing `held["evaluation"]` assertions while preserving live chat disabled state.

## Implementation-Time Plan and Detail Updates

* Local judgment (`P01-T01` environment setup): User-level editable links in `~/.local/lib/python3.12/site-packages` pointed to a pruned sibling worktree, causing `mypy` to report `import-not-found` on `zava_forward.agents`. Reinstalling `-e src/core -e src/agents -e src/api` (`--user --break-system-packages --no-deps`) restored the standard repository editable package layout expected by `mypy` without modifying any repository configuration or source files.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `PYTHONPATH=src:tests:../core/src:../agents/src:../orchestrator/src:../importer/src:../core/tests:../agents/tests python3 -B -m unittest tests/test_ai_consumption_api.py tests/test_ai_tasks.py` | `src/api` | Passed | 112 tests OK |
| `python3 -m ruff check src tests` | `src/api` | Passed | All checks passed |
| `python3 -m ruff format --check src tests` | `src/api` | Passed | 195 files already formatted |
| `python3 -m mypy tests/test_ai_consumption_api.py` | `src/api` | Passed | 0 issues in 1 source file |
| `python3 -m mypy src tests` | `src/api` | Passed | 0 issues in 221 source files |
| Hosted CI on Cycle 1 commit | GitHub Actions | Unobserved | Branch intentionally not pushed per caller instruction |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled — `P01` and `P01-T01` are checked (`[x]`) and match phase details and test ownership matrix (`0` test removals, `0` new test methods, in-place assertion update).
* Completed-work evidence and handoff prose: Reconciled across plan, phase details, and changes record.
* Validation, blockers, remaining work, and follow-up items: Reconciled — 112 unit tests + `ruff` + `mypy` green, zero blockers, zero remaining in-scope tasks.
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None in declared scope (`P01` / `P01-T01` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-164-pr1761-ci-cycle1-plan.md, `## Follow-Up Items`
* Post-merge Issue #164 owner governance prerequisites (`RV-001`) remain outside offline local-testable scope while `chat-case-conversation` stays `disabled`.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`, `P01-T01`), all markers `[x]`
* Validation coverage: Focused tier passed in `src/api` (112 unit tests, `ruff check`, `ruff format --check`, single-file and full `mypy`); hosted CI unobserved because branch is not pushed per caller instruction
* Blockers: None
* Current plan and detail updates: Restored local editable package links for `mypy` recorded as local environment setup note
* Planning and critique state: Ready (`Pass` critique recorded)
* Follow-up items: Post-merge Issue #164 governance gates (`RV-001`)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Parent automatic RPI Agent
