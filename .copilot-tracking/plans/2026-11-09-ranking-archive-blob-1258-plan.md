# Issue 1258 Blob JSON persistence plan (2026-11-09)

Refs #1258. Planned before any merge, code or test edit. Follows the Blob research record `.copilot-tracking/research/2026-11-09-ranking-archive-blob-1258-c4-research.md`. Details: `.copilot-tracking/details/2026-11-09-ranking-archive-blob-1258-details.md`. Cycle: c4 of at most five total (c1 to c3 spent; c5 is reserve and not planned).

Tier: owner-selected DEMO tier for this push (targeted changed and impacted modules, no `rpi-checks --all`, no SQL, browser, image or scanner run). FULL receipt, independent exact-head review, hosted checks and human approvals remain required later and are not claimed.

## Objective

Move the application ranking publication, verification and status path to the owner-selected Blob JSON persistence while keeping every observable ranking publication contract: dated immutable records, first-writer-wins conditional create, idempotent retry with the original date, verifiable content and metadata, path-free refusals, and the committed-unconfirmed outcome with no false success and no rollback after an uncertain write.

## Scope

In: one small core adapter, `ranking_archive_blob.py`; Blob dispatch in `ranking_publication.publish/verify/overdue`; archive selection and error wording in `Store`; the API 409 wording; the runner `--blob` selection; README and tests.

Out: any Azure resource, container, role grant, Bicep environment variable or deployment; an emulator install; a generic storage abstraction; the private `ZF_DATA` file and any other JSON dataset; an archive SQL migration; extending, deleting or re-testing the filesystem hardening (c1 to c3 code stays as the local adapter, unchanged); retention or purge; AI, SQL, browser or image work.

## Design decisions

1. Blob adapter reuses the repository REST pattern: it subclasses `AzureBlobDocumentStore` (SAS or managed identity, injectable transport, container and https validation) like `BlobDigestStore`, adds create-only upload with metadata, read with metadata, and a paginated name listing. No delete or overwrite method exists.
2. Selection: `ZF_RANKING_ARCHIVE=azure-blob` plus the existing `ZF_BLOB_ACCOUNT_URL`, `ZF_BLOB_CLIENT_ID`, `ZF_BLOB_SAS` and a new `ZF_RANKING_BLOB_CONTAINER`. Unset keeps the local folder adapter, labelled development and test only. An unknown selector, a missing or invalid URL or container refuses with a path-free storage error. No fallback from a failed Blob to the folder.
3. Name and content: same `ranking-{version}-{as_of}-{hash12}.json` name and canonical content. The blob name is derived from validated snapshot fields only and is matched against a strict pattern; no caller-supplied URL, container or path reaches the adapter.
4. Metadata (verifiable, ASCII): `policy_version`, `as_of`, `published_on`, `snapshot_hash`, `record_sha256`. Existing-record validation and `verify()` compare them with the content. Missing or mismatching metadata is a problem, never a pass.
5. Create-only: `PUT` with `If-None-Match: *`. 201 is written. 412, or 409 with no error code other than `BlobAlreadyExists`, means exists: the record is read and validated against the snapshot as today (`written False`, original `published_on`), otherwise refused and never overwritten. Other 4xx is a definite refusal (path-free storage error with the HTTP status only).
6. Uncertain write: a transport failure, timeout, 408 or 5xx on the `PUT` raises `ArchiveWriteUncertainError`, a subclass of `DurabilityUnconfirmedError` (written None, text says the record may or may not be stored and nothing was rolled back). Store audits `ranking_snapshot_publication_unconfirmed`, API returns 409 `committed_unconfirmed`, the runner reports `committed_unconfirmed`. A retry resolves it idempotently through the conditional create. No delete, no rewrite, no success claim.
7. Errors never contain the account URL, container, record URL, SAS or tokens.
8. Runner: `--archive DIR` or `--blob`; a Blob archive skips the free-space probe and the file existence probe (the conditional create is the idempotence check).
9. Honesty: the local folder adapter documents that fsync evidence does not show container persistence; the Blob adapter documents that the container immutability policy, role grant and provisioning are infrastructure and are not proved here, and that tests use an in-memory REST fake, not an emulator or a real account.

