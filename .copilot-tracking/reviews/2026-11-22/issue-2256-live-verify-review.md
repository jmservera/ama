# Review: issue 2256 live verification

Execution: once. Outcome: conformant for verify-only scope.

* Claims match probe output; Unknown due and wait are reported as limits, not proven.
* No src change; no secrets in artifacts (probe script reads credentials at runtime only).
* Routed follow-up: seed demo offers with a timezone-aware offered_at and due_at so the screen shows real waiting and due times (later work).
