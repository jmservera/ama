---
title: Stock fabric link 168 acceptance review
description: One post-implementation review with explicit evidence and residual routing
ms.date: 2026-10-15
---

Task 168 / stock-fabric-link-168. Review execution: Complete (one pass).
Outcome: Defects found. Not accepted as full issue/application delivery.

## Compared Artifacts

* .copilot-tracking/research/2026-10-15/stock-fabric-link-168-research.md
* .copilot-tracking/plans/2026-10-15/stock-fabric-link-168-plan.md
* .copilot-tracking/details/2026-10-15/stock-fabric-link-168-phase-details.md
* .copilot-tracking/plans/2026-10-15/stock-fabric-link-168-critique.md
* .copilot-tracking/changes/2026-10-15/stock-fabric-link-168-changes.md

## Assessed Boundary

P01 and P02-T01/T02 implementation/evidence complete. P02-T03 is review and
authorized topic delivery, intentionally not yet marked complete. Issue criteria
1/2 remain unchecked for actual retained private corpus; criterion 3 has
summary/tests/public documentation. No live app acceptance or owner review.

## Review Method

Parent compares task-wide artifacts and issue/ADR constraints. One independent,
read-only implementation lens examines the new module/tests and migration wiring
for high-confidence correctness gaps; it does not perform another RPI lifecycle,
change source or write a separate review record.

## Findings and Routing

### RV-001: Medium - wheel-installed CLI can miss destination repositories

Action owner: future implementer. Destination: a later `rpi-implement` task.
Evidence: `src/core/src/zava_forward/core/synthetic/stock_fabric.py`,
`_destination`, derives checkout roots from source/cwd ancestors, not resolved
destination ancestors. The independent lens emulated wheel site-packages and
an external cwd; an explicit output under this checkout was accepted, while the
editable-checkout control rejected it. No output was written by that probe.

Impact: default ZF_DATA remains private, and tested editable-source invocation
refuses repo output, but a wheel installed elsewhere can write generated records
inside a destination checkout. The stated general containment guarantee is
incomplete. Resolve by inspecting destination ancestors for repository markers
and adding an installed-wheel/external-cwd regression in the existing test owner.

Disposition: open; do not fix/re-review inside this completed lifecycle.
Publish a draft PR with this defect explicit, not a conformant acceptance claim.

### RV-002: Medium - retained private stock acceptance and owner decisions remain unavailable

Action owner: project owner. Destination: distinct owner-directed research/plan
follow-up for SN-01 private generator or explicit deferral, inventory mapping,
unit-identity semantics and 980-case home-field reconciliation.

Evidence: issue 168 unchecked criteria, inventory SN-01 partial, research C7,
updated synthesis and changes record. The connected 60,000/980 fixture proves
local synthetic behavior only. Do not infer actual private counts, regenerate
private geography, fabricate unit IDs or mark original criteria 1/2 complete.
This is a pre-existing evidence/decision gap, not a new source-code defect.

### RV-003: Medium - live application/image/human evidence remains absent

Action owner: authorized environment operator and human reviewers.
Destination: distinct validation follow-up, beginning with CI image and SQL
checks. Local Docker build failed on socket permissions. API suite skips
97 unavailable SQL Server/Azure-dependent tests. No real inference,
SQL Server/Azure workflow, billable deployment or human acceptance occurred.

The requested data-tool slice leaves existing AI availability, release,
approval and resident consent boundaries unchanged; it does not disable AI or
claim that local templates satisfy mandatory real-AI application acceptance.

## Plan and Critique Reconciliation

P01 and P02-T01/T02 have implementation and command evidence. The seven critique
findings were explicitly accepted and implemented: core owns resolution and
enrichment, non-unit semantics are explicit, one exact 60,000/980 input is used,
invalid identities fail, provenance covers moved dependencies, case metadata
survives closed SQLite restart, and new semantic assertions are in the typed
non-exempt owner. RV-001 exposes an incomplete edge of destination containment,
not an approved divergence. No second critique or Review occurred.

P02-T03 source review is complete, while commit/push/PR remain delivery actions
after this review. No extra implementation phase is authorized by the outcome.
Owner/live follow-ups are outside active scope and stay distinct from RV-001.

## Validation Coverage

Source suites: core 332; API 477 with 97 skips; agents 70; orchestrator 17;
importer 39. Total 935 including skips. All five ruff/format/mypy gates pass.
Final targeted existing/new generator tests: 12 + 7 pass. Migration regressions:
25 pass after restoring documented missing dependencies. Local real HTTP
health/login/case: 200/200/200 with fictional 60,000-home/980-case SQLite seed;
stock linkage/fabric/EPC and source home/resident decision retained.
Markdown local file links and whitespace checks pass. Docker denied.
No validation result overrides the open finding or unavailable acceptance.

## Outcome and Routing

Execution Complete; outcome Defects found, severity summary 0 critical,
0 high, 1 medium implementation defect plus 2 medium acceptance/evidence
residuals. RV-001 routes to later implementation, RV-002 to owner-directed
research/plan, RV-003 to authorized platform/human validation. No conformant
or full issue acceptance claimed; recommended delivery is a draft PR using
Refs #168 with original unmet criteria and RV-001 visible.
