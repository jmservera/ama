---
title: Issue 349 live6 changes
ms.date: 2026-11-19
---

No source, test, infrastructure or cloud change. Only `.copilot-tracking` artifacts were added.
Tier: FOCUSED applies by default; no source file changed, so no unit test, mypy or ruff run is
applicable. `rpi-checks.py --all` was not run.

## Per-criterion table (demo, synthetic, desktop)

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Tenant owner provisions app, roles, credential | Unproven | Needs Application Administrator; Graph reads denied (r5) |
| 2 | Credential in private vault via in-VNet path | Proven for the demo | r5: Key Vault reference, public access disabled, private endpoint |
| 3 | API auth and audience use the registration; callbacks preserved | Partly proven | Sign-in works; prior callback list unreadable |
| 4 | Private roster reconciled in VNet, replicas reloaded | Unproven, not applicable | No owner-supplied roster |
| 5 | Real user session, logout, switching, wrong-role and unknown-staff denial | Proven for the test account; denial unproven | Resident account sign-in failed twice (r5) |
| 6 | Anonymous 401, forged-header denial, positive request | Proven with qualification | curl 401; browser redirect to Entra; `/api/cases` 200 signed in |

No box on #349 is ticked. Remaining criteria are tenant-owner actions or need a second-role human sign-in.
