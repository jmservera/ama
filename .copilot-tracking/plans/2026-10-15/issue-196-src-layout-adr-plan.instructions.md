<!-- markdownlint-disable-file -->
# Plan: issue 196 src layout and cut-over ADR

Research: [issue-196-src-layout-adr-research.md](../../research/2026-10-15/issue-196-src-layout-adr-research.md)
Details: [issue-196-src-layout-adr-details.md](../../details/2026-10-15/issue-196-src-layout-adr-details.md)
Critique: executed once (see below).

## Phases

* [x] Phase 1: Write `docs/adrs/0006-src-layout-and-cutover.md` (Status Proposed) covering every #196 acceptance criterion.
* [x] Phase 2: Update `docs/reference/README.md` index and append `docs/reference/log.md`.
* [x] Phase 3: Validate links, ASCII punctuation, module coverage; record RPI artifacts; commit, push, open PR.

## Critique (one pass, compatible findings applied)

* Dependency rule would be violated if `doc_controls` moved to importer (store imports it): applied, kept in core.
* Registry needs excludes for `src/**/web/vendor/**` and `src/**/data/**`: applied as a prerequisite registry PR (#198).
* Candidate-name AC: owner already selected `zava_forward`: recorded with candidates for the record, not assumed.
* No source code changes in this task; no tests to run beyond link review.
