<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue 349 tenant readiness preflight

## Metadata

* Task ID: 349-tenant-readiness-preflight
* Critique date: 2026-10-22
* Plan: .copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: bounded offline/read-only slice for issue 349; two new files only; default read-only; no secret-returning queries; no identities printed or committed; tests for UUID versus systemAssignedIdentity, app-role contract, non-destructive callback requirements and unavailable capability reporting; strict file ownership; Refs #349 only; live acceptance stays unmet; no paid or Azure job.
* Research and evidence considered: .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-research.md; spot checks of infra/tests (discovery) and tools/rpi-checks.py (infra unittest discover at line 476) and the existing systemAssignedIdentity guard in infra/modules/edge-existing-guard.bicep.
* Decisions, dependencies, and acceptance criteria considered: plan Functional/Non-Functional Requirements, Acceptance Criteria, phases P01 to P03, Critique Disposition.
* Assessment boundary: plan credibility only. No source verification of the live probes W1 and W2; no implementation exists to inspect.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| UUID vs systemAssignedIdentity test | Covered | P02-T01, FR 2 |
| App-role contract | Partial | Fields compared and source of truth unspecified (PC-003) |
| Non-destructive callback | Partial | Registration field and URL source unspecified (PC-004) |
| Unavailable capability reporting | Covered | FR 5, P01-T01 |
| Read-only / no secret query | Partial | Denylist-style guard, projections not enforced (PC-001) |
| No identities printed | Partial | Tenant and account output handling unspecified (PC-002) |
| File ownership | Covered | Two new files; gate discovers new test (no edit needed) |
| Refs #349 / live criteria unmet | Covered | Acceptance Criteria; P03 PR step is only implicit (PC-007) |
| No Azure job | Partial | P03 live run uses current credentials against live Azure (PC-005) |
| P03 gate | Partial | Lint/format and gate-state expectations missing (PC-006) |

## Verdict

* Verdict: Revise
* Rationale: The slice is well bounded and justified, but the read-only guarantee is specified as a denylist of examples rather than an enforced allowlist of exact projections and Graph URLs, and several tested contracts (role fields, callback location, expected tenant, audience) are underspecified. All fixes are direct planner corrections to details and acceptance criteria.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Read-only guard is a denylist; `az` argv allowlist does not constrain projections or Graph URLs

* Related IDs: FR 1, NFR leak, P01-T01, C8, C9
* Evidence: plan Functional Requirements 1 ("any other argv ... `--query password` raises"); phase details P01-T01
* Concern: Allowing `containerapp show` and `rest --method GET` by command name still permits unprojected output (env vars, identity principal IDs, tenant IDs) and any GET URL, including Graph credential-bearing properties or `$expand`/non-Graph hosts. A `--query password` string check is trivially bypassed.
* Impact: A future or mistaken call can return secrets or identities; the guard test only proves rejection of listed examples.
* Smallest useful change: Specify that the runner accepts only exact, built-in command templates: every `az` call must carry a fixed `--query` projection or `$select` from the checker's own constants; `rest` must be GET, `--url` must start with `https://graph.microsoft.com/v1.0/applications` or `/servicePrincipals`, must contain `$select`, must not contain `passwordCredentials`, `keyCredentials`, `addPassword`, `$expand`; reject extra flags (`--debug`, `--verbose`, `--body`, `--headers` with tokens). Add tests for each rejection, plus a test that every call the checker makes in a full run satisfies the allowlist.
* Action owner: planning parent
* Exact resolving evidence: P01-T01 detail lists the template/URL rules; P02-T01 lists those rejection tests and the "all emitted argv pass the guard" test.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Tenant, account and auth output handling can leak identities; expected tenant is undefined

