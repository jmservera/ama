# Issue 185 review, round 2 (2026-11-03)

Execution: single self-review. Outcome: conformant for the slice; open items routed.

## Acceptance criteria

* Approach decided and recorded with credential owner: still proposed, owner confirmation pending. Unmet.
* One device identity per stock home: proven (PR #647).
* Credentials issued and stored without appearing in source or logs: proven only against fakes, now including rotation. Live Key Vault unmet.
* Teardown removes all simulated identities: proven against fakes, including after rotation. Live teardown unmet.

## Findings

* Low: process-local run lock; live adapters need an atomic reservation.
* Low: rotation is not yet wired to a CLI or orchestrator entry.

* Medium (PR #849 review, corrected 2026-11-03): after ROTATION_REVOKE_FAILED or ROTATION_INCOMPLETE the new manifest was lost, so the caller could not name the live new credentials. Corrected with documented scope: `DeviceIdentityError.new_manifest` carries the non-secret new references; the supported recovery is teardown through it. Retrying `rotate` after such a failure is unsupported and fails with ROTATION_STATE_MISMATCH (pinned by a test, no secret leaked). The `assert result is not None` guards became explicit errors. Core device identity tests pass.

## Follow-ups (ranked)

1. Owner confirmation of the decision (blocks live work).
2. Live Registry and Key Vault adapters.
3. CLI/orchestrator entry.

PR uses Refs #185.
