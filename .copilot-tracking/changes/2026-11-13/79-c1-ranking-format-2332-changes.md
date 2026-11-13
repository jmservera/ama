# Changes: C1 ranking publication review fixes (#79)

* `infra/tests/test_bicep_policy.py`: ruff-formatted (wrapped the 124-character `expected_role` dict); no behaviour change.
* `src/orchestrator/tests/test_ranking_publish.py`: added `test_sql_backed_store_selected_by_zf_store_publishes_open_cases` (real SQLite `SqlStore` through `ZF_STORE=sqlite`; the MSSQL variant needs Azure SQL and stays unproven).
* Plan details file added. Original `79-ranking-snapshot-retention-2122-*` artifacts unchanged.
