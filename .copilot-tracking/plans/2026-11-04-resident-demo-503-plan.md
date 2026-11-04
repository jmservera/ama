# Plan: resident demo 503 retry guidance (#1054)

* Slice 1 (this PR): bulkhead 503 sends `Retry-After: 3` and plain wording "Try again in a few seconds"; test asserts both.
* Slice 2 (later, web): show the retry hint and an automatic single retry in demo.js once the web redesign lands.
* Slice 3 (later, evidence): re-measure the authenticated burst to decide whether 8 is right.
* Critique: one pass, compatible; bulkhead kept; other 503s unchanged; no security, SQL, infra or deployment change, so focused tier.
