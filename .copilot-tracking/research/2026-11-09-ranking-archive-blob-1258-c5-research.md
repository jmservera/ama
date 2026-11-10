# Issue 1258 Blob listing validation research, cycle c5 (2026-11-09)

Refs #1258. Read-only research before any plan, test or source edit. The c1 to c3 filesystem records, the c4 research/plan/critique/changes/review and the c4 independent Functional verdict are history and are not edited or regraded.

## Authority and scope

* Coordinator brief (2026-11-09): run c5, the FINAL productive cycle under the five-total authorization. No sixth cycle, reset or automatic exhausted-cohort grant exists. Fix only the independent c4 Functional finding 1 (Medium).
* Start: HEAD `f724f4bcaac1c5c5b9c5825ffd1cf253f1796b37`, tree `491a2dcfdd8bf24056ef86ba0158b896d0904cab`, branch `fix/ranking-archive-ancestor-durability`, clean. Base main `06e3f2f456ab008f8e41f013d9019c2d82ea05b9` is already an ancestor. No fetch, merge or rebase is needed for this cycle.
* Tier: owner-selected DEMO targeted tier only. No full gate, SQL, browser, images, scanner, cloud, emulator or resource provisioning. SharedSQL belongs to #1288/#1292 and is untouched.

## Correction-cycle accounting (actual, not reset)

| Cycle | Commit | Evidence |
| --- | --- | --- |
| c1 | e40a89ed4 | filesystem records |
| c2 | a00387098 | filesystem records, PC-002 left open |
| c3 | 61df23715 | filesystem records, PC3-1 left open |
| c4 | 3b8320ac6 | Blob adapter; authored review approve, independent Functional approve_with_comments 0H/1M |
| c5 | this cycle | listing structure validation only |

After c5 zero productive cycles remain.

## Finding being fixed (independent Functional, finding 1, Medium)

`BlobRankingArchive.names()` in `src/core/src/zava_forward/core/ranking_archive_blob.py` checks HTTP 200 and XML syntax, then collects `root.iter("Name")` over every descendant and reads `NextMarker`. A 200 body of `<Error><Code>InternalError</Code></Error>` or `<EnumerationResults/>` returns `[]`. `rp.verify` then reports `count 0, problems []`, Store/API report an ordinary empty and overdue archive, and the runner publish passes its archive readability preflight. That contradicts the owner-approved contract that an unreadable listing is an error, never a healthy empty archive. This is a confirmed bounded adverse-response defect, not a claim that Azure normally emits such bodies.

## Evidence read

* Adapter lines 144 to 171 (current code above). `names()` is the only listing consumer; `rp.verify`, `rp.overdue`, Store status and the runner all call it.
* Fixture `src/core/tests/ranking_blob_fixture.py` `_list` emits `<EnumerationResults><Blobs><Blob><Name>..</Name></Blob>..</Blobs><NextMarker>..</NextMarker></EnumerationResults>`; only `list_status` is injectable, so an injectable 200 body is needed.
* Existing mocked REST contract tests: core `test_ranking_archive_blob.VerifyTests`, API `BlobPublicationWiring.test_status_reports_a_tampered_blob_and_an_unreadable_listing`, runner `BlobArchiveRunnerTests.test_definite_refusal_and_unreadable_listing_are_refusals_never_empty`. They cover non-200 only.
* Existing callers already map `BlobArchiveError` (an `OSError`): verify raises, Store status reports a path-free problem with `count 0, overdue True`, runner reports `archive_unreadable`/problem and refuses publish before any PUT.

## Azure List Blobs response shape relied on (documented behavior, not retrieved this cycle)

The List Blobs XML root is `EnumerationResults` (with `ServiceEndpoint` and `ContainerName` attributes), containing `Prefix`, `Marker`, `MaxResults`, a direct `Blobs` element whose children are `Blob` elements each with a direct `Name` child, and `NextMarker` (empty on the last page). An empty container returns an empty `Blobs`. The fix follows exactly that shape and does not define a wider schema. Attributes and the other direct children of the root (`Prefix`, `Marker`, `MaxResults`) and the children of a `Blob` other than `Name` (such as `Properties`) are ignored. A `BlobPrefix` child of `Blobs` appears only with a delimiter, which this request never sends, and is rejected as an unexpected structure (review R5-2).

## Findings that drive the plan

1. Parse in one small helper that returns `(names, next_marker)` and raises a fixed-text `BlobArchiveError`.
2. Require root tag `EnumerationResults` and exactly one direct `Blobs` child. A missing `Blobs`, wrong root or non-`Blobs` structure is unreadable.
3. Traverse only `Blobs/Blob/Name`. A `Blob` without exactly one non-blank direct `Name` is malformed and the whole listing is refused, never silently skipped. Foreign names that are well formed but outside `ranking-*.json` are still ignored (existing behavior test).
4. Preserve a valid empty `Blobs` and an absent or blank terminal `NextMarker`.
5. Keep `BlobArchiveError` text fixed: no body, URL, container or secret.
6. Out of scope: Bicep, R-1 policy-name guard, emulator, migration, SQL, other adapters.

## Planning readiness

Ready. Unperformed and not claimed: Azurite or any real account, container, WORM policy, roles, Bicep environment, deployment, existing-record migration, hosted CI, SharedSQL, final integration after #1292 delivery.
