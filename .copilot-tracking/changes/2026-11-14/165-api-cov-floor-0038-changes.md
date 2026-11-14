---
title: Issue 165 api and agents branch coverage floor changes
ms.date: 2026-11-14
---

## Changes

* Added `src/agents/tests/test_branch_floor.py` (9 tests).
* Added `src/api/tests/test_auth_branch_floor.py` (12 tests). In isolation `auth.py` reaches 94% branch coverage, up from 48% in the targeted subset run.
* `src/api/pyproject.toml`: added the new test module to the existing mypy `disallow_untyped_calls = false` override.

## Validation

* `ruff check`, `ruff format --check` and `mypy`: clean in `src/agents` and `src/api`.
* `src/core/tests/test_scenario_manifest.py`: 8 tests OK.
* `src/api` suite: 3113 tests OK (623 skipped).
* `src/agents` suite: 445 tests, 8 failures and 7 errors in `test_paired_report_command`, `test_chat_model` and `test_regulatory_gates`. They are identical on the unmodified base, so pre-existing. The new agents tests pass.

## Divergences

* The `/home/azureuser/source/ama/.venv` interpreter is absent; `python3` with worktree `PYTHONPATH` was used.
* No CI coverage floor was added: none exists, and adding one changes gate semantics outside this slice.
* Not pushed.
