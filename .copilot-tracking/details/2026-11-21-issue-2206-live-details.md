# Details: issue 2206 (2026-11-21)

* `check_revisions(app)`: active revisions with health, running state, traffic; fail if no active Healthy revision with 100 traffic total.
* `check_jobs(job)`: latest execution status; fail if Failed, warn if none.
* `check_health(app)`: GET https://{fqdn}/healthz; pass on 200.
* `check_counts(reader)`: cohort homes and consent granted/declined/other from sensor_consumer_control; unavailable on reader error.
* CLI: `python3 tools/demo_preflight.py [--resource-group ama] [--strict]`; apps default ca-cutover-test-demo-api, ca-resident-demo; jobs default job-cutover-test-demo-load/-audit/-orch, job-live-simulator, job-live-receiver.
