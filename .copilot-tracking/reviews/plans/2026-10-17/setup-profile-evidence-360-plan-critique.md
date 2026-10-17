<!-- markdownlint-disable-file -->
# RPI Plan Critique: setup-profile-evidence-360

## Metadata

* Task ID: issue-360-followup
* Task slug: setup-profile-evidence-360
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/setup-profile-evidence-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/setup-profile-evidence-360-phase-details.md
* Critique execution status: Complete
* Execution boundary: exactly one final-candidate critique; no implementation or additional review.

## Inputs and Criterion Boundary

* Caller requirements: neutral resource-bound staging must not fabricate production; actual omitted production defaults must veto; authoritative development and dev/test/demo evidence remain mandatory. Production, unknown, conflict, failure, malformed/null data, inaccessible exports and incorrect binding must refuse safely.
* Preserved decisions: no safety inference from names, purpose or ingress; preserve #385 API selection and read-only cloud-job refusal, Key Vault/private-service restrictions, first-ProgrammeManager admin mapping and distinct seeded assignment.
* Supplied research: .copilot-tracking/research/2026-10-17/setup-profile-evidence-360-research.md, particularly Q1-Q3, C1-C6 and W1-W4.
* Source evidence inspected: infra/scripts/setup-entra.py, infra/tests/test_setup_entra.py, infra/tests/test_staff_azure.py, infra/main.bicep, infra/modules/containerapps.bicep and infra/README.md.
* Repository context consulted: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory is context, not evidence.
* Dependencies assessed: source distributions installed before tests, metadata export authority, exact selected subscription/resource binding, single-critique disposition before implementation and one later implementation Review.
* Acceptance boundary: credibility of the proposed source/test/documentation work, not proof that code is implemented, tests pass, live permissions work or #360 d/e are accepted.
* No Azure operations, Graph operations, private datasets, application tests, dependency installations or production-file edits were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Neutral bound staging; Q1-Q2; P01-T02 | Covered | Resolve the actual exported declaration before assigning a default. An undeclared, absent recognized parameter is neutral, not production. |
| Genuine production defaults; C1, W2; P01-T02 | Covered | infra/main.bicep:84 declares production. Explicit values take precedence; omission uses the historical declaration's literal default. Independent development tags cannot erase production evidence. |
| Authoritative development and safe environment; P01-T02 | Covered | Neutral evidence supplies no approval; both profile and environment evidence remain necessary. No naming, purpose or ingress shortcut is proposed. |
| Exact binding and history failures; Q2; P01-T02 | Covered | Only selected-app/bound-environment outputResources qualify; relevant state must be Succeeded. Environment readback identity must equal the bound ID. |
| Raw CLI export schema; W3-W4; P01-T01/P01-T02 | Covered | Details expressly require raw CLI shape and the exact list-returned deployment name through the existing subscription-scoped wrapper. Cited CLI implementation independently confirmed during this critique. |
| Unknown, malformed/null, unresolved and failed evidence; P01-T02/P02-T01 | Covered | Container/value/declaration guards, required-value/default refusal, ARM-expression refusal and export failure cases are explicit. Present null tag values must not disappear. |
| Independent conflict retention; Q3; P01-T02 | Covered | Both deploymentProfile/tags-profile and environmentName/tags-environment are collected, with resource/environment contradictions retained. |
| Actual supplied failing-first regression; P01-T01 | Covered | Direct require_demo call, app profile absent, environment development/test, neutral app stage and environment-bound module/main records. The before-fix assertion is captured before source edits. |
| Existing setup ownership and bounded additions; P02-T01 | Covered | Existing test_setup_entra ownership retained; no removals; at most 18 additional methods using subTest tables; null-tags bound-success expectation explicitly changes to refusal. |
| Practical regression evidence; P01-T01/P02-T01 | Covered | Editable core/agents/api/orchestrator installations precede fresh baseline and complete setup/staff suites; historical suite counts are not reused as fresh evidence. |
| #385, Key Vault, private services and admin mapping; P01-T02/P02-T01 | Covered | Non-classifier paths remain unchanged and complete existing suites remain required. Existing relevant tests are present in both named test files. |
| Minimal implementation and lint scope; P01-T02/P02-T01 | Covered | Three recognized contract parameters, no dependency or general ARM interpreter, existing Azure wrapper and focused changed-line checks alongside configured README checks. |
| Runbook and knowledge routing; P02-T02 | Covered | Correct the blanket omission claim in infra/README.md:1555, document export read authority and neutral-not-approval semantics, update existing route and append log. |
| Review, delivery and acceptance boundaries; P03 | Covered | One immutable implementation Review, honest residual/pending status, privacy-safe commit identity, main PR referencing rather than closing #360, no merge or history rewrite. |

## Verdict

* Verdict: Pass.
* Rationale: The plan and phase details together specify the smallest sound contract-aware repair and a bounded, practical regression strategy. The safety-critical alternatives are already resolved by the caller: neither ignoring omitted profile values nor assuming production for every omission is acceptable. The candidate distinguishes those cases using the actual deployment contract and retains contradictory-evidence vetoes.
* Severity summary: Critical 0; High 0; Medium 0; Low 0.
* This is planning acceptance only. It does not substitute for the failing-first result, implementation evidence, full suite results or the single later Review.

## Findings

No actionable PC-xxx findings. No substantive plan correction or unresolved significant user decision was identified within the supplied boundary. The implementation obligations below are already in the candidate; they are not deferred findings or additional scope.

## Contract and Smallest-Sound-Implementation Assessment

### Exact export and value/default contract

