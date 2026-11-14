<!-- markdownlint-disable-file -->
# Research: UX design traceability and test-evidence matrix (issue 149)

Date: 2026-11-13. Task slug: ux-design-traceability-149-2328. Branch docs/demo-149-ux-traceability-evidence-2328, base origin/main 3033dc9c21e57c7f86eca3882fffaf7e9a025033, target main.
Research disposition: executed. Planning Readiness: Ready.

## Scope

Issue #149 criteria 3 and 4 (still unticked): "Accessibility, content and usability evidence is recorded as test results, not asserted" and "Design artefacts are traceable to journeys and requirements". Only the local engineering part can be closed here. Human assistive-technology review (#155) and live staff usability trials are `pending human test`; nothing is ticked and no conformance is claimed.

## Non-overlap

Open PRs #1575 and #1576 touch `wcag-conformance-baseline.md`, `docs/reference/log.md` and `panels.js`. They are not edited (panels.js is only read as a test input). The knowledge-base log entry is therefore deferred to a later change after those PRs merge.

## Findings

* `docs/reference/research/ux/information-architecture-navigation.md` does not exist. The matrix goes in `design-system.md`, which already holds the verification section and `test_design_system.py` guards its token content.
* Role screens registered in `role-screens.js` (13 ids): asset-board, programme-queue, technical-queue, quality-queue, resident-choice, safety-lead, hazard-triage, data-operator, procurement-packages, contractor-job-pack, finance-invoices, finance-funding, resident-service-issues. `atlas-screen-trace.md` already traces perspectives to screens but has no requirement IDs or test references, and no check that cited tests exist.
* Requirement IDs: PRD SA-001 to SA-010 (table near line 549), NFR-001, AC-034 to AC-043; BRD NFR-008, NFR-009 (verified present by grep).
* Existing evidence modules (verified names): `test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, `test_design_system.py`, `test_production_ux_acceptance_protocol.py`, per-screen modules, and core `test_atlas_screen_trace.py`, `test_scenario_manifest.py`, `test_needs_inventory.py`.
* Human gates: `usability-test-programme-plan.md` results record is blank; `production-ux-acceptance-protocol.md` and the baseline record AT as Not run.

## Decision

Add a machine-readable Journey -> Requirement -> Design artefact -> Web surface -> Automated test -> Human evidence table to `design-system.md`, and a test that parses it and checks each reference resolves (files, role-screen ids, panel functions, API routes, test class and method via AST, requirement IDs in PRD/BRD) and that every row's human column starts with `pending human test`.

## Follow-ups

* Append the knowledge-base log entry once #1575/#1576 merge.
* Human AT run (#155) and staff usability sessions stay open owner work.
