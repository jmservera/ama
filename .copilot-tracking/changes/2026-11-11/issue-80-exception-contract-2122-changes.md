<!-- markdownlint-disable-file -->
# Changes: #80 exception-register CSV contract (issue-80-exception-contract-2122)

Plan: [plan](../../plans/2026-11-11/issue-80-exception-contract-2122-plan.md). Details: [details](../../details/2026-11-11/issue-80-exception-contract-2122-details.md). Research: [research](../../research/2026-11-11/issue-80-exception-contract-2122-research.md). Critique: [critique](../../plans/2026-11-11/issue-80-exception-contract-2122-critique.md).

Branch docs/exception-export-contract-80-2122, base 077ad5ad20293a1d79932ea14e9f639dd11e5a22.

## What was implemented

Only the bounded documented proposal and its evidence trace, all under `.copilot-tracking/`:

* research, plan, details (the PROPOSED contract), critique, this changes record, the review and the session state.
* The contract states: browser-only four-field visible-summary CSV; existing audit-on-view and audit-on-denial permitted, controlled-domain writes prohibited, activation makes zero requests; closed-vocabulary cells with fail-closed rules; formula-safe CSV; bounded meaning of "all records"; a case matrix with no file for filtered-empty, roles-not-named, denied, unavailable, malformed and partially unreadable states; observable requirements O1-O7; next slice and policy questions.

## Amendments and divergences

* Critique findings PC-001 to PC-007 were applied to the details before implementation closed (see the critique). No divergence from the admitted scope.
* An initial plan draft pre-ticked P3 to P6; it was corrected to unchecked before the critique ran, then ticked as each phase finished.

## Not changed

No application, endpoint, UI, test, tool, workflow, docs/, `docs/reference/`, cutover-pack, owner memory or private-data file. No GitHub issue, board, PR or push. No source allowance added; no Capacity cycle reset. No acceptance criterion ticked or relaxed; #80 whole-issue criteria 2 and 4 remain unmet.

## Validation performed

* Static source reading only (see research). Relative-link and diff-scope review recorded in the review. No runtime, browser, full or `--changed` gate was run; none is applicable to a documentation-only tracking change and none is claimed.
