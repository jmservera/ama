<!-- markdownlint-disable-file -->
# Asset and board evidence class: details (2026-11-03)

* Phase 1: in `assetCost`, `passed` also requires `m.evidence_label`; the Evidence class row is `screenValue(m?.evidence_label)`; the Reading row names the evidence class condition.
* Phase 2: `test_missing_evidence_class_is_unknown_and_hides_cost` in `src/api/tests/test_asset_board_screen.py`.
* Phase 3: `src/api/README.md` browser-check paragraph and `docs/reference/log.md`.
* Phase 4: unittest for asset and conformance tests, ruff, mypy.
