# Demo automatic roster plan

Task: auto-roster-360, Refs #360. Status: implementation ready after one critique.

## Executive Summary

Replace only missing/exact-template roster intake with a fail-closed demo
generator. Read authoritative SQL codes/roles/supplier scopes, select the admin
and seed-shuffle distinct enabled Graph members, show a private-data-free plan,
confirm and atomically persist it, then retain existing reconciliation.

## User Decisions and Requirements

* Owner explicitly requests end-to-end implementation, four RPI artifacts,
  offline validation, commit, push and PR. No Azure writes or live setup.
* Demo only; production profile must override demo/test naming.
* No invented codes, people, roles, supplier names or human approvals.
* Preserve distinct identities; choose the explicitly permitted stop alternative
  on a shortage rather than weaken SQL duplicate safeguards.
* Missing/ambiguous admin asks one plain question; `--admin-upn` resolves it.
* `--yes` accepts roster and SQL confirmations; read-only modes never write.

## Goals

No manual template filling, deterministic assignment, persistent reruns and
honest final SQL/restart status without private-directory output.

## Scope and Non-Goals

Only infra implementation/tests and directly related docs. No application UX,
runtime role changes, deployment, mailbox creation or directory permission grants.

## Functional Requirements

* Exact-template detection only; populated invalid rosters continue to fail.
* Validate development demo/test profile before candidate/Graph enumeration and
  mutations; add profile tag to deployment metadata and support existing
  deployment parameter evidence matched to selected app/environment.
* Shared person validation for generator and initializer; exclude resource naming,
  disabled and guest accounts. No claim of independent Exchange attestation.
* ProgrammeManager admin reservation, stable code ordering, seeded shuffle,
  existing Contractor supplier scope, no reshuffle of persisted roster.
* Versioned private roster envelope with seed and staff array; both readers
  retain legacy arrays. Atomic 0600 file, 0700 directory, no symlinks/Git paths.
* Exact private-host command on SQL candidate connectivity failure.

## Non-Functional Requirements

No private values in errors/output; retain lock refusal, no partial overwrite,
complete Graph pagination, existing SQL validation and one post-Entra SQL plan.

## Acceptance Criteria

Offline tests prove admin none/one/many, exclusions, reproducibility, persistence,
shortage counts, production refusal, no identifier leaks and ordered orchestration.
Live acceptance is explicitly Not run.

## Phase Checklist

<!-- P01 -->
### P01: Generator and authoritative contracts

* [x] P01-T01: Private roster format, candidate scope and shared person validator.
* [x] P01-T02: Profile guard, admin selection, seed and guarded persistence.
* [x] P01-T03: Integrate pre-mutation intake and preserve continuation ordering.

<!-- P02 -->
### P02: Evidence and delivery

* [x] P02-T01: Offline regression tests, ruff and mypy; local app smoke if applicable.
* [x] P02-T02: Update runbook, evidence, index and append-only log.
* [ ] P02-T03: One post-implementation review; commit/push/PR.

## Validation Ownership and Bounds

Extend `infra/tests/test_setup_entra.py` and
`infra/tests/test_initialize_workbench_staff.py`; add at most one focused shared
contract test module if needed. Remove only the two superseded template-stop
test expectations, not their privacy/readonly coverage. Canonical source is
infra scripts; no generated code. Reuse infra unittest runner with absolute
project paths, targeted ruff/mypy; no live setup. Independent critique owns
only its artifact, not implementation or test changes.

## Critique Disposition

Single critique executed, verdict Revise; compatible corrections applied:
PC-001: require Graph `mailboxSettings/userPurpose` equal `user` for automatic
selection, in addition to enabled Member/naming filters. Missing read authority
or unknown purpose fails closed; no automatic grants. Microsoft Graph official
mailbox-settings API and resource docs retrieved 2026-10-16 confirm this field
and MailboxSettings.Read requirement. PC-002: profile key is
`zava-forward-deployment-profile`, propagated by allTags to app/environment.
Fallback only matches exact outputResources IDs; omitted profile is production;
all applicable conflicting/unknown evidence refuses, never names alone.
PC-003: envelope is `{"version":1,"seed":<nonnegative integer>,"staff":[...]}`;
shared decoder validates version, seed and nonempty array, then existing row
validators apply. PC-004: candidate output carries only a bound boolean; any
existing SQL binding stops regeneration before writes. PC-005: exact private-host
command omits admin input, which is prompted privately when needed. PC-006:
missing manager position or invalid one-shot admin answer stops; shortage is
remaining codes minus distinct eligible non-admin members.
No owner-policy change or repeated critique is needed.

## Follow-Up Items

Live person/Exchange attestation, tenant sign-in, SQL binding and restart remain
separate operational evidence, not inferred from mocks.

## Handoff

Research: `.copilot-tracking/research/2026-10-16/auto-roster-360-research.md`.
Details: `.copilot-tracking/details/2026-10-16/auto-roster-360-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-16/auto-roster-360-changes.md`.
