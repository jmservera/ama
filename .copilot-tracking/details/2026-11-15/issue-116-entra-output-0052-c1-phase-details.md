<!-- markdownlint-disable-file -->
# RPI Phase Details: Cycle 1 (`c1`) Parent Rebase and CI Fixes for PR #1766 / Issue #116

## Metadata

* Task ID: issue-116-entra-output-0052-c1
* Task slug: issue-116-entra-output-0052-c1
* Related plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-research.md

## Phase Index

| Phase ID | Name                                                                            | Status   | Detail sections |
|----------|---------------------------------------------------------------------------------|----------|-----------------|
| P01      | Rebase Onto Updated Parent Branch (`#164` / `PR #1761`)                         | Complete | P01, P01-T01    |
| P02      | Fix PR #1766 Content Standard and Author Review Record Projection Failures      | Complete | P02, P02-T01    |
| P03      | Focused Regression Coverage and Validation                                      | Complete | P03, P03-T01    |

<!-- rpi:phase id=P01 -->
## P01: Rebase Onto Updated Parent Branch (`#164` / `PR #1761`)

### Context

Research (`C1`, `C2`) verified that `origin/feat/demo-164-chat-grounding-provenance-0900` advanced from `9a0dd54fa` to `7f83f4749` (`02ab20cac` `#1753` and `7f83f4749` `#1761`). Note that while unpushed `.copilot-tracking/` files must be safe during `git rebase`, any uncommitted `c1` `.copilot-tracking/` files should be temporarily moved aside (or stashed / backed up in the session workspace) before running `git rebase origin/feat/demo-164-chat-grounding-provenance-0900` and restored immediately after rebase completes so `git rebase` starts on a clean working tree.

### Intent

Rebase `feat/ai-116-entra-output-0052` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`), preserving every `#164` and `#116` change.

### Boundaries

* Included: `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, conflict resolution in both `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_ai_tasks.py` (`Endpoints`), and restoring the active `c1` `.copilot-tracking/` artifacts afterward.
* Excluded: Force-pushing or touching any remote branch.

### Likely Targets

* `src/api/src/zava_forward/api/server.py`: `/api/ai/report` imports (`from zava_forward.agents import ai_eval, chat_eval`) and JSON payload (`"evaluation": ai_eval.run_eval(), "chat_evaluation": chat_eval.run_eval(), "live": s.ai_live_report(u), "registry": ai_registry.registry(), "consumption": consumption`).
* `src/api/tests/test_ai_tasks.py`: Keep both `#164` `Endpoints` chat-report tests (`test_report_separates_chat_multi_turn_evaluation_from_single_turn_evaluation` and `test_report_chat_failure_does_not_alter_single_turn_results_and_live_stays_disabled`) and `#116` `TasksMixin` / `Endpoints` role-visibility tests.

### Dependencies

* None.

### Validation Expectations

* `git status` shows rebase complete on `feat/ai-116-entra-output-0052` with `origin/feat/demo-164-chat-grounding-provenance-0900` as direct ancestor.

### Completion Evidence

* Clean rebased commit history atop `7f83f4749`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase branch onto `origin/feat/demo-164-chat-grounding-provenance-0900` and resolve `/api/ai/report` overlap

#### Context

In `src/api/src/zava_forward/api/server.py`, `7f83f4749` (`#1761`) changed `from zava_forward.agents import ai_eval` to `from zava_forward.agents import ai_eval, chat_eval` and formatted `/api/ai/report`'s `self._json(200, ...)` block with `"chat_evaluation": chat_eval.run_eval()` and `"live": s.ai_live_report()`, whereas `09416f614` (`#116`) changed `"live": s.ai_live_report()` to `"live": s.ai_live_report(u)`.

#### Intent

Temporarily move active untracked `c1` `.copilot-tracking/` files to `/home/azureuser/.copilot/session-state/a11ca27c-12dd-430f-ae05-7850842d627c/files/c1-backup/` so the working tree is clean, run `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, resolve conflicts in `src/api/src/zava_forward/api/server.py` (preserving `"chat_evaluation": chat_eval.run_eval()` and `"live": s.ai_live_report(u)`) and `src/api/tests/test_ai_tasks.py` (`Endpoints` immediately before `test_mode_flag_and_review_over_http`, preserving `#164`'s two chat-evaluation report tests alongside `#116`'s tests), finish `GIT_EDITOR=true git rebase --continue`, and restore the `c1` `.copilot-tracking/` files.

