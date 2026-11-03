<!-- markdownlint-disable-file -->
# Plan critique: issue-98-r1-manifest-freshness

* Critique execution: Complete (single pass). Verdict: Proceed.
* PC-001: do not mutate snapshots or invent a stale status in stored data. Disposition: applied; freshness is computed at view time.
* PC-002: do not claim AC-051 or tick criteria. Disposition: applied; README and PR say partial.
* PC-003: avoid a second saved-state field that could drift. Disposition: applied; no persisted state added.
