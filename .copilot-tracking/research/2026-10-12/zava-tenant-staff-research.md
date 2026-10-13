---
title: Tenant Staff Initialization Evidence
description: Evidence for app-role and internal staff initialization
ms.date: 2026-10-12
---

## Task and Research Disposition

Task zava-tenant-staff-2026-10-12. Research reused from the targeted live
investigation and official Graph API reference. Planning Readiness Ready.
No directory identities or employment attributes are stored in this artifact.

## Findings

* Live console logs show `no staff record with this oid`, after tenant and
  mapped-role validation. Graph independently confirms the Coordinator role.
* The database has ten staff positions: three coordinators, two resident
  liaisons, and one each of manager, safety liaison, grants/evidence officer,
  inspector and support officer. Only the manager has an identity binding.
* Eight app-role kinds are registered, including Contractor. One additional
  contractor position is needed to exercise every kind: eleven distinct
  accounts, preserving existing work codes and assignments.
* Existing manager has Default Access and Programme Manager. Both must remain;
  Default Access is not a mapped workbench role.
* SqlStore loads staff once. Staff initialization requires restarting the API
  replicas; updating SQL alone leaves the in-memory authorization roster stale.
* Case owner labels are mutable; owner_code is the stable workload key.
  Historical audit, approvals and recommendations must not be reattributed.
* The tenant has enabled member accounts with job/department/group hints, plus
  room/desk/workspace accounts. Resource accounts must not receive staff roles.

## User Direction and Boundary

The owner explicitly requests tenant people instead of generated staff names,
retaining the main admin and existing Coordinator role. Role/title/group
matching is illustrative demo coherence, not a qualification assessment.
Assign only this enterprise application's roles, never directory roles or
group memberships. Preserve tenant checks, one mapped role, explicit staff
binding, contractor scope, generated stock, case IDs and the append-only ledger.

## Official Source

Microsoft Graph v1.0, Grant an appRoleAssignment for a service principal:
https://learn.microsoft.com/en-us/graph/api/serviceprincipal-post-approleassignedto?view=graph-rest-1.0
Retrieved 2026-10-12. POST uses principalId, resourceId and appRoleId.
Delegated management needs AppRoleAssignment.ReadWrite.All plus
Application.Read.All and a supported administrative role.

Microsoft Entra, Manage users and groups assignment to an application:
https://learn.microsoft.com/entra/identity/enterprise-apps/assign-user-or-group-access-portal
Checked 2026-10-12 during implementation. Assignment explicitly does not
cascade to nested groups. Effective-role reconciliation therefore reads direct
memberOf pages; transitive-only assignment must not satisfy initialization.

## Handoff

Use a private operator roster with live directory attributes. Commit only the
initializer, synthetic tests, generic instructions and evidence. Reconcile
Graph roles first, atomically update SQL staff/current owner labels, then
restart the existing API and verify idempotency and preservation.
