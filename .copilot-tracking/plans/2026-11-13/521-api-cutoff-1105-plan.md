# Plan: #521 API cutoff local test proof

1. Create `/tmp/venv-521api-1105` with `--system-site-packages`; `pip install --no-deps -e src/core src/agents src/api` (upgrade setuptools/wheel only if needed).
2. Verify `zava_forward.api.resident_demo.app.__file__` and `zava_forward.core.resident_showcase.__file__` are inside the worktree `src/`.
3. From `src/api` run `env -u ZF_DATA -u ZF_TEST_MSSQL PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest -v test_resident_demo_check test_resident_demo_api`, saving the producer exit code to a file.
4. Record origins, counts, skips, exit codes and hashes in the changes file; delete the venv.
5. Independent review, commit `Refs #521`, record witness.

Critique amendments: use `--no-build-isolation --no-index`; `PYTHONDONTWRITEBYTECODE=1`; check `git status --ignored` and remove egg-info; retain compact `-v` log summary; claim limited to what the tests assert.

No edits to `src/`, `infra/`, `docs/`. No network beyond pip no-deps local editable (build isolation off if offline). Validation tier: Focused.
