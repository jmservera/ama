<!-- markdownlint-disable-file -->
---
title: Issue 349 ama-restart readiness research
description: Read-only diagnosis of the demo app 403 and tenant authority, 2026-10-24
ms.date: 2026-10-24
---

## Scope

Continuation of issue349-tenant-readiness-preflight (draft PR #437). Owner
2026-10-24 asked to restart coordination and remove only locally fixable
blockers to a feedback-ready login path. Research disposition: executed,
read-only, bounded. No Azure, Graph or Entra write; no secrets, tokens, IDs or
roster read. Planning Readiness: Ready (no change candidate found).

## Branch state

Worktree clean. Branch feat/tenant-readiness-preflight-349, head 44ba5b77,
fetched origin/main f1e2d830 (merge-base 140d8f49 is stale; main moved by one
line in .github/rubric/artifacts.json only). Draft PR #437 open, head unchanged.
Existing tool infra/scripts/tenant-readiness-preflight.py reviewed, not
rewritten. Focused tests: 35 passed (infra/tests/test_tenant_readiness_preflight.py).

## Evidence (2026-10-24, read-only)

| Probe | Result |
| --- | --- |
| Existing preflight vs resource group ama, app ca-cutover-test-demo-api, with public URL | overall blocked, exit 1, acceptanceEstablished false |
| az-session, api-ingress, api-auth-enabled, api-issuer-tenant, callback-target | ready |
| api-audience | mismatch, system-assigned-identity-literal |
| api-credential-setting | absent |
| graph-read-capability (az session, a service principal) | denied |
| Remaining graph-* checks | unknown, blocked by api-audience |
| m365 session (device code, user) Graph GET applications and servicePrincipals, top 1 | HTTP 403 both |
| App state | provisioning Succeeded, running status Running, revision 0000001 healthy, traffic 100 |
| Replicas on revision | 0 (minReplicas 0, maxReplicas 4) |
| Ingress | external true, one ipSecurityRestrictions rule, action Deny, range 0.0.0.0/0 |
| Easy Auth | enabled, RedirectToLoginPage, Entra provider configured, anonymous paths include / and /healthz |

## Established cause of public 403

Ingress IP restriction Deny for 0.0.0.0/0 is the platform-level cause: the
Container Apps ingress rejects every client before the app or Easy Auth sees
the request. This explains 403 on /, /health and /api/me regardless of Accept
header, even though Easy Auth would exempt / and /healthz. Zero replicas is not
the cause (scale-to-zero cold start returns a delay, not 403) and is a
secondary note. Auth 403 is excluded because Easy Auth is configured to
redirect, not return 403. Direct provenance (added after critique PC-001): a header-only GET of /health
returned HTTP/2 403, text/plain, 19-byte body "RBAC: access denied", with no
WWW-Authenticate or app headers. That is the Envoy ingress denial body, not an
Easy Auth redirect or 401. This is the most strongly supported cause, not an
exclusive proof: the rule is IPv4 0.0.0.0/0 and the app's own logs were not read. The site is not usable and no 401 acceptance exists.

## Sign-in blockers (all human or tenant authority)

* Audience is the literal systemAssignedIdentity, so there is no Entra
  application for the API. Creating one is a Graph write; denied to both sessions.
* No credential setting on the app; credential creation and delivery are
  separate human gates.
* Neither current session can read Graph applications: authority missing, not
  consented. Possession of a login does not imply consent.
* The Deny-all ingress rule is a deliberate network control tied to the
  owner-blocked #360 private-transport recovery; not touched here.
  #126 all-in budget and tranche approval remain separate live gates.

## Locally fixable blockers

None identified for the deployed login path within the read-only preflight
boundary (not a proof that no code defect exists; runtime logs were not read). Every blocker requires an Azure or Entra write, or an owner decision.
No code defect found; the preflight classified the app correctly and kept
output within its closed schema.
