---
title: Resident Demo Authority End Live Check (Issue #521)
description: Live and source evidence for the unticked #521 criterion on the resident demo authority end, now 2028-01-01T00:00:00Z exclusive, with what stays unproven and why
ms.date: 2026-11-18
---

## Scope and limits

Issue #521 asked to extend the resident demo authority to the end of January 2027. The owner decisions of 2026-11-03 and 2026-11-04 on the issue supersede that date with the exclusive end `2028-01-01T00:00:00Z` (through 31 December 2027 UTC). This note checks the unticked criterion 4, "live Azure change applied and verified", on 2026-11-18 under the owner decisions of the same date: synthetic demo, desktop only, live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO/Legal approval and person-run assistive-technology testing are not needed for the demo and are not claimed.

No source, infrastructure or Azure resource was changed and no throwaway resource was created. Only read-only Azure commands ran. The sign-in credentials were read at runtime by the script and never printed; the filled-form screenshot hides both fields.

Evidence: [live_check.py](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live/live_check.py), [live-checks.json](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live/live-checks.json) and two desktop (1280x900) screenshots in the same folder.

## Findings

| Check | Result |
|-------|--------|
| Source single truth | `src/core/src/zava_forward/core/resident-demo.json` carries `maximum_expiry_utc` `2028-01-01T00:00:00Z`; `resident_showcase.AUTHORITY_END` reads it. |
| Source tests | `src/core` `test_resident_showcase` and `test_resident_showcase_sql`: 82 tests OK (27 skipped, SQL-dependent). `infra` `test_resident_demo_secrets` and `test_resident_demo_deploy`: 33 tests OK. |
| Live app setting | `az containerapp show -g ama -n ca-resident-demo`: `ZF_DEMO_EXPIRES_AT` is `2028-01-01T00:00:00Z`, revision `ca-resident-demo--0000012`, min replicas 0. |
| Demo API app | `ca-cutover-test-demo-api` (revision `0000031`, min 0) has no expiry setting, as the infra README records. |
| Live sign-in | Playwright desktop run against the public HTTPS URL: correct demo login succeeds (`signed_in` true), page title carries "synthetic showcase, not live", password absent from page text. |
| Cookies | `__Host-zfdemo`: Secure, HttpOnly, SameSite=Strict; `__Host-zfdemo-csrf`: Secure, SameSite=Strict. |
| Session binding and sign out | `/demo/view` without the session-binding header returns 409; after sign out `/demo/session` reports `signed_in` false. |

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1 (ticked) Authority end consistent across code, SQL, helper, docs, tests | Source re-checked, not re-ticked here | Constant and focused tests above. The January 2027 wording in the issue is historical; source holds the 2028 boundary. |
| 2 (ticked) Cost estimate and cap, no resource or role added | Not re-derived | Prior record stands; this run added nothing. Actual spend read on 2026-11-18 in the [#462 live note](./resident-showcase-live-proof-2026-11-18.md): USD 440.90 against the USD 700 cap. |
| 3 (ticked) Rotation and renewal steps documented | Not re-derived | No Key Vault rotation per owner decision. |
| 4 Live Azure change applied after owner confirmation, verified and recorded | Partly proven | Proven: the live app expiry setting is `2028-01-01T00:00:00Z` and a real HTTPS sign-in works. Owner confirmation of the exact value is the issue's 2026-11-03/04 decisions. Unproven: the live SQL constraint and `allowed_case` windows, because the server `sql-cutover-test-rzsrg` has public access disabled and is reachable only from the private network; and the source commit behind the deployed image digest, because the registry is private. A successful sign-in shows the row is valid now, not that it ends on 2028-01-01. |

## Not proven and why

* Live SQL window and constraint: private-only server, and executing queries through the app container would go beyond a read-only check. A person with network access can run the read-only probe in the infra README section "Live state check".
* Expiry behaviour at the cutoff and after a 1,800 second session: not waited out; covered by unit tests.
* Applied-change timestamp and the authorising confirmation of the 2028 value: the issue records the decision; the apply time is not in Azure metadata read here (revision `0000012` dates from 2026-11-17).
* Issue #521 stays open on this record.
