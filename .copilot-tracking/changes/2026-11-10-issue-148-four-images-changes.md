<!-- markdownlint-disable-file -->
# Changes: issue 148 four-workload image wiring

Readback 2026-11-10T01:45Z. Plan `.copilot-tracking/plans/2026-11-10-issue-148-four-images-plan.md`. Base `26bf987ca`; prospective records commit `c9fa753f3`.

## Source (two owned files)

* `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py`: `WorkloadImage`/`WORKLOAD_IMAGES` (api `zava-forward-mvp`/`apiImage`, agents `zava-forward-agents`/`agentImage`, orchestrator `zava-forward-orchestrator`/`--orchestrator-image`, importer `zava-forward-importer`/`importImage`); four builds from `src/<project>/Dockerfile` with context `<repo-root>/src` and the approved pool, first failure stops with the project name and chained original error; shared `_require_images` for `images` verification and before the application deploy (resume guard); application deploy passes the three parameters plus explicit `--orchestrator-image`; `agentImage`/`importImage`/`orchestratorImage` reserved from overrides; static `images` listing in the dry-run plan.
* `src/orchestrator/tests/test_rebuild_azure.py`: repository-aware fake `acr build`/`show-tags` with build-failure and unpublished modes; nine new test methods (build contexts, tag-to-input mapping, build failure, unpublished image, API-only resume, all-four resume, reserved overrides, dry-run listing without I/O); `test_image_build_uses_the_approved_pool` now checks all four builds.

## Evidence (venv `~/.venvs/issue148-four-1110`, pip, editable core + orchestrator[dev])

* Baseline before edits: `test_rebuild*.py` 54 tests OK.
* New tests on UNCHANGED source: `tests.test_rebuild_azure` ran 39, failures=10, errors=1 (nine methods, one with three subtests; 10 failures + 1 dry-run KeyError).
* After change, from `src/orchestrator`: `PYTHONPATH=../core/tests python -m unittest discover -s tests -q` ran 112, OK, no skips. Without the core test path three modules (`test_digest_blob`, `test_document_rescan_job`, `test_source_monitor`) fail to import `dataset`/fixtures: an environment path issue, unrelated to this change.
* `ruff check .` pass; `ruff format --check .` 13 files formatted; `mypy` no issues in 16 source files. An initial E501 on a new comment was fixed.
* Not run: full gate, real builds, Azure, SQL/browser. Fake runners prove wiring only; criterion 4 stays unmet.

## Divergences

None from the plan; critique findings 1 and 4 applied (message wording, discovery guard).
