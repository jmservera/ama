# Changes: 146-workbook-budget-panel-0327 (Refs #146)

* Added `infra/tests/test_ai_observability_workbook_budget.py` (4 tests, pass).
* Validation: `unittest discover -s infra/tests` 589 run, 1 pre-existing error (`zava_forward.orchestrator` not installed in this environment); `az bicep build` ok; ruff check/format clean for the new file. Repo-wide `ruff check/format --check infra/tests` already fails on other files (72 errors, 22 unformatted) before this change.
* Hosted CI not observed; branch not pushed.
