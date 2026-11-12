<!-- markdownlint-disable-file -->
# Plan: #1402 C2 post-parent integration and requalification

Research: [research](../../research/2026-11-11/aftercare-blank-state-1402-c2-integration-1111-research.md). Details: [details](../../details/2026-11-11/aftercare-blank-state-1402-c2-integration-1111-details.md). Prospective; committed before any integration or validation. This plan describes integration verification, not new source implementation.

## Phases

* [ ] 1. Preserve original head as local ref `evidence/1402-c1-e8468` (annotated-free lightweight tag, local only).
* [ ] 2. Rebase own three commits onto `origin/main` (no push). Record old to new mapping and prove replay completeness (four commits, range-diff, whole-diff inspection).
* [ ] 3. Verify identities: the two issue-owned files byte-equal to e8468; numeric restoration files byte-equal to `origin/main`.
* [ ] 4. Fresh focused requalification under new evidence directory `evidence/2026-11-11/aftercare-blank-state-1402-c2-integration-1111/`: intake plus aftercare (expect 67 tests), API screen (expect 13), ruff check and format on the two touched files, mypy on the source file.
* [ ] 5. Write C2 changes record, one Review, state; commit; freeze clean; handoff.

## Constraints

No source or test edits. No SQL, installs, browsers, cloud, full gate, private data. A conflict or any failure stops and is reported. Prior evidence directories are never modified.
