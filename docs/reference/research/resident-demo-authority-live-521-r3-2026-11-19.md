---
title: Resident Demo Authority End Live Check, Run 3 (Issue #521)
description: Retained raw evidence for the unticked #521 criterion 4 on 2026-11-19, closing the 2026-11-18 retention gaps and stating what stays unproven
ms.date: 2026-11-19
---

## Scope and limits

Refs #521. Synthetic demo, desktop only, under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Only read-only Azure commands ran; nothing was created or changed, so no throwaway resource exists. Credentials were read at runtime and never printed; the filled-form screenshot hides both fields. Run 3 after the [first](./resident-demo-authority-live-521-2026-11-18.md) and [second](./resident-demo-authority-live-521-r2-2026-11-18.md) 2026-11-18 notes; it re-observes the live state with retained raw output and records that the revision has since moved on. The SQL, registry and activity-log probes are not repeated; their refusals are in the second note.

Evidence folder: `.copilot-tracking/evidence/2026-11-19-issue-521-live/` ([az-resident-demo.json](../../../.copilot-tracking/evidence/2026-11-19-issue-521-live/az-resident-demo.json), [az-revisions.json](../../../.copilot-tracking/evidence/2026-11-19-issue-521-live/az-revisions.json), [az-demo-api.json](../../../.copilot-tracking/evidence/2026-11-19-issue-521-live/az-demo-api.json), [live-checks.json](../../../.copilot-tracking/evidence/2026-11-19-issue-521-live/live-checks.json), [core-tests.txt](../../../.copilot-tracking/evidence/2026-11-19-issue-521-live/core-tests.txt), [infra-tests.txt](../../../.copilot-tracking/evidence/2026-11-19-issue-521-live/infra-tests.txt), two screenshots).

## Observations (2026-11-19)

| Check | Result |
|-------|--------|
| App expiry setting | `ca-resident-demo` `ZF_DEMO_EXPIRES_AT` is `2028-01-01T00:00:00Z`. |
| Revision | Latest `ca-resident-demo--0000014`, created 2026-11-18T22:39:23Z, Healthy, ScaledToZero; min 0, max 1. Earlier notes saw `0000012`; `0000014` is newer (changed after those runs, cause not recorded here) and still carries the 2028 value. |
| Image | `zava-resident-demo@sha256:65481780...bbbd19` in the private registry; source commit not derivable. |
| Demo API app | `ca-cutover-test-demo-api` revision `0000033`, min 0, no expiry-named setting (matches the infra README). |
| Live sign-in | Playwright desktop run over HTTPS: `signed_in` true, title "synthetic showcase, not live", password absent from page text, `/demo/view` without the binding header returns 409, signed out afterwards. |
| Cookies | `__Host-zfdemo` Secure, HttpOnly, SameSite=Strict; `__Host-zfdemo-csrf` Secure, SameSite=Strict. |
| Source tests | `src/core` `test_resident_showcase` and `test_resident_showcase_sql`: 82 tests OK (27 skipped, SQL-dependent). `infra` `test_resident_demo_secrets`: 16 tests OK. |

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1 (ticked) Authority end consistent across code, SQL, helper, docs, tests | Proven for source | Source tests above; the issue's January 2027 wording is historical. |
| 2 (ticked) Cost estimate and cap; no resource or role added | Not re-derived | This run added nothing; prior record stands. |
| 3 (ticked) Rotation and renewal steps documented | Not re-derived | No Key Vault rotation per owner decision. |
| 4 Live change applied after owner confirmation, verified and recorded | Partly proven | Proven with retained output: live app expiry `2028-01-01T00:00:00Z` and working HTTPS sign-in. Owner confirmation of the exact value is the issue's 2026-11-03/04 decisions. Unproven: the live SQL constraint and `allowed_case` windows (server `sql-cutover-test-rzsrg` is private-only; querying through the app would exceed a read-only check), the apply timestamp of the 2028 value (revision `0000014` supersedes the one that carried it, so Azure metadata does not date the change), and the source commit behind the image digest. |

## Conclusion

No source change is justified; the remaining gap is live SQL access, which needs a person with private-network access running the read-only probe in the infra README section "Live state check". #521 stays open on this record. Hosted CI, human approval and independent exact-head review are not observed.
