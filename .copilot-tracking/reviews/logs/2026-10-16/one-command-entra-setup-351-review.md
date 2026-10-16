---
title: One-command Entra setup review
description: Independent post-implementation assessment for issue 351
ms.date: 2026-10-16
---

## Scope and Evidence

Historical independent Review: the findings and verdict below apply to the
original assessed source. The owner's subsequent selected implementation
disposition is appended at the end; it is not a second Review.

* Task: 351, one-command-entra-setup-351.
* Review date: 2026-10-16.
* Review scope: one independent full post-implementation RPI review.
* Assessed boundary: expanded owner contract, current plan, phase details,
  PC-001 through PC-008, changes/acceptance audit, complete new script and
  tests, and the tracked existing-source/documentation diff.
* Canonical artifacts: the task-slug research, plan, critique, phase-details
  and changes files under their respective 2026-10-16 directories.
* Context: original case study, addendum opening, knowledge index and memory.
  These provide project boundaries, not evidence of live technical acceptance.
* Source boundary: no source fixes, nested agents, Azure calls, private roster
  or dataset reads, or access to excluded legacy/environment paths.

## Opening Review State

* Interpreted review goal: independently assess the complete expanded issue 351 implementation against accepted intent and PC001-PC008.
* Review scope: full offline implementation, documentation and acceptance audit.
* Evidence readiness: canonical research, plan, details, critique and changes exist; script and tests available for complete reading. Prior validation is parent-reported, with one subsequent preservation patch awaiting final validation.
* Acceptance basis: expanded owner contract, current plan and critique dispositions; tenant deployment is not required for code completion.
* First comparison boundary: plan/critique/changes reconciliation followed by complete script/tests and existing tracked source/docs diff.
* Active read-only boundaries: only this review record may change; no Azure calls, private roster/data reads, or excluded legacy/environment paths.
* Initial blockers: none to performing the review; actual tenant/SQL/sign-in acceptance remains unexecuted.

## Execution Status

* Execution status: Complete.
* This status describes the review execution, not deployment, publication or
  acceptance. Both new files were read completely: 971 script lines and 638
  test lines at this boundary. All supplied canonical task artifacts and the
  tracked existing-source/docs diff were compared.
* P02-T03 remains legitimately open for parent disposition/publication.
  No reviewable-artifact ambiguity or evidence blocker prevented this review.
* Outcome: Not accepted. Three Medium implementation defects remain.
* PR readiness: blocked; any publication before correction must be draft and
  explicitly identify RV-001 through RV-003. These are not hidden follow-ups.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | CLI, discovery, registration/SP/roles, roster, auth/runtime, consent, credentials | Partial | Most behavior is implemented; RV-001, RV-002 and RV-003 qualify the acceptance audit |
| P01-T02 | Additive API/edge tags and compatibility CLI | Reconciled | Tags preserve existing tags; old imported callback-only API remains; broader CLI behavior is documented |
| P02-T01 | New fake-az tests and retained regressions | Partial | Broad offline coverage exists, but fresh conflicting roster, storage preflight and already-failed converged runtime cases are missing |
| P02-T02 | Infra guide, manifest metadata, index/log and validation | Reconciled with validation limit | Documentation distinguishes offline proof and human gates; prior checks precede the final small preservation patch |
| P02-T03 | Independent review and PR | In progress | This record supplies the single review; parent owns correction, final validation and publication |
| Follow-Up Items | Live tenant, consent, SQL/restart and browser gates | Reconciled | Separate operator acceptance, not a requirement to deploy during code development |

## Completed Work Assessment

