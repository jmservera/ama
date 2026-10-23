<!-- markdownlint-disable-file -->

# Review: issue-119-map-options-recovery

Date: 2026-10-20. Review actually performed via the rpi-review skill, once, for the recovery boundary.

* Plan: .copilot-tracking/plans/2026-10-20/issue-119-map-options-recovery-plan.md
* Details: .copilot-tracking/details/2026-10-20/issue-119-map-options-recovery-phase-details.md
* Critique: .copilot-tracking/reviews/2026-10-20/issue-119-map-options-recovery-plan-critique.md (Revise, dispositions applied, not repeated)
* Changes: .copilot-tracking/changes/2026-10-20/issue-119-map-options-recovery-changes.md
* Research: .copilot-tracking/research/2026-10-20/issue-119-map-options-recovery-research.md

## Execution and outcome

* Execution status: Complete for the working-tree boundary (uncommitted P01, P02, P03-T01). P03-T02 (commit, full local gate, receipt) is deliberately after this record and is evidenced outside it by the external receipt.
* Outcome: Residual work. Documentation conforms to the owner direction and AC1-AC3, AC5, AC6; AC4 and whole-issue criteria are not accepted here.

## Comparison to the plan

* AC1: re-read claims confirmed; the inconsistent OS secondary rate is labelled unverified in the options doc. Met.
* AC2 and AC5: WCAG baseline records "Not run" and states engineering evidence is not a screen-reader run; ADR delta labels the Entra header point an inference; DPO question open. Met.
* AC3 and AC6: clarifications appended to six original markdown artifacts, original JSON untouched, log append-only; only deleted line is the replaced line in the new options doc. Met.
* AC4: pending (gate not yet run at record time). An earlier runner (pids 1610738/1610739) on the draft head remains as historical, non-final evidence.

## Findings

* RV-001 (Medium, residual work): issue criterion 2, an actual screen-reader test, is unmet; no screen reader, display or AT is available on this host. Route: distinct follow-up, human or assistive-technology tester per the baseline protocol.
* RV-002 (Medium, residual work): provider paid rates, plan terms, attribution wording and DPA and sub-processor positions remain unverified (OS, MapTiler, Azure paid rate and geography/auth, Microsoft DPA). Route: rpi-research follow-up needing owner-approved or signed-in sources.
* RV-003 (Low, residual work): the owner provider decision and DPO personal-data view of tile areas are not made. Route: owner.
* RV-004 (Low, process): the log append and clarification appends used shell commands, not the edit tool. Content is append-only and diff-reviewable; no later action beyond independent assessment.
* RV-005 (Low, process): the draft critique and draft artifacts predate the RPI skills; disclosed by appended clarifications and the recovery artifacts. Independent assessment should treat the original records as unverified.

## Validation

git diff --check clean; no non-ASCII additions; src/api tests.test_accessibility_baseline 7 OK (static only, not accessibility acceptance). Full gate: pending, external.

## Follow-Up Items routed

Human screen-reader run; vendor verification; owner decision. No whole-issue acceptance criterion is ticked and no closing keyword is used.
