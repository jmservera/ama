<!-- markdownlint-disable-file -->
# Review: Issue #107 release record, serving attestation, race tests

* Review execution: `executed` once, post-implementation. Outcome: `conformant with qualifications` (no material open finding; qualifications below are routed follow-ups).
* Tier: Focused (pip venv `/tmp/venv-107-2315`, removed after validation; no `uv`). Ruff 0.17.1, mypy 2.4.0 (pinned in `src/core/pyproject.toml`).
* Plan: [plan](../../plans/2026-11-13/107-release-race-2315-plan.md); changes: [changes](../../changes/2026-11-13/107-release-race-2315-changes.md)

## Bullet assessment

* Release record binding: now also persists `scope`, frozen `evaluation_summary` (digest-bound to evidence) and `consumption` budget/alert configuration, beside the existing provider/endpoint/deployment/serving model, prompt/policy/data/provenance/permission versions, approver, expiry and status. Tests: `test_rai_release`, `TaskReleaseRecord.test_recorded_release_persists_the_full_binding_and_revocation`, refusal test.
* Serving attestation: outcome always stored; non-match quarantines, suspends the release, writes events and sets a visible `fallback`. Honest limit: the provider-returned `model` is the only signal; no independent control-plane attestation is claimed.
* Race/restart: new test revokes through a second SQL connection while generation is blocked in a worker thread, then restarts and shows only a new human record re-enables; attestation suspension survives restart. Existing OS-process cases (`ProcessRaces`) unchanged. MSSQL variants inherit through `MssqlUnleasedRevocation` but were NOT executed here (no disposable SQL Server); SQLite only.

## Validation actually run

* `src/core` `test_rai_release test_scenario_manifest test_needs_inventory`: 28 tests OK. Also `test_assistants_identity test_ai_consumption test_ai_dispatch_marker`: with the above 78 OK.
* `src/api` `test_assistant_release test_assistants test_ai_consumption_api`: OK after fixing two existing assertions that pinned the old attestation shape (`test_ai_consumption_api`, now 40 OK); `test_assistant_release` 65 OK (7 MSSQL skips).
* `src/agents` full discover: exit 0.
* `src/core` full discover (3249 tests): 51 failures/errors, none in touched areas: 50 in `test_device_registry_azure` (missing optional `azure-iot-hub` dev dependency) and 1 `test_priority_order.SqliteLegacyEdges` "database is locked" under parallel load, which passes alone (8 OK).
* `src/api` full discover (3007 tests, first run before fixing the pinned assertions): 10 import errors (missing `playwright`) and the 9 pinned-shape failures, since fixed and rerun green.
* `ruff check`, `ruff format --check`: clean in `src/core`, `src/agents`, `src/api`. `mypy`: clean in `src/core` (300 files) and `src/agents` (54); `src/api` mypy reports 66 pre-existing missing-stub errors (playwright and others), not run as a gate.

## Findings and routing

* Follow-up 1: run `MssqlUnleasedRevocation` on a disposable SQL Server under the full tier.
* Follow-up 2: independent control-plane serving-version attestation and a named approver (OQ-017) remain unmet; live Azure acceptance (4th bullet) not claimed.
* Scope note: no #107 criterion is ticked; independent exact-head review and hosted CI still required. Focused tier: not a full gate receipt.
