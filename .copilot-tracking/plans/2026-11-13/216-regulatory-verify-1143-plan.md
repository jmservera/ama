# Plan: #216 regulatory offline verification (1143)

* [ ] Phase 1: create /tmp/venv-216-1143 (system-site-packages), upgrade setuptools and wheel, editable install src/core, src/agents, src/api with --no-deps --no-build-isolation; verify __path__ inside worktree.
* [ ] Phase 2: run the 18 modules listed in the details file per package with `env -u ZF_DATA -u ZF_TEST_MSSQL`, log to /tmp, save true exit codes, sha256 logs.
* [ ] Phase 3: record counts, skips, sha256, literal AC boundaries for #215 and #216 (read from gh issue view, read-only) in the changes file; remove the venv.
* [ ] Phase 4: independent code-review, review file, clean commit, commit-complete witness.

No edits to src/ or docs/. No network, Docker, browser, push.
