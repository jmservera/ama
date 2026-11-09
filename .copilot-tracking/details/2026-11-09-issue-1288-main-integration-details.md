<!-- markdownlint-disable-file -->
# Details: #1288 ordinary main integration

Plan: [plan](../plans/2026-11-09-issue-1288-main-integration-plan.md).

## Phase 2 merge

`git merge --no-ff origin/main` with message "merge: bring main cd687abad into the #1288 recovery branch", Refs #1288 and the Copilot trailer, using the repo-local noreply identity. Projection is clean; the semantic check is Phase 3 plus the tests below. The merge must not alter any E1-E7 record; main's tracking files are additive and ranking-named.

## Phase 3 inventory commands

* `git diff --name-status 84b1a6d06 HEAD` after the merge, equal in content to main's delta since 5c3b8b4be.
* `git diff 84b1a6d06 HEAD -- src infra` must contain only main's paths (the candidate's own paths must be byte-identical to 84b1a6d06 except server.py and core/README.md, which must hold both sides' hunks).
* `git diff cd687abad HEAD -- src/api/pyproject.toml src/core/pyproject.toml` shows the candidate-only config, and `git diff 5c3b8b4be cd687abad -- <pyprojects>` is empty, which proves main did not change the profile inputs.

## Phase 4 profiles (pinned ruff 0.17.1, mypy 2.4.0)

* Core: owned `mktemp -d` venv with only `-e src/core[dev]`; from `src/core` run `ruff check .`, `ruff format --check .`, `mypy`.
* API: `.venv-1288` (core[sql,blob] and agents); from `src/api` run the same three. Confirm the blob SDK is importable so the Blob adapter is type-checked against the real SDK.

## Phase 5 targeted tests

From `src/core` with PYTHONPATH=tests: test_ranking_archive_blob, test_ranking_publication, test_ranking_publication_runner, test_ai_consumption*, test_ai_input_bounds, test_sensor_consumer*.
From `src/api` with PYTHONPATH=../core/tests:../agents/tests:tests: test_ranking_publication_wiring, test_quality_simulation_lane, test_ai_transport_deadline, test_role_endpoint_inventory, test_ai_call_site_inventory, test_ai_consumption_api, test_assistants, test_assistants_dispatch, test_assistant_release, test_quality_sensors_c7, test_quality_sensors_e2, test_ai_tasks.
Infra: main's `infra/tests/test_bicep_policy.py` only if it runs offline without Azure; otherwise recorded as not run with the reason.

## Evidence rules

Raw logs in session `files/logs-1288-main-integration/`. Skips are recorded per suite with the reason. Selected failures are not waivable.
