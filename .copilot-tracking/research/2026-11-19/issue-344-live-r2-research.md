---
title: Issue 344 live r2 research
description: Opening research for the second 2026-11-19 live pass on issue 344
ms.date: 2026-11-19
---

Refs #344. Research disposition: executed. Goal: find the first unticked criterion that can be proven or built for the demo with code and tests.

Prior evidence read: public-browser-access-live-r4-2026-11-19.md (criterion 1 unmet for browser-style anonymous API calls, Easy Auth RedirectToLoginPage; fix needs infra/containerapps.bicep or an app-level flow).
Planning Readiness: pending fresh evidence (see below).

## Fresh evidence (evidence/2026-11-19/issue-344-live-r2/)

* Anonymous curl: /healthz 200, / 200, /api/me 401, /api/cases 401, /app 401.
* Browser-style request (browser User-Agent, Accept application/json) to /api/me: 302 to login.microsoftonline.com (tenant id redacted).
* SQL sql-cutover-test-rzsrg: public network access Disabled, TLS 1.2, 0 firewall rules.
* auth-globalvalidation.json is empty (az auth show returned nothing); the setting is taken from infra/modules/containerapps.bicep lines 302-304: RedirectToLoginPage unless entraBearerOnly.

## Tier decision

The only buildable gap is criterion 1 (anonymous API 401 for browser-style clients). Fixing it changes the Easy Auth security control and deployment (Bicep plus redeploy, or an app-level sign-in flow). That is FULL tier and a production-affecting change, and the owner barred production changes; the brief says to stop. Criteria 3 and 4 are proven for the demo; 5 is reachability only, with the /api/time/status 500 still unfiled.

Planning Readiness: Ready (conclusion: no buildable demo criterion within FOCUSED tier).
