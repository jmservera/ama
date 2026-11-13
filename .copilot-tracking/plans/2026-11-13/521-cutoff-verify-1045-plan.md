# 521 cutoff verify plan

* [ ] P1 Plan critique by independent subagent before any venv/test (critique file).
* [ ] P2 Create /tmp/venv-521-1045, pip install -e src/core and src/api --no-deps; verify __file__ origins in worktree.
* [ ] P3 Run four unit suites, capture counts, skips, producer exit codes.
* [ ] P4 Write changes file with file:line consistency table and verdict; remove venv.
* [ ] P5 Independent code-review, review file, clean commit (Refs #521), commit-complete witness.

Tracking-only writes; no src/infra/docs edits.
