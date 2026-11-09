# Issue 1258 Blob JSON persistence phase details (2026-11-09)

Refs #1258. Phase details for `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-plan.md`.

## P1 Failing-first tests

* New `src/core/tests/test_ranking_archive_blob.py` with an in-memory REST fake (PUT with `If-None-Match`, `x-ms-meta-*`, GET returning metadata headers, list with `NextMarker` pagination, 5xx, lost-response and 403 injection, a log of every request, no DELETE) in the shape of `FakeImmutableContainer`:
  * conditional create, one request, `If-None-Match: *`, metadata present, no overwrite or delete ever sent;
  * idempotent repeat with the original `published_on`; two threads on one fake keep one record;
  * existing record that is damaged, different, wrongly named, or has missing or wrong metadata is refused and the stored bytes are unchanged;
  * uncertain write (response lost after commit; failure before commit; 503; timeout) raises `ArchiveWriteUncertainError` with `written None`, the stored state is not changed by the error path, and the retry reports written False or True accordingly;
  * definite refusal (401, 403, 404, 400) raises `BlobArchiveError` whose text has no URL, container, SAS or token;
  * unavailable configuration: selector unknown, URL missing or not https, container missing or invalid, token endpoint failure; text path-free, no request sent;
  * name guard: a name outside the record pattern is refused before a request;
  * verify and list: pagination, tampered body, metadata mismatch, wrong name, unregistered policy, unreadable listing (OSError), latest and overdue;
  * a read failure is not reported as an empty archive.
* `test_ranking_publication_runner.py`: Blob `run` publish, already published, uncertain write shows `committed_unconfirmed`, verify, no capacity probe, unreadable listing is `archive_unreadable`, CLI `--blob` with and without configuration.
* `test_ranking_publication_wiring.py`: through `/api/ranking/publish` and `/api/ranking/publication` with the Store's archive replaced by a Blob adapter on the fake: manager-only, written then idempotent, audit chain, concurrent publish, uncertain write 409 with `committed_unconfirmed` and audit, retry sound, definite refusal 503 path-free with no audit of success, unavailable configuration 503 path-free, status verify problem on a tampered blob.
* Red: run before any source edit. The new module fails on import; the runner and wiring additions fail on behaviour. Record counts.

## P2 Core adapter and dispatch

* `ranking_archive_blob.py` (about 150 lines): `BlobArchiveError(OSError)` with a short `reason`; `BlobArchiveUncertain(OSError)`; `BlobRankingArchive(AzureBlobDocumentStore)` with `create(name, data, meta) -> bool`, `read(name) -> (bytes, meta)` and `names() -> list[str]`; `open_ranking_archive(env, transport)` returning the adapter, or None when the selector is unset, or raising `BlobArchiveError` for an unknown selector or invalid configuration. Never include URL, container or credentials in messages; token and listing failures use fixed text.
* `ranking_publication.py`: `ArchiveWriteUncertainError`; `DurabilityUnconfirmedError` message becomes a class attribute so the subclass can differ; `_existing` split into a shared judge so file and Blob use one validation; `publish`, `verify` and `overdue` dispatch on the archive object; the folder code path is byte-for-byte behaviour compatible, existing tests unchanged.

## P3 Adapters

* `Store._ranking_archive()` returns the Blob adapter when selected, else the folder. `ranking_publication_status` opens the archive inside its error handling and words a Blob read failure as the ranking archive, not a folder. `publish_ranking_snapshot` audits an uncertain write without saying the record was written, and words the 503 for Blob without the hard-link text.
* API server: 409 text chosen by exception type; outcome stays `committed_unconfirmed`.
* Runner: `--blob` mutually exclusive with `--archive`; Blob skips `_free_bytes` and `os.path.exists`; uncertain write text.
* Docstrings and `src/core/README.md`: Blob selection, variables, local adapter limits, what is not proved.

## P4 Static checks

`ruff check` and `ruff format --check` on changed files; `mypy` using `src/core/pyproject.toml`; add the new test module to the existing relaxed override lists only if mypy requires it.

## P5 Records

Changes record with actual commands, exits, counts, skips, red and green; one Review after implementation; commit with the privacy email and trailer; coordinator handoff file.
