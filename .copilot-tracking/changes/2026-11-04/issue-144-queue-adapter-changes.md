# Changes: issue 144 queue adapter (2026-11-04)

* Added `src/agents/src/zava_forward/agents/queue_azure.py` and `src/agents/tests/test_queue_azure.py` (13 tests).
* `infra/README.md` criterion 1 row and `docs/reference/log.md` updated.

Validation run (from `src/agents`, PYTHONPATH to this worktree): unittest test_queue_azure, test_worker, test_dispatch, test_dependency_rule (39 OK); ruff check and format --check; `mypy --cache-dir=/tmp/mypy-144` over src and tests (44 files, clean). Not run: complete gate, full suites, benchmarks, image build, any Azure call. Security-adjacent: gate left to the coordinator.
