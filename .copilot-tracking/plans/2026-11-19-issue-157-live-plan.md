# Plan: issue 157 live (2026-11-19)

Tier: FOCUSED (documentation index row; no src, SQL, infra or deployment change). Details: .copilot-tracking/details/2026-11-19-issue-157-live-details.md

* [x] Phase 1: tag the retired-path mention in docs/reference/README.md:1355 with archive tag v0.21.0, so the #440 checkpoint gate tool exits 0.
* [x] Phase 2: run tools/test_check_legacy_references.py (existing repo-clean test is the regression) and the guard tool.
* [x] Phase 3: record the per-criterion table, log entry, review; commit.

Critique (single pass, self): compatible; D3 src edit rejected because it needs FULL tier that this task forbids running. 
