# Issue 136 ranking archive Blob Bicep wiring plan (2026-11-09)

Refs #136, Refs #1258. Research: `.copilot-tracking/research/2026-11-09-ranking-blob-bicep-136-research.md` (Ready). Details: `.copilot-tracking/details/2026-11-09-ranking-blob-bicep-136-details.md`. Tier: DEMO targeted (owner-selected 2026-11-09). Local only: no push, PR, issue, board or merge; no Azure call.

## Objective

Add the direct missing source wiring for the #1258 Blob ranking archive: a private container, an opt-in flag, the exact consumer environment variables on the API app, and an explicit unset-by-default immutability prerequisite. Source only. Default and production behaviour, capacity and budget ceilings are unchanged.

## Decisions (from research)

* D1 Option B: opt-in `enableRankingArchiveBlob` (default `false`) in `main.bicep`; `storage.bicep` gets `enableRankingArchive` and `rankingArchiveImmutabilityDays` (default `0`, `@minValue(0)`); `containerapps.bicep` gets `rankingArchiveContainer` (default empty).
* D2 Container `ranking-archive`, `publicAccess: 'None'`, created by a separate conditional resource so the existing indexed container array and its two policies are untouched.
* D3 Immutability: a conditional unlocked time-based policy only when the flag is on AND days > 0 (same pattern as `ledger-digests`, `allowProtectedAppendWrites: false`). Days `0` means "no policy; manual prerequisite". No duration default; nothing claims WORM or durable release when unset or unlocked. Locking stays an owner action.
* D4 API env only when the container name is non-empty: `ZF_RANKING_ARCHIVE=azure-blob`, `ZF_RANKING_BLOB_CONTAINER=ranking-archive`. The existing `ZF_BLOB_ACCOUNT_URL` and `ZF_BLOB_CLIENT_ID` are reused. No `ZF_BLOB_SAS`, key, connection string or secret.
* D5 No role change. The existing API account-scope Storage Blob Data Contributor assignment covers Put/Get/List. The over-breadth (delete) is recorded as a residual and routed, not changed.
* D6 Guard `pilotRankingArchiveRequiresConfiguredRetention` (declared in `modules/guard.bicep` with its constrained parameter and `checked` output entry, passed from `main.bicep`): pilot with the flag on requires days > 0. It checks only that a duration is configured; it decides no duration and verifies no approval or lock.
* D7 Explicit `false`/`0` values in `main.test.bicepparam` with comments; dev and pilot example files keep defaults.
* D8 No migration of existing folder records; Blob starts empty (restated in docs).

## Phases

- [x] Phase 1 Research (done, Ready)
- [x] Phase 2 Plan, details, one critique (Revise, PC-001..PC-004 applied)
- [ ] Phase 3 Implement: storage.bicep, containerapps.bicep, main.bicep, param file, tests, infra/README section and register row
- [ ] Phase 4 Validate (DEMO tier): `az bicep build` of `main.bicep`; lint via the existing policy test; `python3 -m unittest tests.test_bicep_policy` in `infra`; an in-test consumer contract check that the compiled env names equal the provider constants parsed from `ranking_archive_blob.py`; `tests.test_identity_rbac` (role guard unchanged); ruff on touched Python if the repo config applies
- [ ] Phase 5 Review once (independent read-only), record outcome, route findings
- [ ] Phase 6 Commit clean freeze with privacy email and Copilot trailer; handoff file

## Acceptance for this child (not epic criteria)

* A1 flag false: compiled storage module has no ranking container or policy, API env has no ranking variables, existing two policies and container order unchanged.
* A2 flag true, days 0: private container exists, no policy, env present, no key/SAS/connection string/public access change.
* A3 flag true, days N>0: one unlocked policy on `ranking-archive` with N days and no append writes.
* A4 pilot + flag + days 0 fails the named guard `pilotRankingArchiveRequiresConfiguredRetention`; test parameter files and guard matrix unchanged otherwise.
* A5 compiled env names equal the provider contract constants.
* A6 docs: README section states source-only, unset prerequisite, residuals, no migration.

## Validation boundary

Not run: full rpi-checks, SQL, browser, images, scanners, deployment, what-if, emulator. Not proved: provisioning, role grant, WORM enforcement, immutability lock, folder-record migration, Azure or demo runtime, deploy approval.

## Critique dispositions

See `.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-critique.md`. PC-001 (guard.bicep plumbing) is applied in D6 and Phase 3; PC-002 adds a compiled-chain test (details test 7); PC-003 renames the guard; PC-004 corrects the cited pattern to ledger-digests.