| Related marker | Files | Assessment and evidence |
| --- | --- | --- |
| P01-T01: entry point and tools | infra/scripts/setup-entra.py | Python standard library, no required arguments, ama default, safe argument errors, tool/extension instructions, fixed hosts, strict Graph pagination and captured CLI streams are present |
| P01-T01: context/discovery | infra/scripts/setup-entra.py; infra/tests/test_setup_entra.py | Management subscription and Graph tenant binding, isolated device login, tag/legacy/name API selection, origin-linked enabled edge routes and eligible custom domains are implemented; pending 344 compatibility is assessed from supplied research, not a tenant claim |
| P01-T01: directory convergence | infra/scripts/setup-entra.py; infra/entra/app-registration.json | Configured UUID preference, managed-identity sentinel fallback, ambiguity stops, additive callbacks/manifest roles, stable role IDs, SP creation and assignment-required enforcement are present |
| P01-T01: roster | infra/scripts/setup-entra.py; infra/tests/test_setup_entra.py | Private typed rows, explicit roles, enabled member/security-group checks, effective direct-group conflict checks and additive assignments are present; conflict validation is too late on a fresh setup, RV-001 |
| P01-T01: credentials | infra/scripts/setup-entra.py | Explicit creation, stable app-bound names, protected body files, retained credentials, orphan detection and store-before-auth activation are present; Key Vault endpoint preflight is missing, RV-002 |
| P01-T01: auth/runtime | infra/scripts/setup-entra.py | Existing exclusions, token store, provider login fields and container settings are retained; HTTPS/Standard proxy and trusted-proxy environment are reconciled; an already-failed rollout can pass, RV-003 |
| P01-T01: modes/output | infra/scripts/setup-entra.py; infra/tests/test_setup_entra.py | Check/dry-run prohibit login and remote mutation; missing prerequisites are distinct from known drift; raw subprocess output is captured, UUID labels redacted and authority instructions use generic portal URLs |
| P01-T02 | infra/scripts/initialize-api-auth.py; infra/modules/containerapps.bicep; infra/modules/edge.bicep | Compatibility routing and minimal discovery tags are consistent with scope; no network/policy weakening appears in the diff |
| P02-T01/P02-T02 | infra/tests/test_setup_entra.py; infra/tests/test_bicep_policy.py; infra/README.md; docs/reference/README.md; docs/reference/log.md | Tests and directly related documentation are substantive; index/log updates preserve the offline/live distinction |

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Change and rationale | Trigger/decision | Reconciliation and assessment |
| --- | --- | --- | --- |
| P01-T02/P02-T01 | Add entraClientSecretName with historical default and module forwarding | Setup-owned secret names would otherwise be overwritten by later declarative deployment; changes record gives the reason | Narrowly coupled persistence improvement; Bicep regression and README explain the parameter and app-local-to-vault redeploy boundary. Justified, no divergent user decision needed |
| P01-T01 | Explicit bearer-only option and preservation of existing Return401 action | Existing service-test mode and pending 344 browser ownership | Plan/details, changes and guide agree; no implicit bearer-to-browser transition, no claim that service mode proves browser acceptance |
| P01-T01/P02-T01 | Preserve complete existing Container App configuration in the secret PATCH and assert ingress remains in fake-az body | Parent-reported small pre-Review preservation patch | Source contains the merge and test assertion. Final full validation is pending parent execution; do not project earlier 101-test success onto this later edit |
| P02-T03 | Material findings block ready delivery rather than becoming automatic follow-ups | PC-008 direct correction | Plan and details correctly express the gate; this review applies it. No second critique or review is required |

The supplied artifacts record one critique and direct compatible corrections.
No evidence of an unapproved divergent architectural decision was found.
Implemented coverage is not equivalent to full disposition: the defects below
show that parts of PC-001/PC-002/PC-003 remain unresolved in executable behavior.

## Critique and Material Revision Assessment

| Critique | Disposition assessment |
| --- | --- |
| PC-001 | Largely applied: tenant/subscription binding, permission hints, fixed Graph/ARM reads and explicit authority limitations. Selected Key Vault endpoint connectivity is not checked before credential creation; see RV-002 |
| PC-002 | Partially applied: create/store/activate ordering, stable names, no rerun rotation and human orphan recovery are implemented. Destination reachability preflight is absent; recovery handling does not replace that precondition, RV-002 |
| PC-003 | Partially applied: typed principals, propagation and effective role checks exist. Planned roster-role conflicts are checked after registration/SP mutations on a fresh run, RV-001 |
| PC-004 | Applied within documented boundary: local exclusive mutation lock, no blind POST retry, unknown-outcome rerun discovery, verification and explicitly unsupported cross-host concurrency. Tests cover a lost application-create response, not every possible interrupted stage |
| PC-005 | Applied for the reviewed contract: eligible origin-linked routes/domains, Standard forwarding, retained exclusions/token store/action and no implicit browser conversion. Actual 344 edge/browser readiness is unproved and remains separate |
| PC-006 | Applied in code: captured CLI streams, allowlisted transient device prompt, isolated private profile, disabled file logging/telemetry, sanitized errors and request-file cleanup. Persistent isolated auth cache is intentionally reused; no real identity output was inspected |
| PC-007 | Applied for defaults/modes: default roster path, incomplete missing roster, blocked unknown state and no login/profile creation in read-only modes. Converged configuration with failed rollout remains an uncovered check defect, RV-003 |
| PC-008 | Applied to planning and this verdict: unresolved material defects block ready publication; only genuinely separate human/live acceptance is residual work |

