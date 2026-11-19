# Issue 107 live plan (2026-11-19)

* [x] Phase 1: add `MssqlAllowance` and `MssqlMaterialMismatch` subclasses (skipped unless ZF_TEST_MSSQL=1) in src/api/tests/test_assistant_restart_non_replenishment.py.
* [x] Phase 2: add composite test `test_old_image_after_a_material_mismatch_cannot_reactivate_or_refill` in `MaterialMismatch`.
* [x] Phase 3: run on SQLite and on a disposable local SQL Server 2022 container; mypy and ruff per src-ci; delete container.
* [x] Phase 4: research note docs/reference/research/issue-107-live-r4-criteria-2026-11-19.md with per-criterion table; index and log.
