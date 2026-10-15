# Changes: #117

* Added `mvp/zavaforward_mvp/doc_controls.py` (scanners, DocControlsMixin); wired into `store.py`, `sqlstore.py`, `server.py`, `projection.py`.
* Added `zf_document_controls.py`, `mvp/evals/document_control_fixtures.json`, registry entry, `mvp/tests/test_document_controls.py`.
* Amended `mvp/tests/test_mvp.py` line 80: pdf fixture body now has a PDF header (new type check).
* Docs: mvp/README.md, ADR 0002, synthetic-data README, `docs/reference/log.md`.
* Validation: full mvp suite, 530 tests OK (85 skipped).
* Divergence: none.
