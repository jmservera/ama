<!-- markdownlint-disable-file -->
# Plan: issue 947

Details: [../../details/2026-11-04/issue-947-followup-details.md](../../details/2026-11-04/issue-947-followup-details.md)
Research: [../../research/2026-11-04/issue-947-followup-research.md](../../research/2026-11-04/issue-947-followup-research.md)

* [x] Phase 1: normalise non-object year digests in `ledger.read_year_digests`; guard `digest_blob.publish`.
* [x] Phase 2: regression tests in core and orchestrator.
* [x] Phase 3: focused tests, ruff, mypy; log entry.

## Critique (single pass)

* Verdict: proceed. A corrupt digest still makes verification fail (`intact` false, listed in `bad_digests`); nothing is silently dropped, so no integrity control is weakened. `read_digests` is out of scope.
