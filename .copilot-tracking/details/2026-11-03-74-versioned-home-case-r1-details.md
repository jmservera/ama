---
title: Issue 74 round 1 details
ms.date: 2026-11-03
---

## Phase 1 and 2

* `record_version(store, user, case_id, metadata)`: staff only, requires integer `expected_version`, plus source, source_version and reason from `change_provenance`. Optional `scheme_id` must exist in `data["schemes"]`. Closed cases are refused. Event carries `links`, `links_sha256`, `stage`, `building_record_version` and the scheme change.
* `view(store, user, case_id)`: sections `home`, `building` (from `buildings.view` minus `homes`), `versions` (newest first), `links`, `scheme`, `changed_since_version`, `notice`. Cost allocation and building costs follow the existing finance-role restriction.
* `SqlStore.DOCS` gains `schemes` so the register persists.

## Phase 3

Tests cover: unrecorded start, retained versions with later links not leaking into earlier ones, conflict refusal, reopen persistence (SQL), invalid scheme/metadata/closed case with no change, sibling home isolation under a shared building ID, role and finance restriction, register validation.

## Phase 4

`ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-74` on the new files; unittest for home_case, buildings, seed_merge, change_provenance.
