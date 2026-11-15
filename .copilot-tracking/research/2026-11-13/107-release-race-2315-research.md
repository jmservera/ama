<!-- markdownlint-disable-file -->
# Research: Issue #107 release-record binding, serving-version attestation and race evidence

* Task: `107-release-race-2315`, branch `feat/demo-107-release-attest-race-2315`, base `origin/main` `3033dc9c21e57c7f86eca3882fffaf7e9a025033`
* Mode: automatic (single non-interactive pass), Research disposition: `executed`
* Planning Readiness: `Ready`

## Scope

Three local software/SQL RAI bullets of #107:

* C-A: persist a release record binding task/purpose, provider/endpoint/deployment/actual serving-model version, prompt/policy/data/provenance hashes, frozen evaluation summary, consumption/budget/alert configuration, named human approvals, scope, expiry and revocation.
* C-B: authoritative serving-version attestation; unexpected returned versions quarantine proposals and trip a visible fallback without promoting unapproved responses.
* C-C: independent SQL connection/worker and race tests for material mismatches, revocation and restart; old images/restarts cannot restore revoked enablement without a new human release record.

Out of scope: live Azure delivered-build acceptance (4th RAI bullet), `infra/`, `monitoring_coverage.py`, `ranking_publish.py`, any named approver or real model call.

## Evidence read

* `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md` (context only).
* `gh issue view 107 --comments`: closure audit 2026-10-31 keeps C6/C8/C10 unmet; PR #1255 and later process-race preparation added sequential and OS-process SQL cases (`ProcessRaces`, `MssqlUnleasedRevocation`); response `model` is "not attestation".
* Source: `src/core/src/zava_forward/core/assistant_release.py`, `rai_release.py`, `ai_registry.py`, `assistants.py` (`complete`, lines ~1720-1790), `ai.py` (`ModelMismatch`), tests `src/api/tests/test_assistant_release.py`, `src/core/tests/test_rai_release.py`, `release_support.py`.

## Findings

1. Record today binds `BOUND` (registry, schema, provider, endpoint, deployment, prompt, policy, data, provenance, permission, model, task contract, evaluation versions), `serving_model`, approver, `expires`, residual risk, evidence list, status (active/suspended/revoked). It does NOT persist: a frozen evaluation summary (only `evaluation_decision: Pass` plus references), consumption/budget/alert configuration, or the task `scope` statement (registry carries `scope`, the record does not).
2. `complete()` compares envelope `model` to the record's `serving_model`. A mismatch quarantines and suspends the release but `serving_attestation` is stored only on mismatch, has no expected value, no outcome vocabulary beyond `mismatch`, no durable event naming the attestation, and no explicit `fallback` field. A matching result leaves no attestation trace, so authoritative evidence of what was checked is absent.
3. Race coverage exists for sequential independent connections, threaded workers after revocation and OS processes (finite allowance, restart). Missing: revocation committed by a second connection *while the provider call is in flight* (generation blocked), followed by restart and proof that only a new human release record re-enables; and an attestation mismatch that survives restart and cannot be undone by re-installing an old binding.
4. Existing fixtures (`release_support.fixture`, `test_assistant_release.body`, `test_rai_release`) construct records without the new fields; they must be extended together with the validator. Old stored records without the new fields fail closed (documented behaviour for extended contracts, `src/core/README.md` "Task-bound RAI release records").
5. No schema change is needed: body is JSON in `assistant_releases.body`.

## Selected approach

* `rai_release`: add pure validators `scope`, `evaluation_summary` (frozen, digest-bound to the evidence list), `consumption` (max calls, max tokens, alert threshold, alert contact); add `attest_serving(record, returned)` returning `matched`, `mismatch`, `unattested`; scope joins the `intended_use` change trigger.
* `assistant_release.record`: require and persist the new fields.
* `assistants.complete`: always persist the attestation (expected, returned, outcome, time); on non-match quarantine, suspend, emit a `serving-attestation` event and set an explicit `fallback` (manual route, release suspended) surfaced by `detail`.
* Tests: unit tests in `src/core/tests/test_rai_release.py`; SQL/race tests in `src/api/tests/test_assistant_release.py` (SQLite default, MSSQL class inherited when selected), including in-flight concurrent revocation, restart and new-record re-enable.

## Risks

* Stricter record contract invalidates older stored records (intended, fail closed).
* Response `model` remains the only authoritative signal the provider returns; it is recorded and enforced as the attestation, but no independent control-plane attestation is claimed. #107 criteria stay unticked.
