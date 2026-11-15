<!-- markdownlint-disable-file -->
# RPI Changes: Cycle 1 (`c1`) Parent Rebase and CI Fixes for PR #1766 / Issue #116

## Metadata

* Task ID: issue-116-entra-output-0052-c1
* Related plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: All three planned phases (`P01`, `P02`, `P03`) and tasks (`P01-T01`, `P02-T01`, `P03-T01`) completed and passed Focused-tier validation.

## Execution Summary

Rebased `feat/ai-116-entra-output-0052` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`, producing rebased `c0` commit `7b882614d`), resolved the `/api/ai/report` overlap in `src/api/src/zava_forward/api/server.py` preserving both `#164` (`"chat_evaluation": chat_eval.run_eval()`) and `#116` (`"live": s.ai_live_report(u)`), replaced the forbidden `'human-approved'` phrase in `src/core/src/zava_forward/core/data_protection.py:233` with `'human-authorized'`, updated `ai_tasks._record_view` to preserve reviewer-authored `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` when `is_author` is `True` while keeping `withheld` / `FORBIDDEN` redaction on AI/workflow outputs, citations, unresolved markers, and `review_evidence["compared"]` for all viewers and full `NOTE_HELD` redaction for non-author viewers, added a focused `TasksMixin` regression test in `src/api/tests/test_ai_tasks.py`, and passed every Focused validation check across `src/core`, `src/agents`, `src/api`, and `tools/rename-zava-tests.py`.

## Completed Work

### Parent Branch Rebase and `/api/ai/report` Conflict Resolution

* Related phase or task: `P01`, `P01-T01`
* Files: `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_ai_tasks.py`
* What changed and why: Executed `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`). `src/api/tests/test_ai_tasks.py` auto-merged cleanly keeping `#164`'s two multi-turn chat evaluation tests alongside `#116`'s tests; resolved the single hunk conflict in `src/api/src/zava_forward/api/server.py` so `/api/ai/report` returns both `"chat_evaluation": chat_eval.run_eval()` and `"live": s.ai_live_report(u)`.
* Completion evidence: `git merge-base --is-ancestor origin/feat/demo-164-chat-grounding-provenance-0900 HEAD` exited `0` (rebased `c0` commit `7b882614d`).
* Validation: Passed (`Endpoints` `/api/ai/report` tests in `test_ai_tasks.py` and `test_ai_consumption_api.py`, plus `src/api` `mypy` and `ruff`).

### Content Standard Docstring Fix and Reviewer-Author `_record_view` Projection Fix

* Related phase or task: `P02`, `P02-T01`
* Files: `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai_tasks.py`
* What changed and why: Replaced the `validate_necessity_exception` docstring in `data_protection.py:233` with `"""Verify whether a human-authorized text-only derivative may be sent to an external model."""` (`98` columns) to remove the disallowed `'human-approved'` phrase flagged by `CopyAudit.test_ai_label_is_exact_and_never_implies_approval`. Updated `_record_view(store, user, rec)` in `ai_tasks.py` with `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))` so the authoring reviewer retains their own `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` without `projection.NOTE_HELD` self-redaction, while unconditionally holding `FORBIDDEN`/`withheld` values on `ai_output`, `shown_output`, `workflow_output`, `citations`, `unresolved`, and `review_evidence["compared"]` for all viewers and redacting reviewer-authored fields to `projection.NOTE_HELD` for non-author viewers (`not reason_ok or projection.contains_withheld_value(..., withheld)`).
* Completion evidence: Both `test_content_standard.py` and `test_human_review_effectiveness_223.py` (`pooled["total_detected_defects"] == 7`) passed with `0` failures.
* Validation: Passed (`unittest`, `mypy`, and `ruff check`/`ruff format --check` in `src/core` and `src/api`).

### Focused `TasksMixin` Regression Test and Focused-Tier Validation

