<!-- markdownlint-disable-file -->
# Review: #1297 correction C4

* Date: 2026-11-09
* Artifacts: .copilot-tracking/research/2026-11-09/sensor-mssql-gate-1297-c4-research.md, .copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c4-plan.md, .copilot-tracking/details/2026-11-09/sensor-mssql-gate-1297-c4-phase-details.md, .copilot-tracking/changes/2026-11-09/sensor-mssql-gate-1297-c4-changes.md (no critique; skipped with recorded rationale)
* Review execution: Complete
* Outcome: Residual work

## Boundary and reconciliation

P01 is ticked with changes evidence. The diff adds one path to SENSOR_MSSQL_DIRECT_DEPENDENCIES and one test plus a changed equality assertion. This review is by the implementing agent, not independent; the coordinator must obtain independent exact-head review.

## Validation

* Pinned Ruff 0.17.1 format and lint, strict mypy: exit 0.
* tools unit tests: 102 tests OK.
* No SQL, gate or browser run; no earlier receipt covers this head.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Execution evidence covers observations() only

* Evidence: the profile trace covers the fixture's observations() with no fault and no composed flag. store_at, SqlStore, MssqlStore and test bodies were not traced (they require SQL or the harness), so other non-keyword modules reached only there are not shown. Modules statically imported but not called (household_conditions, retrofit_effects, sensor_stock, stock_fabric, scale_fixture, provenance, sensor_identity) remain unselected. If the fixture later uses composed=True, they become exercised.
* Destination: distinct follow-up; owner cost/coverage policy (closure-wide or project-core-wide mssql selection) or a gate-integrated trace, neither decided here.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Hand-maintained exact-path list

* Evidence: the AST test catches new direct imports and the call-site test catches removal of the indoor_projection call, but new exercised-only dependencies are not auto-detected.
* Destination: accepted residual.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: No gate evidence for this head

* Destination: the coordinator admits a fresh full gate on the committed head and verifies the receipt against current origin/main.

## Integration risks

* #184 overlaps remain out of scope (sensor IDs to ten; DEFAULT_TESTS conflict with test_sensor_sql_check).

## Adverse observations

* E501 comment caught before commit; trace scripts created via bash heredoc under /tmp; ignored tools/__pycache__/ retained; critique skipped.
