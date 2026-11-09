---
title: Review - #1297 correction C1
date: 2026-11-09
---

Execution: Complete (self-review, local boundary). Outcome: Residual work.

Artifacts compared: research, plan with critique disposition, details, critique and changes record under 2026-11-09, plus the independent Medium finding.

## Reconciliation

P01 is checked with changes evidence. Details match the implementation and critique PC-001 to PC-004 are applied. Acceptance criteria are met at the tool-contract level: sensor core paths select mssql, unrelated paths do not, and the flagged zero-skip command is in the trusted matrix for such a selection.

## Findings

* RV-001 (Medium, residual): no actual SQL, project-core discovery, `--changed` or `--all` gate has run on this head. The prior full receipt (/mnt/ama-gates/g1297-fdf-1108/receipt.json) is historical. Destination: coordinator full gate plus verify-receipt, independent exact-head review, hosted CI.
* RV-002 (Low, residual): over-selection by design. Any core path containing "sensor" (including unrelated sensor tests such as test_sensor_stock.py) triggers the heavier mssql group in focused runs. Accepted as fail-closed.
* RV-003 (Low, residual): shared first-party core modules without sensor, sql or store in the name that the suite uses can still select only project-core. The full gate remains authoritative. Destination: optional follow-up (import-closure-derived selection).
* RV-004 (Low, adverse): ignored tools/__pycache__ left in the worktree (not deleted per instruction); some artifacts written via bash.
* RV-005 (Low, integration): #184 must extend the pinned IDs to ten and resolve the DEFAULT_TESTS conflict with test_sensor_sql_check; the sensor path rule also covers its added files. Out of scope.

No material defects found in the changed code.
