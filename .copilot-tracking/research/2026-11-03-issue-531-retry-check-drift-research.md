---
title: Issue 531 retry-count drift research
ms.date: 2026-11-03
---

* Research disposition: executed (read-only review of the issue, merged PRs and current main 2c2eb4615, plus fresh validation runs).
* Planning Readiness: Ready.
* Evidence: criteria 1 to 6 of #531 are delivered by merged PRs #538, #581, #604, #628, #685, #725 and re-verified in PR #758. Criterion 7 (live verification on the employee site) is owner-run and stays unmet; no agent session can sign in interactively.
* New finding: after the 2026-11-02 re-verification, `app.js` changed script retries from two (250 and 500 ms) to three (`SCRIPT_RETRY_DELAYS` 250, 500, 1500 ms) and added cold-start read retries (`fetchReadRetrying`). The unit tests still pass (86 tests OK), but `checks/loading_briefing_browser_check.py` still asserted the old budget and failed on current main:
  * `companion_failure_check` expected 3 requests for a blocked `/panels.js`; the page now makes 4 (one load plus three retries).
  * `helper_bootstrap_check` treated `failures == 3` as terminal and expected 3 requests; with three retries the third retry now succeeds, so terminal is `failures == 4`.
* `src/api/README.md` (Workspace script recovery, #524) still described the two-attempt budget.
* Environment note: pip-installed zava-forward distributions are absent here, so validation used explicit `PYTHONPATH` to this worktree.
* Scope decision: smallest coherent slice is to align the browser check and the README with the current retry behaviour. No UI or behaviour change, so web design skills are not applied.
