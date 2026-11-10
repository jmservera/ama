<!-- markdownlint-disable-file -->
# Research: issue 1288 H2 matching-context restart observation

Readback `date -u` 2026-11-10T00:20Z. Verification only. E11 succeeded; E12 and E13 are unused and are not consumed. No source, test, schema or shared-doc change. Original H0 (FAIL, inconclusive) and H1 (FAIL, confounded) records stay immutable.

## Starting evidence (read from the H1 handoff and raw snapshot)

* H1 raw: `logs-h1-executed-1109/sql-run/h1.json`, handoff `handoff-1288-h1-executed-1109.md`, harness `merged-sql-proof-1109/harness_h1_restart_context.py` (all external, unchanged).
* First service: flag `review-suggested`, actionable. Variant A (default `Ai`, no release context): `not-current`, `display_state` `release-denied`, `current_release` null. Cited IDs, ID/reading pairs, role projection, task state and task body hash were equal to the first service.
* After A the row `assistant_releases.fx-quality-evidence` went from active revision 1 to revoked revision 2. Which call revoked it (construction, `detail`, `release_reference`, `sensors`) is not established.
* Variant B ran AFTER A, so it observed `release-denied` for a release already revoked. B is confounded and does not discriminate. No source bug and no B failure may be claimed from H1.

## What H2 must establish

* Matching-context independent provider, fresh SQL store and service, constructed FIRST (no default-`Ai` call beforehand) on a NEW disposable database, read the same persisted flag.
* Hypothesis H2: with an independent provider bound to the same synthetic release context (same `runtime_binding` digest, release active before construction), the fresh service reports flag `review-suggested`, actionable, with the same cited IDs, ID pairs, role projection, task state and task body hash as the first service, and the `fx-quality-evidence` row stays active revision 1.
* Contrary outcomes are recorded as observed (a revoke or `not-current` under a matching context would be a finding for the owner, not something to repair here).

## Existing seams (read only)

* `src/core/tests/release_support.py::install` sets `ai.model_version`, `model_version_strong`, `ai.release = store.release_context`, then deletes and recreates `fx-*` rows with `revision` 1. It is used once by the first service (`ready()` via `mock()`), and MUST NOT be used for a restart variant.
* `MssqlFixture.open_store` returns a new `MssqlStore` (new connections, default `Ai`); a provider is attached by `store.ai = provider; provider.release = store.release_context`, exactly what `install` does for the first store. A second store, provider and service are therefore independent of the first service's objects and connections.
* `Assistants.detail`, `release_reference` and `sensors` are the observation calls from H1. `runtime_binding(task, ai)` gives the binding digest.

## Main advance

* `origin/main` is `ddeebd01694ddb46b456451d9ac6390347e51aaa` (accounting PR 1339 merged). Product files changed since the pinned a859 base: `src/agents/README.md`, `src/agents/src/zava_forward/agents/chat.py`, `src/core/src/zava_forward/core/ai.py`, `src/core/src/zava_forward/core/resident_decisions.py` plus their tests. Quality sensor and assistants modules are not in the list. This is the ordinary-merge input after the plan. H0 and H1 stay historical a859 observations; H2 on the new main does not attribute their cause.

## Limits

* Provider is the existing synthetic `CapturingProvider`; TLS peer stub only; 0 real provider, model, cloud calls; stub-peer bytes expected 0.
* Hosted CI runs no Quality MSSQL class; slot checks are in-process only (carried from H1).
* No resident, QA, release-owner or financial approval is invented. A stub is not an actual model or release approval.
