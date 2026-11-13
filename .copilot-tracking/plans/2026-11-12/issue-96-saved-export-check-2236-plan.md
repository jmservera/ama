---
title: Issue 96 saved Held export freshness check plan
description: Plan for a default-OFF synthetic-demo POST that reports which fields of a saved Held export are stale
ms.date: 2026-11-12
---

## Objective

Serve the existing `form_export.export_freshness` read-only so a saved Held copy can be checked for exactly its stale and unaffected fields. Refs #96. No core change, no new authority, no UI, synthetic demo only.

## Phases

* [x] Phase 1: route and guard in `src/api/src/zava_forward/api/server.py`.
* [x] Phase 2: API tests and inventory entry.
* [x] Phase 3: `src/api/README.md` section, focused validation, handoff.

## Decisions

* `POST /api/cases/{case_id}/form-review/{draft_id}/held-export/freshness`, body is the saved export object. Same guard as the download: 404 `Not found.` unless enabled.
* Reuse only `form_export.export_freshness`; it writes nothing and returns `reviewed: false`.
* A body that is not an object, or whose `draft_id` differs from the path, answers 400 and never reaches the comparison.
* Response 200 passes the result through with `Cache-Control: private, no-store`. Invalid, Stale, Current and Unavailable are all 200 results of the check; they are not errors.
* No ticking of C6, no reviewed export, no submission or eligibility claim. Text states the check is a comparison, not an approval.

## Validation (owner demo focused tier)

* Core `test_form_export`, `test_form_dependencies`; API new module, `test_form_held_download_api`, `test_form_staging_api`, `test_role_endpoint_inventory`; `git diff --check`; README link/diff review.
