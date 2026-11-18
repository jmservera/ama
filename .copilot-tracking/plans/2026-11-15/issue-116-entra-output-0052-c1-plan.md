<!-- markdownlint-disable-file -->
# RPI Plan: Cycle 1 (`c1`) Parent Rebase and CI Fixes for PR #1766 / Issue #116

## Task Metadata

* Task ID: issue-116-entra-output-0052-c1
* Task slug: issue-116-entra-output-0052-c1
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-c1-plan-critique.md

## Executive Summary

Cycle 1 (`c1`) prepares `PR #1766` (Issue #116, branch `feat/ai-116-entra-output-0052`) for clean coordinator review and merge onto its updated parent branch `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`, following the merge of `PR #1761`) while resolving both hosted CI failures reported on `PR #1766`.

First (`P01`), we run `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900` on `feat/ai-116-entra-output-0052` and cleanly resolve the guaranteed overlaps in `src/api/src/zava_forward/api/server.py` (`/api/ai/report`) and `src/api/tests/test_ai_tasks.py` (`Endpoints`), preserving both `#164` (`chat_eval` import, `"chat_evaluation": chat_eval.run_eval()`, and chat-evaluation report tests) and `#116` (`"live": s.ai_live_report(u)` and role-visibility tests). Second (`P02`), we replace the forbidden `'human-approved'` phrase in `src/core/src/zava_forward/core/data_protection.py:233` with `'human-authorized'` (`"""Verify whether a human-authorized text-only derivative may be sent to an external model."""`), and update `_record_view(store, user, rec)` in `src/core/src/zava_forward/core/ai_tasks.py` so the review author (`is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))`) retains their own `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` without `projection.NOTE_HELD` replacement while keeping `withheld`/`FORBIDDEN` redaction on `ai_output`, `shown_output`, `workflow_output`, `citations`, `unresolved`, and `review_evidence["compared"]` for all viewers and full `not reason_ok` / `withheld` `NOTE_HELD` redaction of reviewer-authored fields for non-author viewers. Third (`P03`), we add `1` focused unit test method on `TasksMixin` in `src/api/tests/test_ai_tasks.py` verifying author vs non-author `_record_view` behavior across JSON and SQL backends and execute the Focused validation tier in an external session-workspace virtualenv with editable `zava_forward` installs (`unittest` including `#164` parent suites, `mypy`, `pyproject.toml`-respecting `ruff check .` / `ruff format --line-length 100 --check .` across `src/core`, `src/agents`, and `src/api` plus targeted `--isolated` check on `data_protection.py`, and `rename-zava-tests.py`).

### User Decisions and Requirements Highlights

* Rebase `feat/ai-116-entra-output-0052` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`), preserving both `#164` and `#116` changes cleanly.
* Fix `src-api` `test_content_standard.py` by replacing `'human-approved'` with `'human-authorized'` in `src/core/src/zava_forward/core/data_protection.py:233` (`"""Verify whether a human-authorized text-only derivative may be sent to an external model."""`).
* Fix `src-core` `test_human_review_effectiveness_223.py:401` inside `ai_tasks._record_view(store, user, rec)` by preserving the review author's own `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` when `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))` while retaining `withheld` checks on AI/workflow outputs, citations, unresolved markers, and `review_evidence["compared"]`, plus full `NOTE_HELD` redaction for non-author viewers.
* Validate locally with the Focused tier (no Docker / full `rpi-checks.py --all` gate) and leave a clean frozen commit with the Copilot trailer without pushing.

### What You May Not Know

* Parent `origin/feat/demo-164-chat-grounding-provenance-0900` advanced by two commits (`02ab20cac` `#1753` and `7f83f4749` `#1761`) and conflicts directly in `src/api/src/zava_forward/api/server.py` at `/api/ai/report`, where `#164` added `"chat_evaluation": chat_eval.run_eval()` and `#116` changed `"live": s.ai_live_report()` to `"live": s.ai_live_report(u)`.
* Naive substitution of `'human-authorized'` into the existing 100-character docstring in `data_protection.py:233` would produce a 101-character line and fail `ruff format --line-length 100 --check`; the exact 98-character docstring requested (`"""Verify whether a human-authorized text-only derivative may be sent to an external model."""`) satisfies both `test_content_standard.py` and `ruff format --check`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop for Cycle 1 (`c1`) of Issue #116 (`PR #1766`, branch `feat/ai-116-entra-output-0052` in `/home/azureuser/source/ama-demo-wt/feat-116-entra-output-0052`) in order: research, plan, implement, review, writing dated `c1` artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) (caller prompt).
* Rebase the branch onto the latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`) and resolve any overlap cleanly, preserving both `#164` and `#116` changes (caller prompt).
* Fix Failure 1 (`src-api` `test_content_standard.py`): in `src/core/src/zava_forward/core/data_protection.py:233`, replace `'human-approved'` with `'human-authorized'` in the docstring (`"""Verify whether a human-authorized text-only derivative may be sent to an external model."""`) (caller prompt).
* Fix Failure 2 (`src-core` `test_human_review_effectiveness_223.py:401`): in `src/core/src/zava_forward/core/ai_tasks.py` inside `_record_view(store, user, rec)`, when `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))`, do not replace the reviewer's own `override_text`, `reviewer_reason`, `reason`, or `review_evidence["reason"]` with `projection.NOTE_HELD` in the returned view; keep `withheld` checks on `ai_output`, `shown_output`, `citations`, `unresolved`, and `review_evidence["compared"]`, and keep `not reason_ok` / `withheld` redaction for non-author viewers (caller prompt).
* Validate locally using the exact Focused-tier commands (`unittest` on `test_content_standard.py`, `test_human_review_effectiveness_223.py`, `test_data_protection.py`, `test_ai_tasks.py`, `mypy` and `ruff check`/`ruff format --line-length 100 --check` in `src/core` and `src/api`, and `python3 tools/rename-zava-tests.py`), commit all code and `c1` RPI artifacts with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer, leave `git status --short` empty, and do NOT push (caller prompt).

## Goals

* Rebase `feat/ai-116-entra-output-0052` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) with zero regression to either `#164` or `#116`.
* Resolve both hosted CI failures (`test_content_standard.py` and `test_human_review_effectiveness_223.py`) while maintaining strict role/field-level visibility redaction on AI outputs and non-author review record views.
* Verify with focused unit tests, `mypy`, `ruff`, and migration checks, and record complete `c1` RPI evidence in a single clean local commit.

