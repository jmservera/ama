# Changes r4: issue 189 live-state verifier

Refs #189. Complete. Tier: src changed (FULL class), but `rpi-checks.py --all` is forbidden by the brief and was not run; no full receipt is claimed. Focused checks below.

## Files

* `src/core/src/zava_forward/core/synthetic/run_live_check.py` (new): `verify_live_run_controls` and CLI over `az` JSON.
* `src/core/tests/test_run_live_check.py` (new): 6 tests.
* `src/core/README.md`: usage paragraph.
* `docs/reference/research/issue-189-live-state-verifier-evidence-2026-11-18.md` and its folder (hub.json owner redacted, budgets with address local parts redacted, verifier output).
* `docs/reference/README.md`, `docs/reference/log.md`: index and log.
* State file reset to task `189-live-r4`; earlier tracked r1/r3 artifacts preserved.

## Validation (from `src/core`)

* `PYTHONPATH=src:tests python3 -m unittest tests.test_run_live_check tests.test_simulator_run_controls_189 tests.test_simulator_run_budget_controls`: 38 tests OK.
* `python3 -m mypy`: no issues in 398 source files.
* `python3 -m ruff check` on the two new files: clean. `ruff format --isolated --line-length 100 --check`: clean.
* Live read-only `az iot hub show` and `az consumption budget list` (resource group `ama`) fed to the CLI: exit 3, only `recipient_reachable` fails.
* Not run: `rpi-checks.py --all`, hosted CI, `src/api` tests (no api files changed), web checks (no web files changed).

## Per-criterion table

| Criterion | Proven or unproven | Evidence or reason |
| --- | --- | --- |
| Cost estimate for N homes before any run (ticked) | Proven (earlier, unchanged) | `run_plan` estimate tests; 38 tests OK |
| Quota headroom against #140 tier (ticked) | Proven (earlier, unchanged) | Live hub B1 capacity 1 passes `hub_tier` |
| Run has an owner | Proven | Live owner tag passes `owner_tag`; blank owner refused in tests |
| Run has a time limit | Proven in code/tests; not live | `RunMeter` and job replica timeout; no simulator job deployed, deploying is a production change not authorised |
| Run has a budget alert | Configuration proven live; delivery unproven | `alert_actual` 80 and `alert_forecast` 100 enabled; recipients noreply, `recipient_reachable` fails; firing needs spend at threshold |
| Criterion 3 as a live conjunction | Unproven | Needs a deployed run and a monitored recipient; owner action |
