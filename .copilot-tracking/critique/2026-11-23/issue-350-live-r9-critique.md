# Issue 350 r9 critique (one pass, final candidate)

Verdict: proceed. Candidate: re-raise lock-busy in the GET assistants branch, log other failures by class, one regression test, evidence note.

* Risk: re-raising changes the body for lock-busy from the assistant message to the busy message. Accepted: it is the already-approved wording for safe methods and adds Retry-After. Applied directly.
* Risk: logging must not leak messages. Candidate logs class and path only; the test asserts the secret is absent. Applied.
* POST branch left alone (not retry-safe). Applied.
* Forecast timeout and the edge 302 are out of scope (owned by #2304 and an owner infra decision). Recorded, not changed.
* Tier FULL because `src/` changes; the coordinator runs the gate; no `--all` here.
