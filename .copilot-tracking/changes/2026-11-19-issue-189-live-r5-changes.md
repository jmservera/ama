# Changes r5: issue 189

* `src/core/src/zava_forward/core/synthetic/run_live_check.py`: budget selected by hub resource scope, name fallback.
* `src/core/tests/test_run_live_check.py`: one new test.
* `docs/reference/research/issue-189-live-r5-2026-11-19.md` and evidence folder; index and log entries.

Validation (FOCUSED; no infra/SQL/security scope; rpi-checks --all not run): `ruff format --isolated --line-length 100 --check` on both files OK; `ruff check` OK; targeted unittest (run_live_check, simulator_run_controls_189, simulator_run_budget_controls) 39 tests OK; `python3 -m mypy` in src/core reports 22 errors in 3 files, identical before and after the change (missing opentelemetry stubs), none in run_live_check.

Live: throwaway job and temporary role created and removed; 3 devices deleted. Spend not measurable here; run lasted under 3 minutes at 0.5 vCPU.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Cost estimate before any run | proven earlier (ticked) |
| Quota headroom vs #140 | proven earlier (ticked), live hub B1 x1 |
| Run has an owner | proven for the demo |
| Run has a time limit | proven for the demo (live halt at expiry) |
| Run has a budget alert | configuration proven; delivery UNPROVEN (unreachable recipients; infra change not made) |

Unmet: the issue criterion stays unticked pending owner decision.