* Related phase or task: `P03`, `P03-T01`
* Files: `src/api/tests/test_ai_tasks.py`
* What changed and why: Added `test_record_view_preserves_author_review_notes_while_holding_tainted_outputs_and_non_author_views` on `TasksMixin` (running under both `JsonTasks` and `SqlTasks`), seeding both `resident.adjustment` (`SYNTH-ADJ-AUTHOR-CANARY`) and `finance.account` (`SYNTH-FIN-AUTHOR-CANARY`) on `ZF-1` and verifying that a `Retrofit Coordinator` author retains their own review fields while tainted AI/workflow outputs, citations, unresolved markers, and `review_evidence["compared"]` remain held, and that both a non-author `Programme Support Officer` (`reason_ok=False`) and a non-author `Building Safety Liaison` (`reason_ok=True`, lacking `FINANCE_VIEW`) receive `projection.NOTE_HELD` on all four reviewer-authored fields.
* Completion evidence: `229` unit tests across `8` suites (`141` in the `4` primary caller suites + `48` in `#164` eval/chat suites + `40` in `test_ai_consumption_api.py`), `mypy` + `ruff` across `src/core`/`src/agents`/`src/api`, and `25` tests in `tools/rename-zava-tests.py` passed with `0` errors.
* Validation: Passed across all Focused-tier commands.

### Cycle 1 Rebase Continuation Onto `0c1fa1da4` (`PR #1769`) and `d8cb35d25` (`PR #1770`)

* Related phase or task: Child rebase continuation `issue-116-entra-output-0052-c1-rebase` (`P01-T01`, `P02-T01`; inside Cycle 1, no new correction cycle spent)
* Files: `src/core/src/zava_forward/core/store.py`
* What changed and why: Executed `git fetch origin feat/demo-164-chat-grounding-provenance-0900` (which fetched `d8cb35d25` from `PR #1770` `Refs #133`, direct child of `0c1fa1da4` from `PR #1769` `Refs #83`) and rebased `7b882614d..e7d05fab4` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25`), producing rebased commits `fc44a697c` (`7b882614d'`) and `41091c2a0` (`e7d05fab4'`). `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_role_endpoint_inventory.py` auto-merged cleanly, `taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint` carried over untouched from `0c1fa1da4`, `d8cb35d25` merged with zero file overlap, and the sole conflict in `src/core/src/zava_forward/core/store.py` (`_queue_candidates` and `_work_context`) was resolved to preserve both `0c1fa1da4`'s `handoff_policy` cache-key entry and 4-argument `handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` call (matching auto-merged `detail`) alongside `7b882614d`'s multi-line Ruff formatting and `#116` role-visibility methods.
* Completion evidence: Both `git merge-base --is-ancestor 0c1fa1da4 HEAD` and `git merge-base --is-ancestor d8cb35d25 HEAD` exited `0` (`fc44a697c..41091c2a0`).
* Validation: Passed across all post-rebase Focused validation commands (`115` caller unit tests, `174` cross-feature `#83`/`#133`/`#116` unit tests, `src/core` `ruff` + `mypy`, `src/api` `ruff`, and `25` `tools/rename-zava-tests.py` tests).

## Implementation-Time Plan and Detail Updates

### Session-Workspace `.pth` Import Resolution and Clean Pre-Commit Review Ordering

