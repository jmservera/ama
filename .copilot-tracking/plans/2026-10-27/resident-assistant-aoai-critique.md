---
title: Resident assistant Azure OpenAI final-candidate plan critique
ms.date: 2026-10-27
---

## Metadata

* Task ID: #469; parent #466, implementation merged in #474.
* Critique date: 2026-10-27.
* Plan: .copilot-tracking/plans/2026-10-27/resident-assistant-aoai-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/resident-assistant-aoai-phase-details.md
* Critique execution status: Complete.
* One independent assessment of the supplied final candidate; no implementation,
  source-artifact edits, nested agents or second critique.

## Inputs and Criterion Boundary

Assessed the supplied research, plan and phase details against the owner's
requirements: real Azure OpenAI in existing RG ama; managed identity, no keys;
hard USD20 inference ceiling; per-resident limit; deterministic fallback;
own-case status/documents/forms only; no specialist or eligibility advice; no
new groups, ingress changes or other Azure role assignments.

Read the relevant existing assistant, HTTP/session, startup/configuration, SQL
reader, SQL provisioning/permission verifier, resident Bicep, provider tests,
architecture and local-gate documentation. Repository context includes the
original case study, resident-service addendum, knowledge-base index and memory.
The branch is feat/resident-assistant-aoai at 885ee05f; no topic PR was returned
by the lifecycle lookup. Existing untracked planning inputs were not modified.

Research W1-W3 are supplied evidence claims, not independently reproduced
tariff, API compatibility, quota or cloud results. This critique judges planning
credibility, not deployed behavior, production approval or cost certification.
The newer owner direction supersedes the older USD5 proposal. It does not,
by itself, extend resident-service authority or approve unrestricted prose.

## Coverage Assessment

| Requirement, research, phase or task | Coverage | Evidence or concern |
| --- | --- | --- |
| Real bounded advisory inference; research contrarian cycle; P01-T02 | Partial | Sentence selection is safe in principle, but usefulness and semantic correctness lack an acceptance oracle; PC-001. |
| Hard USD20 cap; research W2; P01-T01/T02 | Partial | Conservative reservations are appropriate; priced envelope and durable attempt semantics need proof; PC-002/003. |
| SQL permissions and migrations; P01-T01, P02-T02 | Partial | Separate schema is sound; existing verifier rejects the proposed grants; PC-004. |
| Runtime composition and identity; P01-T01/T02 | Partial | Existing startup rejects common AI settings and injects only rules; PC-005. |
| Per-resident five/rolling-hour limit; P01-T01 | Partial | Session-handle stability across key rotation is unspecified; PC-006. |
| Own-case authorization, no specialist advice, fallback; P01-T02 | Covered with dependencies | Fixed topics, approved text, mandatory caveats and post-inference authorization are explicit; PC-001/005 require executable acceptance. |
| Default-off account, dedicated role, no ingress; P02-T01 | Partial | Scope is explicit; deployment-policy assertions are missing; PC-007. |
| Expiry and renewed budget; P01/P02 | Partial | Funding horizon and existing service expiry differ; PC-008. |
| Real Azure evidence and live limitations; P02-T02/P03 | Partial | Limitations are acknowledged, but success categories need separation; PC-009. |
| Branch, review and publication; P03-T02 | Covered | Main target matches supplied merged-parent direction; independent Review, exact-head receipt and human gates retained. |

## Verdict

* Verdict: Revise.
* Severity summary: 6 High, 3 Medium; no Critical findings.
* Rationale: The architecture is plausible and appropriately constrained, but
  the plan does not yet make real inference value, hard-cap correctness,
  permission migration and actual startup wiring sufficiently testable.
  Correct these directly before implementation; do not broaden authority.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Real advisory value is asserted, not demonstrated

* Related IDs: Goals; P01-T02; research Contrarian/Alternatives.
* Evidence: The research says the model chooses and sequences sentences;
  src/core/src/zava_forward/core/resident_assistant.py already supplies fixed
  status/documents/forms answers. Existing architecture explicitly calls the
  old selector low-value. The candidate specifies no selection examples or
  task-quality acceptance beyond valid IDs.
