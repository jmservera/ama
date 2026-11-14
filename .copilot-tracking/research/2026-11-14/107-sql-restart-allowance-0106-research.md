<!-- markdownlint-disable-file -->
# Research: Issue #107 criterion 8, restart and independent-connection non-replenishment

* Research disposition: `executed`. Planning Readiness: `Ready`.
* Branch: `test/demo-107-sql-restart-allowance-0106`, stacked on `feat/demo-107-release-attest-race-2315` at `f73a48f34` (PR #1594).
* Objective: independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances.

## Evidence

* `src/core/src/zava_forward/core/assistants.py`: suspension is read per call from `meta.continuity` on the caller's own SQL connection (`continuity`, `suspended`, `dispatch_hold`); release admission is read from `assistant_releases` on the caller's connection (`admission`, `rel.assessment`). `claim` and `complete` re-check both. No process-level cache of either state.
* Allowance: `_reserve` stores `calls`, `tokens`, `expires`, `used_calls`, `reserved_tokens` in `assistant_allowance`, keyed by `Limits.pool = digest(ZF_ASSIST_AUTHORITY)`. Each reserve re-applies `min(stored, configured)` for calls, tokens and expiry, so a restart with larger env values cannot raise the stored ceiling and `used_calls` is never reset.
* `src/core/src/zava_forward/core/assistant_release.py` and `rai_release.py`: a material change (`changed_triggers`, `missing_binding`) revokes the active record on read; `change` refuses reactivation of a revoked record; `record` is the only path that creates an active record.
* Existing coverage (parent `f73a48f34` and earlier): `test_assistant_release.py` has revocation on a second connection, racing workers plus restart, blocked-generation revocation, attestation suspension surviving restart, and OS-process `ProcessRaces` for revocation, partially used allowance and prompt/policy/permission changes. Not covered: SQL continuity suspension seen from another connection at claim, dispatch and completion; stored token ceiling and concurrent last-call race over fresh stores; non-refund of consumption after revoke plus a new record; scope and serving-model mismatch as separate worker variations; old-image reactivation attempt.
* Environment finding: editable installs point at `/home/azureuser/source/ama`; tests need `PYTHONPATH` set to this worktree's `src/*/src` so the stacked code is exercised.

## Gap analysis

* A probe test (`calls=1` spent, restart with a different `ZF_ASSIST_AUTHORITY`) executes: the pool is keyed on the operator authority string, so naming a new authority creates a fresh pool. A restart or default reload with the same authority cannot refill (tested). Whether an arbitrary new authority string should refill is an unresolved design and authorisation-boundary question (the independent critique rated it blocking); it is not closed here, no production change is made, and it is routed as the first follow-up.
* No persistence gap was found for revocation, suspension or consumed allowance across `SqlStore` re-instantiation for an unchanged authority. Production files stay untouched. Claim limited accordingly: non-replenishment is proven for restart, reload and larger env, not for a changed authority string.

## Planning Readiness

Ready: add one new test module and register it in the existing typed-test mypy override.
