# Issue 1258 Blob JSON persistence research (2026-11-09)

Refs #1258. Read-only research before any plan, merge, code or test edit. Earlier original, c1, c2 and c3 filesystem records are history and are not edited or regraded.

## Authority and scope

* Owner decision on issue 1258 (2026-11-08T18:44:58Z): "Use a blob storage for JSON persistence". It selects Blob for the operational ranking archive JSON. It is not further local-directory or mount-relocation hardening, not an archive SQL migration, and not approval to migrate unrelated JSON or private datasets, create Azure resources, change access permissions or relax resident and human controls.
* Coordinator brief (2026-11-09): restore the application publication and archive path to Blob, demo-targeted validation tier, local only, Refs 1258, no cloud fallback, no full receipt, no Azure, crash or deployment acceptance claimed. The five FULL and production acceptance criteria of the issue stay unticked.
* Start: HEAD 61df2371508f4b549b7d3a85a86770f4f83cead9 on `fix/ranking-archive-ancestor-durability`, ignored-inclusive status clean. Fetched `origin/main` is 06e3f2f456ab008f8e41f013d9019c2d82ea05b9 (34 commits after the branch's merge base f548b65f). Merge base f548b65f.

## Correction-cycle accounting (actual, not reset)

| Cycle | Commit | Evidence |
| --- | --- | --- |
| c1 | e40a89ed4 | `...-1258-c1-*` records; writable-parent cutoff removed |
| c2 | a00387098 | `...-1258-c2-*`; mount-table boundary; PC-002 Blocking left open |
| c3 | 61df23715 | `...-1258-c3-*`; owner comment 6722289866 authorised one cycle beyond the then two-cycle limit; PC3-1 ABA race Blocking left open |

Three scoped review-correction cycles are spent. The repository default confirmed by the owner on 2026-11-09 is at most five total per issue, so at most two remain (c4, c5). This owner-re-scoped Blob source change is c4 because it changes source. The records of this cycle use the suffix `blob-c4`. c5 is held in reserve and is not planned. The owner's Blob decision supersedes, and does not resolve, the filesystem blockers PC-002 and PC3-1; they stay open in their records, the filesystem contract is not extended here.

## Current contract that must be preserved (merged ranking publication, issues 79 and 1231)

Source: `ranking_publication.py` at main f548b65f (unchanged on main to 06e3f2f4: `git diff HEAD...origin/main` names no ranking file).

* One immutable, dated record per policy version, as_of date and snapshot hash, named `ranking-{version}-{as_of}-{hash12}.json`, content `{"published_on", "snapshot"}` in canonical JSON.
* Idempotent: the same snapshot reports `written False` with the original `published_on`; an existing record that is unreadable, differs from the snapshot, has a mismatching hash or name, or has an invalid date is refused with `PublicationError` and never overwritten.
* First writer wins: creation is conditional (hard link on the file system). Concurrent writers keep exactly one record and the loser reports it (issue 1231).
* `verify()` rehashes every record and reports count, problems and latest date; `overdue()` compares the latest date with a supplied day. Nothing reads a clock.
* Outcomes: confirmed publication; refusal (`PublicationError`, Store `ValueError`, API 400/refusal); storage failure (`OSError`, Store `ArchiveStorageError`, API 503, path-free); committed-unconfirmed (`DurabilityUnconfirmedError`, record kept, audited `ranking_snapshot_publication_unconfirmed`, API 409 `outcome: committed_unconfirmed`, runner status `committed_unconfirmed`, no rollback, a retry reports the record as already published).
* Adapters: `Store._ranking_archive()` (a folder beside the data), `Store.publish_ranking_snapshot`, `Store.ranking_publication_status`, API `POST /api/ranking/publish` and `GET /api/ranking/publication` (manager only), and the runner `ranking_publication_runner` (`schedule`, `publish`, `verify`; `--archive DIR`; `free_bytes` capacity check; `os.path.exists` idempotence probe).
* Everything else in c1 to c3 (hard link stage, ancestor syncs, held-descriptor walk) is the local file system adapter's concern and does not apply to Blob.

## Repository Blob patterns found

| Pattern | Location | Fit |
| --- | --- | --- |
| REST over `urllib` with injectable `transport`, SAS (`ZF_BLOB_SAS`) or managed identity token, no new dependency | `core/documents.py` `AzureBlobDocumentStore`; env `ZF_BLOB_ACCOUNT_URL`, `ZF_BLOB_CONTAINER`, `ZF_BLOB_SAS`, `ZF_BLOB_CLIENT_ID` | Best: core already uses it, tests use a fake transport, container name and https URL are validated, and credentials are never logged. |
| Create-only JSON, `If-None-Match: *`, 409/412 means exists, paginated listing, read | `orchestrator/digest_blob.py` `BlobDigestStore` | The exact semantics needed; lives in the orchestrator package, so the core module cannot import it and a small core adapter is needed. |
| SDK `BlobServiceClient` with `DefaultAzureCredential`, `upload_blob(overwrite=False)` | `core/lawstore.py` `AzureBlobSnapshots` | Second pattern; optional extra `blob`; no conditional-create outcome or metadata surface, and tests need the SDK. Not chosen. |
| In-memory REST fake: PUT once, 409 on exists, list XML | `orchestrator/tests/test_digest_blob.py` `FakeImmutableContainer` | Approved fixture pattern; reused in shape. |

No Blob emulator (Azurite) exists in the repository, `tools/`, workflows or the venv, and a global install is not permitted. Infra defines the `evidence` and `ledger-digests` containers and the API managed identity (`containerapps.bicep`, `ZF_BLOB_CLIENT_ID`); it defines no ranking container, and this task has no authority to add one. Therefore tests use an in-memory REST fake and are reported as mock, not emulator, evidence. Docker is present but no admission is planned: a local emulator run is not needed for the contract and is not claimed.

## Blob facts the design relies on (Azure Put Blob REST, API version 2021-08-06 as already used)

* `If-None-Match: *` makes Put Blob create-only: success 201, an existing blob gives 409 `BlobAlreadyExists` (some paths 412). A committed block blob is visible whole or not at all, so no staging file exists and `stage_retained` does not apply.
* `x-ms-meta-*` request headers store metadata with the blob; Get Blob returns them as response headers; names must be valid identifiers and the values must be ASCII.
* A request that times out or returns 5xx can have been committed server side, so an uncertain PUT is neither success nor failure. This is the Blob analogue of the committed-unconfirmed outcome; the next conditional create resolves it idempotently.
* Blob persistence is provided by the storage service; a container immutability (WORM) policy is infrastructure and cannot be proved by this code. File `fsync` evidence for the local adapter says nothing about a Blob container.

## Findings that drive the plan

1. The publish, verify, existence probe and capacity check are the only path-dependent operations. `publish()` and `verify()` can dispatch on the archive object (a Blob archive or a folder) with the validation, naming, canonical form and idempotence code shared, so no storage platform layer is invented.
2. `Store._ranking_archive()` is called by the Store and by about 30 existing tests as a local path, so the folder remains the default local adapter, explicitly labelled development and test only. Blob is selected by `ZF_RANKING_ARCHIVE=azure-blob`, mirroring the `ZF_DOC_STORE` selector, with the existing account URL, identity and SAS variables and one new container variable `ZF_RANKING_BLOB_CONTAINER`. A missing or invalid selector, URL or container refuses publication with a path-free storage error; there is no fallback to the folder.
3. The runner's capacity probe and `os.path.exists` are file system specific; for Blob they are replaced by the conditional create and skipped.
4. Error text must not carry the account URL, container, record URL or tokens: only the HTTP status and a fixed description.
5. The API 409 text and the Store audit detail currently say the folder sync failed; the Blob uncertain write needs its own wording without claiming the record was written.
6. Overlap: main moved `sensor_analysis_store.py` and `test_mssqlstore.py` only on the Store and API test side; issue 1292 (SharedSQL work) is not delivered and may touch Store hooks. The planned Store edit is confined to `_ranking_archive`, `ranking_publication_status`, `publish_ranking_snapshot` and the API 409 text. Final current-main integration and affected tests after 1292 delivery are left to the coordinator.

## Planning readiness

Ready. Gaps stated, not assumed: no real storage account, Azurite or container exists to test against; the immutability policy, the container, the role grant, the Bicep environment variable and deployed persistence are not provisioned or verified; real timeout and 5xx behaviour of Azure is not reproduced; SharedSQL, browser, images and scanners are not required for this change and are not run.
