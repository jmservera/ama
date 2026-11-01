<!-- markdownlint-disable-file -->
# Research: issue 440 third stabilization checkpoint (2026-11-01)

Research disposition: executed. Planning Readiness: Ready.

## Question

After 40 merged commits since the second checkpoint (main 36a1d0da), what is the current-main state of the feedback-first journey and package boundaries, and which #440 criteria remain unmet?

## Evidence

* Pin: freshly fetched `origin/main` b18f7f98e4c890b99187bda9eebd2c7b810e3b91 (tree e78c8e9885cf8e17b1d80af943351f16e7b07263). 40 commits since 36a1d0da (feature wave: role-screens web, core queues, regulatory/RAI gates, infra and scale harness).
* Documents at this pin: BRD 0.21.0 draft (blob 34d88395), PRD 0.21.0 in-review (blob c788b917); ADR 0001-0006 unchanged from the second checkpoint; coordinator blob 0c66ef19.
* Criteria 1-6 are met by merged text (PR #461) plus checkpoints 1 and 2 (PR #688).
* Criterion 7: #687 was filed for PERF-440. PR #689 (merged) added attribution diagnostics to `test_sqlreads.py`; PR #720 (reproduction under IO contention) is open and unmerged. #687 stays open; this is not claimed as resolved.
* Criterion 8: native `/agent` discovery is coordinator-attested only (owner-approved one-time check, 2026-10-24); the seven HVE scenarios are simulated; the original independent Review of PR #461 was Partial. No coordinator edit is made here, so no new Major HVE change arises.
* A foreign complete gate (`rpi-checks.py --all`, issue 233, /tmp/rpi-233-r3) holds the heavy lock; it is not interrupted, read or duplicated.

## Constraints

Focused tier, documentation and evidence only, no source change, no Azure, no private data, no threshold waiver.

## Conclusion

Run the five package suites plus ruff/format/mypy on the pinned head, record results in the evidence pack, re-triage against open issues, and use `Refs #440` naming criteria 7 and 8 as unmet.
