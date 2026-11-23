# Issue 2257 r6 review

Executed once after implementation. Outcome: conformant, one routed follow-up.

* Diff matches the plan: one `app.js` flag, one condition, one extended test (red without the fix, 73 targeted tests green, ruff clean).
* Auto redraw stays bounded (one attempt, reset on success or click). JSON application errors are not retried.
* No styling or markup change, so no web-design source fetch finding applies.
* Routed follow-up: deploy and observe a real failure to confirm the cause and the gateway redraw live.