## Critique dispositions (one critique, `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-critique.md`, Revise, PC-001 to PC-007 applied)

* Composition, not subclassing: the adapter wraps an `AzureBlobDocumentStore` for URL, SAS, token and transport and exposes only `create`, `read` and `names` (supersedes design decision 1's subclass wording).
* Conflict rules: 201 or 200 created; 412 exists; 409 with `BlobAlreadyExists` or no code exists; other 409 and other 4xx are definite refusals; a failed read of an "existing" blob is a refusal.
* Token or configuration failure before dispatch is a sanitised definite refusal; only a failure after dispatch (transport error, 408, 5xx) is an uncertain write. Exceptions are not chained.
* Retry idempotence applies to the identical snapshot; a changed input is a new record.
* No migration of existing folder records is authorised: Blob starts a fresh archive. This is an explicit limit and an unresolved history dependency.
* `record_sha256` is over the exact stored bytes; metadata headers are matched case-insensitively. The runner `path` for Blob is the opaque record name.

## Phases

| Phase | Work | Exit |
| --- | --- | --- |
| P0 | Fetch main, commit research, plan, details, critique records; merge `origin/main` locally (no rebase, reset, force, stash) | Merge clean or reconciled; ranking blobs unchanged |
| P1 | Failing-first tests: Blob contract (core), runner, Store and API wiring | Red recorded: import failures, then behavioural failures |
| P2 | Adapter and `ranking_publication` dispatch | Core contract tests green |
| P3 | Store, API 409 wording, runner flag | Wiring tests green |
| P4 | README and docstrings; ruff, mypy on changed files | Clean |
| P5 | Changes record, one Review, frozen commit, handoff | Review executed once |

## Validation (DEMO tier, one worker, synthetic temp data, no network)

* Core: `cd src/core && PYTHONPATH=<worktree src>:tests python3 -m unittest test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner -q` (existing 97 plus new).
* API: `cd src/api && PYTHONPATH=<worktree src>:../core/tests:../agents/tests python3 -m unittest discover -s tests -p test_ranking_publication_wiring.py -q` (existing 24 plus new).
* `ruff check` and `mypy` on the changed core files per `src/core/pyproject.toml`.
* Impacted modules: `test_documents` (adapter base class) and `src/orchestrator/tests/test_digest_blob.py` (shared base) are run to show the base class is unchanged in behaviour.
* Skips, exits and counts recorded as they occur. SharedSQL, Docker, emulator, browser, scanners and the full matrix are not run.

## Acceptance mapping to the issue

| Criterion | Plan evidence |
| --- | --- |
| Pre-created or sync ancestors | Superseded by owner Blob decision; the filesystem criterion is not satisfied or ticked here |
| Post-write uncertainty is committed-unconfirmed, no false success or rollback | Uncertain-write tests (lost response, not stored, 5xx), audit and API tests |
| Failing-first regression | Red logs before the adapter exists |
| Retry, concurrency, audit, path-free 409/503, original date intact | Core, runner and API tests |
| Full RPI, FULL receipt, independent review, hosted checks | Not performed; remain unticked |

## Risks and limits

* Mock transport only; real Azure status codes for timeouts, immutability policy errors and the 409 error code header are not exercised.
* The Blob container, WORM policy, identity role and environment variable do not exist; deployed Blob persistence is unproved.
* Overlap with issue 1292 on Store hooks; the final exact-current-main merge and affected tests wait for its delivery.
* Child 1259 (archive path health) targets this parent; its filesystem health assumptions need review against Blob after this contract is ready. No sibling code is copied.
