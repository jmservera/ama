# Issue 441 research: resident portal BRD/PRD/ADR integration state (2026-11-17)

Disposition: executed. Planning Readiness: Ready. Base origin/main eb51af5c. Tier FOCUSED, docs only.

## Measurement

* Issue 441 criteria 1-4 and 6-9 are ticked; the 2026-11-04 comment records 8/9 proven after PR 1566 (36a2a57335).
* Criterion 5 (requirements-owner disposition of FR-044/AC-084) stays unmet. Owner comments record: 2026-11-02 in-principle
  approval subject to named Legal/Compliance approval, per-message review normative; 2026-11-02 demo-only decision (synthetic data,
  not an OD-53 approval, production OFF).
* Measured gap: `grep -n -E "2026-11-02|DEMO-EXCEPTION|in principle"` over the BRD and PRD finds no record of either owner direction
  (the only hit is an unrelated BRD line 573). BRD OD-53 (line 2171) and PRD OQ-029 (line 2953) still read as if no owner direction
  exists beyond 2026-10-23.
* Normative wording is already correct: BRD 1683-1687 and PRD 1049-1052 keep per-message review as default, exception OFF.

## Decision

Smallest fix: record the owner directions in BRD OD-53 and PRD OQ-029 without changing status, add a KB log entry, and add a
regression test that fails if the directions are absent or if the docs claim approval. No status upgrade; criterion 5 stays open.
