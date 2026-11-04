# Review: resident demo 503 retry (#1054, slice 2)

* Execution: one review. Outcome: conformant for the slice.
* Checks: retry bounded to one; stale-session guard via `transition`; 503 with no header falls back to 3 s; manual retry button and plain wording preserved; no resident data or consent changes.
* Residual: sign-in flow load (post-login `loadView`) shares the same path, so it also retries once; not separately tested.
* Unmet acceptance: decision on whether 8 is right (needs live re-measured burst); live verification on `ca-resident-demo`.
