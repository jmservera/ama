# Research: #79 criterion 4, scheduled and retained ranking snapshot publication

Date: 2026-11-13. Base: origin/main ee068a4b5. Tier: focused. Refs #79. Disposition: executed.

## Question

Criterion 4 of #79: "Ranking snapshot publication is scheduled and retained (ADR 0002 deviation)". What on `main` already proves it, and what exact gap remains in software or infrastructure?

## Evidence on main

| Area | Finding | Source |
| --- | --- | --- |
| Archive and verify | Create-only, hash-verified dated records, `schedule`/`publish`/`verify`, idempotent, never overwrites or purges | `src/core/src/zava_forward/core/ranking_publication.py` |
| Runner | `run()` and CLI; the case source is an explicit local JSON file (`--cases`), `--today` is an input | `ranking_publication_runner.py` |
| Blob store | Owner-selected Blob JSON adapter (create-only `If-None-Match: *`, no overwrite or delete, mock REST fixture `ranking_blob_fixture`), env selector `ZF_RANKING_ARCHIVE=azure-blob` | `ranking_archive_blob.py`, `tests/test_ranking_archive_blob.py` |
| Dependencies | The adapter reuses `AzureBlobDocumentStore` REST and managed identity. No `azure-storage-blob` is declared in any `src/*/pyproject.toml`; none is needed | `documents.py` |
| Retention | Private `ranking-archive` container with an optional, unlocked, owner-set immutability policy (`rankingArchiveImmutabilityDays`, default 0); pilot guard requires a positive duration | `infra/modules/storage.bicep`, `guard.bicep` |
| API | Manager-only manual publish and status endpoints use the Blob archive when the selector is set | `store.py`, `server.py` |
| Schedule | `PROPOSED_SCHEDULE` and `SCHEDULE` are prose contracts only. `infra/README.md` states "no job is deployed for it" | `infra/README.md` ranking archive section |
| ADR 0002 | Status row: "no scheduled publish step; named policy owner and sign-off still open" | `docs/adrs/0002-pilot-readiness-architecture.md` line 1077 |
| Policy | Current policy is an unsigned draft, so `publish` refuses with `approval_missing` unless `--exercise` | `ranking.py`, runner `run()` |

## Gap

Nothing triggers publication. The runner needs a local case file and an operator, while production data is in the store (Azure SQL). Existing scheduled jobs (`ledgerVerify` runs `orchestrator.digest_blob`) show the pattern: an orchestrator module that opens the store from the environment, a Container Apps Schedule job, an alert marker line and a non-zero exit on failure.

Gap items:

1. An orchestrator entry point that reads open cases and `as_of` from the configured store, calls the runner with the run date and the Blob archive, and exits non-zero unless the record is published or already published.
2. A Container Apps `Schedule` job, created only when the ranking Blob archive is enabled, that runs the entry point with the store and Blob settings.
3. Tests that fail before the change, plus a compiled-template test for the job.
4. Documentation correction (infra README, orchestrator README, ADR status row) that keeps criterion 3 open.

## Boundaries

* Criterion 3 stays open: the policy is an unsigned draft and the job must refuse it (no `--exercise` or sign-off bypass). Until a named owner signs a new policy version the scheduled job exits non-zero with a blocked marker. That is the honest state, not a defect.
* Retention duration is not approved. The job adds no retention value; immutability remains the owner-set, unlocked `rankingArchiveImmutabilityDays`. No claim of locked WORM.
* No UI copy is touched, so `test_content_standard.py` is unaffected.
* No Azure call, deployment or role grant. The `ledgerVerify` identity (`api`) already holds account-level Storage Blob Data Contributor.

## Planning readiness

Ready.
