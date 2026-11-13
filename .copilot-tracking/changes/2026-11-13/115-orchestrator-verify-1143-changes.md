# Changes: orchestrator verification (3b05143179)

Tracking-only. No `src/` or `docs/` edits.

## Result

* Command: `python -m unittest discover -s tests -v` from `src/orchestrator`, under `env -i PATH=/usr/bin:/bin HOME=/tmp/orch-home PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../core/tests` (ZF_DATA, ZF_TEST_MSSQL, ZF_DOC_* absent).
* True producer exit code (saved directly to file): 0.
* Ran 115 tests in 24.631s, `OK (skipped=1)`.
* Log: `/home/azureuser/.local/share/ama/phase-witness/rpi-115-orchestrator-20261113T1143Z/orch-1143-unittest.log`, sha256 `6202d3d48378877b3a1ea58ae0a623e09b73235f69f53641a95caa8099ae4a24`.
* Environment: venv `--system-site-packages`, pip upgrade of setuptools/wheel, editable `--no-deps --no-build-isolation` installs of core, agents, importer, orchestrator. Every `zava_forward.{core,agents,importer,orchestrator}` namespace path and every importable core/orchestrator submodule `__file__` resolved inside the worktree `src/` (checked under `env -i`; without it the inherited site adds a second core path to the main checkout, so the env isolation matters). `/tmp/venv-orch-1143` removed; no egg-info or `__pycache__` left in `src/`.

## Per-module counts

| Module | Tests |
| --- | --- |
| test_dependency_rule | 2 |
| test_digest_blob (#115 ledger digest) | 30 |
| test_document_rescan_job (#117) | 10 |
| test_rebuild (#148) | 23 |
| test_rebuild_azure (#148) | 39 |
| test_source_monitor | 5 |
| test_token_store | 4 |
| test_version | 2 |
| Total | 115 |

## Skips

* 1: `test_document_rescan_job.RescanCommand.test_selected_mssql_driver_error_is_sanitized_before_store_return`, reason "optional MSSQL driver absent". That coverage (MSSQL driver error sanitisation) is not exercised here.

## Limitations

* No dedicated worker task dispatch (#144) module exists under `src/orchestrator/tests`; no test names matched it, so #144 is not separately evidenced by this run.
* Network denial was not enforceable unprivileged; tests are offline by design, no Docker, MSSQL, cloud or model calls were made.
* Focused tier only: no complete local gate or hosted CI observation is claimed.
