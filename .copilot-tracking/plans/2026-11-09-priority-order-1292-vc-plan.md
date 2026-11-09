<!-- markdownlint-disable-file -->
# Plan: issue 1292 validation correction (2026-11-09)

Research: [research](../research/2026-11-09-priority-order-1292-vc-research.md). Details: [details](../details/2026-11-09-priority-order-1292-vc-details.md). Critique: [critique](2026-11-09-priority-order-1292-vc-critique.md). Owner-selected demo-targeted tier (modified and impacted tests, no blanket full gate); hosted CI and independent exact-head review remain mandatory. Correction cycle 5 of 5 (default budget).

* [x] Phase 1: reproduce controls on archived `9814cf6` and frozen-start sources (selector only) on an owned SQL Server under nonqueued shared-lock admission.
* [x] Phase 2: add `JsonResidentDecisions.reseed` and `MssqlResidentControls.create_owned_database`/`reseed`; use it in the one test; add the `type: ignore[assignment]` in `MssqlBeginRecovery.adapter`.
* [x] Phase 3: restore API dev dependencies (done in the environment, recorded), rerun the 7 modules and the API discover command.
* [x] Phase 4 (executed; one structural JSON-only skip in the resident MSSQL class disclosed): owned SQL Server run: `test_priority_order` (93), `test_resident_decisions` MSSQL class and the corrected selector 10 times, plus SQLite/JSON; pinned ruff 0.17.1 and mypy 2.4.0 (`mypy` whole-package config); import provenance.
* [x] Phase 5: records, review (once), local commit; handoff.

Stop conditions: any assertion, expected value, skip, production-file or private-data change; SQL or lock unavailable (record blocked, keep the failure visible); a production-cause failure after the fixture is corrected (stop, return a separate fix draft). No push, issue, board or PR change.
