# Changes: C1 correction of the #80 list-export candidate

* Rebased `feat/demo-80-every-list-export-2035` onto origin/main `f427b8c4e` (contains `9c8c898`). One conflict, `src/api/tests/test_role_endpoint_inventory.py`: kept `proposal-freshness` and every new CSV route.
* `src/api/tests/test_list_export_inventory.py`: working regex (single backslashes) with a positive self-check and a link count; exact column-order assertion replaces the tautology; new law-row and proposal-row contract tests.
* `src/importer/src/zava_forward/importer/xlsx.py`: `safe_cell` neutralises formula prefixes after leading whitespace, as core does. New `src/importer/tests/test_xlsx_safe_cell.py`.
* `src/api/src/zava_forward/api/server.py`: law CSV adds `review_status`, `reviewed`, `authority_type`, `official_url`, `supersession`; proposals CSV adds `epoch_current`, `relied_on`, `source_state`, `source_verified`, `source_verified_at`, `review_decision`, `reviewed_at` via `proposal_export_row` (no reviewer names, notes, outputs or snapshots).
* No divergence from the plan. Critique run once; no re-critique.
