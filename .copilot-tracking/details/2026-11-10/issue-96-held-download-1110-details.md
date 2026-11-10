---
title: Issue 96 served Held draft download consumer details
description: Phase details for the Held draft download route, link, tests and browser checker
ms.date: 2026-11-10
---

## Phase 1: server

File `src/api/src/zava_forward/api/server.py`.

* Import `form_export` with the existing core import line.
* Add module function `held_download_enabled(provider_name, env=None)`: true only if `env.get("ZF_FORM_HELD_DOWNLOAD") == "synthetic-demo-only"`, `env.get("ZF_DEPLOYMENT_PROFILE") == "demo"` and `provider_name != "trusted-proxy"`.
* GET dispatch: where the form paths are admitted, also admit `len(parts) == 6 and parts[:2] == ["api","cases"] and parts[3] == "form-review" and parts[5] == "held-export"`. Route to `_forms(u, url.path, None)`.
* `_forms`: before the `parts[3]` dispatch, when `len(parts) == 6`: if not enabled return `_json(404, {"error": "Not found."})`; call `form_export.draft_export(app.store, user, unquote(parts[2]), unquote(parts[4]))`; the exporter returns `status == "Held"` on success, so any other status returns 409 `{"error": notice}` with no attachment; else `_send(200, json.dumps(result), "application/json; charset=utf-8", {Content-Disposition, Cache-Control})`.
* Four-part form-review view: when enabled add `held_download_enabled: True` to the returned dict.
* Keep the existing `except` mapping.

Exit: unauthorised or unknown requests produce no artifact; repeated GET does not mutate (asserted by tests).

## Phase 2: screen

File `src/api/src/zava_forward/api/web/role-screens.js`.

* `fundingDraftPanel(draft, downloadEnabled)` and the `drafts.map` call become `drafts.map((d) => fundingDraftPanel(d, extra.review.held_download_enabled === true))` (explicit arrow, so `map` index is not passed).
* After the table: when `downloadEnabled && draft.draft_id`, a paragraph with the anchor `href` `/api/cases/{encodeURIComponent(case id)}/form-review/{encodeURIComponent(draft id)}/held-export`, `download="held-form-draft-export.json"`, class `btn alt`, text "Download Held draft (unreviewed)", and the note. The case id is passed in as a third parameter from `c.id`.
* No auto download, no script handler, native keyboard behaviour, existing focus styles.

## Phase 3: tests

* New `src/api/tests/test_form_held_download_api.py` reusing `FormApi` setup from `test_form_staging_api` via import: equality of served body to `form_export.draft_export` result including `content_sha256` and history; headers; default OFF and each guard variable alone, trusted-proxy; unauthorised roles and contractor; revoked rights after load (role change); unknown case, other case, unknown draft; malformed paths, wrong method, trailing segments; Unavailable 409 no attachment; repeated GET no state mutation (store data snapshot and audit length); view flag present only when enabled.
* `test_finance_grants_screens.py`: one render test: link with exact href when flag true; absent when flag missing, review unreadable, draft Unavailable.
* `test_role_endpoint_inventory.py`: add `/api/cases/ZF-1/form-review/DRAFT/held-export` to `GET_ENDPOINTS` (explicit route entry). Shared lists are existing and small; this is an inventory addition required by the brief, not a fixture rewrite. Also add a `test_inventory_covers_held_export_route` mirroring the job-pack pattern (entry present and `"held-export"` in `SERVER_SRC`), because the coverage regex cannot see a route built from path parts.

## Phase 4: browser

New `src/api/checks/held_form_download_browser_check.py` modelled on `schema_download_browser_check.py` with its own synthetic fixture built from `test_form_review` helpers, env set only in the owned server process, loopback, keyboard Tab and Enter to the link, JSON captured, history/hash/notices asserted, no non-safe methods after sign-in, narrow and wide viewport, axe if available, denied roles see no link, direct URL denied. Runs under `/tmp/ama-rpi-heavy.lock` actual-holder admission only.

## Phase 5

Changed-web review against fetched rules, README note, focused validation, changes record, handoff.
