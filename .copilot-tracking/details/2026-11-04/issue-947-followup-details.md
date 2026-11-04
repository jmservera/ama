<!-- markdownlint-disable-file -->
# Details: issue 947

* Phase 1: `src/core/src/zava_forward/core/ledger.py` `read_year_digests`; `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` `publish`.
* Phase 2: `src/core/tests/test_recovery.py::test_non_object_digest_file_is_unreadable_and_fails_closed` (null, list, scalars; asserts the marker, `intact` false and `bad_digests`); `src/orchestrator/tests/test_digest_blob.py::test_non_object_year_digest_file_is_skipped_not_raised`.
* Phase 3: unittest for `tests.test_recovery` and `tests.test_digest_blob`, ruff check, mypy with `--cache-dir=/tmp/mypy-946`.
