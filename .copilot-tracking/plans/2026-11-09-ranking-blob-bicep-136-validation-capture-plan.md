# Plan: validation-only capture for the frozen #136 candidate (Refs #136, #1258)

Details: `.copilot-tracking/details/2026-11-09-ranking-blob-bicep-136-validation-capture-details.md`. Research: `.copilot-tracking/research/2026-11-09-ranking-blob-bicep-136-validation-capture-research.md`. Prospective: this plan and its critique are committed BEFORE any check runs.

## Scope

* Re-run the selected DEMO-tier checks on the unchanged frozen source and capture command, environment, tool and source identities, all stdout and stderr, and each producer exit into the external directory `coordinatorfiles/logs-136-validation-capture/run-rhvN6X/` (session files directory, created by `mktemp -d`). Logs stay after validation; nothing is auto-removed; no generic `/tmp` path.
* No edit to production, test or Bicep source. No main, #1292 or sibling import. No productive correction; the child count stays 1 of 5.

## Phases

1. Commit these prospective records (research, plan, details, critique, state).
2. Capture identities: git HEAD, tree, status, `git diff 95fcaf561 HEAD --stat` must list only `.copilot-tracking`, the source paths byte-identical to `95fcaf561` and `3de2c2f4c`, tool versions.
3. Run checks, one log file per command, exit recorded in a `exits.tsv` and in each log footer.
4. Hash all logs (sha256) and verify the worktree source is still byte-identical.
5. Commit only dated command, result and identity records, plus the review and state. Raw logs stay external.
6. One Review, then the handoff.

## Checks (cwd noted)

* `infra/`: `az bicep build --file main.bicep`; `az bicep lint --file main.bicep`; `az bicep build-params --file` for `main.test`, `main`, `main.pilot.example` and `iot-hub-live` (`.bicepparam`), each separately.
* `infra/`: `python3 -m unittest tests.test_bicep_policy tests.test_identity_rbac tests.test_secret_lifecycle tests.test_api_ingress_transport tests.test_governance` (expect 100 tests).
* `src/core`: `PYTHONPATH=src python3 -m unittest discover -s tests -p test_ranking_archive_blob.py` (expect 25) and `-p test_ranking_publication_runner.py` (expect 45), after printing the imported `zava_forward.core` path.
* `src/api`: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_ranking_publication_wiring -q` (expect 35) in an owned venv with editable installs of this worktree, after printing the imported Core and API paths. The ambient run is performed first only as a path probe; if it resolves to the primary checkout it is recorded as INVALID and not counted.
* Root: the exact CI ruff commands for the changed infra test file (`check` and `format --check`, `--isolated`, line length 100, py312), plus the CI three-file form. Also plain repo-config `ruff check` and `ruff format --check` on that file as the qualified baseline: RUF100 expected on the untouched `# noqa: S307`; recorded as nonselected baseline, not suppressed.

## Stop rules

A failing selected check stops publication; the actual output is reported. A source change, an import of other lineage, or an invalid-path result counted as a pass is forbidden.
