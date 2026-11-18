---
title: Issue 130 standalone nomination-route form submission research
ms.date: 2026-11-17
---

## Scope

Issue #130 comments report that the standalone `?view=nomination-routes-html` forms (acknowledgement, correction, challenge) submit as URL-encoded browser POSTs, which `server.py` `_body()` parses as JSON, giving HTTP 400. Base: origin/main eb51af5c9.

## Opening evidence (static)

* `src/api/src/zava_forward/api/nomination_routes.py` renders `<form method="post" action="/api/cases/{id}/resident">` with no script.
* CSP is `default-src 'self'`, so an inline script is blocked; a same-origin static script under `src/api/src/zava_forward/api/web/` is allowed and is auto-served by `StaticAssets`.
* Trusted-proxy mutations need header `X-ZF-CSRF: 1`; a native form cannot send it.

## Planning readiness

Ready after reproduction (see below).

## Measurement (reproduction at base eb51af5c9)

Research disposition: executed. New browser test `test_standalone_route_forms_submit_in_browser` (synthetic SQLite fixture, loopback server, headless Chromium, route-restricted cookie session) submitted the standalone acknowledgement form. Result on unfixed code: response status `[400]`, expected `[200]` (`Could not read that.`). This confirms the issue comment reproduction at the current base for the acknowledgement path; the shared handler covers correction and challenge forms, whose form ids share one script selector.

Planning Readiness: Ready.

Deviation record: the first fix attempt was written before the plan, changes file and `implement-start` witness existed; it was moved out of the tree (`/tmp`) and reapplied after the witness call. The reproduction test was added before the changes file (test file only).
