<!-- markdownlint-disable-file -->
# Details: issue 1204 port coordinator contract to main

## Phase 1

* Files: `.github/agents/ama-backlog-delivery-coordinator.agent.md`.
* Command: `git merge-file <agent> <325ef2ba4^ version> <325ef2ba4 version>`; exit 0 means no conflicts.
* Success: main's #1511/#1821/#1843 text retained; #1813 liveness, live-refresh and handoff rules present.

## Phase 2

* `python3 tools/check-coordinator-handoff.py` passes.
* `python3 -m unittest tools.test_check_coordinator_handoff` passes (11 tests).

## Phase 3

* `git diff --check`, review of removed lines (reworded, not dropped), Conventional Commit `fix(delivery): ...` with trailers.
