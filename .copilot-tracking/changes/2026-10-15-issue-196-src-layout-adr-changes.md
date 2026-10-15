<!-- markdownlint-disable-file -->
# Changes: issue 196 src layout and cut-over ADR

Plan: [issue-196-src-layout-adr-plan.instructions.md](../plans/2026-10-15/issue-196-src-layout-adr-plan.instructions.md)

## Added

* `docs/adrs/0006-src-layout-and-cutover.md`
* RPI artifacts for task `issue-196-src-layout-adr` (research, plan, details, changes, review)

## Modified

* `docs/reference/README.md`: ADR 0006 index row
* `docs/reference/log.md`: appended restructure entry

## Divergences

* Importer project owns no existing `mvp` module because `doc_controls` is imported by the stores; recorded in the ADR.
* `mvp/data/` is absent in this worktree; relocation is documented only, nothing read or moved.

## Validation

* Relative links in the ADR and index resolve; no non-ASCII characters in the ADR.
* All 41 `mvp/zavaforward_mvp` modules except `__init__` are assigned a target.
* No executable change, so no test suite was run.
