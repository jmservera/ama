---
title: Public browser access phase details
description: Evidence and completion boundaries for issue 344
ms.date: 2026-10-16
---

Task ID: 344. Slug: public-browser-access-344.

## P01

P01-T01: Existing edge module has unverified comments, root HEAD probe and
missing explicit route pattern. Add entry point using existing environment/app/
workspace references, with private-origin checks before deployment. Keep main's
production guard unchanged. Additive entry point does not claim profile promotion.

P01-T02: Initializer currently always selects origin FQDN. Add explicit HTTPS
public URL option, strict hostname validation and require explicit Custom
X-Forwarded-Host/Proto proxy
configuration when host differs. Preserve registration redirects/roles/secrets.
Only configure the existing auth platform; no tenant writes without a valid
registration. Probe whether normal browser mode preserves anonymous API 401;
if not, use narrow platform exemptions backed by server denial and spoof tests.
Existing literal systemAssignedIdentity must be reported, never accepted as a
valid tenant application. Missing credential means callback/login stays Blocked.

P01-T03: Compile entry points and modules to stdout, run infra unittest,
initializer/edge targeted tests and project tests as needed. Use installed
packages; on missing dependencies, pip install declared extras into session venv.
Use absolute core/agents test paths for API. Local app on loopback with generated
synthetic fixture only; no Azure-shaped mock as deployment proof.

## P02

Critique corrections: exactly one origin, fixed API Host and certificate name,
endpoint-only public domain, no rewrite rules. Live conflicting Host,
X-Forwarded-Host and Forwarded must not select another app or callback host.
Do not exempt API routes absent documented trusted-header behavior and positive
platform-principal contract evidence. Existing positive server unit tests are
local contract evidence only. If unavailable mark coexistence Blocked.

Capture baseline auth action/proxy before changes (no secret values). A critical
failure disables the new endpoint and restores only changed action/proxy fields,
leaving every existing resource and private network intact. No intentional live
failure injection. Historical asset provenance is the supplied matrix's 16 web
rows; compare current src paths, never legacy source. Redirects prove auth
interception only, not image asset presence or rendered functionality.

P02-T01: New resources only: afd-cutover-test profile, ep-cutover-test endpoint,
og-api origin group/api origin, route-api, wafcutovertest, sp-waf and diagnostics.
New managed Private Link connection belongs to that edge and is approved only
after exact environment/request verification. No deletions. Do not deploy full
main with publicAccess=true or convert data/quarantine/purge settings.

P02-T02: Mode is default browser (RedirectToLoginPage), forwardProxy Custom with
Front Door-overwritten X-Forwarded-Host/Proto.
Keep health/static welcome exact exemptions. Anonymous API must produce 401
without client needing redirect suppression; test forged principal and malformed
bearer too. Never capture Set-Cookie, tokens, tenant/client/subscription IDs or
raw Entra Location in committed evidence. Capture redacted redirect host/path,
boolean callback-host match, statuses and UTC time. Read SQL state/private
connections management metadata only. Do not manufacture credentials.

P02-T03: Matrix's complete per-file inventory includes 16 historical web assets
and modules spanning sign-in, roles, queues, cases, map/sensors, workflow,
consent, finance/grants/quality/procurement, documents, evidence, time,
chat/assistants, policy/law, ledger/recovery and profile/session.
For each record static presence, public/authenticated reachability and evidence
boundary. File shared prerequisite gap rather than duplicate one issue per
blocked route; specific missing functionality gets its own issue or existing
open issue reference. All 16 assets can be checked as protected redirects, not
as rendered acceptance. Preserve historical proof and add dated current result.

## P03

P02-T03 audit instrument amendment: create only
job-cutover-test-public-audit, a manual job in cae-cutover-test using the exact
serving API digest and existing API MI solely for private registry pull. Its
command enumerates package assets/hashes, never opens Store, dataset, SQL,
staff or credentials. Retain and record the job; no existing proof job changed.
This supplies image presence evidence distinct from redirects and functionality.
A second execution on that same owned job probes only anonymous health/API/
application/login statuses and redacted redirect host against the private API.
It does not follow login or open protected data and is not public proof.

P02-T02 live correction: Standard forwarding accepts a supplied RFC Forwarded
host even though Front Door overwrites X-Forwarded-Host. Use Custom with exactly
X-Forwarded-Host / X-Forwarded-Proto in both entry points and initializer guard.
The attempted edge header-delete rule was rejected by Azure because Forwarded
is reserved. Remove only the empty, unused `afd-cutover-test/originheaders`
rule set created by that failed attempt; the route has no rule-set association
and no rule was created. No pre-existing resource or group may be deleted.

P03-T01: Review exact changed diff and commands once, record findings/outcome and
route later work. Do not claim full acceptance with material blockers.
P03-T02: gh account must resolve jmservera/8036360. Repo-local
8036360+jmservera@users.noreply.github.com for author/committer and required
Copilot trailer. Target main, Refs only, no merge or force-push. Report PR and
remaining real-user/feature boundaries plainly.
