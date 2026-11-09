<!-- markdownlint-disable-file -->
# Details: issue 1292 validation correction (2026-11-09)

## Phase 2 edits (test files only)

* `src/core/tests/test_resident_decisions.py`
  * `JsonResidentDecisions.reseed(data, name)`: write the seed to `tmp/<name>/synthetic.json`, set `self.path`, `self.store = self.open_store()`. JSON and SQLite behave exactly as the previous inline code (new file, new SQLite path).
  * `MssqlResidentControls`: keep one admin connection (`self.admin`), extract `create_owned_database()` (UUID `zf_resident88_*` name, `CREATE DATABASE`, cleanup that drops exactly that database, `ZF_SQL_DATABASE` set), call it from `setUp`, and override `reseed` to create a fresh owned database before delegating. Cleanup order is last in, first out, so each store closes before its database is dropped.
  * `test_challenge_edited_in_case_outside_generation_candidates` calls `self.reseed(data, "edited-in")` in place of the four rewrite lines. Every assertion is unchanged.
* `src/core/tests/test_priority_order.py`: `# type: ignore[assignment]` on `conn.driver = types.SimpleNamespace(...)`.

Why this preserves the semantics: the generation-cap state under test (the seed plus 41 appended copies of the already-submitted ZF-1 case, 40 candidates, an edit adding a case outside them, a challenge against the retained human edit) is built by the test and its assertions are unchanged. The only state discarded is the setUp seed and design submission of the first database, which the JSON and SQLite backends already discard for this test (new file, new SQLite path); no generation, version or proposal state is reseeded away.

## Phase 3

Environment only: `pip install -e "src/api[dev]"` in the worktree `.venv` (dev extra pins `playwright==1.64.0`, `ruff==0.17.1`, `mypy==2.4.0`). `playwright` import was the sole cause of all 7 errors.

## Commands (from `src/core` unless stated; `PYTHONPATH=tests:../agents/tests` for core)

* Control: `python -m unittest -v test_resident_decisions.MssqlResidentControls.test_challenge_edited_in_case_outside_generation_candidates` with source and tests from `9814cf6`, from the frozen start, and from the corrected tree.
* Core: `test_priority_order` (SQLite/memory then MSSQL, 0 skips), `test_resident_decisions` (JSON/SQLite classes, then MSSQL class), corrected selector x10, adjacent SQLite suite used before.
* API: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q`; seven modules by name with `PYTHONPATH=tests:../core/tests:../agents/tests`.
* Static: `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/api` with ruff 0.17.1 and mypy 2.4.0.
