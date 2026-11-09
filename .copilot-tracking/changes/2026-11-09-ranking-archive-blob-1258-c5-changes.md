# Issue 1258 Blob listing validation changes, cycle c5 (2026-11-09)

Refs #1258. Implements `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-c5-plan.md` and details. Base HEAD `f724f4bcaac1c5c5b9c5825ffd1cf253f1796b37` (tree `491a2dcfdd8bf24056ef86ba0158b896d0904cab`). Fixes only independent c4 Functional finding 1 (Medium).

## Changed paths

* `src/core/src/zava_forward/core/ranking_archive_blob.py`: new `_parse_listing`; `names()` uses it. Requires root `EnumerationResults`, exactly one direct `Blobs`, and for each direct `Blob` child exactly one direct, childless, non-blank `Name`. Any other child of `Blobs`, parse failure (`ParseError`, `LookupError`, `ValueError`) or structure raises `BlobArchiveError("ranking archive listing was unreadable")`. Only `Blobs/Blob/Name` is collected; blank/absent terminal `NextMarker` and valid empty `Blobs` still work. Raised outside the `except` so no chained body.
* `src/core/tests/ranking_blob_fixture.py`: `list_body` injects a verbatim HTTP 200 listing body.
* `src/core/tests/test_ranking_archive_blob.py`: 15 adverse bodies through `names`, `rp.verify` and `rp.overdue` (fixed text, no secrets); valid empty, blank marker, foreign names, stray/nested `Name` ignored; ordinary pagination test unchanged.
* `src/api/tests/test_ranking_publication_wiring.py`: Store/API status for wrong root, missing `Blobs`, malformed `Blob`: 200 with `count 0, latest None, overdue True` and one path-free problem; valid empty shows no problem.
* `src/core/tests/test_ranking_publication_runner.py`: verify `overdue None, count 0` (problem) and publish `archive_unreadable` with no blob and no PUT; valid empty is overdue with no problems.
* `src/core/README.md`: one sentence.

Bounded note: Store/API publish is a conditional create and does not read the listing, so an invalid listing does not and need not stop an API publish. The runner publish does consult the listing in its preflight and refuses before any PUT; that is the covered path.

## Red first (preserved)

Before the source edit: core `test_ranking_archive_blob` `FAILED (failures=13, errors=1)`; runner `FAILED (failures=1)`; API wiring `FAILED (failures=3)` (log `red-*.log`). The first green attempt also failed twice and is preserved: runner (valid empty `verify` status is `problem` because empty is overdue, assertion corrected to `overdue True, count 0, problems []`) and API (my first draft asserted publish refusal, which is not the contract; corrected to status only). Logs `first-green-attempt-*.log`.

## Green (DEMO targeted tier), PYTHONPATH on this worktree's `src/*/src` and tests

* core `python3 -m unittest test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents`: Ran 137 OK, exit 0.
* API `test_ranking_publication_wiring.py`: Ran 35 OK, exit 0 (stderr traceback noise is existing expected logging).
* `ruff check` on the adapter, core test and fixture: pass; `ruff format --check`: clean after formatting the test file (additive diff); `mypy` on the adapter from `src/core`: no issues.
* Not rerun, not impacted: orchestrator `test_digest_blob.py` (separate adapter). Not run by tier: full gate, scanners, SQL (SharedSQL held by #1288/#1292), browser, images, emulator, cloud. Logs in `/home/azureuser/.copilot-tracking-logs-1258-c5/` (not committed).

## Not proved

No Azurite or real account: the XML shape follows documented List Blobs behavior and is unverified against a service. Container, WORM, roles, Bicep env, deployment, existing-record migration, hosted CI, final integration after #1292 delivery and the Minor R-1 policy-name guard remain explicit and unperformed. The FULL and production criteria of #1258 stay unticked.
