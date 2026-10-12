---
title: API Authentication Initialization Details
description: Safe existing-registration callback synchronization
ms.date: 2026-10-12
---

## P01

Use Azure CLI through the current operator profile to discover Container Apps
FQDN, enabled authentication, client ID and tenant. Use a separately selected
tenant profile for Graph. Explicit `--login` may create a private profile and
request device-code authentication, but must never overwrite the operator's.
Read the registration by client ID, preserve all current redirects, patch only
`web.redirectUris` when needed, then verify callback and preserved redirects.
Check-only mode must fail if initialization is missing, without patching.
Graph failures and tenant/client mismatches are explicit failures.

Tests use mocked Azure CLI responses, not a live tenant or real credentials.
The existing creation script remains responsible for first-time registration,
roles, assignments and explicit secret provisioning. The new initializer only
repairs post-deployment callbacks. Document that an authorised tenant login
remains a human bootstrap, not something RG Owner permissions can supply.

## P02

The owner reports the callback repair done; application management is still
unavailable to the current operator. Neither fact proves interactive sign-in
or tenant role/name transition. Preserve that acceptance boundary.

## P03

Preserve permissions for existing migration targets, but give newly created
public assets mode 0644. Normalize packaged web assets to readable files and
searchable directories without changing the non-root runtime or permitting
application writes. Exercise a mode-0600 logo input during the CI image build.
Verify actual PNG bytes, MIME type and source equality from the deployed
application server; keep ingress authentication enabled. This server-level
check does not establish interactive browser acceptance.
