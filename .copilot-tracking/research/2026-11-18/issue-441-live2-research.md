# Issue 441 live2 research (2026-11-18)

Note: slug live2 because the prior run's issue-441-live artifacts and state are tracked; they are preserved unchanged (my first write overwrote them in the working tree, restored with git checkout before any commit; the witness research-open event seq 2 was logged against that overwritten state).

Disposition: executed. Scope: audit docs integration of resident portal BRD, PRD and proposed ADR against the nine #441 criteria; docs-only, demo desktop, tier FOCUSED, no src change.

## Evidence

* `python3 tools/test_resident_portal_docs.py`: Ran 2 tests, OK.
* Identifier counts present in BRD and PRD for FR-053, FR-062, AC-104, AC-111, AC-126, OD-52..55; AC-140 PRD only.
* `git ls-files docs/adrs`: 0001-0007 only; PRD line 1358: proposal `id: null`, registration UNMET.
* BRD FR-044/AC-084 line 1602; OD-53 line 2171 OPEN; owner direction 2026-11-02: demo display does not satisfy FR-044/AC-084.
* 60,000 treated as homes (BRD 709, PRD 1074, 1598).
* No Azure, browser or credential action: all criteria are document content or human decisions.

Planning readiness: Ready. Result table: docs/reference/research/resident-portal-441-live-status-2026-11-18.md.
