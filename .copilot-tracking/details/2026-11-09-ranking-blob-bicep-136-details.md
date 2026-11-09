# Issue 136 ranking archive Blob Bicep wiring details (2026-11-09)

Plan: `.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-plan.md`. Refs #136, Refs #1258.

## Phase 3 file-level changes

* `infra/modules/storage.bicep`
  * add `param enableRankingArchive bool = false` and `@minValue(0) param rankingArchiveImmutabilityDays int = 0` with descriptions that say unset means no policy and that the policy is created unlocked.
  * add `resource rankingArchiveContainer ... containers@2024-01-01 = if (enableRankingArchive)` named `ranking-archive`, `publicAccess: 'None'`, parent `blobService`.
  * add `resource rankingArchiveRetention ... immutabilityPolicies@2024-01-01 = if (enableRankingArchive && rankingArchiveImmutabilityDays > 0)` named `default`, parent the container, `immutabilityPeriodSinceCreationInDays`, `allowProtectedAppendWrites: false`.
  * `output rankingArchiveContainer string = enableRankingArchive ? rankingArchiveContainer.name : ''`.
* `infra/modules/containerapps.bicep`: `param rankingArchiveContainer string = ''`; add a conditional env array to the API `concat` (existing style) with the two variables when non-empty.
* `infra/modules/guard.bicep`: add constrained `@minLength(1)` param `pilotRankingArchiveRequiresConfiguredRetention` (description starts the way the generic guard test requires: contains `Empty means`) and its `checked` entry.
* `infra/main.bicep`: params `enableRankingArchiveBlob bool = false`, `rankingArchiveImmutabilityDays int = 0` (`@minValue(0)`); guard check `pilotRankingArchiveRequiresConfiguredRetention`; pass to storage and containerapps (`storage.outputs.rankingArchiveContainer`).
* `infra/main.test.bicepparam`: explicit `false` and `0` with comments.
* `infra/tests/test_bicep_policy.py`: new class or tests (see below); adjust `assert_retention_controls` to count policies unconditioned only (the two existing) and tolerate the conditional ranking policy.
* `infra/README.md`: a "Ranking archive Blob wiring (Refs #136, #1258, 2026-11-09)" section after the coverage register, a register row, a parameter-table entry.

## Tests (new, existing file)

1. Defaults: flag false, days 0; storage module has no `ranking-archive` container resource active (condition references the flag), the two unconditioned policies intact, API env contains ranking variables only under a condition on the non-empty container.
2. Evaluate conditions for flag true/days 0 and flag true/days 30 using the existing `evaluate` helper: container active, policy inactive/active; policy properties (days parameter, no append writes, no `immutabilityPolicy lock` state property).
3. Container `publicAccess` is `None`; no `ZF_BLOB_SAS`, no `listKeys`, no secretRef for the ranking variables.
4. Contract consistency: parse `SELECTOR` and `CONTAINER_VAR` from `src/core/src/zava_forward/core/ranking_archive_blob.py` by regex; assert the compiled API env names equal them and the selector value `azure-blob` is accepted by `open_ranking_archive` source (string compare), and the container value equals the storage output name.
5. Guard: pilot + flag + 0 fails `pilotRankingArchiveRequiresConfiguredRetention`; pilot + flag + days > 0, non-pilot + flag + 0, pilot + no flag pass (via `evaluate`).
6. Role unchanged: the roleAssignments argument set in `main` compiled output is identical in count to before (assert no new role GUID beyond the three known), via the existing identity RBAC style.
7. Compiled chain: parse the compiled `main` template; assert the storage module output `rankingArchiveContainer` is a conditional on `enableRankingArchive` returning the literal container resource name, `main` passes `containerapps.rankingArchiveContainer` from `reference(storage).outputs`, and the API env entries reference that parameter; evaluate off, on/0 and on/30 and check the resulting env values and absence of any policy for off and 0.