## Scope and Non-Goals

### In Scope

* Git rebase of `feat/ai-116-entra-output-0052` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) and conflict resolution in `src/api/src/zava_forward/api/server.py` (and `src/api/tests/test_ai_tasks.py` if needed).
* Docstring update in `src/core/src/zava_forward/core/data_protection.py:233`.
* Reviewer-author check (`is_author`) in `src/core/src/zava_forward/core/ai_tasks.py` (`_record_view`).
* Focused unit test addition in `src/api/tests/test_ai_tasks.py` covering author vs non-author `_record_view` projection, plus Focused-tier validation across `src/core`, `src/api`, and `tools/rename-zava-tests.py`.
* Recording all `c1` RPI tracking artifacts under `.copilot-tracking/` and creating a clean local commit.

### Non-Goals

* Running `tools/rpi-checks.py --all` or Docker image builds.
* Pushing the rebased branch to `origin` (`coordinator` independently reviews and pushes).
* Changing `projection.DEFAULT_REASON_ROLES` or weakening non-author redaction on review records or `ai_live_report`.

## Functional Requirements

* FR-1: Clean parent rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900`
  * Observable acceptance criteria: `git merge-base --is-ancestor origin/feat/demo-164-chat-grounding-provenance-0900 HEAD` exits `0`; `/api/ai/report` in `src/api/src/zava_forward/api/server.py` returns both `"chat_evaluation": chat_eval.run_eval()` (`#164`) and `"live": s.ai_live_report(u)` (`#116`); all `#164` and `#116` tests in `src/api/tests/test_ai_tasks.py` remain present and pass.
* FR-2: Content-standard compliance in `data_protection.py`
  * Observable acceptance criteria: `src/core/src/zava_forward/core/data_protection.py:233` uses `"""Verify whether a human-authorized text-only derivative may be sent to an external model."""` with zero disallowed occurrences of `"human-approved"`, and `src/api/tests/test_content_standard.py` passes completely.
* FR-3: Author-preserving, non-author-redacting `_record_view` in `ai_tasks.py`
  * Observable acceptance criteria: In `ai_tasks._record_view(store, user, rec)`, when `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))` is `True`, `out["override_text"]`, `out["reviewer_reason"]`, `out["reason"]`, and `out["review_evidence"]["reason"]` are not replaced with `projection.NOTE_HELD` (so `test_human_review_effectiveness_223.py` passes with `pooled["total_detected_defects"] == 7`), while `ai_output`, `shown_output`, `workflow_output`, `citations`, `unresolved`, and `review_evidence["compared"]` continue to enforce `FORBIDDEN` and `withheld` checks unconditionally for all viewers and non-author viewers (`is_author is False`) continue to have `override_text` (when matching `withheld`) and `reason` / `reviewer_reason` / `review_evidence["reason"]` (when `not reason_ok or projection.contains_withheld_value(val, withheld)`) replaced with `projection.NOTE_HELD`.

## Non-Functional Requirements

