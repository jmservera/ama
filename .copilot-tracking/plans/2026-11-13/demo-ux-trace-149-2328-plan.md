<!-- markdownlint-disable-file -->
# Plan: UX design traceability matrix (issue 149)

Date: 2026-11-13. Task slug: ux-design-traceability-149-2328. Research: [research](../../research/2026-11-13/demo-ux-trace-149-2328-research.md). Details: [details](../../details/2026-11-13/demo-ux-trace-149-2328-details.md).
Validation tier: Focused (docs plus a documentation-guard test; no workflow, dependency, deployment or security change).

## Phases

* [x] Phase 1: Add the matrix section to `docs/reference/research/ux/design-system.md` (update `ms.date`).
* [x] Phase 2: Add `src/api/tests/test_ux_design_traceability.py`.
* [x] Phase 3: Run the focused checks and record output in the review.

## Critique (single pass, final candidate)

* Verdict: proceed. Risk: the test could be satisfied by prose. Mitigation: the test parses table rows, resolves test classes and methods by AST, and requires the pending-human text on every row.
* Risk: touching banned files. Mitigation: none of the three is in the diff; verified by `git diff --stat`.
* Risk: overclaiming. Mitigation: every row says `pending human test`; the section states that no criterion is ticked.
