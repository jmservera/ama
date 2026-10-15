# Changes: M3 synthetic tools and data governance (refs #199)

Plan: [plan](../plans/2026-10-15-issue-199-m3-synthetic-plan.md).

## Summary

One pull request. 14 matrix rows moved with `git mv` (4 modules, 3 fixture files, 7 tests); no shim or copy in `mvp/`. Remaining `mvp/` code imports `zava_forward.core.synthetic`; `chat_fixture` is reached through `PYTHONPATH` until M5. Check names kept. No dependency change, so the hashed requirements were not regenerated and no pin was loosened (pip only). No SQL changed; `sensor_backfill` already used `INSERT ... WHERE NOT EXISTS`.

## Divergences

* `core/synthetic.output_dir`: generated data defaults to the per-user `ZF_DATA` folder (ADR 0006), a file path means its folder. Not under `src/`.
* `chat_fixture` has a local `ROLE_NAMES` because `auth` is M5; `mvp/tests/test_chat_fixture_roles.py` guards equality.
* `build_mvp_dataset.py` still defaults to `mvp/data/` (repoint is #200); the real private data copy is an owner action and was not read.
* Temporary ruff and mypy exemptions for moved files (core, agents, importer), ending in M6.

## Validation (local)

| Command | Result |
| --- | --- |
| Baseline on `main`: `cd mvp && PYTHONPATH=.:../src/core/tests python3 -m unittest discover -s tests` | Ran 551, OK (skipped=92) |
| Baseline `src` projects | core 167, api 8, agents 8, orchestrator 4, importer 4; total 742 |
| After: `cd mvp && PYTHONPATH=.:../src/core/tests:../src/agents/tests python3 -m unittest discover -s tests` | Ran 505, OK (skipped=92) |
| After: each `src/<project>`: `PYTHONPATH=tests python3 -m unittest discover -s tests` | core 196, agents 25, importer 9, api 8, orchestrator 4, all OK |
| Total after | 747, at least the 742 baseline (+5: 3 output_dir, 1 role guard, 1 registry check) |
| `ruff check .`, `ruff format --check .`, `mypy` in all five `src` projects | clean |
| `python3 -m unittest discover -s infra/tests` | Ran 75, OK |
| `python3 -m compileall -q mvp/zavaforward_mvp src/core/src` | OK |
| `pip wheel --no-deps src/core` | wheel contains `synthetic` |
| CLI smoke: `scale_fixture --help`, `sensor_backfill --estimate-only`, `chat_fixture --help` | OK |
| `python3 tools/rename-zava-tests.py` | 7 errors from missing `pptx`/`PIL` locally, same as M2, unrelated |
| Docker image build, SQL Server (`mssql` job) | Not run: docker socket permission denied, no local SQL Server; relying on CI |
