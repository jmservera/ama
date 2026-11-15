# Details: C1 correction

## Phase 1
* `git fetch origin main`; `git rebase origin/main`; conflict only in `src/api/tests/test_role_endpoint_inventory.py`.

## Phase 2
* `src/api/tests/test_list_export_inventory.py`: single-backslash regex with a positive self-check and a link count; exact column-order assertion for the concern row.
* `src/importer/src/zava_forward/importer/xlsx.py`: `safe_cell` also neutralises prefixes after leading whitespace. New `src/importer/tests/test_xlsx_safe_cell.py` also compares with `list_export.safe_cell`. Core already has a whitespace test in `src/core/tests/test_list_export.py`.

## Phase 3
* `src/api/src/zava_forward/api/server.py`: `proposal_export_row`; law rows gain `review_status`, `reviewed`, `authority_type`, `official_url`, `supersession`. Tests in `test_list_export_inventory.py` (`ExportRowContracts`).
