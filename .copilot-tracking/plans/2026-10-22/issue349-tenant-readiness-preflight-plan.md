<!-- markdownlint-disable-file -->
# RPI Plan: Issue 349 tenant readiness preflight

## Task Metadata

* Task ID: 349-tenant-readiness-preflight
* Task slug: issue349-tenant-readiness-preflight
* Planning status: ready
* Plan date: 2026-10-22
* Phase details: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-plan-critique.md

## Executive Summary

This plan adds one standalone, read-only checker, `infra/scripts/tenant-readiness-preflight.py`, and focused tests. It reports, with sanitized statuses only, whether the deployed API's Entra prerequisites can be inspected and match the repository's contract: a valid UUID client audience (not the literal `systemAssignedIdentity`), the single-tenant registration, the expected app-role definitions and the public callback. Today's live probe shows the audience is the literal `systemAssignedIdentity`, no credential setting exists and Graph reads are denied for the current credentials, so the report would show blockers that only an authorized tenant owner can clear. The checker is a prerequisite slice; it does not complete any #349 acceptance criterion.

### User Decisions and Requirements Highlights

* Read-only and sanitized by default: no mutation, no secrets, no identities in output or commits.
* New files only (checker and its test); no edits to owned or existing files.

### What You May Not Know

* Graph denial is reported as `denied`, never as `absent`; absence is only reported when Graph answers a not-found.
* The checker cannot prove sign-in works; real-user callback, credential delivery and staff binding remain human-gated.

### Unresolved Decisions or Blockers

