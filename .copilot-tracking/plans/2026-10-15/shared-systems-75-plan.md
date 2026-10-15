---
title: Building shared systems implementation plan
ms.date: 2026-10-15
---

Task: 75 / shared-systems-75. Parent: full-loop RPI user request.

## Executive Summary

Add a read-only, explicitly scoped building model in core and a staff-facing
building view in api, reusing migrated stores and home workflows. Imported
building records cannot approve a home or allocate costs. Local evidence is
not real SQL Server, model, Azure or human acceptance evidence.

## User Decisions and Requirements

* Follow issue 75 and the 2026-10-15 src pivot; use the specified clean branch.
* Commit research, plan, details, critique, changes and review with the code.
* Preserve consent and independent human gates; use synthetic data only.
* Preserve AI paths, core/workload boundaries, SQL Server portability and Azure-only deployment.
* Run project suites, ruff, mypy and local app checks; record commands/results.
* Push topic branch and open main PR with Refs #75. Do not close the issue.

## Goals

Make shared context inspectable without conflating home evidence, decisions,
allocations or package applicability.

## Scope and Non-Goals

Core model validation/read views, checked-document persistence, scoped blockers,
API/web navigation, synthetic tests and documentation. No building data editor,
hold release, AI approval, live deployment, inferred allocation or real facts.

## Functional Requirements

* A versioned building record contains systems, dependencies, holds, shared works
  and GBP costs with source references. Home links use explicit building_id.
* Affects lists name exact cases; missing applicability remains unknown.
* Home decision, evidence and cost_allocation remain on home records.
* Staff can navigate home/building/home. Existing Finance roles alone see costs;
  contractors and unknown roles cannot view buildings or sibling context.
* Shared blockers are additional to home gates, never a substitute. They block
  affected home advancement and new/reissued work instruction, not hazard intake.

## Non-Functional Requirements

No new dependencies, dialect-specific SQL, workload imports into core, runtime
tracking references, private data or modifications to forbidden paths.
Strict typing/lint on new files; preserve existing migration exemptions.

## Acceptance Criteria

* [x] Building record shows all five shared-context categories.
* [x] Home evidence and allocation stay home, with role-restricted costs.
* [x] Regression proves shared building ID does not inherit approvals.
* [x] Explicit scopes, unknowns, authorization, restart persistence and gate
  behavior verified with synthetic data.

## Phase Checklist

<!-- P01 -->
### P01: Model and integration
* [x] P01-T01: Typed building validation/view/blockers and store persistence.
* [x] P01-T02: API, home/building navigation and financial projection.

<!-- P02 -->
### P02: Evidence and delivery
* [x] P02-T01: Add regression tests and execute local validation.
* [x] P02-T02: Document model, update knowledge index/log and prepare review handoff.

P01 and P02 complete. Administrative publication follows the single Review:
commit reviewed artifacts, push topic and open main PR, with no merge.

## Validation Ownership

Core tests own model, scope, independent gates and SQLite restart tests.
API tests own role endpoint, navigation and HTTP smoke coverage. Remove no tests.
Maximum additions: two test modules and one wholly fictional fixture helper.
Canonical targets are src/core and src/api; no generated production targets.
Run all five source suites, project ruff/format/mypy, JS syntax, local HTTP
smoke, migration regression and Docker permission probe. No mocks count as
real inference or SQL Server. Record failures, skips and remediation.

## Critique Disposition

One final-candidate independent critique executed, verdict Revise. All findings
are compatible planner-owned corrections, applied without a second critique:
PC-001 explicit case_ids/package_ids matching (null unknown, [] none);
PC-002 Finance sees shared costs but never home allocations in building view;
PC-003 mandatory JSON/SQLite reopen and legacy-database tests, no reseed;
PC-004 independent consent/funding/technical/quality/closure/evidence assertions.
Candidate is implementation-ready with those contracts in phase details.

## Follow-Up Items

Real register/owners, live SQL Server/Azure/inference and human UX evidence
remain outside local model acceptance. BRD FR-002 reference mismatch remains
documented in research; do not rewrite the approved source requirements.

## Handoff

Research: .copilot-tracking/research/2026-10-15/shared-systems-75-research.md.
Details: .copilot-tracking/details/2026-10-15/shared-systems-75-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-15/shared-systems-75-changes.md.
