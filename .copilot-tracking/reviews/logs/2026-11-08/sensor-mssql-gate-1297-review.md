# Review: issue #1297 sensor MSSQL gate

* Task: sensor-mssql-gate-1297. Date: 2026-11-08. Reviewer: implementing agent's single in-task Review (self-review; independent exact-head review is still required and is not claimed).
* Artifacts compared: .copilot-tracking/plans/2026-11-08/sensor-mssql-gate-1297-plan.md, .copilot-tracking/details/2026-11-08/sensor-mssql-gate-1297-phase-details.md, .copilot-tracking/plans/2026-11-08/sensor-mssql-gate-1297-critique.md, .copilot-tracking/changes/2026-11-08/sensor-mssql-gate-1297-changes.md, .copilot-tracking/research/2026-11-08/sensor-mssql-gate-1297-research.md, git diff of tools/rpi-checks.py and tools/test_rpi_checks.py.
* Review execution: Complete for the local boundary (source diff, focused tests). Evidence boundary excludes actual SQL, project-core full discovery, full gate, hosted CI.
* Outcome: Residual work (no open defect found in the boundary; acceptance criteria requiring SQL, full gate, independent review and CI remain unmet and are routed).

## Acceptance criteria assessment

* AC1 exact exception: met locally. check_skips accepts the reason only for group project-core, non-integration, exact pinned pair; reason not in EXPECTED_SKIP_REASONS. Tested with altered group, integration, ID, reason, class; real flag-less sensor log accepted only in project-core.
* AC2 required dispatch and receipt verification: met locally by unit tests. Matrix and Runner.sql run the sensor module after SQL_SELECTORS with ZF_SENSOR_MSSQL=1; command() and verify_commands require eight verbose ok headers once, count eight, zero skips; tampering of argv, env, cwd, missing command, counts, skips and log evidence rejected. Actual execution on SQL not demonstrated.
* AC3 named test: pinned and asserted; actual MSSQL pass not demonstrated here.
* AC4 existing checks preserved: existing SQL_SELECTORS argv and env unchanged and asserted; tools suite 97 tests OK; ruff and strict mypy clean.
* AC5 full gate, independent review, hosted CI: not performed (coordinator).

## Findings

* RV-001 (Medium, residual, destination: distinct follow-up in #184 delivery): pinned set is the eight tests on main; the #184 candidate has ten (two inherited weather tests). Evidence: git diff fa7ae0c 57d1527 on test_sensor_analysis_store.py. #184 must extend SENSOR_MSSQL_REQUIRED_TESTS deliberately or its full gate will fail closed.
* RV-002 (Medium, residual, destination: #184 / separate issue): sensor_sql_check.DEFAULT_TESTS expansion conflicts with main's test_sensor_sql_check; untouched here by instruction.
* RV-003 (Medium, residual, destination: coordinator heavy validation): actual SQL execution, project-core discovery output and verified full receipt are unobserved. Plan: --all full gate on the frozen commit and verify-receipt; expect the mssql group sensor command Ran 8 with no skips and project-core eight enumerated discovery skips.
* RV-004 (Low, residual): earlier full receipts (including the failed #184 receipt) will not verify against the new matrix by design; they are preserved untouched.
* RV-005 (Low, process, adverse): the environment's editable zava_forward install resolves to the primary checkout; tests that import it here may exercise primary source. New tests avoid imports. Gate runs use snapshot installs.
* RV-006 (Low, process, adverse): two file writes used python from bash instead of the edit tool; startup attempt explored source before activating rpi-research. Preserved in changes record.
* RV-007 (Low, residual): the sensor suite resets shared tables and cases in rpi_disposable; it runs last in the group so existing suites are unaffected. If a later suite is appended after it, revisit.

## Routing

* RV-001, RV-002: #184 owner via rpi-plan/rpi-implement when rebasing.
* RV-003: coordinator-admitted heavy validation, then independent exact-head review and hosted CI.
* Others: no action beyond recording.

## Validation evidence

* tools tests Ran 97 OK (/tmp/rpi1297-tools-tests.log); ruff clean; mypy --strict clean; flag-less sensor module Ran 8 skipped=8 exit 0.
