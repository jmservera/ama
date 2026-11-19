---
title: Issue 349 live demo changes
---

No source code changed (FOCUSED tier; `rpi-checks.py --all` not run). Added or changed:

* docs/reference/research/entra-signin-live-demo-2026-11-18.md (new research note)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/evidence/2026-11-18/issue-349-live/ (scripts, redacted JSON, screenshots, original failed attempts)
* RPI artifacts under .copilot-tracking/{research,critique,plans,details,changes,reviews,rpi-sessions}/

Live actions: Playwright desktop runs against ca-cutover-test-demo-api and ca-resident-demo; curl status probes; read-only `az containerapp auth show` and `az containerapp show`; `az ad app/sp list` denied (insufficient privileges). No Azure change, nothing created, nothing to delete.

## Per-criterion status for #349 (demo)

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Tenant owner provisions app, roles, credential | Partly proven: working GUID registration and role claim; provisioner and audience unreadable |
| 2 | Credential reaches vault via approved in-VNet path | Unproven (not inspected; rotation excluded) |
| 3 | API auth and audience use real registration; callback with prior callbacks preserved | Partly proven: callback works, audiences match; callback list not read |
| 4 | Private staff roster reconciled in VNet | Unproven: `bound` false, demo has no roster |
| 5 | Real user sign-in, `/api/me`, workbench, logout, wrong-role and unknown-staff denial | Proven with test account only; wrong-role inside employee app and real-user parts unproven |
| 6 | Anonymous 401, forged-header denial, positive authenticated request | Partly proven (browser 302s retained; 401 and forged-header results not retained) |

Validation: documentation link and diff review; literal scan of evidence files for the three credential values found no match; no unit tests apply (no src change).
