<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 349 tenant readiness preflight

## Metadata

* Task ID: 349-tenant-readiness-preflight
* Task slug: issue349-tenant-readiness-preflight
* Related plan: .copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-research.md

## Phase Index

| Phase ID | Name                    | Status | Detail sections |
|----------|-------------------------|--------|-----------------|
| P01      | Checker implementation  | ready  | P01, P01-T01, P01-T02 |
| P02      | Focused tests           | ready  | P02, P02-T01 |
| P03      | Validation and evidence | ready  | P03, P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Checker implementation

### Context

The existing helper runs `az` with `--query` projections and validates UUIDs and hostnames but fails on the first problem and can log in or write (C5 to C10). The checker is a new standalone file.

### Intent

Produce a sanitized multi-check report that never mutates.

### Boundaries

* Included: new script only.
* Excluded: edits to existing scripts, docs, workflows.

### Likely Targets

* infra/scripts/tenant-readiness-preflight.py: new.

### Dependencies

* none

### Validation Expectations

* `python3 infra/scripts/tenant-readiness-preflight.py --help` documents read-only behaviour.

### Completion Evidence

* Changes record entry with the live sanitized result.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Allowlisted read-only runner and status classification

#### Context

Only `account show`, `containerapp show`, `containerapp auth show` and `rest --method GET` to Graph v1.0 are needed. Errors are classified from stderr keywords without echoing the message.

#### Intent

The runner accepts only exact built-in command templates: each `az` call carries a fixed `--query` projection or `$select` from the checker's own constants; `rest` must be GET with a URL starting `https://graph.microsoft.com/v1.0/applications` or `/servicePrincipals`, containing `$select` and none of `passwordCredentials`, `keyCredentials`, `addPassword`, `$expand`; extra flags (`--body`, `--headers`, `--debug`, `--verbose`) are rejected. The runner raises on anything else before any process starts; `Forbidden`/`Authorization_RequestDenied`/`AuthorizationFailed` map to denied, `NotFound`/`ResourceNotFound`/`Request_ResourceNotFound` to absent, other failures to unknown.

#### Boundaries

* Included: allowlist, timeout, status mapping.
* Excluded: logins, profile creation, writes.

#### Likely Targets

* infra/scripts/tenant-readiness-preflight.py

#### Dependencies

* none

#### Validation Expectations

* Tests inject the runner; forbidden argv tests.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Contract checks and CLI

#### Context

Role contract is read from infra/entra/app-registration.json (`appRoles` and `capabilityRoles`, `ZavaForward.<key>`); callback path from the manifest. Graph reads use `$select` lists without credentials, projected to booleans and counts.

#### Intent

Report is a closed schema: check id, status, fixed reason code, booleans and counts only; no free text from az or Graph, no stderr. Tenant is derived from the signed-in account (`account show` projects only the tenant) and compared in memory with the Graph/auth issuer, never printed. Audience class `uuid`/`systemAssignedIdentity`/`absent`/`invalid` (case, braces, whitespace handled) plus a boolean allowed-audience containment check; non-UUID audience marks Graph checks `not-applicable` with the audience blocker named. Role contract: eight `appRoles` plus four `capabilityRoles` from the manifest, compared on `value` (`ZavaForward.<key>`), `isEnabled`, `allowedMemberTypes` containing User and uniqueness, on the application; `appRoleAssignmentRequired` on the service principal. Callback: `web.redirectUris` exact match on `https://<host>/.auth/login/aad/callback`, host from `--public-url` else ingress FQDN with the existing HTTPS hostname validation; when the host differs from the FQDN, forward proxy `Custom` with `X-Forwarded-Host` and `X-Forwarded-Proto` is required. Checks: tenant, ingress, auth enabled, audience class, credential-setting presence, application lookup, single-tenant audience, identifier URI, role contract, callback, edge proxy, service-principal assignment requirement. Text and `--json` output; exit 0 only if all applicable checks are ready, 1 otherwise, 2 for usage.

#### Boundaries

