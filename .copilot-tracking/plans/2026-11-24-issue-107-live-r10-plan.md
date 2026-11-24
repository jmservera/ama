# Issue 107 live r10 plan (2026-11-24)

Tier: FULL for src-adjacent test code (`src/api/tests`), but `rpi-checks.py --all` is not run (coordinator runs gates). Focused local checks: ruff, mypy, targeted unittest on SQLite and local docker SQL Server 2022.

## Steps

1. Extend `assistant_process_worker.py` VARIATIONS with `data` (capability categories), `provenance` (assistants.PROVENANCE) and `model` (provider serving version).
2. In `test_assistant_release.py` `ProcessRaces`: add data-variation test via the existing `check_changed_binding_process`, and a global-variation helper for provenance and model (changed process runs only the target task; fresh original-binding process stays denied, allowance not replenished, no extra provider calls).
3. Run on SQLite, then on docker SQL Server (`ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=localhost`); delete the container afterwards.
4. Research note under docs/reference/research, knowledge-base index and log entries.

## Critique (executed once)

* Risk: global variations also revoke other capabilities in the changed process. Mitigation: run only the target task there and assert other capabilities untouched.
* Risk: duplicating in-process coverage. Accepted: the new tests add the separate-OS-process dimension only.
* Verdict: proceed; no conflict with confirmed decisions. No Azure resource is created.
