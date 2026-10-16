---
title: Bicep quality gates 139 final-candidate plan critique
description: Independent bounded assessment of offline infrastructure gate coverage
ms.date: 2026-10-16
---

## Metadata

* Task ID: #139
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/bicep-quality-gates-139-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/bicep-quality-gates-139-phase-details.md
* Critique execution status: Complete
* Execution count: One independent final-candidate assessment.

## Inputs and Criterion Boundary

* Caller requirements: offline endpoint, no keys/listKeys, Entra-only SQL,
  purge, immutability, production isolation, named unsupported-combination
  checks and in-memory mutations using the same clean-template assertions.
  Preserve source and legacy workflow/job/check identities.
* Research: .copilot-tracking/research/2026-10-16/bicep-quality-gates-139-research.md,
  claims C1-C9, checked against the relevant existing infrastructure evidence.
* Primary evidence: infra/tests/test_bicep_policy.py,
  infra/tests/test_edge_module.py, infra/tests/test_iothub_module.py,
  infra/tests/test_identity_rbac.py, infra/main.bicep,
  infra/bicepconfig.json, infra/modules/privateEndpoint.bicep,
  infra/modules/network.bicep, infra/modules/storage.bicep,
  infra/modules/authTokenStore.bicep, infra/modules/monitoring.bicep,
  infra/modules/containerapps.bicep, infra/modules/sql.bicep,
  infra/modules/guard.bicep, .github/workflows/src-ci.yml and
  .github/workflows/mvp-validation.yml. Other service-module control and
  endpoint declarations were inspected through a bounded Bicep search.
* Context: infra/README.md, docs/adrs/0006-src-layout-and-cutover.md,
  docs/case_study_48_original.md, docs/case_study_48_addendum.md,
  docs/reference/README.md and docs/reference/memory.md.
* Decisions and dependencies: reuse the existing unittest suite and linter;
  add source gates within the existing namespace job; retain legacy gates;
  use pip for missing Python distributions/tools. P02 validation depends on
  P01 implementation. Publication follows successful validation and review.
* Exclusions: #138, deployment, Azure resource queries, live ARM/network
  validation, policy locking, legal retention decisions and wider security
  auditing. No private dataset, environment files, editor configuration or
  issue-tracking cache was accessed. No additional agents were used.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Endpoints; C6/C8; P01-T01 | Covered | Service-specific group, target, subnet, DNS and actual endpoint wiring are explicitly required, including the optional token store. This addresses the current aggregate-group weakness and complements existing source-based DNS coverage. |
| No keys/listKeys; C1/C8; P01-T01 | Covered | Existing forbidden-function and credential checks are retained, with explicit IoT Hub and nested Log Analytics local-auth coverage added. Same-assertion mutation evidence is required for requested controls. |
| Entra-only SQL; P01-T01 | Covered | Existing compiled assertions require azureADOnlyAuthentication and forbid administrator login/password; no test removals are permitted. SQL mutation coverage is an acceptance criterion. |
| Purge; C4; P01-T01 | Covered | Existing tests cover the vault property and main-to-module forwarding. The exhaustive profile/public/purge matrix and mutation requirement strengthen these checks. |
| Immutability; C5-C7; P01-T01/P01-T02 | Covered | Exact audit-archive and ledger-digests targets, positive constrained retention and audit minValue(1) are required. Unlocked policies remain explicitly distinguished from locked WORM/legal acceptance. |
| Production no public; C4/C6; P01-T01 | Partial | The input matrix tests profile intent, but the candidate does not explicitly close missing public-access properties/module arguments or compiled Container Apps internal/SQL firewall-condition gaps. See PC-001. |
| Named unsupported combinations; P01-T01 | Covered | Exhaustive profile/public/purge combinations plus edge/pilot positive and negative guard cases are explicit. Existing SharePoint, token-store readiness, role-map, guard constraints and guard dependency tests remain in scope. |
| In-memory mutations; P01-T01/P02-T01 | Covered with PC-001 qualification | Deep copies must fail the same assertions used for clean compiled JSON; no fixture-only or source-mutation shortcut is allowed. Public isolation needs the more precise negative set below. |
| CI identity preservation; C3; P01-T02/P02-T01 | Covered | Source workflow retains namespace/src-namespace and other existing jobs; the legacy MVP validation workflow, validate job and steps are preserved. Infra triggers and all-file build/lint coverage are explicit. |
| Offline/pip/private-file boundaries; P01/P02 | Covered | No deployment or #138 work; pip-installed editable distributions, required compiler failure, isolated scoped ruff, no committed compiled snapshots and protected-file exclusions are explicit. |
| Documentation and delivery; P02-T02 | Covered | README limitations, append-only log, one review, privacy-safe commit identity, trailer and Refs #139 publication are specified without authorizing deployment or merge. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The candidate is otherwise credible and appropriately bounded.
  One planner-owned clarification is needed to prevent a production-isolation
  gate from passing when a required property or parameter is absent. This is
  distinct from validating that the profile computes false or rejects an
  unsupported input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Make production isolation assertions presence-sensitive and cover compiled network gates

