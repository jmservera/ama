# Changes: issue 1297 rpi-checks skip allowlist and env wiring

Plan: .copilot-tracking/plans/2026-11-16/issue-1297-fix-plan.md. All four plan phases implemented; no divergence from the plan or critique.

* tools/rpi-checks.py: `DISCOVERY_SKIPS` per group exact (module.Class, reason) pairs replace the reason-only and chat-only logic through `skip_allowed`; `required_classes` and `_classes_executed` demand zero skips and at least one ok test per pinned class; new required steps in the plan and the Runner: SQL opt-in classes with `ZF_STAFF_INTAKE_MSSQL`, `ZF_SENSOR_MSSQL`, `ZF_SENSOR_DRAFT_MSSQL`; browser Chromium classes with `ZF_BROWSER_TESTS=1`; staff intake axe class with `ZF_AXE_PATH`; public simulation startup tests in image-api with `ZF_API_IMAGE`; `changed_groups` couples opt-in test modules and infra Bicep paths to mssql, browser and image-api.
* tools/test_rpi_checks.py: fixtures synthesise class evidence; suite count updates; new tests for exact-pair tolerance, class evidence and selection.
* src/README.md: local-only coverage list updated.

Validation: tools tests (106) pass; gate-style ruff, format and mypy --strict pass. Full gate: see the review artifact and the external receipt.

Remaining work: `ZF_RESIDENT_MSSQL` classes (resident decisions, priority order, aftercare) are tolerated by a global reason and executed nowhere; `JsonResidentDecisions` "SQL replay only" is therefore not-applicable only in name. Follow-up.

## Amendment 1 (first gate run findings)

* Skip and execution parsing now merges docstring-test id headers into their result line (`merge_docstring_headers`), so infra `PublicSimulationStartupTests` skips resolve to their class. A regression test covers it.
* The gate holds the shared heavy lock for the whole run. `heavy_lock_or_none()` in `src/api/tests/test_unaccepted_handoff_download_ui.py` honours `ZF_HEAVY_LOCK_HELD=1`, set only in the browser opt-in step of the plan and Runner.
* Observed, not fixed: importer round-trip zip-timestamp flake and a load-induced project-core timeout on 4 CPUs.