* Concern/impact: Reordering a fixed answer can remain an expensive echo.
  Valid IDs alone also permit omission or ordering that misrepresents unknown,
  closed or next-step facts. No supplied owner decision explicitly accepts
  sentence selection as sufficient advisory capability.
* Smallest useful change: Define the bounded selection task, catalogue rules,
  mandatory semantic units and worked contrasting cases. Require useful
  context-sensitive explanation without exposing untrusted prose, including
  documents-unknown and generic-form limits.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T02 with expected selections and
  resident-facing answers; evaluation cases for open/closed/unknown states,
  unsafe omissions/order, eligibility requests and all three topics; explicit
  pass criteria distinguishing useful inference from topic echo.
* Decision route: Direct planner correction first. Owner decision only if
  useful advisory inference cannot fit the boundary: accept a reduced selector
  scope or separately authorize a different bounded approach. Do not silently
  choose either or introduce unrestricted prose.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The one-cent reservation lacks an auditable cost envelope

* Related IDs: Hard USD20 requirement; NFRs; P01-T01/T02; research W2.
* Evidence: Research prices regional nano and assumes <=4096-byte prompt plus
  <=256 output tokens; the plan does not define whether that limit includes
  all instructions, catalogue, schema and message overhead.
* Concern/impact: A count of 2000 attempts is a hard monetary ceiling only
  when every possible request is provably below USD0.01. The mapping among
  regional SKU, model/version, API request and tariff is not pinned in the
  acceptance contract.
* Smallest useful change: Specify the complete priced wire envelope, conservative
  input-token/overhead bound, output/completion parameters and arithmetic.
  Reject incompatible deployment/version/configuration or expired tariff
  approval before credentials/transport. Define which deployment callers the
  application ledger can control; do not claim a subscription-wide cap.
* Action owner: Planning parent.
* Exact resolving evidence: Dated tariff/SKU record and calculation showing
  maximum per-attempt charge <=USD0.01; exact-payload boundary tests, immutable
  USD20 ceiling tests, and documented ledger scope including any live smoke
  calls. No unaccounted diagnostic inference.
* Decision route: Direct planner correction; USD20 is already decided.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Durable reservation lifecycle needs executable SQL tests

* Related IDs: P01-T01; P03-T01; retained failures/concurrency acceptance.
* Evidence: Details name reserve/complete procedures and serializable global
  locking, but P03 chiefly promises SQL text/contract checks and defers real
  SQL integration to activation.
* Concern/impact: Text assertions cannot establish committed-before-HTTP
  reservations, no overspend under contention, or survival of ambiguous commit,
  process death, completion failure and migration reapplication. Completion
  must not release spend or allow a reservation to fund repeated transport.
* Smallest useful change: Specify fixed integer-cent limits and the reserve,
  commit, single-dispatch, complete state contract; no auto-retry of ambiguous
  reservations. Make new accounting integration selectors exercise the actual
  procedures in the existing isolated SQL harness before acceptance.
* Action owner: Planning parent.
* Exact resolving evidence: Planned real-SQL tests at 1999/2000 accepted
  reservations, concurrent last-cent and fifth-per-resident attempts, rolling
  window boundaries, crash/restart, commit-response loss, duplicate completion,
  completion outage and idempotent migration with a nonzero balance. Failure
  paths retain reservations and make no extra model calls.
* Decision route: Direct planner correction. Missing local SQL prerequisites
  block the applicable gate; cloud activation is not a substitute.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Existing permission verification rejects accounting grants

* Related IDs: P01-T01; P02-T02.
* Evidence: infra/scripts/resident_showcase_sql.py verify_rights permits only
  CONNECT and SELECT on resident_showcase.v_resident_case. Proposed EXECUTE
  grants on two resident_ai procedures fall outside that allowlist.
* Concern/impact: Reusing the existing Entra administrator tooling without a
  deliberate verifier migration makes later apply/verification reject the
  legitimate identity. Broadening the verifier indiscriminately would weaken
  the resident data boundary.
* Smallest useful change: Name the accounting migration/helper and narrowly
  reconcile the verifier with exactly the two procedure grants. Preserve all
  base-table, role, ownership, public and direct-write restrictions.
