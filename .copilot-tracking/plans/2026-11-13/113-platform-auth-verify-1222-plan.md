# Plan: 113-platform-auth-verify-1222

1. Create venv /tmp/venv-113-1222 (system site packages); upgrade setuptools, wheel; editable `--no-deps --no-build-isolation` install of src/core, src/agents, src/api.
2. Verify `zava_forward.core/agents/api` `__path__[0]` and a submodule `__file__` resolve under the worktree src/.
3. Run Core module list from `src/core/tests` with `env -u ZF_DATA -u ZF_TEST_MSSQL python -m unittest -v <modules>` (cwd src/core, PYTHONPATH not set to mvp); same for API from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`. Save logs under /tmp, exit code via `$?` to file.
4. Parse per-module counts and skips; sha256 logs; write changes.md; delete venv and logs.
5. Independent code-review, review.md, commit with trailer and Refs.

Success: all selected modules run; failures reported honestly, not fixed (no src/docs edits).

## Critique dispositions (rubber-duck: approve with changes)

* Run bare module names from each tests directory; API PYTHONPATH=../../core/tests:../../agents/tests. Accepted.
* Loopback sockets in API tests are local-only; accepted and recorded, no external network. Accepted.
* Unset ZF_BROWSER_TESTS, ZF_DOCUMENT_RESCAN_MSSQL, ZF_SENSOR112_MSSQL, ZF_CONTINUITY_MSSQL, isolate HOME, PYTHONDONTWRITEBYTECODE=1; check `git status --ignored`. Accepted.
* setuptools/wheel upgrade is mandated by the brief (package index only); failures reported. Partially accepted.
* Record Node prerequisite; distinguish skips from verified coverage. Accepted.
