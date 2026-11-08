---
title: Issue 135 employee exception screen research
ms.date: 2026-11-07
---

* Task: `issue-135-exception-screen`. Parent topic: #73 (not #123). Base/main `23b26a7f3a4693cd20dcf0447303d97491096cb3`.
* Research disposition: executed (source and doc reading only; no browser, server, SQL, model or network run).
* Planning Readiness: Ready.

## Evidence read

* Case study original and addendum framing, `docs/reference/README.md`, `docs/reference/memory.md` (context only), UX design system, WCAG baseline and content standard (blocked message = reason, owner, next action; AI labels; no approval implied).
* Handoff `handoff-111-135-225-2026-11-07.md` including the appended clearance. #1081 delivered the Store projection and API, #666/#868 the queue and failed-AI feeds. #1007 importer helper is not connected intake. #229 case-derived screen is a different thing.
* Issue #135 body: five unchecked criteria; depends on #80, #84, #122; parent #73. This slice does not close any of them.
* Web Interface Guidelines fetched successfully from the current vercel-labs source on 2026-11-07 (command.md). Applicable: semantic table/link/heading, `role=status`/alert for async state, empty states, long text wrapping, no `outline: none`, `Intl` dates.

## Existing contract: GET /api/exceptions

* `server.py` calls `Store.exception_register(user, staff_from_env(env))`; `PermissionError` becomes 403 with `{error}`. Every successful or denied view writes an audit entry, so the screen must load the register only on an explicit request.
* With no staff configured, only `MANAGER_ROLES` may read it and the response is `state: "roles_not_named"` with empty `items` and an `unrouted` explanation. With staff configured, only a named email is allowed.
* Response keys: `state`, `items`, `unrouted`, `sources`, `banner`, `access` (`roles` for the viewer, `scope` kind to role), `note`.
* Item keys: `id`, `kind`, `owner`, `owner_role`, `summary`, `status`, `original_source`, `eligibility` (always Unknown), `runbook`, `recovery` (null), plus `values` (conflicts: value, source, date, version), `error` (failures) and `ref`.
* Kinds: `source_conflict`, `identity_conflict`, `failed_import`, `failed_ai_run`, `failed_integration`, `stranded_task`. Only `source_conflict`, `failed_ai_run` and `stranded_task` are fed today.
* Failed AI items exist only for recorded quarantined results or an AI-mode request that fell back with a reason. Deliberate workflow-only records raise nothing, so absence of an item is not evidence of a model result, and the screen must say so without inventing rows.
* `runbook` text says "ask a human to re-run from the task screen". It is engineering placeholder guidance and must be labelled as not an approved runbook; no re-run control exists to point at.
* `sources` carries NOT_CONNECTED (failed imports) and NO_HEALTH_CHECK (service health Unknown). `banner.state` is `unknown` or `outage` or `no_known_outage`.
* `owner` is whichever email `ZF_EXCEPTION_STAFF` configures. It is a configuration value, not an appointment.

## Existing UI seam

* `roleScreensView` in `role-screens.js` renders registered screens; `data-operator` is available to `screenManagers` only. A screen may define `overview(signal)`, but the host calls it with the signal only and, when `overview` exists, skips `summarise`.
* `api()` in `app.js` uses `routeController.signal`, calls `throwIfAborted` after parsing, maps 401 to sign-in and other statuses to an Error carrying `status` and server text. `h()` appends strings as text nodes, so returned text is never parsed as HTML.
* Existing helpers: `screenPanel`, `screenTable` (labelled focusable scroll region, caption, `th scope=col`), `screenFields`, `screenValue`, `screenUnknown`.

## Decisions

* Add an explicit GET link (`#/screens?screen=data-operator&exceptions=1`) on the existing screen; no auto-load, no control other than links.
* Pass `(signal, rows, caseRecord)` to `overview` so the data-operator screen keeps its existing page summary and adds the register panel. Other screens ignore the extra arguments.
* Validate the response shape before rendering; on failure render only a truthful unavailable or denied panel.
* Reserved paths only: `role-screens.js`, `test_data_operator_screen.py`, one new synthetic renderer test beside it.

## Risks and limits (adverse, preserved)

* A named steward whose signed-in role is not a manager cannot open this screen; widening `roles` would infer authority from profile names and is out of scope. Owner decision pending.
* Pure renderer tests use a node `vm` fake DOM; real browser feature check is pending coordinator heavy admission.
* Human and assistive-technology acceptance (#151/#155) and runbook naming are not claimed.
