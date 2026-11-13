# Details: C1 ranking publication review fixes (#79)

## Phase 1: format
* Run `ruff format --isolated --line-length 100 infra/tests/test_bicep_policy.py`. Expected diff: only the `expected_role` dict wrapped near line 1469.
* Verify `--check` and `ruff check` (CI selection `E,F,I,B,UP`, py312).

## Phase 2: SQL-backed store test
* Add `test_sql_backed_store_selected_by_zf_store_publishes_open_cases` to `ScheduledPublicationTests`.
* Write a temp seed JSON with one open and one closed case; call `job.main` with `store=None` and env `ZF_STORE=sqlite`, `ZF_DATA`, `ZF_STATE`, `ZF_AS_OF`, so `factory.open_store` builds a real `SqlStore`.
* Assert exit 0, `RANKING_PUBLISH_OK status=published`, one blob whose snapshot holds only the open case.
* Limit: `MssqlStore` (Azure SQL) is not exercised; it inherits `SqlStore` reads.

## Phase 3: validation commands
* `python3 -m unittest infra/tests/test_bicep_policy.py`
* `src/orchestrator`: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q`, `ruff check`, `ruff format --check`, `mypy`
* `src/core`: `tests.test_scenario_manifest`, `tests.test_needs_inventory`

## Phase 4: cleanup
* Remove `/tmp/venv-79-c1` and untracked `.egg-info` / `build` directories; commit; `git status --porcelain` empty.
