<!-- markdownlint-disable-file -->
# Research: issue 572 chat-panel Chromium test in the local gate

Date: 2026-11-01. Task slug: `issue-572-chat-panel-gate`. Disposition: executed. Planning Readiness: Ready.

## Findings (evidence from origin/main at cb57c1b7)

* AC1 delivered: `tools/rpi-checks.py` defines `CHAT_PANEL_BROWSER_SELECTOR` and runs it in the `browser` group with `ZF_BROWSER_TESTS=1`, `suite=True`, `integration=True` (both the command inventory near line 735 and the executor near line 1685). Merged via #575, #595, #600, #606.
* AC2 delivered: `EXPECTED_SKIP_REASONS` still contains the broad reason, but `check_skips` accepts it only for the exact `CHAT_PANEL_DISCOVERY_SKIP` test/reason pair in group `project-api`; integration groups reject any skip not in `SQL_NOT_APPLICABLE`.
* AC3 delivered: `tools/test_rpi_checks.py` has regressions for inventory, required-stage execution and unexpected-skip rejection (55 tests).
* AC4 unmet: no fresh complete exact-head local gate receipt exists (closure audit comment on #572, 2026-10-31). The task scope excludes the heavy local gate; CI is the evidence.

## Validation of current state

* `python3 -m unittest tools.test_rpi_checks`: 55 tests OK.
* Pinned-profile ruff 0.17.1 (`--isolated --select E,F,I,B,UP --line-length 100`) check and format: pass. mypy `--strict`: pass.
* Real run of the exact chat-panel case with `ZF_BROWSER_TESTS=1`: 1 test, OK, 0 skips.

## Conclusion

No source change is needed. The slice is evidence only: record validation and open a PR with `Refs #572` naming AC4.
