---
title: Issue 349 Tenant Prerequisites for Browser Sign-in, Live Demo Round 6
description: Sixth live demo check of issue 349, diagnosing the resident-account wrong-role probe that failed in round 5
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure in resource
group `ama`, no drills, no production change. This round made no Azure call and created
nothing, so nothing needs deleting. Credentials were read at run time and never printed.
Evidence is in `.copilot-tracking/evidence/2026-11-19/issue-349-live6/`
(`resident6.py`, `resident6.json`). Round 5
([note](issue-349-tenant-prerequisites-live-r5-2026-11-19.md)) stands unchanged.

## Finding

The round 5 resident probe failed at sign-in. A redacted navigation log shows the browser
reaching the Entra tenant sign-in page, then the home-realm redirect to
`sts.microsoftonline.com`, which fails with `net::ERR_NAME_NOT_RESOLVED`; Chrome then
shows its error page. `getent hosts sts.microsoftonline.com` returns nothing on this
host while `login.microsoftonline.com` resolves. The cause is the worker host's DNS, not
the application, so no role decision was observed and no wrong-role result is claimed.

## Acceptance criteria

| # | Criterion | Demo status | Basis |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions app, roles, credential | Partly proven (unchanged) | Needs Application Administrator rights; Graph read denied in r5 |
| 2 | Credential in private vault, nothing published | Proven for the demo (r5) | Vault reference, public access disabled, private endpoint |
| 3 | Audience and callback use the registration | Partly proven (r5) | Sign-in completes; prior callback list unreadable |
| 4 | Private roster reconciled in VNet | Unproven, not applicable to the demo | No owner-supplied roster |
| 5 | Sign-in, logout, wrong-role and unknown-staff denial | Test account proven (r5); wrong-role live proof blocked by host DNS | Code-level denial is covered by `src/api/tests/test_entra_authoritative.py::test_anonymous_unassigned_wrong_tenant_and_bad_oid_are_denied` and the admin-alone tests |
| 6 | Anonymous 401, forged-header denial, positive request | Proven with a qualification (r5) | Unchanged |

## Conclusion

The first unmet criterion (1) is a tenant-owner action, not a source change, so no code or
test was added and no box on #349 is ticked. To close criterion 5 live, run the resident
probe from a host that resolves `sts.microsoftonline.com`.
