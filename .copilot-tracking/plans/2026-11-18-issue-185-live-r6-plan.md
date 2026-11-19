---
title: Issue 185 live r6 plan
ms.date: 2026-11-18
---

Refs #185. Tier FULL applies to the candidate (src/core change); the full receipt is not run by this worker.

* [x] Phase 1: add `SasEnrollment` to `device_registry_azure.py`; create sends `type=sas`, no key, DISABLED, run marker, `If-None-Match: *`.
* [x] Phase 2: tests in `test_device_registry_azure.py` using the existing simulator: SAS body has no key; Hub-generated keys in the response never reach caller, errors or repr; mixed X.509/SAS spec; invalid ids refused; ownership read and ETag delete work for SAS identities.
* [x] Phase 3: live proof assessed and not performed; no Azure resource was created, so the adapter is proven in simulator tests only (stated in the changes record).
* [x] Phase 4: research note, index, log, changes record with per-criterion table, review, commit.

Details: [details](../details/2026-11-18-issue-185-live-r6-details.md). Critique: [critique](../critiques/2026-11-18/issue-185-live-r6-critique.md).
