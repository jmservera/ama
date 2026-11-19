---
title: Issue 130 standalone form submission plan
ms.date: 2026-11-17
---

## Plan

* [x] Phase 1: Measure the 400 with a browser regression test.
* [ ] Phase 2: Add same-origin `web/nomination-routes.js` that submits the three standalone forms as JSON with `X-ZF-CSRF: 1` and reports results in the existing `role="status"` feedback element; reference it from the standalone HTML.
* [ ] Phase 3: Validate (targeted API tests, ruff format, mypy), review, commit.

Decision: client-side JSON submission, not a server urlencoded parser. It keeps the server contract (JSON only), the CSRF header on trusted-proxy, and needs no new server surface. Inline script is rejected because CSP is `default-src 'self'`.

Tier: FOCUSED (no SQL, security control, infrastructure, deployment or gate change; CSP and CSRF unchanged). Critique: single pass, see critique file.
