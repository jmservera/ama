# Details: preserve confirmed active delivery in backlog sync (Refs #1207)

* Edit tools/backlog-sync.py and add tools/test_backlog_sync.py; append docs/reference/log.md. Do not touch the coordinator agent, schedules, other worktrees, the board or the network.
* Success: tests cover each acceptance item with mocked `gh`/`gh_json`; no `gh` call in tests; the invalid CLI input exits non-zero before any gh call.
* Validation: `python3 -m unittest discover -s tools -p test_backlog_sync.py`, CLI argument check, ruff (CI options) and mypy on the test and tool. No gate or heavy suites.