#### Boundaries

* Included: `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_ai_tasks.py`.
* Excluded: Unrelated files from `#1753` or `#1761`.

#### Likely Targets

* `src/api/src/zava_forward/api/server.py`
* `src/api/tests/test_ai_tasks.py`

#### Dependencies

* None.

#### Validation Expectations

* `git merge-base --is-ancestor origin/feat/demo-164-chat-grounding-provenance-0900 HEAD` exits `0` and both `#164` and `#116` tests in `test_ai_tasks.py` exist without conflict markers.

#### Completion Evidence

* Rebase completed cleanly onto `7f83f4749`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Fix PR #1766 Content Standard and Author Review Record Projection Failures

### Context

Research (`C3`-`C7`) reproduced both hosted CI failures locally:
1. `CopyAudit.test_ai_label_is_exact_and_never_implies_approval` in `src/api/tests/test_content_standard.py` fails because `src/core/src/zava_forward/core/data_protection.py:233` contains `"human-approved"`.
2. `HumanReviewEffectiveness223Tests.test_blank_worksheet_has_no_spoilers_and_human_sessions_pool_safely` in `src/core/tests/test_human_review_effectiveness_223.py:401` fails (`6 != 7`) because `ai_tasks._record_view` replaces a `Retrofit Coordinator` reviewer's own `override_text`, `reviewer_reason`, and `review_evidence["reason"]` with `projection.NOTE_HELD`.

### Intent

Apply surgical fixes in `data_protection.py` and `ai_tasks.py` so content-standard and human-review-effectiveness invariants pass without weakening role/field-level visibility enforcement.

### Boundaries

* Included: `src/core/src/zava_forward/core/data_protection.py` and `src/core/src/zava_forward/core/ai_tasks.py`.
* Excluded: Modifying `projection.DEFAULT_REASON_ROLES` or `human_review_effectiveness.py`.

### Likely Targets

* `src/core/src/zava_forward/core/data_protection.py`: `validate_necessity_exception` docstring (line `233`).
* `src/core/src/zava_forward/core/ai_tasks.py`: `_record_view(store, user, rec)` (lines `262-308`).

### Dependencies

* P01.

### Validation Expectations

* `test_content_standard.py` and `test_human_review_effectiveness_223.py` pass with `0` failures and `ruff format --line-length 100 --check` passes in `src/core`.

### Completion Evidence

* Both targeted CI test suites pass locally.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Replace `'human-approved'` with `'human-authorized'` in `data_protection.py` and preserve author-owned fields in `ai_tasks._record_view`

#### Context

In `data_protection.py:233`, replacing `"""Validate a bounded, human-approved scoped necessity exception for document AI processing."""` with `"""Verify whether a human-authorized text-only derivative may be sent to an external model."""` eliminates `"human-approved"` while staying at `98` columns (`<= 100`). In `ai_tasks.py`, `_record_view(store, user, rec)` projects AI comparison/review records. Computing `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))` lets the review author read back their own `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` while still applying `withheld` and `FORBIDDEN` checks to `ai_output`, `shown_output`, `citations`, `unresolved`, and `review_evidence["compared"]`, and still redacting `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` to `projection.NOTE_HELD` for any non-author viewer lacking visibility.

#### Intent

Update `data_protection.py:233` and `ai_tasks._record_view` with exact `is_author` scoping.

#### Boundaries

* Included:
  * `src/core/src/zava_forward/core/data_protection.py`: Replace docstring at line `233` with `"""Verify whether a human-authorized text-only derivative may be sent to an external model."""`.
  * `src/core/src/zava_forward/core/ai_tasks.py`: Inside `_record_view(store, user, rec)`:
    * Compute `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))`.
    * Keep `ai_output` (`FORBIDDEN` or `withheld`), `shown_output` (`withheld`), `workflow_output` (`withheld`), `citations` (`withheld`), `unresolved` (`withheld`), and `review_evidence["compared"]` (`ai` `FORBIDDEN`/`withheld`, `workflow` `withheld`) checks unconditional for all viewers.
    * Redact `override_text` to `projection.NOTE_HELD` only when `not is_author and out.get("override_text") and projection.contains_withheld_value(out["override_text"], withheld)`.
    * Redact `reason`, `reviewer_reason`, and `review_evidence["reason"]` to `projection.NOTE_HELD` only when `not is_author` and `(not reason_ok or projection.contains_withheld_value(val, withheld))` (matching `ai_tasks.live_report`).
