<!-- markdownlint-disable-file -->
# Research: issue 572 r2 re-verification

Disposition: reused (prior evidence in merged PRs #575, #595, #600, #606, #757, #627, #719, #731, #756, #789, #827, #925). Planning Readiness: Ready.

* AC1-AC3 are delivered. `git diff 61a4ac543 HEAD` shows no change to `tools/rpi-checks.py`, `tools/test_rpi_checks.py` or `src/api/tests/test_chat_panel.py` since round 1.
* AC4 (fresh complete exact-head gate with browser and MSSQL groups) needs Docker, MSSQL and Chromium and is owned by the coordinator. It cannot be proven in a PR and a receipt is not reusable across a source, base or tool change.
* Smallest slice: evidence-only re-verification at main a7effea1d. No security, infrastructure, SQL or deployment change.
