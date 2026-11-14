# Review: #144 worker SIGTERM drain

* Execution: single pass. Outcome: conformant for the slice; no open material findings.
* A legitimate provider timeout coinciding with shutdown is also redelivered; harmless, bounded by fence and retry.
* Follow-ups: wire `DRAIN_SECONDS` to deployment grace period in infra after PR #1583 merges; subprocess SIGTERM test of the enabled path.
