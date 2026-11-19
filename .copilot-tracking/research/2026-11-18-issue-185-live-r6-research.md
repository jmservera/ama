---
title: Issue 185 live research (round 6, code increment)
description: Opening research record for the SAS enrolment code increment of issue 185
ms.date: 2026-11-18
---

Refs #185. Disposition: reused plus executed. Planning Readiness: Ready.

## Scope and decisions

* Synthetic desktop demo; live Azure authorised (group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). Billing reconciliation, DPO/Legal approval and person-run AT testing are not needed.
* Unticked criteria: (3) credentials issued and stored without appearing in source or logs; (4) teardown removes all simulated identities.
* Owner asks for the remaining demo-scope code and tests. Earlier rounds (r1 to r5) proved the two criteria operationally with an out-of-repository driver and listed the gap: the repository adapter `device_registry_azure.py` supports X.509 thumbprints only, so Hub-generated symmetric keys (the owner's demo choice) are not provisioned by repository code.
* Tier: changing `src/core` means the FULL tier applies to the candidate; `rpi-checks.py --all` is forbidden for this worker, so the FULL receipt stays with the coordinator. Focused checks run here.

## Existing evidence (reused)

* [Live evidence](../../docs/reference/research/issue-185-live-device-identity-evidence-2026-11-18.md), [r4 audit](../../docs/reference/research/issue-185-live-r4-audit-2026-11-18.md), [r5 reverification](../../docs/reference/research/issue-185-live-r5-reverification-2026-11-18.md).
* Baseline: `test_device_registry_azure` 39 tests OK with pinned `azure-iot-hub==2.7.0`.

## Gap to close

* Add a SAS enrolment kind: identity created with `authentication.type = sas` and no keys supplied, so the Hub generates them; the adapter never reads or returns key material (the create response is discarded).
* Keep conditional writes, DISABLED start, run marker and ETag delete unchanged.
* Tests via the existing simulator: request body carries no key, a key in the Hub response never reaches the caller, errors, logs and reprs.
