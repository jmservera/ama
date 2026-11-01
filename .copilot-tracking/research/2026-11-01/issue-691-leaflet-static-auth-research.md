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
* Unproven as the live cause: no live log was retrievable. `identity.bind()` catches roster-read exceptions and `identity.link()` suppresses store errors by default, so the mocked `bind` failure in the regression test shows removal of the binding dependency for non-HTML assets (defensive hardening), not reproduction of a database-caused asset failure.
* HTML entry points (including `/law.html`) keep the full `_user()` admission check; only non-HTML assets use provider authentication alone.
* Expected denials (403 /api/assistants and /api/chat/regulatory/status for administrators, 503 /api/account/photo and /api/law/alerts with stores off) were classified as expected in PR #694; no change here.

Planning Readiness: Ready.
