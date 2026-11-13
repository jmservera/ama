---
title: Issue 74 criterion 2 shared-building versus per-home separation research
description: Evidence-only static and focused local fixture trace of building-level dependencies, holds, works and costs shown apart from per-home evidence, decision, allocation and outcome
ms.date: 2026-11-13
---

## Scope and disposition

* Issue 74, criterion 2 only. Base main 1f870ec92. Evidence only; no source, test, issue, board or cloud change. Research disposition: executed.
* Excluded as prior exact slices: own-home negative controls (PR 1406) and the null-funding/Unknown question (clean 10e5b87f5; explicit-True projection intentionally maps null/absent/False to not confirmed; no source correction admitted). No building-version retention criterion is invented.
* Recovered history: 16 issue comments read (tail). Latest records: PR 1504 read-only scope display, PR 1506 limitations, 08:15 null-funding closeout. Criterion 2 remains unticked. Finite source-correction history and any renewed grant: UNKNOWN (not recovered, not zero, no grant inferred).

## One data-to-UI trace

1. Fixture `src/core/tests/building_fixture.py`: building SYN-B1 shared by homes ZF-2 and ZF-3; works and costs rows populated; dependencies and holds are empty lists (line 85-87).
2. Domain `buildings.py:36` `record` validates categories systems, dependencies, holds, works, costs (line 10); `buildings.py:156` `view` returns shared rows, removes costs for non-Finance roles (`costs_restricted`), lists homes only with id, stage, closed, and states that home evidence, consent, approvals, allocations and outcomes stay on each home.
3. Home case `home_case.py:119` `view` returns `building` (shared, `homes` removed) and `home` (decision, stage, closed, funding_confirmed, documents, quality, cost_allocation or restricted) as separate keys plus the notice.
4. API serves it at `/api/cases/{id}/home-case`; UI `app.js:1354` renders a separate card titled "Shared at building level, not this home's evidence" (dependencies, holds, works, costs; costs restricted or unknown text at 1360).

## Existing discriminating tests (current source)

* `test_home_case.py::test_shared_building_id_never_transfers_evidence_between_homes` (two homes, SQLite and in-memory stores): building has no documents, quality, decision or cost_allocation; building cost 12000.00 versus ZF-3 home allocation 6000.00.
* `test_buildings.py::test_shared_view_keeps_home_evidence_allocations_and_approvals_home` and `::test_cost_visibility_and_role_denial`.
* API `test_home_case_api.py` lines 71, 130, 143 cover the same split over HTTP (not run here).

## Findings

* Separation of building COSTS from per-home allocation and evidence is proved by existing tests on current source. Works are returned by the same shared view but no selected test asserts the work row (critique finding); works separation is statically read only. API tests assert selected decision and cost fields, not the full split.
* Residual, unproven by this view test: the fixture has empty dependencies and holds, so non-empty building dependency and hold rows rendered apart from per-home keys are not asserted in the home-case view (gate use of holds is covered in `test_explicit_home_and_package_scope_blocks_only_matching_instruction`). Per-home outcome is represented only as stage/closed/quality state; no distinct outcome field exists, and its adequacy is a product decision, not a defect proven here.
* No reproduced defect; no source correction admitted. UI rendering was read statically only; no browser run.

## Limitations

* Browser, API HTTP, accessibility and human acceptance not exercised. Passing core tests is not criterion 2 acceptance.
