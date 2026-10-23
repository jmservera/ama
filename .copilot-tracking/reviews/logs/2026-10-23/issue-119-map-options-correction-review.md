<!-- markdownlint-disable-file -->

# Review: issue-119-map-options-correction

Date: 2026-10-23. Review actually performed via the rpi-review skill, once, for the correction boundary (uncommitted working tree on head 0e7c9f9a5a9bc7d56d6b6a01a68ec015929ae39e, main 140d8f494482c78e84d15f3d46b9223d3c487af0). No second Review runs for this task.

* Plan: .copilot-tracking/plans/2026-10-23/issue-119-map-options-correction-plan.md
* Details: .copilot-tracking/details/2026-10-23/issue-119-map-options-correction-phase-details.md
* Critique: .copilot-tracking/reviews/2026-10-23/issue-119-map-options-correction-plan-critique.md (Revise, six dispositions applied, not repeated)
* Changes: .copilot-tracking/changes/2026-10-23/issue-119-map-options-correction-changes.md
* Research: .copilot-tracking/research/2026-10-23/issue-119-map-options-correction-research.md
* Independent review that prompted this cycle: MAP-001 and MAP-002 on head 0e7c9f9a.

## Execution and outcome

* Execution status: Complete for the documentation-only working-tree boundary. The full gate, push and PR write are deliberately outside it.
* Outcome: Residual work. MAP-001 and MAP-002 are corrected as planned; no defect was found in the corrected text. Whole-issue criteria are not accepted.

## Comparison to the plan

* AC1 (labels): the claim inventory in the changes record matches the document. A grep of Learn, docs.os.uk, maptiler, ODbL, Protomaps, Geofabrik and eu.atlas shows every hit under a draft, unverified or re-read label; Row A, B, C, D, E, the Option bullets, the Entra premise, the cost method sentence, the unverified list and the ADR 0002 delta were read. Met.
* AC2 (budget): USD500 and USD 535.41 appear only in the superseded-history paragraph; the USD 700 all-in ceiling, expiry 2026-10-25T16:02Z, Unknown headroom, refresh gate, verified headroom plus finite separate approval and no retirement authority are stated; the addendum anchor exists. Met.
* AC3 (preservation): git status shows only the four documentation files modified and new 2026-10-23 artifacts; no 2026-10-20 or 2026-10-21 tracking file is modified; log.md has zero deleted lines. Met.
* AC4 (acknowledgement): the changes record states the earlier PC-001 and AC1 completion claim was not borne out. Met.
* AC5: both issue criteria unmet, screen reader NOT RUN, no provider selection, no closing keyword. Met.
* AC6: git diff --check, ASCII scan, link and anchor existence and the static accessibility baseline test (7 tests) passed. Static test is not accessibility acceptance. Met for the correction boundary; no full gate by design.

## Findings

* RV-001 (Medium, residual work): issue criterion 2, an actual screen-reader run of the list alternative, is unmet. Route: distinct follow-up for a human or assistive-technology tester.
* RV-002 (Medium, residual work): vendor rates, terms, attribution wording, DPA, processor and regional or authentication assurances remain unverified; this cycle only labels them. Route: rpi-research follow-up with owner-approved sources.
* RV-003 (Medium, residual work): current all-in October forecast and headroom are Unknown under the USD 700 ceiling expiring 2026-10-25T16:02Z; a refreshed post-change forecast is needed before any tranche. Route: owner and cost-owner follow-up; no paid execution here.
* RV-004 (Low, residual work): prior receipts for 0e7c9f9a are historical after this change; a fresh exact-head full gate and independent review are needed. Route: coordinator.
* RV-005 (Low, process): the plan marker ticks and the critique-disposition edits used a shell script instead of the edit tool. Content is diff-reviewable; no further action beyond independent assessment.
* RV-006 (Low, wording): the first "Cannot yet be verified" bullet is slightly long after the generic label was prepended. Not a defect; route to optional later cleanup.

## Validation

* git diff --check, ASCII scan of added lines, deletion count (52 in-file rewrites, none in the log), label grep, link and anchor check, src/api tests.test_accessibility_baseline (7 OK). Not run: full gate, Docker, Azure, web retrieval.

## Routing

* No defect needs rpi-implement; no decision gap needs rpi-plan. RV-001 to RV-004 are distinct follow-ups.