* Action owner: Planning parent.
* Exact resolving evidence: Planned verifier tests accepting only CONNECT,
  resident-view SELECT and the two exact EXECUTEs; rejecting extra procedure,
  schema/table grants and grant-option permissions. Real-SQL execution under
  the resident principal proves procedures work while direct accounting writes,
  case mutations and unauthorized reads remain denied; reapply remains valid.
* Decision route: Direct planner correction; no new Azure role is needed.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Startup and request wiring need one explicit end-to-end contract

* Related IDs: P01-T01/T02; P02-T01.
* Evidence: src/api/src/zava_forward/api/resident_demo/__main__.py constructs
  ResidentDemo without a provider. core/resident_showcase.py rejects ZF_AI,
  AI_ and AZURE_OPENAI environment prefixes. The current Provider accepts only
  Topic, not case or accounting context; the HTTP handler currently returns
  503 on provider failure.
* Concern/impact: An adapter can pass isolated mocks yet remain unreachable
  from startup, lack a trusted resident accounting key, or continue returning
  errors rather than deterministic fallback.
* Smallest useful change: Specify namespaced validated activation settings,
  endpoint/deployment/identity binding, ledger adapter ownership and trusted
  per-request accounting context. Preserve legacy defaults and unrelated
  forbidden settings. Separate model failure fallback from authorization
  failure, which must not disclose a stale case.
* Action owner: Planning parent.
* Exact resolving evidence: Startup-composition tests for default rules,
  explicitly configured MI provider and missing ledger fallback; HTTP tests
  proving reserve-before-token/transport, labelled 200 rules fallback on
  provider/accounting failure, and denial after logout/revocation/expiry during
  both successful and failing inference. Tests must use the real composition
  factory/entry point, not only manually injected callbacks.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Session-derived rate-limit identity can reset on key rotation

* Related IDs: Per-resident limit; P01-T01.
* Evidence: core/resident_showcase.py SessionCodec.handle derives its handle
  from the session signing key and case ID. Details require a stable handle
  from a verified session but do not define its rotation behavior.
* Concern/impact: Separate logins share a handle, but signing-key rotation
  changes it. Persisting the session handle therefore does not automatically
  preserve a per-resident rolling-hour limit across all redeployments.
* Smallest useful change: Define the trusted canonical accounting identity and
  its stable pseudonym/rotation policy without new secrets or Azure roles.
  State that identity represents the synthetic resident mapping, not verified
  real-person identity.
* Action owner: Planning parent.
* Exact resolving evidence: Tests for repeated logins, process restarts,
  signing-key rotation and concurrent instances sharing the same resident
  allowance, plus distinct residents retaining independent limits.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Bicep compilation does not prove deployment safety

* Related IDs: P02-T01; P03-T01; default-off/no-other-roles requirements.
* Evidence: Details promise enable=false and a scope guard; acceptance primarily
  requires compilation. Existing infra/resident-demo.bicep also manages ingress,
  the app, identity and unrelated role assignments and must not be reused to
  provision this account.
* Concern/impact: A compilable standalone template can still create a disabled
  account's deployment/role, create or alter identity resources, or grant at
  excessive scope.
* Smallest useful change: Add compiled-template policy tests for both enable
  states and reviewed deployment parameters; reference the existing identity.
* Action owner: Planning parent.
* Exact resolving evidence: Disabled template has no deployable account,
  deployment or role; enabled template has only dedicated account, pinned
  regional Standard deployment and its one account-scoped OpenAI User role,
  with keys/local auth disabled, no auto-upgrade/dynamic quota, correct
  principal and ama guard. No group, app, ingress, identity or unrelated role
  creation/update; recorded live parameters match the reviewed template.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Budget renewal is not service-authority renewal

* Related IDs: User decisions; expiry fallback; P01/P02.
* Evidence: Plan records funding through 2026-12-31 but leaves expiry unspecified.
  Existing core AUTHORITY_END/configuration, provider EXPIRES and showcase SQL
  allowlist constraint stop at 2026-11-01T00:00:00Z.
* Concern/impact: Different implicit expiry choices can disable new inference
  unexpectedly or extend resident access beyond existing approval.
