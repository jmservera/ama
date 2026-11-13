---
title: Issue 96 saved Held export freshness check details
description: Phase details for the saved-export check route
ms.date: 2026-11-12
---

## Phase 1: route and guard

* In the POST dispatch condition at `server.py` (the `len(parts) == 4` form clause) add an alternative: `len(parts) == 7`, `parts[:2] == ["api","cases"]`, `parts[3] == "form-review"`, `parts[5:] == ["held-export","freshness"]`.
* In `_forms`, handle `len(parts) == 7` before the existing `len(parts) == 6`: 404 when `held_download_enabled` is false; 400 unless `body` is a dict whose `draft_id` equals `unquote(parts[4])`; call `form_export.export_freshness(app.store, user, unquote(parts[2]), body)` and return 200 JSON with `Cache-Control: private, no-store`.
* `body` may be a non-dict (parsed JSON list); check type first.

## Phase 2: tests

* New `src/api/tests/test_form_saved_export_check_api.py` on `staging.FormApiFixture`: default-off and trusted-proxy 404; Current for a fresh export with no state change; Stale naming only the dependent fields after a source version change with unaffected listed; edited copy and legacy history-less copy Invalid; mismatched draft id and non-object body 400; unauthorized actor refused; store state unchanged; GET not served on the path.
* Inventory: add the route to `POST_ENDPOINTS` and a source-string assertion.

## Phase 3: docs and validation

* README subsection after the Held download section.
