# Issue 350 research, 2026-11-20 (task issue-350-live)

Research disposition: executed. Planning Readiness: Ready.

Live (revision `ca-cutover-test-demo-api--0000037`, resident `--0000015`), evidence copied to
`docs/reference/research/issue-350-live-r4-2026-11-20/` and summarised in
`docs/reference/research/issue-350-live-r4-2026-11-20.md`.

Findings
* C1 unchanged: anonymous `/api/*` 401 to curl, 302 to browser UA; Easy Auth `RedirectToLoginPage`. Edge change, outside demo authorisation.
* C9: `/api/time/status` now 200 (gated, "switched off"); the earlier 500 is fixed on the deployed image.
* C8: scheduled jobs now exist (`orch` every 5 min, recent runs Succeeded; `audit` 02:00 daily, no execution listed).
* C2/C3/C5 progress: 443 open + 537 closed, agreement across stats, map, list and CSV `view=all`.
* NEW DEFECT (C5/C10 agreement): own-queue list and `/api/me` say 16, CSV/`flag=nodecision`/stats.team say 133.
  Cause isolated: the SQL `cases.owner_code` column disagrees with the case body for 8 of 9 owners (stage, area, wave agree).
  `SqlStore.page_cases` (SQL path) filters on the column; `Store.page_cases` (CSV and nodecision flag) filters on the body.
  `SqlStore._migrate` rebuilds derived columns only when rank policy, schema or support encoding change, so body/column drift is never repaired.
* C4 gate blocked (real_ai_delivery_gate), no release (releases=[], 3 gaps), suspension SUS-1 active. C5 provider public OSM. C6 photo 503. C7 law 503.

Decision: add drift detection/repair for identity columns in `SqlStore._migrate` with a unit test (src/core, FULL tier, local commit only). No redeploy (production change not authorised).
