# Changes: #106

* `mvp/zavaforward_mvp/ai_tasks.py`: `source_hashes`, `provenance`, Hold status, `review_evidence`, report column.
* `mvp/tests/test_ai_tasks.py`: provenance/evidence test, changed-source hold test; roundtrip test reordered so its own writes precede the proposal.
* Validation: full suite from `mvp/` ran 484 tests; the only 2 errors were the reorder issue, fixed and re-run on the AI test modules (OK).
