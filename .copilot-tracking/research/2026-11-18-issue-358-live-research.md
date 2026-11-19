---
title: Issue 358 live research (opening)
ms.date: 2026-11-18
---

## Scope

Issue #358 criteria: (1) expired stored credential guard test, (2) non-production
round-trip proving the secrets rebuild preserves Key Vault-referenced secrets,
(3) four-file conflict with #352. Demo authority 2026-11-18: live Azure in
resource group `ama`, no Key Vault rotation, no production change.

## Opening findings

* Criteria 1 and 3 were delivered by merged #374 (issue comment).
* `ca-cutover-test-demo-api` now holds one Key Vault-referenced secret (earlier
  comments recorded `secrets: null`), so a populated baseline exists.
* Plan: read-only baseline of the demo app; run the real `preserve_app_secrets`
  plus ARM PATCH round-trip on a throwaway app in `cae-cutover-test-demo`; delete it.
