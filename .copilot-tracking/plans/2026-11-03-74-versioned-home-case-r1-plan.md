---
title: Issue 74 round 1 plan
ms.date: 2026-11-03
---

## Stacked slices

1. This PR: core versioned home case, scheme register, view and tests (Refs #74).
2. Later: API routes (GET view, POST record version) with role and conflict tests.
3. Later: web screen with version history, Fluent 2, keyboard and 200% zoom checks.
4. Later: versioning of building records themselves and automatic capture.

## Phases for slice 1

* [x] Phase 1: `home_case.py` with `record_version`, `view`, `links`, `schemes`; Store delegates.
* [x] Phase 2: add `schemes` to `SqlStore.DOCS`.
* [x] Phase 3: `test_home_case.py` on JSON and SQL stores.
* [x] Phase 4: README section, ruff, mypy, focused tests.

## Critique (executed once)

* Verdict: compatible with changes, applied directly.
* Reuse `change_provenance.operation` instead of a bespoke writer. Applied.
* Optimistic `expected_version` is required so concurrent writers cannot silently fork versions. Applied.
* Do not copy free text or resident details into frozen links (IDs and statuses only). Applied.
* Do not add an API or UI in this slice; keep it small. Applied.
* No confirmed user decision was contradicted; no user question needed.
