# Issue 136 ranking archive Blob Bicep wiring research (2026-11-09)

Refs #136, Refs #1258. Read-only research before any plan or source edit. Task `ranking-blob-bicep-136`, Research disposition `executed`, Planning Readiness `Ready`.

## Identities (qualified honestly)

* Worktree `issue-136-ranking-blob`, branch `feat/ranking-blob-bicep-136-1109`, seed and HEAD at start `f724f4bcaac1c5c5b9c5825ffd1cf253f1796b37` (tree `491a2dcfdd8bf24056ef86ba0158b896d0904cab`), clean. Declared child PR target: `fix/ranking-archive-ancestor-durability` (#1258), not `main`.
* Pinned parent source already contains `main` `06e3f2f456ab` (merged in the parent at `c62611379`). Fetched `origin/main` is `daf45a46ca85b93cfac510ef6f8b2d685dec5136`: one commit (`docs: add blind judging and execution flows to the paper (#1307)`), whose diff touches no `infra/` or `src/` path (`git diff HEAD...origin/main --stat -- infra src` is empty). It is unrelated, is not merged here and is not claimed as integrated. The parent is still moving (C5 listing correction); nothing is propagated from it. Final integration waits for the parent freeze and review.
* Dependency is the #1258 Blob contract, not a parent hierarchy. #136 is already partially delivered by earlier records; this child is `Refs #136`, `Refs #1258`, no closing keyword, no epic criteria ticked.

## Authority and scope

* Owner decision on #1258 (2026-11-08): Blob JSON for ranking persistence. The owner prioritises a fully working demo and Bicep architecture before 16 November. Production legal, compliance and hardening acceptance is deferred, not satisfied.
* Coordinator brief (2026-11-09): add only the missing direct source wiring named by the #1258 handoff ("Blob container, immutability/WORM policy, role grant, Bicep env vars"). Source definitions only: no Azure calls, deployment, what-if, role grant inference, WORM duration decision, folder-record migration or deletion, or new spend. Demo-targeted validation tier.
* Cycle accounting: this is new direct source wiring, not a review-correction cycle of any #136 record. Earlier #136 correction counts (c1, pm, pmc2, r1, r1c1 records) are retained unchanged and nothing is reset or granted.

## Provider configuration contract (read from source, not guessed)

Source: `src/core/src/zava_forward/core/ranking_archive_blob.py` (`open_ranking_archive`), `store.py` `_ranking_archive`, `ranking_publication_runner.py`, `src/core/README.md` (Blob JSON persistence).

| Variable | Contract | Needed by |
| --- | --- | --- |
| `ZF_RANKING_ARCHIVE` | `azure-blob` selects Blob; empty or `local` selects the dev/test folder; any other value refuses. Blob never falls back to a folder. | Store, API routes, runner `--blob` |
| `ZF_BLOB_ACCOUNT_URL` | Existing variable; same account URL as the document store | same |
| `ZF_RANKING_BLOB_CONTAINER` | Container name; required when Blob is selected | same |
| `ZF_BLOB_CLIENT_ID` | Optional managed identity client id (existing) | same |
| `ZF_BLOB_SAS` | Optional SAS; deliberately NOT wired (no keys or SAS in Bicep) | none |

The adapter can only create (conditional `If-None-Match: *`), read and list blobs: no overwrite, delete or caller-chosen location. It needs Put Blob, Get Blob and List Blobs on one container.

## Existing infrastructure facts

* `infra/modules/storage.bicep`: private account (`allowBlobPublicAccess` false, shared key off, public network `Disabled` unless the development switch, private endpoints for blob and queue). Containers are a fixed array with `publicAccess: 'None'`; `audit-archive` and `ledger-digests` are addressed by index and carry `immutabilityPolicies` (`auditImmutabilityDays`, `ledgerDigestImmutabilityDays`, both default 365, `@minValue(1)`, created unlocked; README states 365 is not an approved legal schedule and locking is an owner action). Account-level versioning, 30-day blob and container soft delete.
* `main.bicep` already assigns the API identity `Storage Blob Data Contributor` on the storage account (a role definition GUID variable, not a new grant) and `containerapps.bicep` already sets `ZF_BLOB_ACCOUNT_URL`, `ZF_BLOB_CLIENT_ID` and `ZF_DOC_STORE=azure-blob` on the API app. The API app is the only deployed consumer of the Store and the ranking routes; the runner is an operator CLI with no deployed job, and `ledgerVerify` is a different consumer.
* No existing Bicep, parameter file or README line mentions the ranking archive.
* Guards: `main.bicep` `parameter-guard` named checks; `test_bicep_policy.py` asserts exactly two immutability policies (`assert_retention_controls`), policy mutation tests, private-endpoint, public-access, no key and parameter example/guard-matrix tests. Baseline run at HEAD before any edit: `python3 -m unittest tests.test_bicep_policy` in `infra`, 57 tests OK.
* Tooling present: `az` with `az bicep build`/`build-params` (Bicep 0.48.1 also on PATH). No cloud call is needed.

## Findings and gaps

* G1. No container exists for the ranking archive. The existing `evidence` container is the document store; reusing it would mix an append-only archive with mutable documents and cannot carry its own immutability policy.
* G2. No env wiring: the API app has no `ZF_RANKING_ARCHIVE` or `ZF_RANKING_BLOB_CONTAINER`, so a deployed API refuses the ranking routes (safe default) and cannot use Blob.
* G3. No role work is needed: the existing API account-scope `Storage Blob Data Contributor` already covers Put/Get/List. Adding or narrowing a role is a tenant authorization change and is out of scope. Residual to record: the role also permits delete; the adapter has no delete, immutability (when configured) and soft delete are the compensating controls, and a container-scoped role (ABAC or container-scope assignment) is a routed follow-up, not done here.
* G4. Approved immutability policy values do not exist for ranking records (the 365-day values are placeholders for audit and digests, "not a legally approved retention schedule"). Therefore the immutability policy must be an explicit manual prerequisite: a duration parameter that defaults to unset (0) creates no policy, and a set value creates an unlocked time-based policy with the existing pattern. No default duration is invented and no output or text may claim WORM or durable release when unset or unlocked.
* G5. Default and production behaviour must not change: a new flag defaults to false; with the flag false the compiled output must keep the container list, policies and API env identical.
* G6. A pilot environment is the only production-like named environment; with the flag on and no approved retention it should refuse rather than silently deploy a non-immutable archive. This only adds a named guard on a new opt-in flag; it decides no duration.

## Options

| Option | Result |
| --- | --- |
| A. Always add container and env to the storage module and API | Changes default and production resources and behaviour; rejected (G5) |
| B. Opt-in flag `enableRankingArchiveBlob` (default false), conditional container, optional unlocked immutability from an unset-by-default duration, API env only when on, pilot guard | Chosen. Smallest change satisfying G1, G2, G4, G5, G6 |
| C. Also add a container-scoped role | Out of scope (G3), needs platform approval |
| D. Pre-set a duration such as 365 | Invents policy (G4); rejected |

## Not proved by this work (carry to every later record)

Source and compiled JSON only: not resource provisioning, role grant, actual WORM enforcement, immutability lock, migration of existing folder records (Blob starts empty), deployment approval, or an emulator or real-account run. Legal, compliance, platform and migration approvals are not inferred.

## Planning Readiness

Ready. Evidence: provider contract above, `storage.bicep`, `main.bicep`, `containerapps.bicep`, `test_bicep_policy.py`, baseline 57 OK, offline Bicep tooling present.
