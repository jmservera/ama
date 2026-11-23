# Issue 202 live details, 2026-11-23

* Phase 1: `git rm` both files; edit src-ci.yml lines 5 and 281; recompute src-ci.yml SHA-256 into WORKFLOW_HASHES.
* Phase 2: replace mvp-validation uses in test_pipeline with src-ci only; assert the old files are absent; drop the mssql parity assertion and the legacy-named CI build test (src-ci already asserts src context).
* Phase 3: docs reword to past tense; append log entry. Validation: infra tests, tools tests (test_rpi_checks, test_src_cutover_repoint, test_check_legacy_references), actionlint if present.
