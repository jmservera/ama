<!-- markdownlint-disable-file -->
# Details: issue 165 criteria audit

## Phase 2

* Create /tmp/venv-165-1531 with --system-site-packages; pip install -e src/core src/agents src/api as needed (pip only, never uv).
* Core (from src/core): python3 -m unittest on test_needs_inventory, test_stock_register, test_stock_fabric, test_sensor_stock, test_stock_reconciliation, test_synthetic_provenance, test_generator_coverage, test_scenario_manifest, test_generated_dataset (EPC generation/conflicts).
* API (from src/api): PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_stock_reconciliation_api.
* Record exact commands, counts and failures.

## Phase 3

* One row per literal criterion: PROVEN or NOT FULLY PROVEN, exact file:line, missing human/AT/policy gate.
* State the EPC-conflict framing mismatch and that no code was changed.
* Criteria 1, 2, 4 and 5 are NOT FULLY PROVEN (human or open-child gates; bounded checks cannot prove all data). Criterion 3 is scoped to recorded rows SN-01..SN-13.
* Cite live issue state with the 2026-11-13 gh retrieval, separate from commit-pinned file:line evidence.

## Phase 4

* Remove /tmp/venv-165-1531, git diff --check, independent code-review, commit with trailer, witness steps.