* Excluded: Changing `ai_tasks.live_report` (which continues to redact `reviewer_reasons` across records whenever `not projection.can_see_reason(user)` or matching `withheld`).

#### Likely Targets

* `src/core/src/zava_forward/core/data_protection.py`
* `src/core/src/zava_forward/core/ai_tasks.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `test_content_standard.py` and `test_human_review_effectiveness_223.py` exit `0`.

#### Completion Evidence

* `data_protection.py` and `ai_tasks.py` updated and formatted within 100 columns.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Regression Coverage, Validation, and Clean Local Commit

### Context

Code-change guidelines require adding focused regression coverage for behavior fixed by this change inside existing canonical test files, running the Focused-tier checks, and committing all `c1` RPI artifacts cleanly without pushing.

### Intent

Add a focused unit test in `src/api/tests/test_ai_tasks.py` verifying `_record_view` for both the authoring reviewer (`is_author=True`) and a non-author viewer (`is_author=False`), run all Focused validation checks, complete `rpi-review`, and create a clean frozen commit with the Copilot trailer.

### Boundaries

* Included: `src/api/tests/test_ai_tasks.py`, Focused-tier validation commands, `.copilot-tracking/` `c1` artifacts, repository-local privacy-safe git email config, and local commit.
* Excluded: `tools/rpi-checks.py --all`, Docker builds, `git push`.

### Likely Targets

* `src/api/tests/test_ai_tasks.py`: Add `1` focused test method on `TasksMixin` (exercising both `JsonTasks` and `SqlTasks`).
* `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md`.

### Dependencies

* P01, P02.

### Validation Expectations

* Provision `/home/azureuser/.copilot/session-state/a11ca27c-12dd-430f-ae05-7850842d627c/files/venv` (`python3 -m venv --system-site-packages` + `pip install --no-deps --no-build-isolation -e src/core -e src/agents -e src/api`) and verify every Focused validation command exits `0`:
  1. `<venv>/bin/python -m unittest src/api/tests/test_content_standard.py src/core/tests/test_human_review_effectiveness_223.py src/core/tests/test_data_protection.py src/api/tests/test_ai_tasks.py src/core/tests/test_ai_eval.py src/agents/tests/test_ai_eval.py src/agents/tests/test_chat_heldout.py src/api/tests/test_ai_consumption_api.py -v`
  2. `(cd src/core && <venv>/bin/python -m mypy && ruff check . && ruff format --line-length 100 --check . && ruff check --isolated src/zava_forward/core/data_protection.py && ruff format --isolated --line-length 100 --check src/zava_forward/core/data_protection.py)`
  3. `(cd src/agents && <venv>/bin/python -m mypy && ruff check . && ruff format --line-length 100 --check .)`
  4. `(cd src/api && <venv>/bin/python -m mypy && ruff check . && ruff format --line-length 100 --check .)`
  5. `<venv>/bin/python tools/rename-zava-tests.py`

### Completion Evidence

* Clean local commit on `feat/ai-116-entra-output-0052` with `git status --short` empty.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add `_record_view` author vs non-author unit test on `TasksMixin`, run Focused validation tier, and commit `c1` artifacts

#### Context

Adding a focused test on `TasksMixin` in `src/api/tests/test_ai_tasks.py` ensures `_record_view` preserves author-submitted `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` for a non-reason role (`Retrofit Coordinator`) while still withholding tainted `ai_output` / `shown_output` / `workflow_output` / `citations` / `unresolved` / `review_evidence["compared"]` for the author AND redacting `override_text` / `reviewer_reason` / `reason` / `review_evidence["reason"]` to `projection.NOTE_HELD` for both a non-author non-reason viewer (`Programme Support Officer`) and a non-author `reason_ok=True` viewer lacking resident/finance authority (`Building Safety Liaison`) when those fields carry withheld values.

#### Intent

Add the focused test in `src/api/tests/test_ai_tasks.py` and run all Focused-tier unit, type, lint, format, and rename-regression checks before review and final commit.

#### Boundaries

* Included: `1` new test method in `src/api/tests/test_ai_tasks.py`, Focused-tier validation execution, and final commit preparation after `rpi-review`.
* Excluded: Modifying unrelated test files.

#### Likely Targets

* `src/api/tests/test_ai_tasks.py`

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* Every command in the Focused validation tier exits `0` with `0` lint/format/type errors.

#### Completion Evidence

* Recorded command exit statuses and counts in `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md`.

#### Unresolved Items

* None.
