---
title: Issue 349 Tenant Prerequisites for Browser Sign-in, Live Demo Round 10
description: Round 10 live read-only recheck and a code-level regression for wrong-role and wrong-tenant denial, with a per-criterion proven, unproven or owner-gated verdict
author: AMA programme
ms.date: 2026-11-23
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure in resource
group `ama`. All Azure and HTTP calls were reads or anonymous requests; nothing was
created, so nothing needs deleting. No credential was read or printed. Evidence is in
`.copilot-tracking/evidence/2026-11-23/issue-349-live10/`. Round 9
([r9](issue-349-tenant-prerequisites-live-r9-2026-11-23.md)) stands except where noted.
No browser sign-in was repeated: the only available sign-in accounts are the test account
(proven in r9) and the resident account (federated to an unresolvable host).

## Live recheck

| Check | Result |
| --- | --- |
| Active API revision | `ca-cutover-test-demo-api--0000057`, Healthy, 100 percent traffic (r9 saw 0000054) |
| Anonymous `/api/me` and `/api/cases` without an HTML `Accept` header | 401 |
| Anonymous XHR; bad bearer; forged `X-MS-CLIENT-PRINCIPAL` | 403; 401; 401 |
| App registration `zava-forward-api` | `AzureADMyOrg` (single tenant) |
| Vault `kv-cutovertest-rzsrg` | public access Disabled, default Deny, 1 private endpoint |

## Code gap found and closed

`TrustedProxyProvider.authenticate` denies a principal whose tenant claims are not exactly
the configured tenant, and denies a contractor who also holds the application administrator
role. Neither path had a test (grep of `src/api/tests` and `src/core/tests`). Round 10 adds
one regression test in `src/api/tests/test_auth.py` for both denials plus the rule that
non-string role claim values are ignored. The behaviour was probed first and already
correct, so no production code changed.

## Acceptance criteria

| # | Criterion | Verdict | Basis |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions single-tenant app, roles, credential | Proven for the demo registration; provisioner owner-gated | Single-tenant audience read again; r9 for roles and credential |
| 2 | Credential in private vault, nothing weakened | Proven for the demo | Vault Disabled/Deny/1 endpoint, read only |
| 3 | Audience from the registration; edge callback with prior callbacks kept | Proven for the resulting state; tool run unproven | r9 facts; the `initialize-api-auth.py` run is not observable |
| 4 | Owner roster reconciled in the VNet, replicas reloaded | Unproven, owner-gated | No owner roster exists; none may be invented |
| 5 | Real user callback, role-scoped `/api/me`, logout, wrong-role and unknown-staff denial | Partly proven | Sign-in proven in r9; live wrong-role denial needs a second working account; denial now also covered by the new unit test |
| 6 | Anonymous 401 and forged-header denial, positive request | Proven with a qualification | Anonymous 401, bad bearer 401, forged header 401, XHR 403 re-observed; positive request proven in r9 |

## Conclusion

Criteria 4 and 5 remain open and owner-gated. No box on #349 is ticked.
