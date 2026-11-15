# Research: 153-btns-rebase-main-2013

Issue #153 (in progress). Target: rebase `fix/demo-153-app-js-notices-1836` onto merged `origin/main` `2489d839e9` (#1542, squash of #1530).

* Branch before: `9fff29a3c`, `91bc7f3e4`, `4b88545e3` on pre-squash `b1d4bc59d` (#1530).
* Requested base `91bc7f3e4~1` is `4b88545e3`, the first #153 commit. It creates `test_app_js_notices_content.py` and the `ownedNotice` helper, which main lacks. Using it as base drops that commit and conflicts (app.js, DU on the test file). Probe: rebase aborted, no state lost.
* Decision: rebase `--onto 2489d839e9 b1d4bc59d`, so all three #153 commits move. Divergence from the instruction, recorded here.
* Planning Readiness: Ready. Research disposition: executed.
