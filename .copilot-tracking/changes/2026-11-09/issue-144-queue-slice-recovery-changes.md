# Changes: issue 144 queue-slice recovery (2026-11-09)

* Merged origin/main `b46a9ad9a` into `fix/demo-recovery-144-1109` (seed `1a9616d4e`).
* Cherry-picked `f7cb6dea4` (poison copy bounded by encoded bytes; 2 files in src/agents plus its 2026-11-05 evidence and log entries).

Test evidence (all exit 0 unless noted):

* test_queue_azure 21 OK; test_worker 6 OK; test_dispatch 15 OK; test_dependency_rule 4 OK.
* Full agents suite with `PYTHONPATH=../core/tests`: 300 tests OK. Without it, 2 import errors (test_chat_model, test_regulatory_gates) from the missing core test path, not from this change.
* ruff check, ruff format --check, mypy: clean. No skips, no Azure or model call, no SQL.
