# Issue 185 review (2026-11-01)

Execution: single self-review after implementation. Outcome: conformant for the slice, with open items routed as follow-ups.

## Acceptance criteria

* Approach decided and recorded with owner: recorded as proposed, owner confirmation pending. Unproven.
* One device identity per stock home: proven in code and tests (already checked).
* Credentials issued/stored without source/log exposure: proven only against fakes (protocol boundary, secret-free repr and errors). Live Key Vault unproven.
* Teardown removes all simulated identities: proven against fake registry with verification; no live teardown. Unproven live.

## Findings

* Low: the real Azure Registry and Key Vault adapters are not written (follow-up, needs owner approval and live access).
* Low: adapters must make `delete(device_id, run_id)` idempotent and run-conditional.

## Follow-ups (ranked)

1. Owner confirmation of the decision and live adapters (value, evidence: ADR 0003 open items).
2. Wire a CLI/orchestrator entry using the module.

Decision: PR uses Refs, not a closing keyword.

## Addendum: Copilot PR review round 1

Four valid findings (rollback scope, stale-manifest ownership, secret-bearing adapter errors, rollback verification references) were fixed in code with regression tests. The original Review outcome above is unchanged; the Registry adapter contract now requires `run_of` and run-conditional atomic `delete`.

## Addendum: Copilot PR review round 2

Two valid findings (credential stored before `issue()` raised; overlapping provision/teardown revoking a newer run's credential) were fixed with run-scoped immutable credential references and regression tests. The original Review outcome is unchanged; the CredentialStore adapter contract now requires per-issuance references and `run_references(run_id)`.
