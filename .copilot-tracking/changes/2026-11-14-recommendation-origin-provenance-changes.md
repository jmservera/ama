# Changes: recommendation origin provenance (Refs #104, #164)

Date: 2026-11-14.

* `src/core/src/zava_forward/core/ai_tasks.py`: `DECISION_RULE`, `GENERATIVE_MODEL`, `origin_of`.
* `src/core/src/zava_forward/core/store.py`: `_rec_view` adds `origin`, `ordering_origin`, `reason_origin`, deterministic `origin`.
* `src/agents/tests/test_recommendation_origin_provenance.py`: 3 tests.

Validation: new tests pass (3); ruff check, ruff format --check and mypy pass in `src/agents`. The editable install resolves `zava_forward.core` to the main checkout, so tests ran with `PYTHONPATH=../core/tests:../core/src:src` to exercise worktree sources. `test_epic104_bounded_ai_invariants` fails to import `heldout_freeze_fixture` under module invocation, same without the change. The full api suite was started but stopped before completion (long-running); not claimed. Hosted CI and the full gate were not run (focused tier).
