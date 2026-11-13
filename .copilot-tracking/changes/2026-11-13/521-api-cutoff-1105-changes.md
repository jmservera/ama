# Changes: #521 API cutoff test proof

Status: complete. Tracking-only; no `src/`, `infra/` or `docs/` edits. Base `3b05143179f83235c5b4e80e70aad99bdc44d83f`. Tier: Focused.

## Evidence

* Venv `/tmp/venv-521api-1105` (`--system-site-packages`), removed after the run. Editable `--no-deps --no-index --no-build-isolation` installs of `src/core`, `src/agents`, `src/api`.
* Deviation: `wheel` was missing (`invalid command 'bdist_wheel'`, first pip rc=1); a public `wheel` 0.48.0 wheel was downloaded and installed, then installs succeeded (rc=0).
* Module origins (inside this worktree):
  * `zava_forward.api.resident_demo.app` -> `<worktree>/src/api/src/zava_forward/api/resident_demo/app.py`
  * `zava_forward.core.resident_showcase` -> `<worktree>/src/core/src/zava_forward/core/resident_showcase.py`
  * `zava_forward.agents.__path__` lists the worktree `src/agents` first, then `/home/azureuser/source/ama/src/agents` (namespace package; these tests do not import agents modules from it).
* Command (from `src/api`): `env -u ZF_DATA -u ZF_TEST_MSSQL PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest -v test_resident_demo_check test_resident_demo_api`
* True producer exit code: 0. Ran 53 tests, OK, 0 failures/errors, no skips reported. Log sha256 `06a1be704e370d54ca1ef00f9bd3b118e5ea8f6ebef2a1990f9b2759bcb3b9f4` (log not retained).
* Boundary tests passed: `ResidentDemoCheckTests.test_sql_fixture_window_ends_at_the_shared_authority_end`, `SessionTests.test_extended_authority_allows_january_and_stops_at_exact_february_boundary`.

## Proof limits

* Asserted: fixture window end is 2028-01-01 and not 2027-02-01 or 2026-11-01; 2027-01-31T23:59:59Z allowed; exact `AUTHORITY_END` rejected (503, token invalid).
* Not asserted in these modules: 2027-12-31T23:59:59Z accepted, explicit +1s/+1ms cases. The API test name still says "february". Not fixed (out of scope).
* Loopback sockets used by tests; no cloud, Docker, MSSQL or browser. `git status --ignored` showed no stray files.
