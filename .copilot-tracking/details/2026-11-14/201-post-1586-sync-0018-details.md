<!-- markdownlint-disable-file -->
# Details: Issue #201 post-1586 sync

## Phase 1

* Per-project runs in `src/<project>` with editable installs; `PYTHONPATH=../core/tests:../agents/tests` for api, `../core/tests` for agents and orchestrator; `tests/test_scenario_manifest.py` from `src/core`; `python3 tools/rename-zava-tests.py`.

## Phase 2

* Insert "Post-1586 cut-over verification reconciliation (2026-11-14, Refs #201)" before the Post-wave heading.

## Phase 3

* Relative-link and anchor check, ASCII scan of added lines, `git diff --check`.

## Phase 4

* Review artifact, Conventional Commit with Copilot trailer, no push.
