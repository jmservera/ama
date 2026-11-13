# Research: issue 107 material-binding change then fresh-process re-admission (C10 composite gap)

Date: 2026-11-12. Mode: LIGHT, local TEST-ONLY. Research disposition: executed. Planning Readiness: Ready.

## Start state (exact, recorded before any edit)

* Worktree `/home/azureuser/source/ama-demo-wt/issue-107-process-binding-1112`, branch `test/process-material-binding-107-1112`, HEAD `43b2187b918206666c63cb25d8b338be09791118`, tree `67cbe8ede92d4f9f02ac3a3f71d0de06872f6b55`, clean.
* Declared parent and future PR target `feat/demo-ai-integration-1112` resolves to the identical commit and tree (stacked topic, deliberate). Fetched `origin/main` is `4f40e7ea8237e18f13ff962857a4c4f3bdfa974c`, tree `e7360069216dc0a8bc6edee077c9454c691cde04`; `HEAD` is an ancestor of it (merge base equals HEAD). Integration to main goes through issue 104.
* Overlap checks: no open PR touches `test_assistant_release.py`, `assistant_process_worker.py`, `release_support.py`, `assistants.py` or `assistant_release.py`; no sibling worktree (including `issue-157-memory-evidence-1112`) has uncommitted or branch changes to those files. No overlap with the 82 funding or 153 employee error-copy work.

## Prior 107 scope and correction history (reconciled from the issue comments and git)

* Merged scoped test increments: 1253 (retain revoked release and finite allowance across workers), 1255 (independent SQL connection release denial before claim), 1268 (OS-process finite-allowance race and revocation/restart), 1271 (restarted partially used allowance clamp). Earlier slices 863, 915, 1095 and the 1166 status record are unrelated source/doc scopes.
* No record found of an exhausted per-candidate scoped boundary, a closed-unmerged correction candidate or a rejected duplicate for this behaviour. The last 107 comment (after 1268) states the composite criterion remains Partial because "old-image/material-mismatch/fresh restarted admission" is not proven. This is therefore genuinely distinct initial test coverage under the general owner backlog approval, not a correction of a spent candidate. No fresh issue-wide count is invented and no spent candidate is reset.

## Exact current tests (read, not assumed)

* Same-process material mismatch: `Release.test_material_mismatch_denies_but_routine_case_edit_only_stales` (patches `RULE_VERSION`, `SYSTEM`, `PROVENANCE` and roles in the test process; asserts denial, no revival on restoring the binding), `TaskReleaseRecord.test_each_binding_mismatch_denies_reactive_and_proactive_with_no_calls` (mutates stored record fields) and `test_endpoint_rollback_does_not_revive_historical_release`.
* Process tests (`ProcessRaces`, run by the SQLite proxy class and the maintained MSSQL selector `MssqlUnleasedRevocation`): finite-allowance race, restarted partial clamp, and revocation (`fx-<capability>` revoked by an operator) then restart. None changes the runtime binding of a worker process. This is the confirmed gap: a worker whose constructed runtime binding differs from the stored release, followed by a fresh process with the original binding.
* Controls 1255/1268/1271 are not duplicated: operator-issued revocation is already covered; this work covers revocation created by material-change invalidation by a different-binding worker and its durability.

## Real semantics (source contracts)

* `assistants.runtime_binding(capability, ai)` is evaluated at call time from module state: `RULE_VERSION`, `RULES[cap]`, `REGISTRY[cap]["purpose"]`/`roles`/`categories`, `SYSTEM`, `PROVENANCE`.
* `Assistants.claim` runs release admission; `assistant_release.assessment` calls `invalidate_changed` for non-legacy tasks: an active record whose bound fields differ in a material-change trigger (`rai_release.TRIGGER_KEYS`: model, prompt, policy, data, permissions, evidence) is persistently revoked by the system with an `invalidated` cause, unless `READ_ONLY`. A later process with the original binding sees a revoked record and cannot restore it (`record` creates a fresh id only with a named approver).
* `RULES[cap]` changes only `policy_version`, `REGISTRY[cap]["purpose"]` only `prompt_version`, `REGISTRY[cap]["roles"]` only `permission_version`, each for that capability. `SYSTEM`/`RULE_VERSION`/`PROVENANCE` are global (all capabilities) so they cannot leave an unrelated capability matching; they are not used.
* Release fixtures are `fx-<capability>` rows from `release_support.install`; the test base class deletes non-fixture releases.

## Design constraint

A constants patch in a worker is a constructed runtime-binding variation, not an old-container image or a real serving-model change. It must be named and documented so, and no claim of old-image semantics is made.

## Limits

Constructed fixtures and a fake provider only. No real provider, activation, deployment, secrets, Azure or SQL acceptance. SQLite results are a proxy. The MSSQL inherited class needs the disposable local SQL service; this session has no ZF_TEST_MSSQL and runs none, so the MSSQL methods are not executed and no SQL pass is claimed. Whole 107/104 stay open.
