<!-- markdownlint-disable-file -->
# Details: pinned-tool validation of recovered #123, 2026-11-09

Plan: [plan](../../plans/2026-11-09/pinned-validation-123-plan.md).

## Phase 1

* `python3 -m venv ~/.venvs/zf123-pinned` (outside the worktree); `pip install ruff==0.17.1 mypy==2.4.0`. Success: `ruff --version` 0.17.1 and `mypy --version` 2.4.0.

## Phase 2 (cwd `src/core`)

* `ruff check .`; `ruff format --check .`; `mypy`.
* `PYTHONPATH=src:tests python -m unittest test_paired_equity test_cohort_eval test_household_conditions test_retrofit_effects test_monitoring_coverage test_rule_engine test_chat_privacy -q`, expecting 146 tests, 0 skips; print `zava_forward.core.__file__` to show current-source imports.

## Phase 3

* `git diff --check`; `git status --short` shows only new tracking files.
