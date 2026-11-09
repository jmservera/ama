# Issue 136 ranking archive Blob Bicep wiring changes (2026-11-09)

Refs #136, Refs #1258. Plan: `.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-plan.md`; details: `.copilot-tracking/details/2026-11-09-ranking-blob-bicep-136-details.md`. Source definitions only; nothing deployed, no Azure call.

## Changes

| Path | Change |
| --- | --- |
| `infra/modules/storage.bicep` | Params `enableRankingArchive` (false) and `rankingArchiveImmutabilityDays` (0, min 0); conditional private `ranking-archive` container (`publicAccess` None); conditional unlocked immutability policy only when enabled and days > 0 (`allowProtectedAppendWrites` false); output `rankingArchiveContainer` (empty when off). Existing container array and two policies untouched |
| `infra/modules/containerapps.bicep` | Param `rankingArchiveContainer` (empty); API env `ZF_RANKING_ARCHIVE=azure-blob` and `ZF_RANKING_BLOB_CONTAINER` only when non-empty. Existing `ZF_BLOB_ACCOUNT_URL`/`ZF_BLOB_CLIENT_ID` reused; no SAS, key or secret |
| `infra/modules/guard.bicep`, `infra/main.bicep` | Params `enableRankingArchiveBlob` (false), `rankingArchiveImmutabilityDays` (0); named guard `pilotRankingArchiveRequiresConfiguredRetention` (pilot + flag requires days > 0; checks configuration only); pass-through to storage and containerapps. No role assignment change |
| `infra/main.test.bicepparam` | Explicit `false` and `0` with comments |
| `infra/tests/test_bicep_policy.py` | `assert_retention_controls` counts only the two unconditional policies; new tests for flag-off identity, private container, optional policy, compiled output-to-env chain, provider constant match (parsed from `ranking_archive_blob.py`), no key/SAS/connection string, and the pilot guard |
| `infra/README.md` | Coverage register row and section "Ranking archive Blob wiring" |

## Critique dispositions applied

PC-001 guard.bicep plumbing, PC-002 compiled-chain test, PC-003 guard renamed to configured retention, PC-004 ledger-digests pattern. No divergence from plan and no amendment needed.

## Validation (DEMO tier; exact commands run from `infra/`, all exit 0)

| Command | Result |
| --- | --- |
| baseline before edit: `python3 -m unittest tests.test_bicep_policy` | 57 OK |
| `az bicep build --file main.bicep --stdout` | exit 0 |
| `az bicep lint --file main.bicep` | exit 0 |
| `az bicep build-params` for `main.bicepparam`, `main.test.bicepparam`, `main.pilot.example.bicepparam` | exit 0 each |
| `python3 -m unittest tests.test_bicep_policy tests.test_identity_rbac tests.test_secret_lifecycle` | 90 OK (59 policy incl. 2 new) |
| `src/core`: `PYTHONPATH=src python3 -m unittest discover -s tests -p test_ranking_archive_blob.py` | 23 OK (provider config contract, unchanged) |
| `ruff check infra/tests/test_bicep_policy.py` | clean after fixing 3 findings in new lines; `ruff format --check` was already failing at HEAD for this file, left alone |

Skipped by tier: full `rpi-checks`, SQL, browser, images, scanners, `az deployment`/what-if, emulator, whole-infra sweep (`test_deploy` and others not run). Missing prerequisites: none for the selected tier.

## Not proved

Provisioning, role grant, WORM enforcement or lock, approved retention duration (unset by design), migration of existing folder records (Blob starts empty), real-account or emulator behaviour, deployment approval, demo runtime. Residual: the existing API account-scope Storage Blob Data Contributor role also allows delete; a container-scoped assignment is a later platform decision. #136 and #1258 acceptance criteria are not ticked; this child is `Refs` only.
