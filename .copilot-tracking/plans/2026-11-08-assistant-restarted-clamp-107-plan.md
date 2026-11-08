# Plan: issue 107 restarted-process allowance clamp test

Date: 2026-11-08. Prospective; committed with its critique before any code.

## Scope

One new method in the `ProcessRaces` mixin of `src/api/tests/test_assistant_release.py`. No helper change expected, no production, runner, store, rubric, schema or doc change.

## Method: `test_restarted_processes_keep_partially_used_allowance_and_stop_at_stored_calls`

1. Create three pending proposals from distinct capabilities (`list(assistants.REGISTRY)[:3]`): `first`, `second`, `third`.
2. Wave `one`: one worker, `call_allowance=2`, tasks `[first]`. Assert results `[[True]]`, one provider call, task `first` ready.
3. Read the pool row and attempts with `self.pool`; assert `calls=2`, `tokens=2000000`, `used_calls=1`, attempts 1. Keep the row as `stored`.
4. Wave `two`: fresh worker with larger configuration (`call_allowance=1000`, `token_allowance=9000000`, `expires=2100-01-01T00:00:00Z`), tasks `[second]`, run to completion. Assert `[[True]]`.
5. Wave `three`: another fresh worker with the same larger configuration, tasks `[third]`. Assert `[[False]]`.
6. Assert exactly two provider calls, `second` ready, `third` disabled with "allowance exhausted" and attempts 0. Assert the pool row equals `stored` except `used_calls` 2 and the attempts count 2, so calls, tokens and expiry are the original stored values, not the larger ones.
7. Distinct pids come from `finish`; waves run one at a time, so no scheduling guess and no sleep.

## Checks (LIGHT, no services)

* From `src/api`, in a fresh external venv under `/home/azureuser/.local/share/ama/gates/g107-clamp-light-r1`, with `pip install -e` for core, agents and api[dev]: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_assistant_release -v` and `test_assistants`.
* Distribution origin check for `zava_forward` modules (must resolve inside this worktree).
* `ruff check`, `ruff format --check` on the touched test (the file is excluded from format; compare block with stdin format as before), and `mypy` for the api project if configured.
* A mutation check: temporarily make the clamp ignore stored calls is NOT done in the tree. Instead record that the new test would fail if the stored limits were replaced by restart limits (reasoned from `disabled()`), and run the test once against a throwaway copy only if cheap.
* MSSQL class tests will skip without `ZF_TEST_MSSQL=1`; disclosed as unverified.

## Future gate

Later FULL on exact current main with `python3 tools/rpi-checks.py --all --base <current-origin-main> --out <new external dir> --jobs 2 --lock-timeout 0 < /dev/null`. The mssql log must show the new method as `ok` under `MssqlUnleasedRevocation`. Not run here.

## Commits

Identity from `gh api user`, repository-local noreply, Conventional Commit, Copilot trailer, `Refs #107` and `Refs #104`. No push or PR.