* Related IDs: FR 3, NFR leak, P01-T02, W1
* Evidence: P01-T02 checks list "tenant" and `account show`; research W1 notes the account is a service principal
* Concern: `account show` yields user name, subscription and tenant IDs; auth show carries `openIdIssuer` containing the tenant ID and allowed audiences containing client IDs. The plan states no source for an "expected tenant" and does not say these values are compared in memory and discarded.
* Impact: Report, `--json`, exception messages or the changes record could expose tenant or client IDs, contradicting the no-identity requirement; mismatch against tenant cannot be tested.
* Smallest useful change: Define the report as a closed schema (check id, status, fixed reason code, counts/booleans only; no free text from az or Graph, no stderr). Add `--expected-tenant` optional or specify that tenant is derived from the auth issuer and compared with Graph in-process only. Specify `account show` projects only a boolean "logged in" or tenant equality. Leak test must exercise tenant, client, object IDs, UPN and secret sentinels across text, JSON, error and exception paths.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 contains the schema and tenant source; P02-T01 leak test names all sentinel kinds and both output formats.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: App-role contract under-specified and not tied to runtime mapping

* Related IDs: FR 3, P01-T02, P02-T01, C1 to C3
* Evidence: P01-T02 ("`ZavaForward.<key>`"), research C1, C3
* Concern: Plan does not say which fields are compared (`value`, `isEnabled`, `allowedMemberTypes`, `displayName`), whether manifest values already include the prefix, whether roles are read from the application, the service principal, or both, or that `appRoleAssignmentRequired` is on the service principal. No check that the manifest contract matches `src/api/.../auth.py` role map, so contract drift passes.
* Impact: A tautological test (manifest vs itself) can pass while the live API rejects roles; "wrongly typed" is not testable as written.
* Smallest useful change: List compared fields and counts (eight app roles plus four capability roles), name application vs service principal sources, and add a read-only test that parses role values from `src/api/src/zava_forward/api/auth.py` (read, not edit) and asserts the manifest set equals them; include missing, disabled, duplicate, wrong-type and extra-role cases.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 field list; P02-T01 drift test and the five role cases.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Callback check location, URL source and non-destructive wording unspecified

* Related IDs: FR 4, P01-T02, C7
* Evidence: FR 4; P01-T02 `--public-url`, `--manifest`
* Concern: Plan does not say where the callback is read (`web.redirectUris`, not SPA/public client), how the URL defaults (ingress FQDN vs `--public-url`), whether comparison is exact, or what happens with a valid-literal `systemAssignedIdentity` (callback marked not-applicable but the requirement statement should still print). Edge forward-proxy requirement is checked only when URL host differs from the FQDN; that comparison and header names are not specified.
* Impact: False `ready`/`absent` on callback; requirement "non-destructive callback requirements" may be only partly evidenced.
* Smallest useful change: Specify `web.redirectUris` exact-match on `https://<host>/.auth/login/aad/callback`, host from `--public-url` else ingress FQDN, https-only host validation (reuse pattern from initialize-api-auth), forward proxy `Custom` with `X-Forwarded-Host`/`X-Forwarded-Proto` when hosts differ; tests for matching, missing, host-differs-with-and-without-proxy, readable-but-empty, and an assertion that the checker emits no argv other than GET and no callback-editing text.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 and P02-T01 contain these rules and cases.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Live run in P03 is not reconciled with "no Azure job" and offline framing

* Related IDs: P03-T01, Acceptance Criteria 2, caller requirements
* Evidence: P03-T01 ("live run needs resource group `ama` and app `ca-cutover-test-api`"); Dependencies
* Concern: The caller bounds the slice as offline/read-only with no paid or Azure job. The plan runs live `az` reads against the signed-in environment without naming it as an explicitly allowed read-only probe, without isolating `AZURE_CONFIG_DIR` / preventing token-cache writes or `az login`, and without stating fallback if sign-in is absent or expired. The acceptance criterion requires a non-zero live exit, which is environment-dependent.
* Impact: Possible reading as a policy deviation; non-reproducible acceptance; changes record may capture environment-specific text.
* Smallest useful change: Reword as an optional, read-only, caller-permitted probe using already signed-in credentials only (no login), state that unavailable sign-in is recorded as `unknown` and still satisfies the criterion, change acceptance to "any non-ready item exits non-zero and sanitized statuses are recorded", and have the changes record hold statuses only (no tenant, client, subscription IDs).
* Action owner: planning parent
* Exact resolving evidence: P03-T01 and Acceptance Criteria 2 reworded; changes record template restricts content to statuses.
* Decision route: direct planner correction (confirm with caller only if they intend to forbid the live probe entirely)

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Validation misses lint, discovery and gate-hygiene expectations