* Related IDs: production-no-public requirement; C4/C6; P01-T01; P02-T01.
* Evidence: infra/tests/test_bicep_policy.py,
  test_every_public_access_setting_follows_the_single_switch checks properties
  only when present and requires an aggregate count of at least eight.
  test_every_module_gets_the_computed_public_access likewise checks only
  modules that still contain the argument.
  test_production_profile_has_no_public_access evaluates the computed
  variables, not every resource's resulting access gates.
  infra/modules/monitoring.bicep alone has four public-access properties;
  enough other services exist that deleting one property's assertion target
  need not breach the aggregate threshold.
  infra/modules/containerapps.bicep also uses
  vnetConfiguration.internal, and infra/modules/sql.bicep conditionally
  creates dev-external-access.
  infra/tests/test_edge_module.py checks the Container Apps internal
  expression through source text, not the compiled object passed to an
  in-memory mutation assertion.
* Concern: P01-T01 specifies per-service endpoint completeness, but only
  profile/public/purge input enumeration for public isolation. It does not
  explicitly require a per-resource inventory of required public properties
  and main-to-module arguments, or compiled assertions for internal
  Container Apps mode and conditional wide-open SQL firewall creation.
  Thus it leaves a concrete route to retain the current presence-conditional
  checks while satisfying an input matrix and a literal-Enabled mutation.
* Impact: Removing publicNetworkAccess or its module argument can evade the
  compiled gate without proving the resulting service default is private.
  Mutating internal mode or the development firewall condition is not
  rejected by the same compiled assertions. A passing offline result would
  therefore provide incomplete evidence for the stated production-isolation
  requirement. This is a gate-coverage concern, not a claim that the current
  templates expose production resources.
* Smallest useful change: Extend P01-T01 to require explicit required-property
  and forwarding inventories for all current network-switch services,
  including auth-token-store and both monitoring ingestion/query settings.
  Assert required entries exist before checking expressions. Include the
  compiled Container Apps internal expression and development-only SQL
  firewall condition. Specify deep-copy mutations deleting a required
  access property, deleting a forwarding argument, forcing public access,
  forcing external environment mode and removing/forcing true the firewall
  condition. Each mutation must exercise the corresponding clean-template
  assertion. Do not prohibit the deliberately supported Front Door edge or
  mistake application ingress.external for environment public exposure.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 explicitly names those presence and
  compiled network-gate assertions and mutations; P02-T01 requires their
  recorded rejection results. During implementation, the clean compiled
  baseline must pass those same helpers, each named deep-copy mutation must
  fail its intended assertion, and the full infra suite with
  REQUIRE_AZ_BICEP=1 must pass. No Azure validation is required to resolve
  this planning finding.
* Decision route: Direct planner correction. Existing user direction already
  requires production isolation and regression-sensitive offline checks; no
  significant or divergent user decision is needed.

## Strengths and Residual Risk

* Extending the current suite rather than introducing a policy engine is
  proportionate. Existing checks and error-level rules are preserved.
* Endpoint ownership, actual DNS/connection wiring, exact immutable-container
  targets and positive retention bounds directly address the research gaps.
* Conditional token-store resources remain covered even when disabled by
  default; all Bicep files, including governance and optional modules, must
  build and lint rather than relying solely on the default main graph.
* Adding gates within the existing source namespace job respects CI identity
  constraints without creating the out-of-scope deployment pipeline.
* Offline assertions establish template intent and mutation sensitivity, not
  Azure acceptance, live DNS/routing, guard-message behavior in ARM, locked
  retention or production readiness. These limitations are explicitly
  retained, not implementation blockers for this slice.

## Questions or Blocking Evidence Gaps

* None requiring a user answer. The supplied evidence supports a complete
  bounded credibility assessment and a direct planner correction.

## Limitations

* This is a plan critique, not implementation acceptance. No compiler, test,
  linter, installation, deployment or network operation was executed.
  Research's Bicep 0.48.1 baseline and missing-distribution diagnosis were
  treated as supplied evidence, not independently rerun results.
* No remote issue/PR lookup was performed. Caller-supplied issue scope and
  CI preservation requirements define the acceptance boundary.
* Existing untracked planning inputs were left unchanged on
  feat/bicep-quality-gates-139. Only this requested critique artifact was
  written. Missing guessed evidence paths were not used as evidence.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the presence-sensitive public-isolation assertion
  and mutation contract to P01-T01, with matching P02-T01 evidence.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/bicep-quality-gates-139-plan.md](.copilot-tracking/plans/2026-10-16/bicep-quality-gates-139-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-16/bicep-quality-gates-139-phase-details.md](.copilot-tracking/details/2026-10-16/bicep-quality-gates-139-phase-details.md) | Task-level correction target |
| [.copilot-tracking/research/2026-10-16/bicep-quality-gates-139-research.md](.copilot-tracking/research/2026-10-16/bicep-quality-gates-139-research.md) | Supplied bounded research |
| [.copilot-tracking/reviews/2026-10-16/bicep-quality-gates-139-plan-critique.md](.copilot-tracking/reviews/2026-10-16/bicep-quality-gates-139-plan-critique.md) | Complete single-pass critique |

## Next Steps

The active planning parent should resolve PC-001 directly and record its
disposition before finalizing. No user action or additional critique pass is
required. This critique stops here.
