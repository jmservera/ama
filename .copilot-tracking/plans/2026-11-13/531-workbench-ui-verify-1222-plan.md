# Plan: 531 workbench UI verification

* [x] Phase 1: create /tmp/venv-531-1222 (system-site-packages), upgrade setuptools/wheel, editable no-deps installs of src/core, src/agents, src/api; verify __path__ inside worktree.
* [x] Phase 2: run each selected module with `env -u ZF_DATA -u ZF_TEST_MSSQL`, log per module, save true exit code and sha256.
* [x] Phase 3: write changes.md, remove venv, independent review, commit (no src/docs edits).