* Tenant authority to identify or create the registration and roles: human blocker (authorized tenant owner).
* Graph read for the checking identity and credential delivery path (#360): human/other-issue blockers.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Bounded offline/read-only prerequisite slice for #349; Refs #349, never closing keywords; not full live acceptance (launch brief).
* Owner-approved synthetic demo: Entra role matching from demo-tenant evidence, random demo assignments when absent, fixed admin ProgrammeManager; production roles manually assigned through the Enterprise App; no directory-admin or professional approval implied.
* Existing auth contract is preserved: validated Entra principal, expected tenant, one mapped role, oid-bound staff; no email fallback or silent rebinding.
* Implement the checker only because research justified it; default read-only; no secret-returning queries; reuse safe CLI patterns; no dependencies.
* Tests must cover UUID versus `systemAssignedIdentity`, the app-role contract, non-destructive callback requirements and unavailable capability reporting.
* Strict file ownership: no edits to setup-entra.py, staff_*.py, staff-azure-worker.py, existing tests, tools/rpi-checks.py, workflows, API/web/core, infra README, KB index/log or addendum.
* Never print or commit identities, UPNs, object IDs or credentials; no private roster or `.env`.
* Validation: focused tests, then `tools/rpi-checks.py --all` with a long lock timeout and unique external receipt, verified before push; draft PR to main, no merge.

## Goals

* Make the tenant blocker's current state reproducible and sanitized before #360 completes.
* Distinguish absent, denied, unknown and mismatched prerequisites without fabricating anything.

## Scope and Non-Goals

### In Scope

* `infra/scripts/tenant-readiness-preflight.py` and `infra/tests/test_tenant_readiness_preflight.py`.
* RPI artifacts under .copilot-tracking for issue349.

### Non-Goals

* Any tenant, app, role, staff, RBAC, ingress or infrastructure change; credential handling; staff inspection.
* #360 transport, #126 costs, documentation edits outside RPI artifacts and `--help`.

## Functional Requirements

* The checker inspects only through an allowlist of `az` argv (`account show`, `containerapp show`, `containerapp auth show`, `rest --method GET`).
  * Observable acceptance criteria: tests show any other argv, any non-GET `rest`, `login`, `credential`, `listSecrets` or `--query password` raises before execution.
* It classifies the API's client audience as `uuid`, `systemAssignedIdentity`, `absent` or `invalid`, and checks (boolean only) that the allowed audiences contain the client audience.
  * Observable acceptance criteria: a UUID is ready; the literal is a blocker that skips Graph registration checks as not-applicable.
* For a UUID it reads the application and service principal with `$select` lists that exclude credentials and verifies single-tenant audience, `api://<client>` identifier URI and the manifest app-role and capability-role contract.
  * Observable acceptance criteria: missing, disabled or wrongly typed roles are `mismatch` with role keys only.
* It states the required callback and edge forward-proxy requirement without changing anything.
  * Observable acceptance criteria: invalid public URLs are rejected; a callback absent from a readable registration is `absent`; unreadable is `unknown`/`denied`.
* Unavailable capability is reported explicitly.
  * Observable acceptance criteria: Forbidden maps to `denied`, not-found to `absent`, missing login, timeouts and malformed output to `unknown`.

## Non-Functional Requirements

* No secret or identity leakage.
  * Objective threshold or evaluation condition: serialized report contains none of the test sentinel IDs, UPNs or secrets.
  * Observable acceptance criteria: a leak test passes.
* Standard library only; Python 3.12.
  * Observable acceptance criteria: no new dependency; unittest runs.

## Acceptance Criteria

* Checker and test exist; focused tests pass; `--help` documents usage and read-only boundary.
* An optional caller-permitted live probe using already signed-in credentials (no login) records sanitized statuses only; any non-ready item exits non-zero, and absent sign-in is recorded as `unknown`.
* The complete local RPI gate passes on the final head with a verified external receipt.
* PR body says Refs #349 only and lists the unmet live acceptance criteria.

## Implementation Context Record

| Context item                     | Current artifact or record |
|----------------------------------|----------------------------|
| Plan                             | .copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-plan.md |
| Phase details                    | .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-phase-details.md |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-plan-critique.md (see Critique Disposition) |
| Relevant research                | .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-research.md |
| Changes-record role              | .copilot-tracking/changes/2026-10-22/issue349-tenant-readiness-preflight-changes.md is created by implementation |
| Planning execution and readiness | complete; ready |
| Continuation context             | automatic parent continues to Implement |

## Sources

* .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-research.md: evidence C1 to C10, W1, W2 and the selected approach.
* infra/scripts/initialize-api-auth.py and infra/entra/app-registration.json: reused patterns and the role contract.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Checker implementation

* Intent: add the read-only checker with a sanitized report.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Allowlisted read-only runner and status classification

* Requirement and evidence: read-only, denied/absent/unknown (C5, C8 to C10, W2).
* Expected result: runner rejects forbidden argv; errors map to statuses.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Contract checks and CLI

* Requirement and evidence: audience, roles, callback, edge proxy (C1, C2, C6, C7, W1).
* Expected result: report, JSON option, exit code and `--help`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused tests

* Intent: prove the required behaviours offline.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: New unittest module

* Requirement and evidence: the four required test areas plus leak and read-only guards.
* Expected result: tests pass without network.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Validation and evidence

* Intent: live sanitized run, gate and publication evidence.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Live read-only run and complete gate

* Requirement and evidence: acceptance criteria above.
* Expected result: sanitized live result recorded; gate receipt verified.
* Detail section: P03-T01 in .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Publication

* Requirement and evidence: branch, author, Refs #349 only, draft PR, no merge (PC-007).
* Expected result: pushed branch and draft PR listing unmet live criteria.
* Detail section: P03-T02 in .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-phase-details.md

## Dependencies

* Azure CLI (existing): optional at runtime; absence is reported as `unknown`.
* Authorized tenant owner: needed for any non-ready item to clear.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 High read-only guard was a denylist | resolved | Exact command templates with fixed `--query`/`$select` constants, Graph URL prefix and forbidden-token rules, extra flags rejected; P01-T01, P02-T01 |
| PC-002 High identity leakage and undefined tenant source | resolved | Closed report schema (check id, status, fixed reason code, booleans/counts); tenant derived from the signed-in account and compared in memory only; leak test over text, JSON, error paths; P01-T02, P02-T01 |
| PC-003 Medium role contract under-specified | resolved | Compared fields, application and service-principal sources and a drift test against the runtime role map (read only); P01-T02, P02-T01 |
| PC-004 Medium callback specifics | resolved | `web.redirectUris` exact match, host from `--public-url` else ingress FQDN, Custom proxy headers when hosts differ; P01-T02, P02-T01 |
| PC-005 Medium live run framing | resolved | Optional probe permitted by the caller using already signed-in credentials only; no login; sign-in absent records `unknown`; changes record holds statuses only; acceptance reworded |
| PC-006 Medium validation hygiene | resolved | Added full infra discovery, ruff when available and clean-commit gate precondition; P03-T01 |
| PC-007 Low publication steps not a task | resolved | Added P03-T02 |
| PC-008 Low audience containment | resolved | Allowed-audience containment (boolean) and malformed-form tests; P01-T02, P02-T01 |

Critique run: one, verdict Revise; all findings were compatible planner-owned corrections applied directly; no user decision required; no second critique.

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-22/issue349-tenant-readiness-preflight-changes.md
* Ready phase or task: P01
* Remaining provisional question or blocker: none for this slice; tenant authority remains a human blocker
