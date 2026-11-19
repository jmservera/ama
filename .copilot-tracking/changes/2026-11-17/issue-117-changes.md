# Changes: issue 117

* Added docs/design/document-scan-retention-legal-hold.md.
* Added tools/test_document_controls_design.py (drift guard).
* Index row in docs/reference/README.md; entry in docs/reference/log.md.

## Validation (FOCUSED)

* Baseline measured: docs/design absent; new test with doc removed: 4 errors (red).
* `python3 -m unittest tools.test_document_controls_design`: 4 tests OK (green).
* `ruff format --isolated --line-length 100 --check tools/test_document_controls_design.py`: pass.
* src/core and src/api tests, mypy: not applicable, no src change. rpi-checks --all not run (gate lock honoured, FOCUSED tier).
* Witness: plan-done and implement-start were first refused (missing critique and changes artifact pointers in state), then accepted after the state was corrected; refusals retained in the witness log.
