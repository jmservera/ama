# Details

* Core run: from src/core, `env -u ZF_DATA -u ZF_TEST_MSSQL /tmp/venv-89-1222/bin/python -m unittest -v tests.test_X ...` with PYTHONPATH unset except sibling test helpers only if the documented command requires it (api: PYTHONPATH=../core/tests:../agents/tests).
* API run: from src/api, same env, discover per module.
* Per module: Ran N, skipped N (with reasons), failures. Exit code saved via `$?` to file; log sha256 via sha256sum.
* No edits to src/ or docs/. Skips never counted as passes.

## Critique dispositions (rubber-duck, verdict Revise, applied directly)

* Coverage: grep of test bodies for provider capacity, appointment, work order and remedy terms maps to the listed procurement, resident, intake, job pack, technical quality and aftercare modules; no module is named capacity other than the Chromium one (excluded). Recorded as coverage basis in changes.
* Isolation: run with HOME=/tmp/zf-home-89, PYTHONDONTWRITEBYTECODE=1, ZF_DATA and ZF_TEST_MSSQL unset, proxies pointed at an unreachable address; pip install uses --no-deps --no-build-isolation (no network index use).
* Writes: editable installs create only ignored egg-info under src; verify with git status and remove untracked egg-info. Logs in /tmp, sha256 recorded, logs and venv removed before commit.
