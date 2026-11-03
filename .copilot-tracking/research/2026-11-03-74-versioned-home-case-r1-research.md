---
title: Issue 74 round 1 research
ms.date: 2026-11-03
---

Research disposition: executed. Planning Readiness: Ready.

## Prior delivery checked

* No merged PR names #74 as its subject. Searches for "Refs #74" returned only unrelated PRs.
* Issue #75 (closed) delivered building-level shared systems, dependencies, holds, works and costs: `src/core/src/zava_forward/core/buildings.py`, `src/core/tests/test_buildings.py`, `src/api/tests/test_buildings.py`, `GET /api/buildings/{id}`. Shared items carry explicit `case_ids` and `package_ids` scope; a shared building ID never satisfies a home's gates (existing tests).
* Existing per-case versioning: work orders (`versions`), handoff history, document versions, row versions in the SQL store. No version on the home case itself, no scheme link anywhere (no `scheme` in src), no retained prior versions of the case's links.

## Criteria status before this slice

* 1 Home case version and links: not met (building_id, contractor and work orders exist but are not versioned or gathered).
* 2 Building-level items shown apart from home evidence: largely met by #75 on the building screen; no single home-case view puts them side by side.
* 3 Shared building ID never transfers evidence or approval: met by #75 gates and tests; not asserted on a home-case view.
* 4 Prior versions retained: not met.

## Slice choice

Core-only: a `home_case` module reusing `change_provenance.operation` (actor, source, reason, audit, SQL and JSON atomicity). Adds a recorded version with explicit links and retained history, a scheme register, and a staff view that keeps home facts, shared building context and versions apart. Touches `sqlstore.DOCS` (persist `schemes`), so SQL tier applies: the coordinator runs the gate.

## Constraints kept

Human approval and resident consent are not touched; recording a version is not an approval. No AI feature. Manual path: the existing case and building screens. Fluent 2, WCAG and plain-language content apply to the later web slice; no web files changed.
