# Plan: 96-finance-grants-verify-1211

1. [ ] Create /tmp/venv-96-1211 (system-site-packages), upgrade setuptools and wheel, editable install core, agents, importer, api with --no-deps --no-build-isolation; verify __path__[0] under worktree src/.
2. [ ] Run Core and API module lists per module with `env -u ZF_DATA -u ZF_TEST_MSSQL python -m unittest -v`, capturing counts, skips, log sha256, true exit codes.
3. [ ] Write changes artifact with counts, skips, AC boundaries; remove venv.
4. [ ] Independent review, review artifact, commit.

Details: see details file. No src/ or docs/ edits.
