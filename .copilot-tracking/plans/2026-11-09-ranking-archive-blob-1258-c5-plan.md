# Issue 1258 Blob listing validation plan, cycle c5 (2026-11-09)

Refs #1258. Plan for the FINAL productive correction cycle. Research: `.copilot-tracking/research/2026-11-09-ranking-archive-blob-1258-c5-research.md`. Details: `.copilot-tracking/details/2026-11-09-ranking-archive-blob-1258-c5-details.md`.

## Objective

Make `BlobRankingArchive.names()` refuse a structurally invalid HTTP 200 List Blobs body with a fixed-text `BlobArchiveError`, so it can never look like a healthy empty archive through `verify`, `overdue`, Store status, the API or runner publish.

## Phases

* [x] Phase 1: red regressions (fixture accepts an injected 200 listing body; core, API and runner tests for wrong root, missing `Blobs`, malformed `Blob`/`Name`, valid empty, ordinary pagination).
* [x] Phase 2: surgical adapter change (`_parse_listing`), nothing else in source.
* [x] Phase 3: targeted DEMO checks (changed and impacted tests, ruff, mypy on the adapter).
* [x] Phase 4: README sentence, changes record, one original Review, state, local commit.

## Contract

* Root must be `EnumerationResults` with a direct `Blobs` child.
* Only `Blobs/Blob/Name` is traversed. Each `Blob` needs one direct non-blank `Name`; otherwise refuse the listing.
* Valid empty `Blobs` and an absent or blank `NextMarker` still return the names so far. Non-blank `NextMarker` still paginates, bounded by the existing page limit.
* Names outside `ranking-*.json` are still ignored.
* Text is fixed: `ranking archive listing was unreadable`. No body, URL, container or secret.
* Unchanged: no put/delete/overwrite exposure, conditional create, source isolation, pre-dispatch authorization refusal versus uncertain write, path-free, audit, manual and cost guards.

## Tier and validation

Owner-selected DEMO targeted tier. Run core `test_ranking_archive_blob`, `test_ranking_publication`, `test_ranking_publication_runner`; API `test_ranking_publication_wiring`; orchestrator is not impacted (separate digest adapter) and not rerun. Ruff and mypy on the touched files. Record that no emulator or real Azure was used.

## Risks

* A real Azure namespace or attribute difference: attributes are ignored and no namespace is expected from List Blobs, which matches documented behavior; unverified against an account and stated as such.
* Last productive cycle: any later finding becomes a recorded follow-up needing new explicit authorization.

## Critique dispositions

One critique executed (`.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-c5-critique.md`), PC5-1 and PC5-2 accepted: `Name` must have no child elements, and parser `ParseError`, `LookupError` and `ValueError` all map to the fixed refusal. Not repeated.
