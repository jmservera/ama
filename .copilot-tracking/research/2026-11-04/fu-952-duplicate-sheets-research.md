# Research: issue 952 duplicate human review sheets

Date: 2026-11-04. Disposition: executed (code read only). Planning Readiness: Ready.

## Prior delivery check

* `gh pr list --search "952 in:body"` returned no PR. Issue 941 (PR "pool human review sessions", Refs #223) introduced `pool_human_sessions` and is the origin; nothing since addresses duplicates.

## Findings

* `src/agents/src/zava_forward/agents/review_effectiveness.py`: `pool_human_sessions` scores every sheet and sums effort and detection. A sheet has no unique identifier; the blank `worksheet()` carries only version, reviewer_code, seconds and answers. The same completed sheet submitted twice is therefore double-counted.
* Existing behaviour to keep: a repeat `reviewer_code` with different content is a separate session reported as not independent (`distinct_reviewers`).
* Existing tests: `tests/test_review_effectiveness.py` pooled-session tests use sheets with different seconds, so a content fingerprint does not disturb them.

## Options

1. Add a sheet id field: changes the worksheet contract and the blank sheet; reviewers would have to fill it.
2. Fingerprint canonical JSON of each sheet and flag repeats (chosen): no contract change, deterministic, covers the case "the same sheet submitted twice".

## Limits

* A sheet edited after copying (one changed second) is a different sheet by this test; it is not claimed to detect near-duplicates.
* Human reviewer competence and authority remain unverified (unchanged open items).

## Acceptance criteria status before work

* Duplicate sheets flagged and not double-counted: unmet.
* A test covers duplicates: unmet.
