# Issue 1258 Blob listing validation details, cycle c5 (2026-11-09)

Refs #1258. Phase details for `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-c5-plan.md`.

## Phase 1: red regressions

* `src/core/tests/ranking_blob_fixture.py`: add `list_body = None`. When set, `_list` returns `200, {}, list_body` verbatim (bytes) so an adverse 200 response can be injected. No other fixture behavior changes.
* `src/core/tests/test_ranking_archive_blob.py` `VerifyTests`:
  * bodies for wrong root (`<Error>...</Error>`, `<EnumerationResults/>` without `Blobs`, root named `Other`, `Blobs` nested under another element, `Blobs` only as a descendant `Name` carrier), and malformed entries (`Blob` without `Name`, blank `Name`, `Name` nested deeper, two `Name`, non-`Blob` child in `Blobs` with a `Name` descendant): `names`, `rp.verify`, `rp.overdue` raise `OSError`/`BlobArchiveError`, text clean.
  * valid empty `Blobs` gives `[]`, `count 0`; valid empty with a blank `NextMarker`; ordinary pagination (existing `page_size=2` test stays green); a stray `Name` outside `Blobs/Blob` is not collected.
* `src/api/tests/test_ranking_publication_wiring.py` `BlobPublicationWiring`: for wrong root and missing `Blobs`, Store status returns `count 0, latest None, overdue True` with one path-free problem; valid empty status shows no problems. Store/API publish is a conditional create and does not read the listing, so it is not asserted to refuse (review R5-1).
* `src/core/tests/test_ranking_publication_runner.py` `BlobArchiveRunnerTests`: wrong root and missing `Blobs` give `verify` status `problem` and `publish` `archive_unreadable` with `fake.blobs == {}` and no PUT request.

## Phase 2: adapter

Replace the inline `root.iter("Name")` loop in `names()` by a module helper `_parse_listing(body) -> tuple[list[str], str]`:

* parse (`ParseError`, `LookupError`, `ValueError`: fixed `unreadable`; critique PC5-2), require `root.tag == "EnumerationResults"`, `blobs = root.findall("Blobs")` exactly one, each `blob in blobs[0]` must have `blob.tag == "Blob"` and exactly one direct `Name` with non-blank text and no child elements (PC5-1); collect those with the ranking prefix and suffix; marker from the direct `NextMarker` child text.
* `names()` calls it and keeps its pagination loop and bound.

## Phase 3 to 4

Run the targeted commands from the plan; write README one-liner next to the existing "unreadable listing" sentence; write the changes record; run one Review; update state; commit locally.
