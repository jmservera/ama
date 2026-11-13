# Plan: verify ranking/queue/gate/handoff/decision suites (Refs #79 #76 #82 #83 #86)

* Phase 1: create /tmp/venv-79-1143 (system-site-packages), upgrade setuptools wheel, editable install core, agents, api (--no-deps --no-build-isolation); verify __path__ in worktree.
* Phase 2: run listed core modules from src/core and API modules from src/api with env -u ZF_DATA -u ZF_TEST_MSSQL, unittest -v per module, log to /tmp, capture true exit codes.
* Phase 3: record counts, skips, sha256, exit codes in changes file; remove venv and logs. No src/docs edits.
