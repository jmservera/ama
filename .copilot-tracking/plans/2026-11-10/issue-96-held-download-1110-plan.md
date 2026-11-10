---
title: Issue 96 served Held draft download consumer plan
description: Plan for a default-OFF synthetic-demo GET download of the existing Held form export and a funding-screen link
ms.date: 2026-11-10
---

## Objective

Add the first served consumer of `form_export.draft_export`: one GET route and one explicit link on the funding screen. Refs #96 only. No core change, no new authority, synthetic demo only. See the [research](../../research/2026-11-10/issue-96-held-download-1110-research.md) and [details](../../details/2026-11-10/issue-96-held-download-1110-details.md).

## Phases

* [x] Phase 1: server route, guard and view flag (`src/api/src/zava_forward/api/server.py`).
* [x] Phase 2: funding screen link (`src/api/src/zava_forward/api/web/role-screens.js`).
* [x] Phase 3: tests: new API test module, Node render tests, explicit inventory entry.
* [x] Phase 4: dedicated served browser checker with private fixture.
* [x] Phase 5: scoped changed-web review against the fetched Web Interface Guidelines, docs note in `src/api/README.md`, focused validation, handoff.

## Decisions

* Default OFF: route served only with `ZF_FORM_HELD_DOWNLOAD=synthetic-demo-only` and `ZF_DEPLOYMENT_PROFILE=demo` and a non-`trusted-proxy` provider; read per request. Otherwise 404 "Not found.".
* Reuse only: `form_export.draft_export` and its `forms._actor` rights on every request; no new role, capability, override or POST.
* Success: 200, `application/json; charset=utf-8`, `Content-Disposition: attachment; filename="held-form-draft-export.json"`, `Cache-Control: private, no-store`, exact byte length, `X-Content-Type-Options: nosniff` (existing). Body is the unmodified exporter dict as JSON.
* Unavailable export: 409 JSON error, no attachment header.
* Existing `_forms` error mapping is reused (403, 404, 502, 503 safe messages).
* The view GET gains `held_download_enabled: true` only when the route is enabled.
* Screen link is a native anchor with `download`, only when the flag is true, the draft is not Unavailable, and has an id. Text "Download Held draft (unreviewed)" with adjacent note: Not submitted, eligibility Not assessed, file built when requested and may be newer than the version shown (shows screen `input_version`).

## Validation (owner demo focused tier, no blanket gate)

* Targeted: new `tests/test_form_held_download_api.py`, `test_finance_grants_screens`, `test_role_endpoint_inventory`, `test_form_staging_api`, core form export/dependency/review unchanged runs, ruff and mypy on changed Python where configured, `node --check`.
* Dedicated browser checker under the heavy lock, loopback only.
* Frozen areas untouched: #153 app 751, #130 app 1062, #131 resident_decisions, general role/paging/atlas fixtures.

## Risks and limits

* Data provenance is an operator attestation; not enforced by code.
* Browser, axe and keyboard checks are engineering evidence, not assistive technology or WCAG acceptance.
* No human, Finance, Legal, privacy, closure or live acceptance is claimed.
