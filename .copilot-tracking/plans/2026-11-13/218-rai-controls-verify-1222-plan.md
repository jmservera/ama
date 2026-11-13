# Plan: 218 RAI controls unit verification

* Phase 1: create venv /tmp/venv-218-1222 (system-site-packages), upgrade setuptools and wheel, editable install src/core, src/agents, src/api with --no-deps --no-build-isolation; verify __path__ inside worktree.
* Phase 2: per package, run the located modules with `env -u ZF_DATA -u ZF_TEST_MSSQL`, cwd per package, PYTHONPATH limited to sibling tests dirs (never mvp); capture log, `$?` to file, sha256, counts, skips.
* Phase 3: write changes.md with counts, skips, hashes, exit codes and AC boundaries; remove venv; independent code-review; commit tracking files only.

Details: see details file. Stop on any install or path-verification failure and record blocker.