There is no evidence requiring a new owner decision or material research
cycle. The findings fit the accepted implementation direction.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Authorized tenant execution and human consent | No Graph/ARM writes were authorized or performed in this development run | Authorized tenant application owner/admin runs setup and records sanitized results | Open distinct operator acceptance; not a source-completion defect |
| Private SQL staff binding/restart | Explicit non-goal of this setup script; app-role grants do not create SQL bindings | Authorized private-network operator follows existing staff procedure with user roster | Open distinct follow-up; do not read private data during code correction |
| Real authorized browser sign-in after 344 | Requires actual tenant, edge readiness and human interaction | 344/deployment operator and authorized user execute sign-in acceptance | UNMET; no inference from fake-az, CLI help or bearer service mode |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Fresh conflicting roster mutates the directory before rejecting the input

* Related scope: P01-T01/P02-T01; whole-roster validation before writes;
  PC-003.
* Evidence: infra/scripts/setup-entra.py setup() calls resolve_roster(), then
  creates/patches the application and SP and enables assignment-required.
  Only afterwards does assign_roster() compare planned group/user roles.
  infra/tests/test_setup_entra.py
  test_group_assignment_and_planned_user_group_conflict first bootstraps a
  fully reconciled environment, so its zero-additional-write assertion misses
  the fresh-registration path.
* Reproduction: a memory-only fake using the supplied FakeAzure, a missing
  registration/SP, and a security-group Coordinator row plus a member-user
  SupportOfficer row produced the expected conflict error only after four
  Graph writes: application POST/PATCH and SP POST/PATCH. No assignment was
  created. No network, private input or filesystem fixture was used.
* Impact: invalid role mappings do not satisfy the promised zero-mutation
  rejection. A rerun can leave directory objects/settings changed even though
  the whole roster was never acceptable.
* Destination: rpi-implement.
* Smallest useful next action: validate planned effective user/group role
  conflicts from resolved membership and explicit role keys before the first
  directory mutation; preflight existing conflicts as soon as the existing SP
  is readable. Add a fresh-state rejection test asserting zero remote writes.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Key Vault connectivity is first tested after minting the one-time credential

* Related scope: P01-T01/P02-T01; selected-storage/network preflight;
  PC-001 and PC-002.
* Evidence: infra/scripts/setup-entra.py secret_reference() lists vaults via
  ARM, checks attached identity, calls the Container App listSecrets endpoint,
  then invokes Graph addPassword. The first data-plane request to the selected
  vault is subsequently keyvault secret set. There is no prior selected-vault
  endpoint reachability/read-only probe. contexts()/discover() exercise ARM
  and Graph, not this vault endpoint.
* Impact: a predictably inaccessible private/default vault can cause creation
  of a credential whose one-time value cannot be stored. The script correctly
  avoids activating auth and blocks regeneration on rerun, but unnecessarily
  strands a valid credential and requires human recovery before retry. This
  does not meet the adopted destination/network-preflight contract.
* Destination: rpi-implement.
* Smallest useful next action: add a bounded, sanitized, non-mutating check of
  the selected vault endpoint before addPassword, with explicit handling of
  unavailable or denied observation. Do not read secret values, claim a read
  proves write authority, weaken networking or silently switch stores. Test
  unreachable/denied preflight with zero addPassword calls, retaining the
  existing safe recovery test for failures that occur after a successful probe.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: A failed existing runtime rollout can pass check as fully converged

* Related scope: P01-T01/P02-T01; check/final summary and runtime verification.
* Evidence: infra/scripts/setup-entra.py setup() checks the Container App
  provisioningState only inside the wait after a nonempty runtime_patch().
  If environment values already match, no provisioning-state condition is
  evaluated. infra/tests/test_setup_entra.py
  test_unverified_runtime_rollout_is_not_success exercises only a run that
  needs a runtime patch.