* Affected plan area or markers: `P03`, `P03-T01`
* What changed: Configured `zava_forward.pth` inside the external session-workspace virtualenv (`/home/azureuser/.copilot/session-state/a11ca27c-12dd-430f-ae05-7850842d627c/files/venv`, with `python-pptx` and `Pillow` installed for `rename-zava-tests.py`) instead of `pip install --no-build-isolation -e`, avoiding `bdist_wheel` build-hook metadata noise and writing zero `.egg-info` directories into the git worktree; also aligned `P03-T01` wording so the single clean frozen commit includes `issue-116-entra-output-0052-c1-review.md` immediately after `rpi-review` finishes.
* Why: Keeps `git status --short` completely free of build metadata while giving `mypy` and `unittest` exact package resolution across `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api`.
* Triggering evidence: `pip install --no-deps --no-build-isolation -e` reported missing `bdist_wheel` on system setuptools (`shellId: 34`), resolved cleanly with `zava_forward.pth` (`shellId: 37`, `shellId: 38`).
* User answer or decision: none (ordinary local validation-environment refinement preserving caller intent).
* Reconciliation performed: Reconciled `P03`, `P03-T01`, `Handoff`, and `Phase Index` across the `c1` plan, phase details, and changes record.
* Planning and critique state: Ready (`PC-001`..`PC-003` remained satisfied).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Caller unit suites (`test_content_standard.py`, `test_human_review_effectiveness_223.py`, `test_data_protection.py`, `test_ai_tasks.py`) | `src/core`, `src/api` | Passed | `141` tests ran in `40.627s` (`OK`) including `JsonTasks` and `SqlTasks` |
| Rebased `#164` + consumption suites (`core/tests/test_ai_eval.py`, `agents/tests/test_ai_eval.py`, `agents/tests/test_chat_heldout.py`, `api/tests/test_ai_consumption_api.py`) | `src/core`, `src/agents`, `src/api` | Passed | `48` eval/chat tests (`189` combined, `OK`) + `40` consumption API tests (`OK`) |
| `src/core` `mypy` + `ruff check .` + `ruff format --check .` + `--isolated` on `data_protection.py` | `src/core` | Passed | `mypy`: `0` issues in `336` files; `ruff`: `All checks passed!`, `283 files already formatted`; `--isolated` `E,F,I,B,UP` + format on `data_protection.py`: passed |
| `src/agents` `mypy` + `ruff check .` + `ruff format --check .` | `src/agents` | Passed | `mypy`: `0` issues in `66` files; `ruff`: `All checks passed!`, `62 files already formatted` |
| `src/api` `mypy` + `ruff check .` + `ruff format --check .` | `src/api` | Passed | `mypy`: `0` issues in `280` files; `ruff`: `All checks passed!`, `196 files already formatted` |
| `tools/rename-zava-tests.py` | Repository migration regression | Passed | `Ran 25 tests in 0.745s — OK` |
| Post-rebase (`0c1fa1da4` -> `d8cb35d25`) caller unit suites (`test_ai_tasks.py`, `test_design_system.py` mapped from absent `test_design_system_source_contract.py`, `test_data_protection.py`) | `src/core`, `src/api` | Passed | `Ran 115 tests in 41.074s — OK` (disclosed filename mapping: `src/api/tests/test_design_system_source_contract.py` does not exist in repository history; canonical suite `src/api/tests/test_design_system.py` executed) |
| Post-rebase (`0c1fa1da4` -> `d8cb35d25`) cross-feature `#83` + `#133` + `#116` suites (`test_handoff_escalation_83.py`, `test_handoff_escalation_api_83.py`, `test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_served.py`, `test_role_endpoint_inventory.py`, `test_content_standard.py`, `test_human_review_effectiveness_223.py`) | `src/core`, `src/api` | Passed | `Ran 174 tests in 61.017s — OK` |
| Post-rebase (`0c1fa1da4` -> `d8cb35d25`) `src/core` (`ruff check .`, `ruff format --check .`, `mypy`), `src/api` (`ruff check .`, `ruff format --check .`), and `tools/rename-zava-tests.py` | `src/core`, `src/api`, repository root | Passed | `src/core`: `All checks passed!`, `284 files already formatted`, `mypy`: `Success: no issues found in 337 source files`; `src/api`: `All checks passed!`, `197 files already formatted`; `rename-zava-tests.py`: `Ran 25 tests in 0.564s — OK` |
| Full local gate (`tools/rpi-checks.py --all`) & Docker builds | Repository-wide | Skipped | Explicitly excluded by caller (`Focused tier, no Docker/full gate`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01` checked and `Complete`)
* Completed-work evidence and handoff prose: Current
* Validation, blockers, remaining work, and follow-up items: Current
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md, `## Follow-Up Items`
* Extract shared post-provider record-visibility scrubbing helper across `ai_tasks._record_view`, `Store._rec_view`, and `ChatIsolation.scrub_thread` (outside immediate `c1` CI fix scope; follow-up owner: later refactoring cycle).
* Confirm organisational control-owner sign-off on OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Microsoft Entra B2B tenant configuration (external governance item outside repository code).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining: none
* Validation coverage: `229` unit tests across `8` suites (`OK`), `mypy` + `ruff` across `src/core`/`src/agents`/`src/api` (`0` errors), and `tools/rename-zava-tests.py` (`25` tests, `OK`)
* Blockers: none
* Current plan and detail updates: Recorded session-workspace `.pth` setup and clean post-review single-commit ordering
* Planning and critique state: Ready (`PC-001`..`PC-003` applied)
* Follow-up items: 2 carry-forward items tracked in plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
