# Issue 200 workflow rename plan (2026-11-01)

* [ ] Rename `name:` to `Source CI` (mvp-ci.yml) and `Source validation` (mvp-validation.yml); job IDs and file names unchanged.
* [ ] Update WORKFLOW_HASHES in tools/rpi-checks.py and the infra/README.md note.
* [ ] Validate: infra/tests, tools/test_rpi_checks.py, rename-zava-tests, actionlint if present, ruff on touched python.
* Critique: one pass, compatible with owner decision (rename after cut-over, one PR). Verdict: proceed; no conflicting advice.
