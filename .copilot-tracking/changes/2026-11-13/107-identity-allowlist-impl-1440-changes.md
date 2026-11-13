# Changes: #107 identity-field sanitisation (1440)

Refs #107, #432.

* `ai_consumption.py`: `safe_identity`, `UNVERIFIED_IDENTITY`; `bounded_model` now sanitises (ledger path).
* `assistants.py`: `sanitize_identity` applied in `shape_result`, `complete` (covers post-back); `_settle_meter` passes None for a rewritten model; release check rejects the replacement marker.
* `ai.py`: evidence envelope model/deployment and `out` model sanitised.
* `tests/test_assistants_identity.py`: RED-first tests (26 failures before implementation, all pass after).

Review fix: `sk-` rejected only at a token start or when followed by 16+ key characters, so `task-fast` and `risk-model` stay valid.

Validation: ruff check and format, mypy src (core) clean; core 14 assistant/consumption modules 666 tests OK; api assistant modules 207 tests OK; agents 336 tests OK. The monolithic core discover run exceeded 900 s and was not completed.
