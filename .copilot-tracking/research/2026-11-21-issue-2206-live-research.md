# Research: issue 2206 demo preflight (2026-11-21)

Disposition: executed. Planning Readiness: Ready.

## Issue

Acceptance (both unticked): (1) checks revisions, job statuses, health, cohort and consent counts without printing secrets; (2) output usable as the runbook preflight record.

## Evidence (live, resource group ama, read-only az commands)

* `az containerapp list -g ama`: ca-cutover-test-demo-api, ca-resident-demo, ca-cutover-test-demo-agents.
* `az containerapp job list -g ama`: job-cutover-test-demo-load, -audit, -orch, job-live-simulator, job-live-receiver.
* `az containerapp revision list`: api revision 0000039 Active, Healthy, Running, traffic 100; resident revision 0000015 Active, Healthy, RunningAtMaxScale, traffic 100.
* `az containerapp job execution list -n job-live-simulator`: latest execution Succeeded.
* `GET /healthz` on both FQDNs: api returns `ok`; resident returns `{"status": "ok", "synthetic": true, "ready": true}`.
* Cohort and consent counts live in SQL tables (sensor_consumer_control, sensor_consumer_control_home). `az sql server show` reports public network access Disabled; a token-based pyodbc connection from this host is refused ("Deny Public Network Access"). The Log Analytics link of the environment is null (azure-monitor destination), so no log source carries the counts.

## Conclusions

* Revisions, job statuses and health are provable live from this host.
* Counts need a SQL path inside the private network; from this host they can only be reported as `unavailable` with the reason. The script therefore takes an injectable count reader (AAD token via `az account get-access-token`, no secret printed) and reports `unavailable` rather than failing silently.
* Hard rule: never print tokens, connection strings or env values; only names, states and counts.