* NFR-1: Static typing, formatting, lint, and migration cleanliness
  * Objective threshold or evaluation condition: `0` errors across `mypy`, `ruff check .`, and `ruff format --line-length 100 --check .` in `src/core`, `src/agents`, and `src/api` (plus targeted `--isolated` check on `src/zava_forward/core/data_protection.py`), and `0` failures in `python3 tools/rename-zava-tests.py`.
  * Operating condition or verification approach, if needed: Executed using an external session-workspace virtualenv (`/home/azureuser/.copilot/session-state/a11ca27c-12dd-430f-ae05-7850842d627c/files/venv` with `--system-site-packages` and editable `-e src/core -e src/agents -e src/api --no-deps --no-build-isolation` installs) so `mypy` resolves cross-package imports cleanly without leaving untracked artifacts in the git worktree, and using project `pyproject.toml` Ruff configs matching `.github/workflows/src-ci.yml`.
  * Observable acceptance criteria: Every Focused-tier validation command exits `0`.

## Acceptance Criteria

* `feat/ai-116-entra-output-0052` is rebased cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) preserving both `#164` and `#116` behavior.
* `src/api/tests/test_content_standard.py` passes with `0` failures.
* `src/core/tests/test_human_review_effectiveness_223.py` passes with `0` failures (`pooled["total_detected_defects"] == 7`).
* `src/core/tests/test_data_protection.py`, `src/api/tests/test_ai_tasks.py` (including a focused regression test on `TasksMixin` for author vs non-author `_record_view`), and parent `#164` suites (`src/core/tests/test_ai_eval.py`, `src/agents/tests/test_ai_eval.py`, `src/agents/tests/test_chat_heldout.py`, `src/api/tests/test_ai_consumption_api.py`) pass with `0` failures.
* `mypy`, `ruff check .`, and `ruff format --line-length 100 --check .` pass in `src/core`, `src/agents`, and `src/api`, and `python3 tools/rename-zava-tests.py` passes.
* Test ownership and bounds lock:
  * Removals: `none` (`0` existing tests removed or weakened).
  * Canonical test targets: `src/api/tests/test_ai_tasks.py` (`TasksMixin`, maximum `1` focused test method added verifying `_record_view` author retention vs non-author `NOTE_HELD` redaction under both `not reason_ok` and `reason_ok=True` with withheld text, plus persistent `withheld` filtering on AI/workflow outputs; `0` new test files; `0` generated files modified).
  * Semantic vs regression coverage: Semantic assertions verify `is_author=True` keeps reviewer-authored `override_text`/`reviewer_reason`/`reason`/`review_evidence["reason"]` while still redacting withheld `ai_output`/`shown_output`/`workflow_output`/`citations`/`unresolved`/`review_evidence["compared"]`, and `is_author=False` redacts reviewer-authored fields to `projection.NOTE_HELD`; regression suites verify `test_content_standard.py`, `test_human_review_effectiveness_223.py`, `test_data_protection.py`, `test_ai_tasks.py`, `test_ai_eval.py`, `test_chat_heldout.py`, `test_ai_consumption_api.py`, and `rename-zava-tests.py`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                      |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md                                       |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md                            |
| Latest critique                  | Complete (`Revise`, all 3 findings `PC-001`..`PC-003` applied directly) at .copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-c1-plan-critique.md |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-research.md                                |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md is owned by `rpi-implement`      |
| Planning execution and readiness | Complete and `ready` for `rpi-implement`                                                                        |
| Continuation context             | Active automatic RPI Agent parent continues directly to `rpi-implement`                                         |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-research.md`: Cycle 1 evidence (`C1`-`C7`) covering parent diff, CI failure tracebacks, contrarian line-length check, and Option C convergence.
* `src/api/src/zava_forward/api/server.py`, `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai_tasks.py`: Target implementation modules.
* `src/api/tests/test_content_standard.py`, `src/core/tests/test_human_review_effectiveness_223.py`, `src/core/tests/test_data_protection.py`, `src/api/tests/test_ai_tasks.py`: Target verification suites.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase Onto Updated Parent Branch (`#164` / `PR #1761`)

* Intent: Rebase `feat/ai-116-entra-output-0052` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) while preserving all `#164` and `#116` changes cleanly.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase branch onto `origin/feat/demo-164-chat-grounding-provenance-0900` and resolve `/api/ai/report` overlap

* Requirement and evidence: FR-1 (`C1`, `C2`)
* Expected result: `feat/ai-116-entra-output-0052` sits cleanly atop `origin/feat/demo-164-chat-grounding-provenance-0900` with `/api/ai/report` returning both `"chat_evaluation": chat_eval.run_eval()` and `"live": s.ai_live_report(u)`, and all `#164` and `#116` tests preserved in `src/api/tests/test_ai_tasks.py`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Fix PR #1766 Content Standard and Author Review Record Projection Failures