The supplied W4 source was read directly at its cited URL, restricted to
export_deployment_as_template. It calls the deployment export operation and
prints json.dumps(result.template, indent=2). Thus the existing Azure.call
JSON parser receives the raw ARM template object. The plan correctly avoids
expecting the REST response wrapper, deployment-list properties or local
current Bicep to contain the historical declaration.

The narrow contract is:

* Deployment history provides properties.parameters entries with value; exported template parameters provide declarations with type and, when present, defaultValue.
* Explicit recognized values are resolved first. A valid explicit value does not also activate that same parameter's unused default.
* Only omission activates a declared literal default. Missing required recognized parameters, malformed declarations/entries and unusable relevant expressions refuse.
* Absence of both a recognized value and its declaration is neutral. A malformed/null parameter structure is not equivalent to absence.
* The recognized tags object can contribute profile/environment independently of deploymentProfile/environmentName. Presence checks preserve null/unknown values for refusal; they must not use truthiness to erase contradictory evidence.
* A recognized production default remains evidence even when a different parameter or resource tag supplies development.
* Unrelated parameters do not require a generic evaluator. Export is by exact qualifying deployment name in ama through Azure.call, preserving its subscription handling. No templateLink fetch or deployment operation is needed.

These obligations are present across Functional Requirements and P01-T02;
they do not require another research or design decision.

### Resource and evidence boundary

infra/scripts/setup-entra.py:568-612 demonstrates the present unconditional
production injection and independent evidence aggregation. The candidate
changes the source of effective parameter evidence rather than introducing
latest-wins history, relaxing profile values or broadening API discovery.
Bound failed records and inaccessible/malformed bound contracts veto even
when resource tags are favorable. Unrelated development records cannot
authorize the selected resources.

The fetched environment must establish the requested identity before its
tags are trusted. Both selected app and bound environment evidence remain
subject to container/value validation. The caller's all-conflicts-reject
direction is preserved; no classifier authorization is granted by direct
ingress, names or purpose.

### Test feasibility and ownership

The reported three-deployment regression must use fictional values with
the supplied semantics, not claim a new live observation. Its direct
require_demo call isolates the defect from Graph/SQL and setup mutation
paths. FakeAzure must associate deployment names with raw exported
templates; legacy bound-history fixtures must retain their intended
contracts when that support is added.

The existing omitted-profile refusal case in
infra/tests/test_setup_entra.py:835-859 must continue to represent a real
production-default contract, not disappear when neutral behavior is added.
The null-tags success case at lines 861-873 is the explicitly authorized
expectation change. The existing bound-value/module-tag tests at lines
875-901 remain useful independent conflict checks.

The proposed additions fit the 18-method ceiling through table-driven
variants rather than one method per malformed case. Tables cover effective
values/defaults, neutral insufficiency, export/container failures, binding
and contradictions. Classifier refusal assertions must observe sanitized
SetupError/AzureError rather than incidental Python exceptions and record
metadata-only calls with no Graph/SQL/roster changes.

Complete existing suites are important, not redundant: setup fixtures also
exercise API selection, existing generated-roster reuse and admin mapping;
staff_azure covers cloud-job read-only and Key Vault/private transport
boundaries. Editable installation and fresh suite counts make the proposed
evidence practical without invoking live setup or Bicep compilation.

## Strengths and Residual Risk

* The main production default and module tags contract are both evidenced in source rather than inferred from deployment names.
* P01 isolates the failing-first observation before production changes; P02 requires full named suites and retains existing test ownership.
* No new runtime dependency, general ARM expression interpreter, cloud job or resource mutation is introduced.
* Missing export authority or unavailable historical templates remains an intentional fail-closed runtime limitation. The plan documents this prerequisite rather than promising universal historical recovery.
* Existing live credential, initializer-publication 403 and tenant/browser/SQL/AI gates remain explicitly unmet. Offline evidence cannot resolve them.
* P03 retains the original Review and reports residual work honestly; this Pass does not pre-approve findings or acceptance from that future Review.

## Questions or Blocking Evidence Gaps

None for this source-only planning boundary. Runtime export availability is
an acknowledged dependency with a specified refusal path, not missing
permission evidence that must be obtained through live Azure access now.

## Limitations

* Tests and implementation were not executed or inspected as completed work; their outcomes remain implementation-owned.
* The reported live resource/deployment shape is supplied fixture evidence, not independently observed tenant state.
* The CLI source verification used the supplied W4 dev-branch URL. No installed Azure CLI version or live export result was queried; the raw-object contract is the cited source behavior, not a live-version attestation.
* This artifact is the only intentional workspace write. Plans, details, research, existing review records and production files remain unchanged.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record this single critique's Pass disposition, then begin P01-T01 with installed editable distributions, fresh baseline and the actual-shape failing-first regression before source changes.
* User response required: no.
* Do not run another critique. Preserve the single later implementation Review and explicit live-unmet boundaries.

| .copilot-tracking/plans/2026-10-17/setup-profile-evidence-360-plan.md | Assessed final-candidate plan |
| .copilot-tracking/details/2026-10-17/setup-profile-evidence-360-phase-details.md | Assessed phase details and bounded test ownership |
| .copilot-tracking/research/2026-10-17/setup-profile-evidence-360-research.md | Supplied contract and source evidence |
| .copilot-tracking/reviews/plans/2026-10-17/setup-profile-evidence-360-plan-critique.md | This complete single critique |

## Next Steps

No user action is required. The active planning parent records the Pass
disposition and continues to P01-T01 under the existing ordered execution
authorization. This critique stops here without implementing, invoking
another stage or performing any additional critique/review.
