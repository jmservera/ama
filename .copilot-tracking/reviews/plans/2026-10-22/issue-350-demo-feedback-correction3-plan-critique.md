<!-- markdownlint-disable-file -->
# Plan Critique: Correction 3 (Refs #350)

* Execution status: Complete
* Verdict: Revise (post-implementation; ran after the code change, disclosed in the plan)
* Inputs: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-correction3-plan.md, .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction3-phase-details.md, .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-correction3-research.md, tools/check-demo-feedback.py diff
* Criterion boundary: requirements P01-T01, P01-T02, P02-T01 against runtime order/cap and JSON parsing behaviour.

## Findings

### PC-001 [Medium]: `math.isfinite` raises OverflowError on huge JSON integers
* Related: P01-T02
* Evidence: `math.isfinite(10**400)` raises OverflowError; the evidence loader accepts arbitrary-size integers, so a crafted `latency_ms` would crash the checker with a traceback instead of a report.
* Smallest change: apply `isfinite` only to floats; add a regression for a huge integer in both signs.
* Owner: implementer (direct correction; no user decision). Resolved after this critique with tests.

### PC-002 [Low]: Cap evidence relies on the before detail being itself capped
* Related: P01-T01
* Evidence: when `before` has 40 entries the true prior count is unknowable offline; the rule `min(len+1, 40)` plus older-contact continuity is the strongest honest check. Accepted residual risk; durability stays blocked.

## Coverage and limitations

Newest-first selection, cap, continuity, strict constants and held-value handling are covered. No live evidence considered. Highest-impact finding: PC-001; owner implementer; no user response required.
