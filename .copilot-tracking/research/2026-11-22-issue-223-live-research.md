# Research: issue 223 live run 5 (2026-11-22)

Refs #223. Disposition: executed. Reuses runs 2 to 4 as prior evidence; re-runs the offline gate and the live retention probe on the current head (6a03928ccb).

Planning Readiness: Ready (documentation-only; no buildable code step, remaining criteria need people or owner appointment).

## Evidence

* Offline gate (src/agents): exit 0, passed true, 11 of 11 checks. test_review_effectiveness 37 OK; test_human_review_effectiveness_223 6 OK.
* Live probe on ca-cutover-test-demo-api (employee demo account, Playwright, credentials read at runtime): case ZF-2025-0148, 50 cases visible; summary tasks returned source template, model null, verified true; reject without reason 400 "Say why."; reject with source-named reason 200 with reviewer, reason, resolved_by and review_evidence including source_hashes; second review 400.
* Evidence folder: .copilot-tracking/evidence/2026-11-22/issue-223-live-r5/.

## Findings

No model task is active, so no model-made defect can be seen live. Remaining unproven items need appointed OQ-017 holders and measured human participants. Follow-ups: none buildable.
