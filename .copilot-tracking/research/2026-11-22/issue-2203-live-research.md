# Issue 2203 research (2026-11-22 run)

Research disposition: executed. Planning Readiness: Ready. Tier: FULL for the src change (one core file), documentation for the rest; the full gate is run by the coordinator, never by this worker.

Evidence: docs/reference/research/issue-2203-live-2026-11-22/ (probe scripts, results, screens). The prose note is docs/reference/research/issue-2203-runbook-live-2026-11-22.md.

## Findings since the 2026-11-21 run (all observed 2026-11-22, UTC)

* The runbook (#2207) is stale against the estate: staff app revision 0043 and resident revision 0020 are deployed (#2192 checkbox, #2196 dual-axis chart, #2198 intermittent readings and #2199 routing all merged and live). Hardening is `enforced` on the staff app, both live jobs and the agents app. `ZF_ASSIST_QUALITY_DEMO_HOMES` is set to five homes.
* Cohort now: 5 of the 21 probed homes read `ok/stale` (12 readings, newest about 51 to 58 minutes old), 16 read `consent-withheld`. Map totals: 443 homes, 25 stale, 7 consent-withheld, 68 no-readings, 343 not-loaded. No home is fresh because readings stopped at about 00:40 UTC while the simulator job still reads Succeeded; the receiver job reads Failed (#2201 open). A live "Reading out of date" alert therefore exists (stale, not the 24 hour offline state).
* Resident app: sensor consent checkbox is live and unchecked; one grant and revoke cycle returned HTTP 200 twice and left it unchecked. Chat routes: documents question to the Documents helper, damp and mould to the Safety route helper, off-topic to the General assistant. Resident AI is disabled by the hard-coded exercise end (EXPIRES 2026-11-01 in resident_demo/assistant.py): labels read "AI unavailable: the AI exercise has ended".
* Operator-triggered AI scope read live: `quality_scope` mode demo-homes with five homes, trigger operator-requested-only, per_reading_calls none, model_call_authority_present false; `proactive` false.
* DEFECT: `GET /api/assistants/forecast` took 153 s and, while it ran, `/api/map` returned HTTP 500 after 15 s (probe4). Cause: `Assistants.forecast` runs inside `transaction()`, which on Azure SQL takes the exclusive application lock (BEGIN IMMEDIATE) for the whole call. It is read-only, so it needs no lock. This also explains the 2026-11-21 transient "Home sensors are unavailable" and the browser employee chat "unexpected error" seen in this run.
* Not provable: employee chat answer (blocked by the lock while a forecast was pending; the re-test needs the fix deployed), live 24 hour offline, wrong-role denial (one staff account), log-level receiver cause (workspace denies public access).
