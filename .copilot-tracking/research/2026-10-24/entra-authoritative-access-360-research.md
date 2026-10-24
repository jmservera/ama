---
title: Entra-authoritative application access research (issue 360, recovery cycle 5 of 5 start)
description: Evidence for replacing SQL staff-row authentication with validated Entra tenant, OID and app roles, plus an ApplicationAdmin role
ms.date: 2026-10-24
---

## Task identity

* task_slug: entra-authoritative-access-360; parent: demo-admin-bind-360-repair3 (cycle 4, SQL-bind route stopped by owner at 14:34Z).
* Owner direction 2026-10-24 (priority change): Entra tenant, OID and explicit app roles decide login and capabilities. No pre-provisioned staff row and no database read on the authentication path. Stable tenant+OID identity for audit and case ownership. Display name and email are not authorization.
* Branch: child `feat/entra-authoritative-access-360` in worktree `ama-wt/issue-360-entra-access`, created from `origin/main` f1e2d830 (verified ancestor of the PR 423 branch, so no stacking needed). The 360 transport worktree is untouched, including its uncommitted bind-admin work.
* Included dependency: the `setup-entra.py` runtime-patch `imageType` fix from commit 8b153af4 (files checked out, not rewritten).

## Observed current behaviour (read from code)

* `auth.py` `TrustedProxyProvider.authenticate`: tenant check, then exactly one mapped staff role among the claims, then a lookup in `store.staff` by oid (optional email fallback), else deny `no staff record with this oid`. Capability roles (`RuleAuthor`, `RuleOwner`, `RegulatoryChat`, `AIRestart`) are only honoured when the oid is bound to a staff row.
* Owner reproduction: role claim present, SQL row unbound, so deny. Cause is the design, not the Entra assignment.
* 264 call sites read `user["role"|"code"|"email"|"name"|"oid"]`. Many gates are role tuples (`MANAGER_ROLES`, `FINANCE_VIEW`, `SAFETY_ROLES`, `QUALITY_ROLES`, `HAZARD_ROLES`, `projection.STAFF_ROLES`).
* About 15 core call sites re-validate the actor with `store.staff.get(user email)` (bulk_edits, procurement, finance, forms, change_provenance, resident_decisions, workflows, coordinator, chat_privacy, chat_isolation). A principal with no staff row would fail these even once authenticated.
* `infra/scripts/setup-entra.py` already merges `appRoles` idempotently, with stable `uuid5(ROLE_NAMESPACE, key)` ids from `infra/entra/app-registration.json`, treats `capabilityRoles` as supplemental to the single staff role, and refuses wrong-audience registrations. An `ApplicationAdmin` capability entry therefore composes with a staff role without tripping the conflicting-roles check.
* Cycle 4 evidence preserved elsewhere: the SQL-bind worker, controller, review and the private-job probes (python, mssql_python, SQL connect and read all succeeded; they showed the in-VNet job route works). That route is no longer the chosen fix.

## Design findings

1. Authentication must be pure claim validation: tenant equals configured tenant, exactly one valid oid GUID, token-asserted roles. No store access.
2. Stable identity: `code = "E-" + sha256(tenant:oid)[:12]`, `oid`, `tid`, `identity_source = "entra"`. Name and email come from claims for display only and are length-limited and stripped of control characters.
3. Admin model limitation: roles are single strings gating many tuples. `ApplicationAdmin` is a capability role. Alone it resolves to the existing highest staff role, Retrofit Programme Manager, so every manager, finance-view and reason-role option is visible. Alongside a staff role, the staff role is kept as the effective role and the admin flag adds the manager option set only. It does not make the holder a Safety Liaison or Quality Inspector, and it creates no approval authority (no self-approval, no named-approver or AI-restart authority, no resident consent). Whether to extend admin to professional-sign-off views is an owner/ADR decision, recorded as a limit rather than assumed.
4. The actor re-validation seam: add one `Store.actor_record(user)` that returns the staff row for a DB-bound person, or for an Entra principal returns the verified principal record built from the signed claims. Replace the `store.staff.get(user email)` actor checks with it. The staff roster stays the source of case assignment and owner labels.
5. Rule capabilities: bound only to a validated tenant+OID principal (not a DB row). `RuleOwner` and `AIRestart` keep their named-person and distinct-authority checks, so the admin is not given them.
6. Email fallback (`ZF_AUTH_EMAIL_FALLBACK`) is removed from the trusted-proxy path.

## Live and deployment facts

* Site ingress is open (guard released in cycle 2). Anonymous and forged principals return 401; healthz 200. The deployed image is the old code, so the owner still sees "Account not authorised" until a tested image runs.
* Registry `crcutovertestrzsrg` is Premium, public access off, no trusted-services bypass, no tasks or agent pools. Local docker push is blocked. Existing options to put the image in the registry: `az acr build` (needs a cost-priced network change or agent pool), or an in-VNet job. This is the open deployment dependency and is researched again in the Plan phase before any billable step.
* Cost gate carried from RPI126: actual 279.67, projection 459.07, reserve 190.93 against the AMA RG-only 700 ceiling. Window ends no later than 17:39Z; absolute expiry 2026-10-25T16:02Z.

## Planning readiness

Ready for planning, with the deployment route and the admin-capability limit as explicit open items.
