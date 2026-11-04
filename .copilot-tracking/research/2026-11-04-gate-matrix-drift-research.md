# Research: gate workflow matrix drift (2026-11-04)

* Disposition: executed. Planning Readiness: Ready.
* `python3 tools/rpi-checks.py --all` preflight compares `WORKFLOW_HASHES` with the digest of each workflow.
* Cause: the last #979 commit (run all projects for dependency manifests and when src-changes fails) changed `.github/workflows/src-ci.yml` after the hash pin, leaving `06ac403c...` stale; current digest is `99a20cf0...`.
* The `changes` job is already classified in `coverage_rows`; the new matrix fallback and `if:` conditions add no uncovered command.
* Test `test_matrix_drift_and_unreviewed_extra_commands_refuse` failed on the stale pin before the fix.
