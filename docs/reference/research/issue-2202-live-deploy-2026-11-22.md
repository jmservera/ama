---
title: Issue 2202 live deploy of the merged demo changes (demo, 2026-11-22)
description: Image build, safe registry push and rollout of origin/main 0d2081ef7a to the demo API and live jobs, the receiver deadline defect found on the first rollout, live proofs and a per-issue table
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`, owner decisions of 2026-11-18. Sign-in values were read at run time and never printed. Probes and outputs sit in [issue-2202-live-deploy-2026-11-22/](./issue-2202-live-deploy-2026-11-22/); watcher logs and execution lists are under `.copilot-tracking/evidence/2026-11-22/issue-2202-live/`.

## What was deployed

* Source: `origin/main` 0d2081ef7a (PRs 2224 to 2228), then the same tree plus one receiver fix (below).
* Push route: `/tmp/acr-push.sh` (opens the registry, waits 150 s, pushes, restores in a trap). Read back after both pushes: registry `crcutovertestrzsrg` public access `Disabled`, default action `Deny`, export policy `disabled`, no IP rules. No Bicep deployment was run.
* Updates, image only: `az containerapp update` on `ca-cutover-test-demo-api` and `az containerapp job update` on `job-live-simulator` and `job-live-receiver`.

| Step | Image digest | API revision | Result |
| --- | --- | --- | --- |
| Before | `sha256:60b1d026...4447878` | `--0000043` | rollback target |
| Main as merged | `sha256:131a4748bea8...ba34d` | `--0000044` | Healthy; receiver runs 02:30 and 03:00 and 03:30 Failed |
| Main plus receiver fix (final) | `sha256:295164ca739d...4f72` | `--0000045` | Healthy, 100% traffic, 1 replica; receiver 04:00 run Succeeded |

No throwaway resource was created.

## Defect found on the first rollout

Executions `job-live-receiver-29921910`, `-29921940` and `-29921970` failed on the merged image. The live stream recorded `stderr F Cannot run: IOT_OPERATION_TIMEOUT` at 03:25:30, the end of the 1500 s window (`watch-job-live-receiver-29921940.txt`). Cause: `HubReceiver` calls `_bounded(sql, deadline)`; when the deadline passes while a write is in flight the callback records `IOT_OPERATION_TIMEOUT` as a failure, so a busy window ends as Failed. Fix in `iot_stream.py`: in a bounded window that timeout ends the window normally; a non-bounded run still fails. Test `test_bounded_window_ends_normally_when_the_deadline_hits_a_write` fails without the change and passes with it; `test_iot_stream` (45 tests), `test_live_receiver_sql`, `test_live_control`, mypy and ruff pass.

## Live proofs on revision `--0000045` (digest `295164ca...`)

| Check | Evidence | Result |
| --- | --- | --- |
| Revision health | `az containerapp revision list`: Healthy, Running, traffic 100 | Proven |
| Chat routing, no 500s | `live_routing_probe.json`: six questions, one attempt each, seven chat POSTs all 200; routes quality, funding, stock, tie to General, general, refused to General. Same on revision 0000044 (six questions, all 200). Screenshots `live-*.png` | Proven (12 asks, 0 non-200) |
| Consent checkbox | `live_probe.json`: native checkbox, grant then withdraw, status text changes, focus stays, choice survives reload; resident left unticked | Proven on the resident page |
| Employee view follows the resident choice | Employee states unchanged for all 50 cases (14 `ok`, 36 `consent-withheld`) before, after grant and after restore | Unproven: the resident fix (PR 2225) lives in the resident image `ca-resident-demo--0000020`, which this task did not redeploy |
| Map-card gauges | `live-map-card-probe.json`, `live-map-card-top.png`, `live-map-card-gauges.png`: two `meter` elements (temperature 0 to 40, humidity 0 to 100) under the Latest reading text, fresh state "Recent reading (within 15 minutes)", no running animations | Proven for a fresh reading; the earlier stale capture on the same card shows the out-of-date note |
| Employee chart | `live-chart-probe.json`: dual axis, dashed humidity, 12 readings | Proven |
| Simulator job | 445 secrets (222 certificate pairs and control file), `failureRate` env present, every execution Succeeded from 04:00 to 04:25 | Runs; see coverage |
| Coverage of homes | `live_coverage.json` at 04:28 UTC: 441 homes read, 109 `fresh` and 1 `stale` readings (110, 24.9%), 7 `consent-withheld`, 324 `no-readings` | Half the homes are in the simulator cohort (222 of 443), but stored readings cover about a quarter because declined homes store nothing. "At least half of homes" is not met as stored readings |
| Receiver run | `job-live-receiver-29922000`, started 04:00, ended 04:25:37 UTC, Succeeded on the final image | One success proven; three consecutive not shown |

## Per-issue table

| Issue | Status | Evidence and limit |
| --- | --- | --- |
| 2191 simulator cap and failureRate, half of homes | Partly proven | Cap and `failureRate` run live (445 secrets, Succeeded runs); the cohort is 222 of 443 (50.1%, earlier note). Stored fresh readings 110 of 441 (24.9%), so the half-of-homes reading criterion is unproven |
| 2192 consent checkbox | Partly proven | Checkbox proven live. Employee-side effect unproven until the resident image is rebuilt and deployed (outside this goal) |
| 2193 map-card gauges | Proven | Live card shows gauges under the latest reading with a fresh reading; stale, offline and withheld card states are test-only |
| 2195 chat routing, no 500s | Proven | 12 asks over two revisions, 0 non-200; the SQL statement serialisation (PR 2227) is deployed. Root cause of the earlier 500s is not independently read (Log Analytics denies this client) |
| 2201 receiver run succeeds | Partly proven | One Succeeded 25 minute run on the final image after a defect fix (above). Three consecutive successes, and the database cause of earlier refusals, remain unproven |

## Follow-ups

1. Rebuild and roll the resident image so the employee view reflects the resident choice (2192).
2. Watch the next two receiver runs (04:30, 05:00) for three consecutive successes (2201).
3. Decide whether declined homes should count towards the half-of-homes reading target (2191).
