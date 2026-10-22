# Plan: non-operative custody preparation (#122)

Task: `continuity-custody-preparation-122`. Date: 2026-10-21. Research: [research](../../research/2026-10-21/continuity-custody-preparation-122-research.md). Details: [details](../../details/2026-10-21/continuity-custody-preparation-122-details.md).

## Scope

* Add one subsection, "Non-operative custody, recovery and witness preparation (#122)", inside the existing `src/core/README.md` issue #122 section, cross-referenced to the #221 section and #114 digest guidance.
* No runtime code, tests, other READMEs, KB index/log or concurrent-issue files.

## Phases

* [x] Phase 1: Draft subsection (custody and verification expectations, decision rights table, witness, stop/recovery/restart sequence, communication, stop conditions, not-evidence rule, criteria status).
* [x] Phase 2: Add a one-line pointer from the #221 section.
* [x] Phase 3: Validate links/markdown, git diff, scope check.
* [x] Phase 4: Commit with privacy-safe identity; freeze clean.

## Critique (single, final candidate)

Execution: performed once, 2026-10-21, on this plan before implementation. Verdict: proceed with amendments, all compatible and applied directly.

* Risk: protocol could read as an approved drill script. Applied: explicit "not evidence" rule and UNASSIGNED/UNAPPROVED markers.
* Risk: invented actors. Applied: roles only, by OQ-017/OD-35 reference.
* Risk: duplicating #221 prose. Applied: link, not restate.
* Risk: touching KB log or issue criteria. Applied: excluded.
* No significant or divergent issue needing a user decision.
