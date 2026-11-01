<!-- markdownlint-disable-file -->
# Plan: issue 441 fresh-main recheck (2026-11-01)

Research: [issue-441-recheck-research.md](../../research/2026-11-01/issue-441-recheck-research.md). Details: [issue-441-recheck-details.md](../../details/2026-11-01/issue-441-recheck-details.md).

## Scope

Documentation evidence only. No BRD, PRD, ADR, addendum, memory or source change. No new code under `mvp/`, `prototype/` or `src/`.

## Phases

* [x] Phase 1: add the read-only verifier and report under `.copilot-tracking/changes/2026-11-01/issue-441-recheck/` (ruff clean).
* [x] Phase 2: record the changes file with hashes, overlap table and criterion mapping.
* [x] Phase 3: append one dated entry to `docs/reference/log.md` (append-only).
* [x] Phase 4: validate (verifier, ruff, log check done); the single independent Review follows in the Review phase.
* [ ] Phase 5: commit with the repository-local noreply email, push without force, open PR with `Refs #441`.

## Decisions

* Do not re-apply the stale draft patches; main already integrates them.
* Do not register an ADR ID; no allocator exists and the owner has not decided.
* Criteria 5 and 9 stay unticked. The PR uses `Refs #441`.

## Validation tier

Focused: verifier, ruff check, ruff format --check on the script, Markdown/link review of the log entry and `git diff`. mypy and unit tests do not apply: no `src/` project is touched. CI is the publication evidence; no heavy local gate.