* Included: `--resource-group`, `--app`, `--public-url`, `--manifest`, `--json`.
* Excluded: any identity or role assignment inspection.

#### Likely Targets

* infra/scripts/tenant-readiness-preflight.py

#### Dependencies

* P01-T01

#### Validation Expectations

* Unit tests and a live sanitized run.

<!-- rpi:phase id=P02 -->
## P02: Focused tests

### Context

Existing tests load hyphenated scripts through importlib and patch the subprocess boundary (infra/tests/test_initialize_api_auth.py:1).

### Intent

Offline tests of the required behaviours.

### Boundaries

* Included: new test file.
* Excluded: existing tests.

### Likely Targets

* infra/tests/test_tenant_readiness_preflight.py: new.

### Dependencies

* P01

### Validation Expectations

* `python3 -m unittest infra/tests/test_tenant_readiness_preflight.py` passes.

### Completion Evidence

* Test output in the changes record.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: New unittest module

#### Context

Fake runner returns canned JSON or raises classified errors.

#### Intent

Cover: UUID vs `systemAssignedIdentity` vs absent/invalid forms and audience containment; role contract with missing, disabled, duplicate, wrong-type and extra cases and a drift test that the manifest role values equal the runtime role maps read from the API auth module (read only); callback present, missing, readable-but-empty, unreadable, host-differs with and without proxy; denied/absent/unknown capability; each argv/URL rejection and a test that every argv emitted in a full run passes the guard; leak test with tenant, client, object, UPN and secret sentinels across text, JSON and error paths; CLI exit codes.

#### Boundaries

* Included: synthetic sentinel values only.
* Excluded: network, real tenant values.

#### Likely Targets

* infra/tests/test_tenant_readiness_preflight.py

#### Dependencies

* P01

#### Validation Expectations

* All tests pass; no live calls.

<!-- rpi:phase id=P03 -->
## P03: Validation and evidence

### Context

The complete local gate is mandatory for a publication candidate.

### Intent

Record a live sanitized run, commit evidence, run the gate, verify the receipt, push and open a draft PR.

### Boundaries

* Included: focused tests, live read-only run, gate, PR.
* Excluded: merging, bypassing the lock, editing the gate.

### Likely Targets

* .copilot-tracking changes and review records.

### Dependencies

* P02

### Validation Expectations

* Focused tests, then the all-checks gate with a unique external receipt, then verify-receipt against current origin/main.

### Completion Evidence

* Receipt path and hash, head SHA, PR URL.

### Unresolved Items

* none

<!-- rpi:task id=P03-T01 -->
### P03-T01: Live read-only run and complete gate

#### Context

The live run needs resource group `ama` and app `ca-cutover-test-api` (names from existing tests and issue).

#### Intent

Optional caller-permitted live read-only probe using already signed-in credentials only (no login, no profile creation); if sign-in is absent the result is `unknown`. The changes record holds statuses only. Then validation order: focused test; full `python3 -m unittest discover -s infra/tests`; ruff on the two new files if available (else record unavailable); commit all implementation and dated RPI evidence; fetch main; run the complete gate with a long lock timeout and unique external receipt on the clean tree; verify the receipt before push.

#### Boundaries

* Included: read-only calls.
* Excluded: printing identities.

#### Likely Targets

* .copilot-tracking/changes/2026-10-22/issue349-tenant-readiness-preflight-changes.md

#### Dependencies

* P02-T01

#### Validation Expectations

* Receipt verifies.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Publication

#### Context

Repository workflow requires a topic branch, repo-local noreply author/committer email, Conventional Commit with Co-authored-by trailer and a draft PR.

#### Intent

Push the branch and open a draft PR to main whose title, body and commits use `Refs #349` only and list the unmet live acceptance criteria; do not merge.

#### Boundaries

* Included: commit, push, draft PR.
* Excluded: merge, force-push.

#### Likely Targets

* GitHub PR

#### Dependencies

* P03-T01

#### Validation Expectations

* A final search of commit and PR text finds no closing keyword next to the issue number.
