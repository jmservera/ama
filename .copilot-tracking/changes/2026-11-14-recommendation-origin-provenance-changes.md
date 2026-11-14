# Changes: recommendation origin provenance (Refs #104, #164)

Date: 2026-11-14.

* `src/core/src/zava_forward/core/ai_tasks.py`: `DECISION_RULE`, `GENERATIVE_MODEL`, `origin_of`.
* `src/core/src/zava_forward/core/store.py`: `_rec_view` adds `origin`, `ordering_origin`, `reason_origin`, deterministic `origin`.
* `src/agents/tests/test_recommendation_origin_provenance.py`: 3 tests.

Validation: new tests pass (3); ruff check, ruff format --check and mypy pass in `src/agents`. The editable install resolves `zava_forward.core` to the main checkout, so tests ran with `PYTHONPATH=../core/tests:../core/src:src` to exercise worktree sources. `test_epic104_bounded_ai_invariants` fails to import `heldout_freeze_fixture` under module invocation, same without the change. The full api suite was started but stopped before completion (long-running); not claimed. Hosted CI and the full gate were not run (focused tier).

## Cycle 1 correction (1 of 5)

Independent review verdict FAIL (Major: no executed proof; Minor: `origin_of` placed before `QUARANTINED` without blank lines and untyped; process: PYTHONPATH workaround).

* `ai_tasks.py`: moved `origin_of` below the constants with the standard spacing and added `source: str | None) -> str` annotations.
* Validation from an isolated venv (`--system-site-packages`, `pip install --no-deps -e src/core -e src/agents`), so no `PYTHONPATH` workaround for core/agents. Resolved `zava_forward.core` to the worktree.
  * `src/agents`: `unittest tests.test_recommendation_origin_provenance` 3 OK; `tests.test_ai_eval` 20 OK; `ruff check .`, `ruff format --check .` (54 files), `mypy` (58 files) pass.
  * `src/core`: `ruff check .`, `ruff format --check .` (254 files), `mypy` (307 files) pass.
  * `src/api`: `test_ai_boundary` and `test_ranking_policy` 19 OK (tests dirs on `PYTHONPATH` as the api README directs). No web/aria-invalid files touched, so the accessibility baseline test was not needed.
* Not run: full suites, hosted CI, full gate.
