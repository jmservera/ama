---
title: Repeatable API Authentication Initialization
description: Owner-requested callback initialization without replacing tenant identities
ms.date: 2026-10-12
---

## Approved scope

The owner reports the callback action done and requests an initialization
script. Implement P01 only: discover the deployed FQDN and existing auth client,
merge its callback into the registration, and make privileged login an explicit,
isolated bootstrap. Preserve redirects, roles, assignments and credentials.
Do not recreate the registration or treat reported callback repair as proof of
interactive browser acceptance. The owner's subsequent missing-logo report
also approves P03: repair asset permissions, rebuild and redeploy the API,
and verify its served logo. Continue the existing open #65.

<!-- rpi:phase id=P01 -->
## P01: Initialization code and delivery

* [x] P01-T01: Add idempotent initialization with tenant/client validation,
  isolated optional device-code login and explicit errors.
* [x] P01-T02: Test reruns, preservation, read/write failures and isolation;
  add the targeted tests to CI.
* [x] P01-T03: Document post-deployment initialization and publish through #65.

P01 is complete and published in source commit 0723508.

<!-- rpi:phase id=P02 -->
## P02: Separate remaining acceptance

* [ ] P02-T01: Verify actual tenant name/role state and signed-in lists/map when
  authorised access and a real user session are available.

P02 remains outside this initialization implementation invocation. The parent
reset's single Review is retained; no repeated Review is requested.

<!-- rpi:phase id=P03 -->
## P03: Owner-reported missing logo

* [x] P03-T01: Make generated assets and image packaging readable by the
  non-root API user; add a restricted-source-permission regression.
* [x] P03-T02: Rebuild and deploy the API image, verify the served PNG and
  preserved health/authentication, and publish the fix through #65.

P03 is complete: deployed asset verification passed and source commit 0723508
was pushed to the continuing PR. New CI remains separate from local/live
evidence; no merge or new Review is performed.

The deployed request fails with PermissionError on `/app/web/zava-logo.png`.
The migration-created file has mode 0600; root-owned Docker COPY preserves it
and the runtime UID 10001 cannot read it. This repair needs no authentication
relaxation or tenant change. P02 remains a separate real-user acceptance gate.
