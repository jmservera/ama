# Plan: issue 2206 demo preflight (2026-11-21)

Tier: focused (tools/ and tests only, no src change; classification basis: no workflow, dependency, permission or src edit). Targeted tests only; no rpi-checks --all.

* [x] Phase 1: tools/demo_preflight.py with injectable runner (az calls), http getter and count reader.
* [x] Phase 2: tools/test_demo_preflight.py using fakes.
* [x] Phase 3: live run, record output in docs/reference/research/demo-preflight-2026-11-21.md; index and log entries.

## Critique (executed once, 2026-11-21)

Verdict: accept with direct dispositions.

* Counts cannot be read live from this host (SQL private): report `unavailable` with reason, exit status distinguishes fail (exit 1) from unavailable (exit 0 unless --strict). Applied.
* Secrets: runner outputs are parsed to a fixed field whitelist; no env, no token echo; errors print only the az exit code and a trimmed first stderr line with no env. Applied.
* Read-only: only `az containerapp revision list`, `az containerapp job execution list`, `az containerapp show` (fqdn), `az account get-access-token` for the SQL count path, and GET /healthz. A test asserts no argv contains create, update, delete, start, restart or exec. Applied.
* Output: Markdown table with UTC timestamp, usable as the runbook record. Applied.
