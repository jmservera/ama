---
title: Resident Demo Authority End Live Check, Run 2 (Issue #521)
description: Second 2026-11-18 live audit of the unticked #521 criterion with raw read-only Azure output retained, a fresh Playwright sign-in and a per-criterion proven or unproven table
ms.date: 2026-11-18
---

## Scope and limits

Issue #521 asked to extend the resident demo authority to the end of January 2027. The owner decisions of 2026-11-03 and 2026-11-04 on the issue supersede that with the exclusive end `2028-01-01T00:00:00Z`. This run repeats the [first 2026-11-18 check](./resident-demo-authority-live-521-2026-11-18.md) and closes its evidence-retention gap: the raw read-only `az` output is now kept. Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure in resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change. Billing reconciliation, DPO/Legal approval and person-run assistive-technology testing are not needed for the demo and are not claimed.

No source, infrastructure or Azure resource changed, and no throwaway resource was created. Credentials were read at runtime by the script and never printed; no screenshots are retained.

Evidence folder: [2026-11-18-issue-521-live-1444z](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/).

## Findings

| Check | Result (retained file) |
|-------|------------------------|
| Live app expiry | `ca-resident-demo` revision `ca-resident-demo--0000012`, provisioning Succeeded, min 0, max 1, `ZF_DEMO_EXPIRES_AT` `2028-01-01T00:00:00Z` ([az-ca-resident-demo.json](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/az-ca-resident-demo.json)) |
| Revision health | One active revision, Healthy, created 2026-11-17T20:19:26Z, ScaledToZero ([az-ca-resident-demo-revisions.json](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/az-ca-resident-demo-revisions.json)) |
| Demo API app | `ca-cutover-test-demo-api` revision `0000031`, min 0; its environment names contain no `ZF_DEMO_EXPIRES_AT` ([az-ca-demo-api.json](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/az-ca-demo-api.json)) |
| Jobs | All eight `job-cutover-test-*` jobs have trigger type Manual ([az-jobs.json](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/az-jobs.json)) |
| Source tests | `src/core` `test_resident_showcase` 42 tests OK; `test_resident_showcase_sql` 40 tests OK (27 skipped, need SQL); `infra` `test_resident_demo_secrets` and `test_resident_demo_deploy` 33 tests OK ([core-tests.txt](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/core-tests.txt), [infra-tests.txt](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/infra-tests.txt)) |
| Live sign-in | Playwright desktop 1280x900 against the public HTTPS app: `signed_in` true, title "Your home improvement progress - synthetic showcase, not live", password absent from page text ([live-checks.json](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/live-checks.json); screenshots were removed and are not retained) |
| Cookies and session | `__Host-zfdemo` Secure, HttpOnly, SameSite=Strict, `__Host-zfdemo-csrf` Secure, SameSite=Strict; the session cookie lives about 30 minutes (matches `SESSION_SECONDS` 1800); `/demo/view` without the binding header returns 409; after sign out `signed_in` is false |
| Live SQL window | Not readable: server `sql-cutover-test-rzsrg` has public access Disabled; an Entra-token login is refused with "Deny Public Network Access" ([sql-and-registry-probe.txt](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live-1444z/sql-and-registry-probe.txt)) |
| Image to commit | Registry tag listing denied; digest `sha256:65481780...` cannot be mapped to a commit |
| Apply time | The activity log (14 days, 50 events in `ama`) holds no `ca-resident-demo` event; only the revision creation time is available |

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1 (ticked) Authority end consistent across code, SQL, helper, docs, tests | Proven for source | Focused tests above pass on the `2028-01-01T00:00:00Z` boundary. The January 2027 wording is historical. |
| 2 (ticked) Cost estimate and cap, no resource or role added | Observed earlier (cited note); raw output not retained | This run added nothing. Spend of USD 440.90 against the USD 700 cap was observed earlier on 2026-11-18 and is cited from the [#462 note](./resident-showcase-live-proof-2026-11-18.md); it was not re-read here. |
| 3 (ticked) Rotation and renewal steps documented | Not re-derived | No Key Vault rotation per owner decision. |
| 4 Live Azure change applied after owner confirmation, verified and recorded | Partly observed | Observed with retained raw Azure output: live app setting is `2028-01-01T00:00:00Z` on a healthy revision and a real HTTPS sign-in works with the guards intact (the Playwright result is in `live-checks.json`; screenshots are not retained). Owner confirmation of the value: the issue's 2026-11-03/04 decisions. Unproven: the live SQL constraint and `allowed_case` windows (private-only server), the image source commit (private registry), the apply timestamp (absent from the activity log) and expiry behaviour at the cutoff (not waited out; unit tested). |

## Owner-only or network-only items

* Read-only SQL probe from the private network: the infra README section "Live state check" records the check; a person or runner inside the network can run it. Opening public access or adding a private endpoint is a production change and is not authorised.
* Explicit owner confirmation of the exact live change is recorded only as the issue's decisions; no separate confirmation of the apply event exists.
* Issue #521 stays open on this record: criterion 4 is not fully proven.

## Evidence limits

* Hosted CI, human approval and independent exact-head review are not observed.
* The sign-in script is reused from the [earlier run](../../../.copilot-tracking/evidence/2026-11-18-issue-521-live/live_check.py).
