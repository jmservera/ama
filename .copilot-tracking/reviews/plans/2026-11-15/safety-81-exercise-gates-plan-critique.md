<!-- markdownlint-disable-file -->
# RPI Plan Critique: PR #1797 c2 Cross-PR Continuity SQL Gate Fix (Refs #81)

## Metadata

* Task ID: safety-81-exercise-gates-c2
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/safety-81-exercise-gates-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/safety-81-exercise-gates-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Remediate the `c2` cross-PR (`#122` / `#220`) `sqlite3.IntegrityError: continuity SQL gate mismatch` failure in `Assistants.challenge()` (`src/core/src/zava_forward/core/assistants.py:4064-4067`) on branch `feat/safety-81-exercise-gates` (`PR #1797` targeting `feat/demo-164-chat-grounding-provenance-0900`), run Focused validation across `src/core`, `src/api`, and `tools/rename-zava-tests.py`, record `c2` rework in `.copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/safety-81-exercise-gates-review.md`, and commit locally without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-15/safety-81-exercise-gates-research.md` (`C1`-`C8`), `.copilot-tracking/plans/2026-11-15/safety-81-exercise-gates-plan.md`, `.copilot-tracking/details/2026-11-15/safety-81-exercise-gates-phase-details.md`, `src/core/src/zava_forward/core/assistants.py` (`1054-1108`, `1935-1948`, `3530-3645`, `3744-4098`), `src/core/pyproject.toml`, `src/api/pyproject.toml`, `src/core/tests/test_challenge_no_retaliation_220.py`, `src/core/tests/test_restart_gate_sql_fences.py`, and `src/api/tests/test_challenge_no_retaliation_api_220.py`.
* Decisions, dependencies, and acceptance criteria considered: Narrow single-DML fix in `Assistants.challenge()` matching `Assistants.review()` (`assistants.py:3638-3641`), preservation of `#122` SQLite and MSSQL `assistant_tasks_gate_update` and `assistant_tasks_hold_update` triggers, actual repository test module paths (`C8`), Ruff `line-length = 100` and `mypy` parity with `.github/workflows/src-ci.yml`, Focused validation tier per caller direction, privacy-safe noreply git identity with `Co-authored-by` trailer, and no remote push.
* Assessment boundary: Evaluates plan and phase-detail completeness, trigger safety across SQLite and MSSQL DDL/DML definitions, lint/format/type configuration behavior, and caller closeout coverage from supplied repository artifacts without live MSSQL server execution or remote CI runs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 / C1-C6                             | Covered  | `P01-T01` updates `Assistants.challenge()` (`src/core/src/zava_forward/core/assistants.py:4064-4067`) to stamp `review_gate_version=?` (`continuity.GATE_VERSION`) and `reviewed_revision=revision+1` alongside `revision=revision+1`, matching `Assistants.review()` (`assistants.py:3638-3641`) with 5 placeholders and 5 bound parameters while preserving `WHERE id=? AND revision=?` optimistic concurrency (`ConflictError`). |
| NFR-1 / C3 / C7                          | Covered  | Preserves `SQLITE_ATTEMPT_TRIGGERS` (`assistants.py:1054-1065`) and `MSSQL_ATTEMPT_TRIGGERS` (`assistants.py:1096-1108`) unchanged. Both SQLite and T-SQL evaluate `SET reviewed_revision=revision+1, revision=revision+1` against pre-update row values (`NEW.reviewed_revision = NEW.revision`), satisfying `assistant_tasks_gate_update` while keeping `assistant_tasks_hold_update` fail-closed when `continuity_open_holds` is active. |
| C4 (Governance isolation)                | Covered  | `Assistants._row()` (`assistants.py:1935-1948`) selects only `body,state,fence,owner,lease_until,attempts,not_before,revision`, and `Assistants.review()` (`assistants.py:3566-3581`) gates verification/acceptance on `body["verification"]` and `not task["stale"]`; stamping `reviewed_revision` never implies human verification or acceptance. |
| NFR-2 / C8 / P02 / P02-T01               | Covered  | Maps shorthand prompt test names to actual repository modules (`tests/test_safety_consent_exercise_scenarios_81.py` in `src/core` and `tests/test_continuity_restart_gate.py` + `tests/test_content_standard.py` in `src/api`) alongside `#220` and `#122` suites, package-local `ruff check .`, `ruff format --check .`, `mypy`, and `python3 tools/rename-zava-tests.py`. |
| P01 / P01-T01 (Ruff `line-length = 100`) | Covered  | Plan requires `<= 100` columns, but `src/core/pyproject.toml:39-47` excludes `assistants.py` from `ruff format` and `E501`; recorded as non-blocking `PC-001` so manual wrapping is verified directly and `ruff format` is not run on the explicit file path. |
| FR-2 (Tracking records & local commit)   | Covered  | Acceptance criteria and `P02-T01` cover `.copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/safety-81-exercise-gates-review.md`, local noreply `user.email`, `Co-authored-by` trailer, clean `git status --short`, and zero remote pushes. |

