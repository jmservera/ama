---
title: Issue 691 follow-up research, leaflet 500 candidate cause
date: 2026-11-01
---

## Context

PR #694 added 5xx and vendor-failure logging and plain wording for expected 403/503 responses, and left the leaflet.js 500 cause unproven (Log Analytics blocked by the network perimeter).

## Findings

* Research disposition: executed (code reading plus local reproduction).
* `server.py` `do_GET` serves every non-public static file, including `/vendor/leaflet.js`, behind `self._user()` when the provider is `trusted-proxy`.
* `_user()` calls `identity.bind(app.store, user)` and `identity.link(app.store, user)`, which read and write the SQL store. Static bytes need no store access, so a transient store error (lock, timeout, restart) raises out of the handler and the edge reports a 500 for the asset while pages served from cache still work.
* Observed live pattern fits: only one asset (the largest synchronous script) failed, not the API calls that used the store successfully.
* Unproven as the live cause: no live log was retrievable. Local reproduction with a store error injected into `identity.bind` returns a failed response for `/vendor/leaflet.js` before the fix and 200 after it.
* Expected denials (403 /api/assistants and /api/chat/regulatory/status for administrators, 503 /api/account/photo and /api/law/alerts with stores off) were classified as expected in PR #694; no change here.

Planning Readiness: Ready.
