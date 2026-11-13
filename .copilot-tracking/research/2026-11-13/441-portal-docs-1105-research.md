# Research: Issue #441 Criterion 9 local documentation checks

Task: `441-portal-docs-1105`. Base `3b05143179f83235c5b4e80e70aad99bdc44d83f`. Disposition: executed.

## Inputs read

* Issue #441 body and comments (`gh issue view 441`), read-only.
* `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md` (context only).

## Findings

* Targets: `docs/brds/agentic-retrofit-programme-brd.md` (v0.21.0, status draft), `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (v0.21.0, in-review, unsigned), `docs/adrs/0007-*.md`.
* Premise mismatch to record, not resolve: at this base `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md` is the contractor intake ADR with status Proposed. No resident portal ADR file exists in `docs/adrs/`. The issue comment "accepting the ADR as ADR 0007 (2026-11-04)" is not visible in the base file. The check reports what the files say and flags the difference.
* BRD FR-044 (line ~1602) and AC-084 state per-message named review is required except for bounded routine resident communication under RULE-028/FR-061. OD-53 open at BRD ~2171.
* Criterion 5 stays unmet: no human requirements-owner disposition is created by this task.

## Planning Readiness

Ready. Scope: read-only checker over the three docs plus cross-referenced docs targets; tracking-only writes.
