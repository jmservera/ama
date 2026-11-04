# Details: resident demo 503 retry (#1054, slice 2)

* Phase 1: `api()` returns `retryAfter` from the header; `loadView(announce, retried)` retries once while the session transition is unchanged.
* Phase 2: behavioural test: 503 shows waiting status, one 3000 ms timer, one extra `/demo/view` fetch, then error text keeps "Try again in a few seconds"; 3 fetches total.
