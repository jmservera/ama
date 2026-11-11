<!-- markdownlint-disable-file -->
# Plan: #80 exception-register CSV contract (issue-80-exception-contract-2122)

Research: [research](../../research/2026-11-11/issue-80-exception-contract-2122-research.md). Details (the PROPOSED contract): [details](../../details/2026-11-11/issue-80-exception-contract-2122-details.md). Critique: [critique](./issue-80-exception-contract-2122-critique.md).

Branch docs/exception-export-contract-80-2122, base 077ad5ad20293a1d79932ea14e9f639dd11e5a22, target main, Refs #80 only. Tier: documentation-only candidate, focused: Markdown, link and diff review; no runtime or full gate.

## Phases

* [x] P1 Research: static reading of endpoint, store, queue, UI, tests, export prior art and #80/#135 refinement.
* [x] P2 Details: write the PROPOSED contract (shape, write rules, four fields, formula-safe CSV, bounded meaning, case matrix, observable requirements, next slice, policy questions).
* [x] P3 Critique: one independent critique of this final plan and details; apply compatible findings.
* [x] P4 Implement: record the evidence trace in the changes file and session state. No file outside `.copilot-tracking/`.
* [x] P5 Review: one post-implementation review; route open work to follow-ups.
* [x] P6 Commit locally with the authenticated noreply identity and the Copilot trailer; write the handoff.

## Boundaries

No application, endpoint, UI, test, tool, workflow, docs/, cutover-pack, memory, private-data or issue/board change. No push, PR, merge, issue comment or acceptance tick. No new source allowance and no Capacity cycle reset. The contract is PROPOSED, not an owner decision.

## Decisions carried

* Existing audit-on-view and audit-on-denial behaviour is permitted; only controlled-domain writes are prohibited.
* Browser-only four-field visible summary; no server route.
* Empty, roles-not-named, denied, unavailable, malformed and partially unreadable states offer no file.
* Company-role or data-role interpretation is hypothesis, not authority.

## Validation

* Link check of every relative link in the new artifacts and `git diff --stat` showing only `.copilot-tracking/` files.
* Spot re-check of cited line numbers against the pinned tree.