* Smallest useful change: State separate exact UTC budget, inference and
  resident-access expiries; preserve the existing access boundary unless
  separately authorized. Make transport obey the earliest applicable expiry
  and keep the lifetime ledger independent of those dates.
* Action owner: Planning parent.
* Exact resolving evidence: Revised expiry matrix and tests immediately
  before/at each boundary, including expiry during token acquisition/inference.
  Documentation explicitly states that December funding does not extend the
  showcase SQL/session window.
* Decision route: Direct correction under existing authority. Only an intended
  extension of resident access requires an owner decision.

<!-- rpi:critique id=PC-009 -->
### PC-009 [High]: Provisioning success is not live resident inference

* Related IDs: Real Azure OpenAI requirement; P02-T02; P03; research Risks.
* Evidence: Research reports null ingress, a deployed revision lacking the new
  code/ledger, unproven quota and uncertain private SQL reachability. Plan
  excludes production activation and app changes from the new infra module.
* Concern/impact: Resource listings or unauthenticated probes cannot demonstrate
  managed-identity inference through the new authorized resident path. A
  deployable implementation may be delivered without satisfying a live-use
  interpretation of #469.
* Smallest useful change: Split acceptance into local implemented capability,
  actual account/deployment provisioning, MI/accounting readiness and
  authenticated resident inference. Mark each observed/not run/blocked with
  its prerequisite; define a safe metered smoke if already authorized and
  reachable. Do not alter ingress or use a developer token to simulate MI.
* Action owner: Planning parent; owner only for additional activation authority.
* Exact resolving evidence: Dated resource/SKU/version and quota outcome;
  SQL migration and principal verification; exact running image/configuration;
  successful MI inference with ledger debit and safe output; authenticated
  own-case smoke only with an available authorized session. Otherwise retain
  explicit blocked rows and no live-success/whole-issue-complete claim.
* Decision route: Direct planner correction to acceptance/reporting. A new
  rollout or access path outside current authority requires owner decision;
  blockers do not authorize ingress, role or group changes.

## Strengths and Residual Risk

* Fixed topics and locally rendered approved sentences avoid displaying
  arbitrary model prose. Missing document facts stay unknown; specialist,
  eligibility, form submission and consent authority remain excluded.
* Permanent conservative reservations, no refunds/retries, dedicated regional
  Standard capacity, managed identity and rules fallback are credible choices
  once the above contracts are evidenced.
* No quota, network reachability, actual resident identity, privacy approval,
  production acceptance or hosted/human approval is established by this plan
  or critique. These limitations are not failures to be bypassed.

## Questions or Blocking Evidence Gaps

No immediate owner response is required for direct plan corrections. If the
bounded selection task cannot demonstrate meaningful advisory value, or
delivery requires extending resident access/authorizing a live rollout, the
planning parent must surface that specific decision rather than presume it.

## Limitations

No Azure provisioning, pricing reproduction, model call, SQL execution,
implementation test or publication gate was performed. Findings are planning
gaps grounded in supplied evidence and relevant source, not observed defects
in an implementation that does not yet exist.

## Recommended Next Action

* Highest-impact finding: PC-002, auditable hard-cap envelope.
* Action owner: Planning parent.
* Smallest next action: Revise the cost envelope and acceptance tests, then
  disposition all PC findings in the plan/details before implementation.
* User response required: No for direct corrections; only the conditional
  scope/authority choices identified above.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/resident-assistant-aoai-research.md](.copilot-tracking/research/2026-10-27/resident-assistant-aoai-research.md) | Supplied research and uncertainty. |
| [.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-plan.md](.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-plan.md) | Assessed final candidate. |
| [.copilot-tracking/details/2026-10-27/resident-assistant-aoai-phase-details.md](.copilot-tracking/details/2026-10-27/resident-assistant-aoai-phase-details.md) | Assessed task details. |
| [.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-critique.md](.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-critique.md) | This single independent critique. |

## Next Steps

Active planning parent: revise and disposition PC-001 through PC-009 directly,
obtain an owner decision only if a conditional scope change is necessary,
then finalize without a second critique. No implementation was performed and
no user action is required for the direct revisions.
