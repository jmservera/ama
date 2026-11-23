---
title: Issue 2245 browser handling of a non-JSON gateway failure
description: The chat widget showed a JSON parser message when the ingress timed out an ask; the fix and a per-criterion table
ms.date: 2026-11-23
---

## Finding

`api()` in `web/app.js` parsed every response body as JSON and rethrew the parser error for a keyed POST such as chat ask. A Container Apps ingress failure (502, 503 or 504) returns a non-JSON body, so the widget would show "Chat unavailable: Unexpected token ..." with no owner or next action. This fits the live free-form ask that failed after about 30 s on 2026-11-23 ([override note](./issue-2245-override-sqlstore-2026-11-23.md)); the server's own 500 and 503 replies are always JSON and were unaffected.

## Evidence

* Reproduction: the new Node-harness test `test_a_non_json_gateway_failure_on_a_change_shows_the_generic_message` failed before the change with `[None, "Unexpected token <", False]` and passes after it with `[504, <generic change message>, true]`.
* An OK response whose body cannot be read still throws, because a committed change cannot be shown.
* Checks from `src/api`: `tests.test_app_wide_ux`, `tests.test_content_standard`, `tests.test_accessibility_baseline`, `tests.test_chat_widget_focus`, `tests.test_app_js_notices_content` (98 tests, OK); ruff check and format on the test file; `python3 -m mypy` clean. No live call was made and no Azure resource was created.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Thread creation no bare 500 on a busy lock | Proven locally (earlier runs) | server tests; unchanged here |
| Plain message when the ask outlasts the gateway | Proven locally | new test; not deployed |
| "Model calls: 1" visible live | Unproven | fix not deployed; needs a revision (owner-gated) |
| Cause of the 2026-11-22 and 2026-11-23 500s | Unproven | Log Analytics denied |
| Which skills and routes call the model | Proven earlier | override note |
