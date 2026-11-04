# Research: resident demo 503 shedding (#1054)

* Prior PRs: #1064 (docs, measured the burst), #1062 closed. No merged code change for #1054.
* Cause: `_route` in `resident_demo/app.py` takes a non-blocking slot from a 8-slot BoundedSemaphore and answers 503 with `UNAVAILABLE`, no `Retry-After`.
* Client (`web/demo.js` line 396) already shows `body.error`, so new wording reaches the panel without web edits (web is out of scope for this slice).
* Decision on 8: keep. The server is a stdlib threading server on one replica; a bound protects the SQL reader. Raising it needs load evidence, so it stays open.
* Planning readiness: Ready. Evidence: docs/reference/research/ux/zava-forward-prototype-profile-review.md line 1147.
