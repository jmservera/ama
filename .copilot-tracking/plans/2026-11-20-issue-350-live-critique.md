# Critique: issue 350 live plan (2026-11-20), one pass

Verdict: proceed.
* Risk: startup cost of parsing every body. Accepted for the demo scale (980 cases); repair is limited to drifted rows. Dispositioned: applied (compare only six identity columns).
* Risk: body may be the wrong side. Body is the source of truth (memory, API item payloads and audit all derive from it); columns are documented derived. Applied.
* Risk: Azure SQL (MssqlStore) path untested locally. Repair uses the same UPDATE as the existing stale rebuild; flagged as unproven live because no redeploy is authorised.
* Not changing the edge (C1), law, photo, models: human/infrastructure-owned.
