# Details: issue 144 current-main integration (Refs #144)

Plan: [plan](../../plans/2026-11-09/issue-144-current-main-plan.md).

## P2 command

`git merge --no-ff origin/main -m "merge: integrate main df8e858b into issue 144 queue slice (Refs #144)"` with repository-local author and committer `8036360+jmservera@users.noreply.github.com` and the Copilot trailer.

## P3 and P4 checks

* `git diff --numstat HEAD MERGE -- docs/reference/log.md` shows zero deletions; `git diff origin/main MERGE -- docs/reference/log.md` shows zero deletions.
* `git diff HEAD MERGE --name-status -- .copilot-tracking` shows no M or D.
* `git diff 63d7f8c1 MERGE -- src/agents` and `git diff HEAD MERGE -- src/agents` are empty.
* `git diff origin/main MERGE --name-only -- src infra tools .github/workflows` lists only the queue adapter and its tests, `infra/README.md` and no dependency manifest.

## P5 checks (venv /tmp/c1venv, Python 3.12.3, ruff 0.17.1, mypy 2.4.0)

Logs are written to `/tmp/rpi144-cm/<id>.log`, one file per producer, never overwritten, with exit captured as `rc=$?` immediately after each command.

* A1 `src/agents`: `PYTHONPATH=$PWD/tests:$PWD/../core/tests python -m unittest -v test_queue_azure test_worker test_dispatch test_dependency_rule` (expected 49 tests, 0 skips).
* A2 Date positive: `python -m unittest -v test_queue_azure.RequestDateTests` (module path printed).
* A3 Date negative: copy `src/agents/src` to `/tmp/rpi144-cm/mut`, delete the `x-ms-date` header line, run the positive class with that copy first on `PYTHONPATH`; it must fail (exit non-zero) and the printed module path must be the copy.
* A4 `ruff check`, A5 `ruff format --check`, A6 `mypy` on `src/agents`.
* C1 `src/core`: `python -m unittest -v test_live_readings test_device_provision test_sensor_analysis_store test_sensor_consumer_live test_paired_equity`; skips are reported, not hidden.
* No SQL, browser, cloud, model, credential or private `ZF_DATA` use. The first failure keeps its full trace.

## P6 checks

`git diff --check origin/main..MERGE` restricted to authored paths; inherited findings counted separately and untouched.
