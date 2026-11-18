---
title: Issue 358 Live Evidence - Credential Expiry Test and Key Vault Secret Preservation
description: Per-criterion record for issue 358 on the synthetic demo, including a real ARM round-trip on a throwaway Container App
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only; live Azure in
resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no
production change). Key Vault rotation was not run. No credential was printed
or stored. Evidence is in `issue-358-live-2026-11-18/`.

## Method

* Criterion 1: ran `infra/tests/test_setup_entra.py` (126 tests, OK), then
  disabled the expiry filter in `secret_reference` (line 1485) and re-ran:
  8 failures. The source was restored; the diff is empty.
* Criterion 2: created `ca-358-throwaway` in `cae-cutover-test-demo` with the
  demo API's user-assigned identity and a real Key Vault reference
  (`kvref`, `keyVaultUrl` + `identity`) plus one plain secret. The real
  `preserve_app_secrets` ran against the live `listSecrets` response, and an
  ARM PATCH (API 2025-07-01) wrote `[*preserved, new_secret]`, as
  `secret_reference` does at lines 1544 to 1582. The result was read back
  after provisioning reached `Succeeded`. The app was deleted and its absence
  confirmed.

## Observations

* Live `listSecrets` returned the Key Vault row with both `keyVaultUrl` and
  `identity` and a value field (values never printed).
* After the PATCH, `kvref` kept the identical `keyVaultUrl` and `identity`,
  the plain secret survived, and the new secret was added
  (`roundtrip-output-run2-polled.txt`, `PASS`).
* Run 1 reported FAIL because the readback happened while the PATCH was still
  `InProgress`; the script was corrected to poll and run 2 passed. Run 1 is
  retained unedited. The run 2 "digest equal subset: False" line is expected:
  the script deliberately dropped the previous run's plain test secret.
* Earlier issue comments recorded `configuration.secrets` as null on the demo
  apps. `ca-cutover-test-demo-api` now holds one Key Vault reference, so a
  populated baseline exists; it was only read, not modified.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| 1. Expired stored credential guard test | Proven | Test exists (merged #374); disabling the guard fails 8 tests |
| 2. Non-production run shows the secrets rebuild preserves Key Vault references | Proven for the rebuild component on a throwaway live app | Real function plus live ARM PATCH and readback |
| 2b. Same via the full `setup-entra.py` run on the deployed demo app | Not proven | Needs Graph `addPassword` and tenant administrator authority (#349/#360); modifying the demo app's credential was out of authority |
| 3. Conflict with #352, delegating `main()` kept | Not re-tested here | Recorded as delivered by #374; no re-verification attempted |

Key Vault secret rotation and any production app were not touched.

## Evidence limits

* `post-delete-check.txt` is empty, so the deletion of the throwaway app has no retained output; treat the deletion claim as an unverified observation.
* The mutation output keeps only its tail; the baseline of 126 passing tests and the restored empty diff are not retained.
* Run 1 is described, not retained; `roundtrip.py` is the corrected run 2 script.
* The retained output includes an Azure subscription identifier and a Key Vault URL; neither is a secret.
