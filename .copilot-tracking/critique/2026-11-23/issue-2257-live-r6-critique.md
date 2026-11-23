# Issue 2257 r6 critique

Executed once. Verdict: proceed.

* Risk: auto-retrying a persistent 5xx loops. Mitigation: the existing `MAP_AUTO_RETRY_DELAYS` allows one redraw; the counter resets only on success or a manual click. Accepted.
* Risk: retrying a JSON application error hides a real fault. Mitigation: the flag is set only when `startupFailure(res)` is true, which requires a non-JSON body. Accepted.
* Risk: the existing unit test slices the failure branch by text; the edit must stay inside it. Accepted; the test is extended, not replaced.
* Disposition: applied directly, no user decision needed.