* Reproduction: a memory-only fake with matching registration, SP, assignment,
  same-client stored credential, auth and runtime environment, but
  provisioningState=Failed returned 0 for --check and printed
  "6/6 Summary: read-only; 0 reconciliation item(s)."
* Impact: a known failed ARM rollout is indistinguishable from successful
  runtime configuration verification. This is a locally inspectable state
  defect, not a demand for tenant deployment, SQL or browser acceptance.
* Destination: rpi-implement.
* Smallest useful next action: evaluate observed provisioning state even when
  no runtime PATCH is needed; report failed/non-ready state as blocked or
  incomplete rather than clean convergence. Add converged-state Failed and
  in-progress cases for both read-only and ordinary no-op runs.

## Defects

* RV-001, RV-002 and RV-003 are current-direction implementation defects.
  All route to later rpi-implement, not unowned residual work.
* No Critical or High finding is asserted. The three Medium gaps are material
  to the adopted preflight/validation/check contract and block ready delivery.

## Routed Findings

| Finding | Destination | Owner / next action | Route reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Active parent: move role-conflict validation before mutations and add fresh-state regression | Implementation fails accepted fail-before-write behavior |
| RV-002 | rpi-implement | Active parent: preflight selected vault endpoint before one-time credential creation | Missing accepted storage/network precondition |
| RV-003 | rpi-implement | Active parent: inspect no-op provisioning state and cover failure/in-progress outcomes | False clean runtime-check result |

Later implementation of these findings does not require another Review.

## Residual Work

* Authorized tenant/Graph/ARM execution, actual consent, SQL staff/restart and
  real user browser sign-in remain explicitly UNMET as distinct operator
  gates. Their absence is not grounds to reject otherwise complete code.
* Parent still owns final validation after the preservation patch,
  finding disposition and eventual commit/PR/check evidence. No source,
  plan, critique, research or changes artifacts were changed by this reviewer.

## Blockers and Remaining Work

* Review execution blockers: none.
* Ready-PR blockers: RV-001 through RV-003 until corrected and supported by
  targeted tests, or explicitly retained in a blocked/draft publication.
* Remaining active delivery: P02-T03 parent disposition and publication.
* Acceptance-audit qualification: "Offline proven" must not be read as
  proving zero-write fresh roster rejection, selected-vault network preflight
  or already-failed no-op runtime verification. Those cases are not currently
  supported by the suite.

## Validation Evidence

| Command / evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Parent-reported combined unittest run for setup, initializer, edge, identity RBAC and Bicep policy | Five targeted infra modules | Passed before final small patch | 101 tests, including 39 new setup tests; dependencies restored after observed missing-package/tool failures |
| Parent-reported ruff --target-version py310 and mypy | New setup script/test code | Passed before final small patch | No claim that these were rerun by this reviewer |
| Parent-reported both CLI --help launches and git diff --check | New and compatibility CLI / diff | Passed before final small patch | Local launch evidence, not interactive login or application serving |
| Static inspection of preservation patch and fake-az assertion | Secret configuration PATCH | Reviewed; final validation pending | Full existing configuration is merged with preserved/new secrets; fake asserts ingress FQDN remains in request |
| python3 -B inline, memory-only FakeAzure orchestration | RV-001 | Reproduced | Fresh planned conflict rejected after four directory writes; no assignment created |
| python3 -B inline, memory-only FakeAzure orchestration | RV-003 | Reproduced | Matching configuration with Failed provisioning state returned check exit 0 |
| Complete source/test reads and existing tracked diff review | All supplied implementation/docs | Complete | No source mutation or live identity/secret output |
| Actual Azure/Graph/Key Vault writes, SQL, interactive/browser acceptance | Operator environment | Skipped / UNMET | Not authorized in this development run; not required as code-completion evidence |

The first RV-001 simulation attempt stopped on a missing fixture-only
pending_domains attribute. After supplying the discover() side effect in the
memory fixture, the reproduction completed as recorded. This was not a source
failure or an Azure attempt.

## Outcome

* Execution status: Complete.
* Outcome: Not accepted.
* Rationale: substantial implementation coverage and sensible human boundaries
  are present, but three reproducible/source-evidenced requirement gaps remain
  in pre-mutation validation, storage connectivity preflight and no-op runtime
  verification. Reported passing checks do not cover these behaviors.
