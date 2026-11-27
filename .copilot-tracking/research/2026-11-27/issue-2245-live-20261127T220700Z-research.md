# Research: issue 2245 live (run 20261127T220700Z)

Disposition: reused (runs 125527Z and 174551Z) plus a new live read-only probe. Planning Readiness: Ready.

Findings

* Live API revision ca-cutover-test-demo-api--0000150 runs image tag demo-337d3999d5; the tag is a git short SHA and `git merge-base --is-ancestor c2213e0da4 337d3999d5` succeeds, so the audit-write retry (PR #2464) is deployed. Closes the image-to-commit gap left by run 174551Z.
* The server turns a SQL write-lock timeout on `POST /api/chat/threads` into a handled 503 with `Retry-After: 5` (server.py around line 838). The widget (`chat.js`) and case panel call `api()` in `app.js`, which does not retry that POST, so the person sees an error on the first send although the immediate retry returns 200. This is the remaining user-visible part of the 2026-11-22 symptom and is fixable in code.
* Not provable for the demo: the 2026-11-22 500 cause and the lock holder (Log Analytics and SQL inspection denied).

Chosen criterion: thread creation does not leave the person with an error after a handled lock-busy 503. Deliver: one bounded client retry with plain-language status, plus a node-vm test.
