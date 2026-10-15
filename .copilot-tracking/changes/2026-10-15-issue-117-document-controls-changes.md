# Changes: #117

* Added `mvp/zavaforward_mvp/doc_controls.py` (scanners, DocControlsMixin); wired into `store.py`, `sqlstore.py`, `server.py`, `projection.py`.
* Added `zf_document_controls.py`, `mvp/evals/document_control_fixtures.json`, registry entry, `mvp/tests/test_document_controls.py`.
* Amended `mvp/tests/test_mvp.py` line 80: pdf fixture body now has a PDF header (new type check).
* Docs: mvp/README.md, ADR 0002, synthetic-data README, `docs/reference/log.md`.
* Validation: full mvp suite, 530 tests OK (85 skipped).
* Divergence: none.

## Review-fix pass (PR 270 feedback)

* `doc_controls.py`: a missing scan field counts as pending and is rescanned on first read or download (`ensure_scanned`); `rescan_pending` is a job entry point for pending uploads under `ZF_SCANNER=defender`; retention approval and rescan removal now save first and delete the blob only after the save succeeds (record restored if save fails).
* `store.py`: read and download call `ensure_scanned` before `require_clean`.
* Tests added for rescan on read, the job, legacy unscanned documents and save failure. Suite: 535 tests OK (83 skipped).
* Open: Defender enablement and scheduling of `rescan_pending` remain unassigned, so the PR body now says Refs #117.
