# Plan: issue 146 workbook cost reconciliation

* [x] Replace the print with a union isfuzzy KQL over `AzureCostExport_CL` and `FocusCost_CL`, same-month and currency match, fallback to Unknown/Unreconciled.
* [x] Adjust the explanatory markdown; keep the 80% actual / 100% forecast not-a-hard-cap note.
* [x] Add `infra/tests/test_monitoring_workbook_cost_reconciliation.py`.
* [x] Validate: JSON, bicep build, infra tests, ruff on new file.

Critique: executed once; compatible findings applied (empty-table fallback via summarize over datatable-seeded unions).
