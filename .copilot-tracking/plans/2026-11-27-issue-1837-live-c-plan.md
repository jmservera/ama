# Issue 1837 plan (run c), 2026-11-27

Refs #1837. Tier: FULL classification because `src/api/checks/` source changes (a browser-check harness, no handler, permission or security control touched). The coordinator owns the gate; this worker does not run `rpi-checks.py --all`.

## Finding that drives the plan

`checks.nomination_browser_check` (read-only nomination view, #1381) fails when the page's background `GET /api/assistants` is still running. `assistants.registry` opens a `BEGIN IMMEDIATE` transaction on its own connection and runs the slow acceptance report inside it, so the harness's out-of-band `nomination_review` write waits the 5 s `busy_timeout` and the 5 s client timeout expires. Evidence: [before-fix diagnosis](../../docs/reference/research/issue-1837-live-2026-11-27-c/lock-diagnosis-before.txt) (two of three probe runs failed).

## Critique (one pass, executed)

Verdict: proceed. Findings applied directly: (1) do not change `assistants.registry` or the SERIALIZABLE/IMMEDIATE transaction policy: that is RAI control-plane behaviour outside #1837 and would need its own research, so record it as a follow-up; (2) the defect is a harness race, so the repair belongs in the check (wait for network idle before the out-of-band write), not a longer timeout, which would hide it; (3) the failure is load dependent, so failing-first evidence is the captured lock-holder stack, and the after-fix proof is repeated runs; (4) live Azure writes stay withheld (irreversible shared-demo records); live evidence is a no-write probe only.

## Steps

* In `src/api/checks/nomination_browser_check.py`, before the second out-of-band `nomination_review`, wait for the page to go network idle.
* Run the check repeatedly, `tests.test_nomination_api_routes`, the standalone-form and challenge axe checks, mypy, ruff.
* Live no-write probe of the deployed demo.
* Research note and per-criterion table in the changes record.