* PR readiness: blocked/draft until the material findings have explicit
  correction and validation dispositions. Separate tenant/SQL/sign-in
  acceptance must continue to be labelled unmet after code correction.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | rpi-implement: RV-001, RV-002, RV-003 | Active parent corrects within accepted direction and validates |
| Decision gap or invalid assumption | None | No divergent owner decision required |
| Material evidence gap | None requiring rpi-research | Use existing mocked validation infrastructure; live evidence remains operator follow-up |
| Non-blocking residual work | Distinct tenant/SQL/browser acceptance follow-ups | Authorized tenant/private-network operator and human user after 344 readiness |

## Artifact Index

| Artifact | Description |
| --- | --- |
| .copilot-tracking/research/2026-10-16/one-command-entra-setup-351-research.md | Research, alternatives and live-evidence boundary |
| .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-plan.md | Current acceptance contract and task markers |
| .copilot-tracking/plans/2026-10-16/one-command-entra-setup-351-critique.md | One independent critique, PC-001 through PC-008 |
| .copilot-tracking/details/2026-10-16/one-command-entra-setup-351-phase-details.md | Mutation, validation and delivery details |
| .copilot-tracking/changes/2026-10-16/one-command-entra-setup-351-changes.md | Acceptance audit, prior validation and amendments |
| infra/scripts/setup-entra.py | Complete production implementation read |
| infra/tests/test_setup_entra.py | Complete new fake-az suite read |
| infra/scripts/initialize-api-auth.py | Compatibility CLI diff assessed |
| infra/main.bicep | Secret-name parameter forwarding diff |
| infra/modules/containerapps.bicep | API tag and secret-name persistence diff |
| infra/modules/edge.bicep | Edge discovery tag diff |
| infra/entra/app-registration.json | Roles/callback metadata and updated procedure |
| infra/tests/test_bicep_policy.py | Compiled persistence-regression diff |
| infra/README.md | Complete tracked documentation diff |
| docs/reference/README.md | Knowledge routing diff |
| docs/reference/log.md | Append-only knowledge-log diff |
| .copilot-tracking/reviews/logs/2026-10-16/one-command-entra-setup-351-review.md | This sole review record |

## Next Steps

Return this one review to the active parent. The parent should resolve
RV-001 through RV-003 through later rpi-implement work, run final targeted
validation including the preservation patch, and record dispositions before
publishing a ready PR. If publishing with unresolved findings, use a blocked
draft PR. Do not run another independent Review or require live tenant
deployment to finish these code corrections.

## Later Owner-Selected Implementation Disposition (2026-10-16)

This is execution evidence from the explicitly requested later implementation,
not a new independent Review. Original execution Complete / Not accepted and
its assessed boundary remain historical and unchanged.

| Finding | Implemented disposition | Regression evidence |
| --- | --- | --- |
| RV-001 | Planned membership/role conflicts checked during resolve_roster before any app/SP writes | Fresh state, both roster orders, all three modes assert no writes or objects; matching roles allowed; removal of guard fails behavioral assertions |
| RV-002 | Selected vault secret-metadata endpoint probed before addPassword; sanitized denial/network errors and existing recovery retained | Unreachable/denied endpoint and timeout create no credential; ordering/reuse/read-only checks; removal of probe creates credential and fails regression |
| RV-003 | Final fresh provisioning read required independently of runtime drift | Failed, in-progress, canceled and unknown states incomplete in ordinary/check/dry-run; success recovers; removal of guard yields false clean exit and fails regression |

All 177 infra tests passed, including 47 setup tests. Each in-memory safeguard
mutation was killed by assertion failures, not runner/import errors. All Bicep
templates build/lint offline and exact workflow infra/container lint/type
checks pass. Secret-inventory parameter expectations and policy formatting
repair the reproduced CI defects. Published PR #352 Custom forwarding is
preserved by regression without editing that branch.

These dispositions remove source-readiness blockers; actual tenant login,
Graph/ARM writes, vault access/secret validity, human consent, SQL bindings/
restart and authorized browser sign-in remain UNMET. The source changes and
current acceptance audit are in the existing task changes record. Issue
checkboxes remain unchanged and the owner retains the merge decision.
