# Changes: issue 2202 live deploy

Refs #2202. Tier: FULL classification applies because `src/api` changed (receiver fix); the complete gate is for the coordinator and `rpi-checks.py --all` was not run. Local checks run: `test_iot_stream` (45), `test_live_receiver_sql`, `test_live_control`, mypy, ruff check and format.

## Changes

* Azure (image updates only, no Bicep, no throwaway resource): two pushes through `/tmp/acr-push.sh`, registry read back Disabled/Deny after each; API app, `job-live-simulator` and `job-live-receiver` set to digest `sha256:295164ca739d5602ca323c65c305cff9d76a3e72faa4623e0dfa931363fd4f72` (API revision `ca-cutover-test-demo-api--0000045`). Rollback digest `sha256:60b1d026...4447878` (revision 0000043).
* Divergence from plan: the first rollout (digest `131a4748...`, revision 0000044) failed three receiver runs with `IOT_OPERATION_TIMEOUT`; `src/api/src/zava_forward/api/iot_stream.py` and `src/api/tests/test_iot_stream.py` changed, rebuilt and redeployed.
* Docs: `docs/reference/research/issue-2202-live-deploy-2026-11-22.md` plus probe folder, `docs/reference/log.md`, `docs/reference/README.md`, `infra/README.md`.

## Per-criterion table (issue 2202 acceptance)

| Criterion | Status | Evidence |
| --- | --- | --- |
| API, resident, simulator and receiver images rebuilt from main and rolled | Partly proven | API, simulator and receiver rolled (digest above). Resident image not rolled: outside this goal |
| Revisions Running and Healthy; hardening enforced with rollback noted | Partly proven | Revision 0000045 Healthy, Running, 100% traffic; rollback noted; `ZF_CONTAINER_HARDENING` is in the app env list; agents-app difference not examined |
| Owner demo checks: sensor charts, map gauges, consent checkbox, chat routing, half of homes with readings | Partly proven | Charts, gauges, checkbox and chat routing proven live; readings stored for 110 of 441 homes (24.9%), half-of-homes unproven |
| Live receipt and log entry | Proven | Receiver `job-live-receiver-29922000` Succeeded; log entry added |

| Per-issue | Status |
| --- | --- |
| 2191 | Partly proven (cohort 222 of 443; stored readings 110 of 441) |
| 2192 | Partly proven (checkbox live; employee effect needs resident image) |
| 2193 | Proven (gauges under latest reading, fresh state) |
| 2195 | Proven (12 asks, 0 non-200 on two revisions) |
| 2201 | Partly proven (one Succeeded run; three consecutive unproven; 04:30 run was still running at record time) |
