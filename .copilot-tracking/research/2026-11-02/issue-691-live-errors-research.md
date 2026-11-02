---
title: Issue 691 research, leaflet 500 and 403/503 live responses (third pass)
date: 2026-11-02
---

* Research disposition: executed (live log attempts plus local reproduction); builds on PR #694 and PR #741 evidence.
* Live logs still unavailable: `az monitor log-analytics query` on `log-cutover-test` fails with `NspValidationFailedError` (public query access disabled) and `az containerapp logs show -n ca-cutover-test-api -g ama` returns "Could not find a replica". No `http-response ... /vendor/` line could be read.
* Local reproduction with the real `TrustedProxyProvider` and an Easy Auth style `X-MS-CLIENT-PRINCIPAL` header (aad, correct tenant, mapped staff role): `/vendor/leaflet.js` returns 200 with the full 147,552 bytes, also when `identity.bind` raises. Unauthenticated requests get 302 to sign-in, not 500.
* Conclusion: the live 500 origin is still not proven from evidence. The only app-side path that could raise on a static asset (identity store binding) was removed for non-HTML assets in #741. A fault in the platform edge or a transient replica restart during the 2026-11-01 redeploy remains possible and cannot be excluded without logs.
* 403 on `/api/assistants` and `/api/chat/regulatory/status`: server gates by role (Application Administrator has no assistants/regulatory chat); the UI skips these calls for that role (#694). 503 on `/api/account/photo` (Graph photo unavailable) and `/api/law/alerts` (law store not loaded) are expected with stores off and are worded plainly in the UI. Browser consoles still print the network line for any non-2xx fetch; that cannot be suppressed by page code.

Planning Readiness: Ready (test-only hardening).