## Verdict

* Verdict: Pass
* Rationale: The candidate plan and phase details accurately isolate and resolve the cross-PR `#122` / `#220` `continuity SQL gate mismatch` in `Assistants.challenge()` using the canonical `Assistants.review()` DML pattern, preserve both `assistant_tasks_gate_update` and `assistant_tasks_hold_update` across SQLite and MSSQL without governance side effects, correct nonexistent shorthand test paths (`C8`), and match `.github/workflows/src-ci.yml` validation and local-only commit constraints. One low-severity non-blocking hygiene note (`PC-001`) is recorded for finalization/implementation so `line-length <= 100` is enforced without whole-file reformatting of `assistants.py`.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Low]: Explicit `assistants.py` Ruff format/E501 exclusions require manual `<= 100`-char SQL literal wrapping rather than file-targeted `ruff format`

* Related IDs: P01, P01-T01, NFR-2
* Evidence: `src/core/pyproject.toml:39-47`, `.copilot-tracking/plans/2026-11-15/safety-81-exercise-gates-plan.md`, `.copilot-tracking/details/2026-11-15/safety-81-exercise-gates-phase-details.md`
* Concern: `src/core/pyproject.toml` lists `src/zava_forward/core/assistants.py` in both `[tool.ruff.format] exclude` and `[tool.ruff.lint.per-file-ignores]` (`"E501"`). Consequently, pasting the single-line SQL string shown in `P01-T01` (`157` columns at 16-space indent) would exceed `100` columns while `python3 -m ruff check . && python3 -m ruff format --check .` still exits `0`; conversely, interpreting `P01` Likely Targets ("and format within `src/core`") as `python3 -m ruff format src/zava_forward/core/assistants.py` on the explicit file path would bypass directory exclusions and reformat all ~4,100 lines of `assistants.py`.
* Impact: Either a silent `> 100`-character line on the touched statement or an unintended multi-thousand-line formatting diff in a migrated module excluded under ADR 0006.
* Smallest useful change: During plan finalization (`Critique Disposition` / `P01-T01`), note that `Assistants.challenge()`'s SQL literal must be wrapped manually across adjacent string literals within `<= 100` columns and validated only via directory-scoped `python3 -m ruff check . && python3 -m ruff format --check .` (never `ruff format` on `assistants.py` directly).
* Action owner: planning_parent
* Exact resolving evidence: `git diff src/core/src/zava_forward/core/assistants.py` touches only the `Assistants.challenge()` `db.execute(...)` statement with every added line `<= 100` characters, and `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check .)` exits `0`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Exact parity with `Assistants.review()` (`src/core/src/zava_forward/core/assistants.py:3638-3641`): identical SQL column order, `continuity.GATE_VERSION` binding, and `WHERE id=? AND revision=?` optimistic concurrency check.
* Trigger and dialect safety verified directly against `SQLITE_ATTEMPT_TRIGGERS` (`1054-1065`) and `MSSQL_ATTEMPT_TRIGGERS` (`1096-1108`): both SQLite and MSSQL evaluate `reviewed_revision=revision+1, revision=revision+1` from pre-update values so `NEW.reviewed_revision = NEW.revision` holds on every update.
* Early contrarian catch of test module names (`C8`) avoids `unittest` module-import failures while covering `#81` (`test_safety_consent_exercise_scenarios_81.py`), `#122` (`test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`), `#220` (`test_challenge_no_retaliation_220.py`, `test_challenge_no_retaliation_api_220.py`), and `test_content_standard.py`.
* Accepted residual risk: When an operator continuity hold (`continuity_open_holds`) is active for `'all'` or the task's `capability`, `assistant_tasks_hold_update` continues to fail closed with `sqlite3.IntegrityError: continuity scope is suspended` on `'ready'` or `'accepted'` task updates (after any independent `hazard_intake` has already been routed via `self.store.raise_hazard(...)`, preserving zero-hazard-delay). Preserving that fail-closed trigger unchanged is an explicit `#122` invariant (`NFR-1`) and caller non-goal.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* MSSQL `AFTER UPDATE` trigger equivalence is verified by static T-SQL semantics and parity with `Assistants.review()` (`assistants.py:3639`) rather than a live SQL Server instance under this Focused-tier check.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Finalize `.copilot-tracking/plans/2026-11-15/safety-81-exercise-gates-plan.md` to `Approved` with `PC-001` recorded in `Critique Disposition` (manual `<= 100`-column adjacent-literal wrapping in `assistants.py`, directory-scoped `ruff` checks only) and advance to `Implement`.
* User response required: No