* Intent: Fix both CI regressions in `data_protection.py` and `ai_tasks.py` without weakening role/field-level visibility enforcement.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Replace `'human-approved'` with `'human-authorized'` in `data_protection.py` and preserve author-owned fields in `ai_tasks._record_view`

* Requirement and evidence: FR-2, FR-3 (`C3`, `C4`, `C5`, `C6`, `C7`)
* Expected result: `data_protection.py:233` uses `"""Verify whether a human-authorized text-only derivative may be sent to an external model."""`; `ai_tasks._record_view` preserves `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` when `is_author` is `True` while keeping `withheld`/`FORBIDDEN` redaction on AI/workflow outputs, citations, unresolved markers, and `review_evidence["compared"]` for all viewers and `NOTE_HELD` redaction of reviewer-authored fields for non-author viewers.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Regression Coverage and Validation

* Intent: Add focused author/non-author `_record_view` regression test on `TasksMixin`, run Focused-tier checks, and prepare `c1` artifacts for `rpi-review` and final clean local commit.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add `_record_view` author vs non-author unit test on `TasksMixin`, run Focused validation tier, and reconcile `c1` artifacts for review and final commit

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1 (`C1`-`C7`, `PC-001`-`PC-003`)
* Expected result: Focused test on `TasksMixin` in `src/api/tests/test_ai_tasks.py` verifies author retention and non-author `NOTE_HELD` redaction across JSON and SQL backends; all Focused `unittest` (including `#164` suites), `mypy`, `ruff`, and `rename-zava-tests.py` checks pass in the session-workspace editable venv; and all code and `c1` RPI tracking files are ready for single-pass `rpi-review` and clean local commit with the Copilot trailer.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md

## Dependencies

* `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`): Fetched upstream parent branch containing merged `PR #1753` and `PR #1761`.
* Session-workspace editable Python virtualenv (`/home/azureuser/.copilot/session-state/a11ca27c-12dd-430f-ae05-7850842d627c/files/venv` with `--system-site-packages` and `-e src/core -e src/agents -e src/api --no-deps --no-build-isolation`): Ensures `mypy`, `ruff`, and `unittest` resolve `zava_forward.*` packages accurately without leaving untracked files in the git worktree.

## Critique Disposition

Single-pass final-candidate critique completed in `.copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-c1-plan-critique.md` (`Verdict: Revise`; `0` Critical, `1` High, `2` Medium, `0` Low; no user questions required):

* `PC-001` [High] (`planning_parent`, direct planner correction — **Applied**): Updated `NFR-1`, `Dependencies`, `P03`, and `P03-T01` to provision an external session-workspace virtualenv (`/home/azureuser/.copilot/session-state/a11ca27c-12dd-430f-ae05-7850842d627c/files/venv` with `--system-site-packages` and editable `-e src/core -e src/agents -e src/api --no-deps --no-build-isolation`) before running `mypy`/`unittest`, and to run `pyproject.toml`-respecting `ruff check . && ruff format --line-length 100 --check .` (matching `.github/workflows/src-ci.yml`) plus targeted `--isolated` formatting check on `data_protection.py`.
* `PC-002` [Medium] (`planning_parent`, direct planner correction — **Applied**): Updated `FR-3`, `P02-T01`, and `P03-T01` so non-author viewers redact `reason`, `reviewer_reason`, and `review_evidence["reason"]` whenever `not reason_ok or projection.contains_withheld_value(val, withheld)` (matching `ai_tasks.live_report`) and top-level `workflow_output` is checked unconditionally against `withheld` alongside `shown_output`.
* `PC-003` [Medium] (`planning_parent`, direct planner correction — **Applied**): Updated `P01-T01`, `P03`, and `P03-T01` to run `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, resolve guaranteed conflicts in both `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_ai_tasks.py` (`Endpoints`), place the new unit test on `TasksMixin` in `src/api/tests/test_ai_tasks.py`, and run post-rebase `#164` and `src/agents` checks (`src/core/tests/test_ai_eval.py`, `src/agents/tests/test_ai_eval.py`, `src/agents/tests/test_chat_heldout.py`, `src/api/tests/test_ai_consumption_api.py`, and `src/agents` `mypy`/`ruff`).

## Follow-Up Items

* Extract shared post-provider record-visibility scrubbing helper across `ai_tasks._record_view`, `Store._rec_view`, and `ChatIsolation.scrub_thread`: Carry-forward engineering-quality cleanup (`RV-001`) outside this surgical `c1` CI fix.
* Organisational control-owner confirmation of OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Microsoft Entra B2B tenant configuration: External governance items on Issue #116 outside local repository scope.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md
* Ready phase or task: Complete (`P01`, `P02`, `P03` complete; ready for `rpi-review`)
* Remaining provisional question or blocker: None
