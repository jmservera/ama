---
title: Issue 2203 live evidence for the 2026-11 demo runbook rewrite
description: Dated live observations of the synthetic demo cohort, cadence, consent mix, resident view, charts and hardening status, with a per-criterion proven or unproven table for the runbook rewrite
author: AMA RPI agent
ms.date: 2026-11-21
ms.topic: reference
keywords:
  - issue 2203
  - demo runbook
  - live demo
estimated_reading_time: 7
---

Refs #2203. Scope is the synthetic desktop demo in resource group `ama`, under the owner decisions of 2026-11-18. Documentation only: no source, infrastructure or Azure resource was changed or created, so nothing needed deleting. Sign-in values were read at run time from the owner files and appear in no retained output (each probe asserts this before it writes a file). Times are UTC on 2026-11-21.

The probes are [probe.py](./issue-2203-live-2026-11-21/probe.py) (staff) and [probe_resident.py](./issue-2203-live-2026-11-21/probe_resident.py) (resident). Results are in [probe-result.json](./issue-2203-live-2026-11-21/probe-result.json) and [probe-resident-result.json](./issue-2203-live-2026-11-21/probe-resident-result.json). Screenshots are under [screens](./issue-2203-live-2026-11-21/screens/).

## Observed

| Item | Observation (2026-11-21) |
| --- | --- |
| Estate | `ca-cutover-test-demo-api` revision `0000039`, Healthy; `ca-resident-demo` revision `0000015`; `ca-cutover-test-demo-agents` scaled to zero. Jobs `job-live-simulator` and `job-live-receiver` exist |
| Cadence | Simulator executions started 10:15, 10:20, 10:25 and 10:30 and the three finished ones read `Succeeded`. Receiver executions started 09:30 and 10:00 read `Failed`, the repository's designed `RUN_DEADLINE` exit at the end of each 1500 second window, as recorded in the [184 note](./issue-184-live-demo-sim-consent-mix-2026-11-20.md) |
| Cohort and consent mix | `/api/map` as Retrofit Programme Manager: 443 homes, 10 with a `fresh` sensor state, 90 `no-readings`, 343 `not-loaded`. The 10 fresh homes are the first 10 of the 20 simulator homes listed in the 184 note; the consent mix (10 granted, 10 declined) was applied on 2026-11-20 and is not re-read here |
| Freshness | Newest reading age across the 10 fresh homes was at most 611 seconds in the run at 10:40, against the 900 second fresh rule |
| Granted home | `ZF-2025-0031`: API state `ok`, 12 readings; Home sensors tab reads "Recent reading (within 15 minutes)", "Alerts for this home: No sensor alerts for this home", a latest reading and a 12 row table ([screenshot](./issue-2203-live-2026-11-21/screens/home-sensors-granted.png)) |
| Declined and no-control homes | `ZF-2025-0148` and `ZF-2025-0331`: API state `consent-withheld`, zero readings; tab reads "Readings withheld: monitoring consent is not granted" with owner and next action ([screenshot](./issue-2203-live-2026-11-21/screens/home-sensors-declined.png)) |
| Transient failure | In one earlier run at about 10:34 both tabs read "Home sensors are unavailable right now" while the same API calls returned 200 over the request context; the next run read correctly with browser responses 200. One occurrence; cause not established |
| Employee charts | `#/progress` shows six charts with headings "Cases opened and closed per day", "per week", "Backlog trend", "Cases by journey step now", "Workload by team now" and "AI briefing review outcomes" ([screenshot](./issue-2203-live-2026-11-21/screens/progress-charts.png)). These are case-flow charts, not sensor charts |
| Resident view | Signed in as the shared resident test user: section "Your home sensors and forecast" reads "newest stored reading is recent (within 15 minutes)", latest 21 Nov 2026 10:30 UK time, a temperature and a humidity history chart over 48 readings with a dashed 24 hour forecast labelled an estimate, and a table alternative ([screenshot](./issue-2203-live-2026-11-21/screens/resident-signed-in.png)) |
| Resident checkbox | The deployed resident page has 0 checkboxes in the sensors section. The monitoring consent checkbox of #2192 is not deployed: the live app is still revision `0000015` |
| Resident chat | The "Help with your case" panel carries an own-record consent checkbox (`assistant-consent`), a question box, a skill selector, and the copy "Each answer says whether AI or rules were used" and "This chat does not send messages to staff". `ZF_DEMO_ASSISTANT_ENABLED` is `true`. No question was sent in this run |
| Offline-sensor alert | The stale or offline filter exists on the overview map ("Show only homes with stale or offline sensors"). No live home is stale or offline: `stale_or_offline_homes` is empty. `src/api` `tests.test_home_sensors_tab` ran 21 tests, OK, covering the "Sensor may be offline" state and the one second switch at 24 hours |
| Role | `/api/me` returns role Retrofit Programme Manager, app role `ZavaForward.ProgrammeManager`, `trusted-proxy` authentication. The tab for another role is covered by the source rule that restricts readings to a Quality Inspector or Retrofit Programme Manager |
| Hardening | `ZF_CONTAINER_HARDENING` is `off` on `ca-cutover-test-demo-api` and `job-live-simulator`, unset on `ca-resident-demo`, `enforced` on the agents app, which still runs the pre-fix image digest `sha256:2217d94d...`. The [144 receipt](./issue-144-live-hardening-receipt-2026-11-21.md) shows a throwaway replica with the current image healthy under enforcement |
| Operator-triggered AI scope | `GET /api/assistants/forecast` timed out at 90 seconds and `/api/assistants/rai-metrics` returned 503 once in this run. The [1288 r6 note](./issue-1288-live-r6-quality-sensor-evidence-2026-11-21.md) recorded `proactive: false` and `call_allowance: 0` with the Quality model refused at release admission. No model call was triggered here |

## Per-criterion result

| Criterion | Result | Basis |
| --- | --- | --- |
| 1. Cohort, cadence, consent mix, resident checkbox, chat routing, charts and operator-triggered AI scope described with dated status | Proven that the runbook can describe each with a dated status; live proof is mixed | Cohort, cadence, consent mix, charts and resident chart observed live. Checkbox observed absent live (source and local proof only). Chat panel inventory observed, no question sent. AI scope not re-read live (forecast timed out); the 1288 r6 reading is cited with its date |
| 2. Stale five-home table replaced or relabelled; links checked | Proven | The runbook relabels the table as the superseded 2026-11-12 target and adds the 20-home section; links checked by a script and the `test_generated_dataset` parser test |
| 3. Offline-sensor alert, role proof and hardening status included | Proven as documentation; offline alert unproven live | Hardening and role read live. No home is offline, and creating one would mean stopping the shared simulator, which the brief did not ask for. Local test evidence only |
| 4. Honest Observed versus Not verified wording | Proven | Each runbook status row separates Observed from Not verified with a date |

Not proven for the demo: a live offline-24h alert, a deployed resident consent checkbox, a live resident chat answer in this run, a fresh operator-triggered AI scope read, and wrong-role denial from a second staff account (only one staff test account exists). Azure billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo (owner decision of 2026-11-18).
