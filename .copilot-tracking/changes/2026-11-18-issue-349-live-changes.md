# Changes: issue 349 live round 3

Tier FOCUSED; no src change. Azure: reads only, no resource created or changed.

## Files

* docs/reference/research/issue-349-tenant-prerequisites-live-r3-2026-11-18.md (new)
* docs/reference/README.md and docs/reference/log.md (index row, appended entry)
* .copilot-tracking/evidence/2026-11-18/issue-349-live2/ (new round 3 files: proof2.py, proof2.json, curl-status.txt, auth-show.txt, secrets.txt, kv-network.txt, env.txt, env-auth.txt, app.txt; workbench screenshot not retained)

## Per-criterion status (issue 349)

| # | Criterion | Status | Reason |
| --- | --- | --- | --- |
| 1 | Owner provisions single-tenant app, roles, credential | Partly proven | Registration, vault credential, role claim work; provisioner, audience, role definitions unreadable (Graph denied) |
| 2 | Credential via private vault, in-VNet, nothing published | Proven for demo | Key Vault reference via user-assigned identity; vault public-disabled with private endpoint |
| 3 | API auth/audience use registration; edge callback, prior callbacks preserved | Partly proven | Edge callback registered (sign-in completes); prior callback list unreadable |
| 4 | Private staff roster reconciled, replicas reloaded | Unproven, not applicable to demo | No roster supplied; admission by Entra identity and role |
| 5 | Real user callback, /api/me, workbench, logout, switching, wrong-role/unknown-staff denial | Proven with test account only | No real person, second-role account or roster |
| 6 | Anonymous 401, forged-header denial, positive request | Proven with qualification | curl 401; browser 302 by design; /api/cases 200 |

No issue box is ticked. Validation: see review record.
