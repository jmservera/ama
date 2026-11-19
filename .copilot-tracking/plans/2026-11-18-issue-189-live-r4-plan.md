# Plan r4: issue 189 live-state verifier

* [x] Add `src/core/src/zava_forward/core/synthetic/run_live_check.py`: `verify_live_run_controls(hub, budgets)` returns per-check results (owner tag, tier and capacity, budget cap, enabled actual and forecast alerts, recipient reachability class); CLI over JSON files; exit 3 on any failing check; emails never printed.
* [x] Add `src/core/tests/test_run_live_check.py`.
* [x] Run focused tests, mypy, ruff format and check.
* [x] Run read-only live `az` capture, feed the CLI, record in `docs/reference/research/issue-189-live-state-verifier-evidence-2026-11-18.md` with a per-criterion table; update index and log.
* [x] Changes, review, commit.

Details: [details](../details/2026-11-18-issue-189-live-r4-details.md). Tier: src changes, so FULL applies, but `rpi-checks.py --all` is forbidden by the brief; no full receipt is claimed. Focused checks run and recorded instead.
