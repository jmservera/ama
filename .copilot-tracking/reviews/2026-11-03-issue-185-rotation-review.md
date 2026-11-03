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

* Medium (PR #849 review, corrected 2026-11-03): after ROTATION_REVOKE_FAILED or ROTATION_INCOMPLETE the new manifest was lost, so a retry failed with ROTATION_STATE_MISMATCH and the caller's old manifest could not name the live new credentials. Corrected: `DeviceIdentityError.new_manifest` now carries the non-secret new references, and the `assert result is not None` guards became explicit errors. A test proves teardown through the recovered manifest leaves no credentials or devices, with no secret in messages. Core device identity tests: 38 pass.

## Follow-ups (ranked)

1. Owner confirmation of the decision (blocks live work).
2. Live Registry and Key Vault adapters.
3. CLI/orchestrator entry.

PR uses Refs #185.
