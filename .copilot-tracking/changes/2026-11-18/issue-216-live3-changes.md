# Changes: issue 216 live3

No src change. Tier FOCUSED (documentation and evidence only; basis: no source, workflow, infrastructure or SQL edit). `rpi-checks.py --all` not run.

Files: research note section (eval-gates-live-216-2026-11-18.md), authorization-live3.json, raw-live3/, report-live3.json, unit-tests-raw-live3.txt, scripts inter.py and mk.py, log entry.

Live actions: four throwaway servers inside ca-cutover-test-demo-api via one `az containerapp exec` session; 18 model calls, 20,128 tokens (limit 30 and 60,000; list price well under USD 0.01). Earlier failed attempts (command length 404, exec 429 rate limit, case view fields causing HTTP 500) made no model calls. No Azure resource created; temporary stores and the session-state file deleted.

Validation: unit tests core (31) and agents (76) OK, raw in unit-tests-raw-live3.txt. Not run: mypy and ruff (no Python source in src changed; helper scripts live in docs evidence), hosted CI (nothing pushed).

## Per-criterion table (issue 216, unticked criteria only)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set | Proven for the demo, with limits | refusals 10 of 10; cited model answers 9 of 9 valid (14 model answers); adversarial 10 of 10; strict failures G05, G06, U01 disclosed; single synthetic case; owner not independent. Note section "Third live pass". |
| Production owner sign-off by named Legal and Compliance professionals, independent grader | Unproven, not needed for demo | Waived by owner decision 2026-11-18 for demo. |
| Citation validity against regulatory rule cards | Unproven for demo | Regulatory chat role not held by the test account. |

Ticked criteria were not re-proven.
