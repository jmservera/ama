<!-- markdownlint-disable-file -->
# Review: #1297 correction C3

* Date: 2026-11-09
* Artifacts: .copilot-tracking/research/2026-11-09/sensor-mssql-gate-1297-c3-research.md, .copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c3-plan.md, .copilot-tracking/details/2026-11-09/sensor-mssql-gate-1297-c3-phase-details.md, .copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c3-critique.md, .copilot-tracking/changes/2026-11-09/sensor-mssql-gate-1297-c3-changes.md
* Review execution: Complete
* Outcome: Residual work

## Boundary and reconciliation

Plan P01 is ticked with changes evidence; critique PC-001 to PC-004 dispositions are in the plan; details were updated for the critique. The diff is tools/rpi-checks.py (constant plus exact-path term in changed_groups) and tools/test_rpi_checks.py (two added tests). The review is performed by the implementing agent against the diff and test output; it is not an independent review, which the coordinator must still obtain.

## Validation

* Pinned Ruff 0.17.1 format check and lint, strict mypy: exit 0.
* tools unit tests: 101 tests OK (99 before).
* No SQL, gate or browser run; the C2 receipt does not cover this head.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Transitive imports are not selected

* Evidence: only direct imports are covered. dataset.py imports store.py and workflows.py, so changes to modules such as workflows.py, ai.py or ledger.py can still select project-core without mssql, and the sensor skips are accepted.
* Destination: distinct follow-up; owner cost/coverage policy decision. Alternatives: (A) direct dependencies only, as delivered; (B) selecting mssql for the whole static import closure or all of project-core, which raises focused-run cost; (C) making check_skips require mssql execution, rejected because focused core runs would always fail. Research closure counts (67 of 128 core modules) came from a script and were not independently reproduced; the critic counted 13 unique direct modules, not 17.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Constant is path-specific and static

* Evidence: the AST test fails if a new direct import is not selected, but the constant list is a hand-maintained subset; renames fail closed through the test equality check.
* Destination: accepted residual.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Full-gate evidence for this head is absent

* Destination: coordinator admits a fresh full gate on the new head and verifies the receipt against current origin/main.

## Integration risks

* #184 adds two sensor methods, which would require updating the pinned sensor IDs to ten, and has a separate DEFAULT_TESTS conflict with test_sensor_sql_check; both are out of scope here.

## Adverse observations

* Two edits via a bash Python one-liner; a wrong negative api path and an E501 line caught before commit; ignored tools/__pycache__/ retained.