* Related IDs: P02, P03-T01
* Evidence: P02 validation `python3 -m unittest infra/tests/test_tenant_readiness_preflight.py`; tools/rpi-checks.py runs `unittest discover -s infra/tests`
* Concern: The focused command uses a path form unsupported by hyphenated-script conventions only if the test imports incorrectly; existing tests load hyphenated scripts via importlib, and the plan notes that. The discovery run in the gate will import the new test, so it must not require az or network and must not alter environment/state. Plan does not mention running `python3 -m unittest discover -s infra/tests` locally or ruff (CI uses ruff on named files; new files are not listed and no workflow edit is allowed) or that a dirty/untracked state invalidates the receipt.
* Impact: Late gate failure or order-dependence with other tests (for example patched `subprocess` or env leaking).
* Smallest useful change: Add validation steps: focused test, full `infra/tests` discovery, `python3 -m ruff check --isolated --select E,F,I,B,UP --line-length 100` on the two new files if ruff is available (otherwise record as unavailable), and commit all implementation and RPI evidence before running the gate with the clean-tree and fetch-main prerequisite stated.
* Action owner: planning parent
* Exact resolving evidence: P02/P03 validation sections list these commands and the clean-commit precondition.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Publication constraints are only in acceptance text, not in a task

* Related IDs: Acceptance Criteria 4, P03-T01
* Evidence: Acceptance Criteria; P03 Intent
* Concern: No P03 task step covers branch/PR rules: topic branch confirmation, repository-local noreply email, draft PR to main with `Refs #349` and no closing keywords (including in commit messages and title), listing unmet live acceptance criteria (tenant registration, role assignment, credential delivery, real-user callback), and not merging.
* Impact: A closing keyword or missing unmet-criteria list is easy to introduce at the end.
* Smallest useful change: Add a P03 task (or P03-T02) with those steps and a final grep check of commit and PR text for `close|closes|fix|fixes|resolve` keywords next to the issue number.
* Action owner: planning parent
* Exact resolving evidence: P03 detail section with the steps; PR body evidence recorded in the changes record.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Low]: Audience class and allowed-audience handling incomplete

* Related IDs: FR 2, W1, P01-T02
* Evidence: FR 2; research W1 (two allowed audiences)
* Concern: Classification covers `uuid`, literal, `absent`, `invalid` but UUID case does not say whether `allowedAudiences` includes the `api://<client>` / client ID, and the literal-vs-UUID case-insensitivity and uppercase/braced forms are untested. Graph-checks skipped as not-applicable are expected, but exit code and summary must state they are blocked by audience.
* Impact: A UUID audience that does not match the allowed audiences reports ready.
* Smallest useful change: Add an allowed-audience containment check (booleans only) and tests for casing, braces, whitespace, empty and `invalid` values; map the not-applicable dependency to the audience blocker in the report.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 and P02-T01 list these cases.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Clear justification, rejected alternatives, strict new-file ownership; `denied` versus `absent` distinction is explicit and testable; new test is picked up by the existing infra discovery without any workflow edit.
* Residual risk (accept): live Graph denial means the registration contract checks are only exercised by synthetic tests; live acceptance for #349 stays unmet by design.

## Questions or Blocking Evidence Gaps

* None blocking. PC-005 needs caller input only if the live probe itself is disallowed.

## Limitations

* Live evidence W1 and W2 taken as supplied; role manifest and auth.py contents were not re-read in this critique.
* No implementation or gate behaviour beyond the discovery spot check was verified.

## Recommended Next Action

* Highest-impact finding: PC-001 (and PC-002 for identity leakage)
* Action owner: planning parent
* Smallest next action: revise P01-T01, P01-T02 and P02-T01 details per PC-001 to PC-004 and PC-008, adjust P03 per PC-005 to PC-007, then record the Critique Disposition and finalize without another critique
* User response required: no
