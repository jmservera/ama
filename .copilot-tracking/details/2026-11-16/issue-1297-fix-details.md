# Details: issue 1297

* Phase 1: `DISCOVERY_SKIPS` maps group to exact (module.Class, reason); `check_skips` tolerates them only when `integration` is false. `required_classes(argv)` and `_classes_executed` demand at least one ok test per pinned class and no skips.
* Phase 2: SQL step argv `unittest -v test_staff_intake_api.MssqlStaffIntakeApi test_live_receiver_sql test_sensor_review_draft.MssqlDraftCases` with ZF_STAFF_INTAKE_MSSQL, ZF_SENSOR_MSSQL, ZF_SENSOR_DRAFT_MSSQL = 1. Browser step with ZF_BROWSER_TESTS=1 for five classes; axe step with ZF_STAFF_INTAKE_BROWSER=1 and ZF_AXE_PATH. image-api step runs `test_public_simulation_startup` in infra/tests with ZF_API_IMAGE=tag and REQUIRE_AZ_BICEP=1. infra group tolerates only the four exact skips. Selection: test modules select mssql/browser; infra bicep and the two infra test modules select image-api.
* Phase 3: tests for tolerance, rejection of foreign class/reason, class evidence, plan/Runner parity (existing parity tests), selection.
* Phase 4: run full gate from the task and verify receipt.

Critique (single, self-run): .copilot-tracking/critique/2026-11-16/issue-1297-fix-critique.md
