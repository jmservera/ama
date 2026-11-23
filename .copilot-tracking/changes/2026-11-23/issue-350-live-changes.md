---
title: Issue 350 live changes (2026-11-23)
---

Refs #350. Tier FOCUSED: no `src/` change. Files added: docs/reference/research/issue-350-live-r6-2026-11-23.md, its raw/ and scripts/ folders, one index row and one log entry. All Azure calls were reads; no resource was created, so nothing to delete. No box on #350 is ticked.

Live targets: api `ca-cutover-test-demo-api--0000054`, resident `ca-resident-demo--0000026`. Main: HEAD 342fad401d, `src/` identical to origin/main ed9500a188.

## Per-criterion table

| # | Criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | Anonymous protected API 401 for browser-style requests, page redirect kept | Unproven at the edge; app side proven | App test passes on main. Live browser User-Agent still gets 302 on `/api/me`, `/api/cases`, `/api/staff`; fix is a platform auth change (infrastructure, outside the demo authorisation) |
| 2 | Every dated row and 16 assets through the public app with authorised roles | Partly proven | Staff sign-in and 28 GET reads; matrix rows, assets, second role and writes not executed |
| 3 | Representative continuing synthetic baseline | Partly proven | 980 cases, 601 work orders, 167 funding, 30 visits, 13 finance, 1 package; restore authorisation not visible |
| 4 | Models, bounded release, five assistants, workflow-only, durable state | Partly proven | 5 assistants, 9 tasks, deployments present, briefing template with SUS-1; release gate blocked (human decision), no model call made |
| 5 | Licensed map provider; map, list, chart, CSV, sensor agreement | Partly proven | 443 map points equal open KPI; OSM tile URL set, licence approval unproven; export and sensors 403 for this role |
| 6 | Delegated photo tokens, consent, binary photo, switching | Unproven | `/api/account/photo` 503 with fallback text; needs authorised consent |
| 7 | Versioned law store configured and seeded | Partly proven | Store responds, 4 cards; 0 sources, `law-snapshots` empty; seeding and approvals human-owned |
| 8 | Ledger, document, digest durability, scheduled jobs | Partly proven | Chain intact 5976 entries; 4 digest blobs; audit job `LEDGER_DIGEST_OK` at 2026-11-22 02:00; jobs succeed; document durability and scanning not re-run |
| 9 | Time capture gated, explanation, case work independent | Proven for the demo | `enabled` false, 403 on personal endpoint, explanatory view, case endpoints 200 |
| 10 | Per-role workflow, consent, finance, chat, export, law, recovery results | Unproven | One role, read-only; no consent, chat, export, recovery or second-role result |
