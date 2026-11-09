# Changes: ranking archive Blob JSON persistence (c4, Refs #1258)

Plan: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-plan.md`. Details:
`.copilot-tracking/details/2026-11-09-ranking-archive-blob-1258-details.md`. Critique (one, Revise,
PC-001..PC-007 applied): `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-critique.md`.
Owner decision (2026-11-08): use Blob for JSON persistence. Cycle accounting: c1..c3 spent, this is c4 of at
most five total; c5 not used.

## Source changes

* New `src/core/src/zava_forward/core/ranking_archive_blob.py`: `BlobRankingArchive` composes
  `AzureBlobDocumentStore` (same REST, SAS or managed-identity auth) and exposes only `create`
  (create-only Put Blob, `If-None-Match: *`), `read` (bytes plus lower-cased metadata) and `names`
  (paginated listing). Strict `ranking-...json` name guard. `BlobArchiveError` (definite refusal, HTTP status
  only, no URL/container/credential) and `BlobArchiveUncertain` (request sent, outcome unknown).
  `metadata_for` writes policy_version, as_of, published_on, snapshot_hash, record_sha256.
  `open_ranking_archive`/`from_environment` select by `ZF_RANKING_ARCHIVE=azure-blob`
  (+ `ZF_BLOB_ACCOUNT_URL`, `ZF_RANKING_BLOB_CONTAINER`, `ZF_BLOB_SAS`/managed identity, `ZF_BLOB_CLIENT_ID`);
  unset or `local` keeps the folder adapter; an invalid Blob selection refuses, never falls back.
* `ranking_publication.py`: `publish`/`verify`/`overdue` accept a Blob archive. Blob publish is one conditional
  create; a conflict reads back and validates (metadata, hash, name, date) and reports already published.
  New `ArchiveWriteUncertainError(DurabilityUnconfirmedError)` (written None, "may or may not be stored",
  nothing rolled back). Blob verify checks metadata and raises OSError on an unreadable listing. Folder code
  path unchanged.
* `store.py`: `_ranking_archive` selects the adapter; status opens the archive inside its try; Blob-specific
  503 text and audit text for an uncertain write (action name unchanged).
* `api/server.py`: 409 `committed_unconfirmed` text chosen by exception type (uncertain write versus folder sync).
* `ranking_publication_runner.py`: `--blob` (mutually exclusive with `--archive`), no capacity or file probe for
  Blob, uncertain write status `committed_unconfirmed`, unconfigured `--blob` exits 2 without a traceback.
* `src/core/README.md`: Blob selection, variables, behaviour, local adapter honesty, what is not proved.

## Tests (failing first)

* New `src/core/tests/ranking_blob_fixture.py` (in-memory mock REST transport, not an emulator) and
  `src/core/tests/test_ranking_archive_blob.py` (23 tests); runner (4) and API wiring (7) Blob tests added to
  existing files.
* Red run before any source edit: core `Ran 102, FAILED (errors=5)`; API `Ran 34, FAILED (errors=10)`.
* Green after implementation (logs kept outside the commit in `/home/azureuser/.copilot-tracking-logs-1258/`):
  * core `test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents`:
    134 tests OK, exit 0.
  * API `test_ranking_publication_wiring.py`: 34 tests OK, exit 0 (existing rule-engine log noise unchanged).
  * orchestrator `test_digest_blob.py`: 27 tests OK, exit 0 (needs `src/core/tests` on PYTHONPATH for `dataset`).
  * `ruff check` exit 0; `ruff format --check` clean on all touched files except `store.py`, which was already
    unformatted at HEAD (not reformatted, to avoid unrelated churn); `mypy` on the three ranking modules: no issues.

## Divergences and amendments

* Runner source must not read `os.environ` (existing guard test), so the environment read lives in
  `ranking_archive_blob.from_environment`.
* Two assertions in my first test draft were corrected during implementation (runner path derived from the written
  blob; transport patched at `documents.urllib_transport`). No implementation requirement changed.

## Not done / not proved

* No emulator exists locally (Azurite absent) and none was installed: evidence is a mock transport only. No real
  storage account, container, immutability policy, role grant, Bicep setting or deployment; no crash or Azure
  acceptance. No full local gate, SQL, browser or scanner run (DEMO tier). SharedSQL not touched.
* Existing folder records are not migrated; a Blob archive starts empty (history dependency, owner decision needed).
* Retry idempotence covers an identical snapshot only; a changed input after an uncertain write is a new record.
* c2 PC-002 and c3 PC3-1 stay open in their original records; the Blob decision supersedes them without resolving them.
* Final exact-main integration and affected tests wait for #1292 delivery (Store/API overlap).
