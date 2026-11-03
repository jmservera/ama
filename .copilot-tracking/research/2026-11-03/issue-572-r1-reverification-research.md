<!-- markdownlint-disable-file -->
# Research: issue 572 r1 re-verification on main 61a4ac543

Research disposition: executed (delta only; earlier research reused). Planning Readiness: Ready.

## Already delivered by merged PRs (Refs #572)

* #575 requires chat-panel Chromium execution in the local gate.
* #595 recognises exact Chromium discovery skips; #606 repairs the skip baseline.
* #600 stabilises the browser test; #757 types the core chat test.
* #627, #719, #731, #756, #789, #827 record evidence and gate reruns.

## Current state on main

* `tools/rpi-checks.py` dispatches `CHAT_PANEL_BROWSER_SELECTOR` with `ZF_BROWSER_TESTS=1` in the browser group and keeps the exact skip pair rule in `check_skips`.
* `tools/test_rpi_checks.py` holds the regression tests for dispatch, exact skips and fail-closed handling.
* Issue #572 is open; the only unchecked criterion is AC4.

## Gap

AC4 (fresh complete exact-head gate with browser and MSSQL groups) needs Docker, MSSQL and Chromium and is run by the coordinator, not here. No code change is justified: the remaining unmet criterion is not a code defect.

## Chosen slice

Re-verify AC1-AC3 against current main with focused checks and record the evidence. No source change.
