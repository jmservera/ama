<!-- markdownlint-disable-file -->

# Task Research: setup-profile-evidence-360

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-17/setup-profile-evidence-360-research.md |

## Research Brief

* Research target: distinguish resource-bound profile-neutral patches from omitted production defaults in actual ARM deployment contracts.
* Purpose and audience: restore owner laptop demo-roster safety classification without weakening production refusal.
* Scope: infra setup classifier, existing helpers, Bicep contracts, setup/staff tests and directly related runbook.
* Non-goals: Azure/Graph/SQL writes, cloud jobs, private data, tag changes, public service changes, full setup acceptance.
* Criteria: explicit bound development plus test/demo/dev evidence; reject genuine production, unknown, malformed, contradictory and failed evidence.
* Requested outputs: cited research, plan/critique, failing-first regression, implementation and one Review.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Q1 ARM effective parameter/default contract; Q2 binding and neutral detection; Q3 preserved refusal and validation boundaries |
| Codebase scope | infra/scripts, infra/tests, infra/main.bicep, infra/modules |
| External scope | Official Microsoft ARM deployment REST/schema documentation |
| Initial internal candidates | require_demo, deployment readers, main/module defaults, setup tests |
| Initial external candidates | ARM deployments get/export-template and parameter schema |
| Research posture | focused |
| Provenance | Bounded caller source defect and supplied live evidence |
| Explicit limits | No remote writes; up to two concrete correction cycles; original Review unchanged |
| Completion basis | All material contract/classification questions evidenced |
| Edits allowed | Research and required workflow tracking only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Selection and scoped authority |
| --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Repository-wide evidence, branch, privacy and test conventions |
| Skill | rpi-research | Selected; three ordered research waves |
| Specialist | hve-core-all:rpi-researcher | Skipped; one tightly coupled bounded trace handled inline |
| Skill | security/accessibility/design | Skipped; not a security audit or web change |

## User Participation and Research Decisions

Owner supplied sufficient criteria and explicit full ordered execution; no clarification needed.
Existing clean branch fix/setup-profile-evidence-360 equals fetched origin/main
1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c; no open PR for this branch.

## Scope and Success Criteria

Preserve all existing credential, API-selection, Key Vault, private service,
read-only job refusal and roster behavior outside profile classification.
Supplied live observations are coordinator-reported, not fresh observations here.

## Direction Controls

* Source-only, no mutating setup, no private datasets, no other dirty worktrees.
* No deletion, rebase, force push or merge; main PR references #360 without closing it.
* Names, purpose or direct ingress alone cannot authorize development.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How do ARM deployment values and template defaults differ? | depth | Answered |
| Q2 | How can neutral app patches be distinguished without ignoring unknown/conflict evidence? | depth | Answered |
| Q3 | Which existing tests and restrictions must remain unchanged? | straightforward | Answered |

## Prior Knowledge Gate

Read original case study, addendum, reference index and memory; memory is context,
not evidence. Supplied failure explanation needs source verification. Infra README
and test inventory identified; current main includes merged #385 compatibility.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Opening: inspect existing classifier, prior helpers, Bicep defaults and ARM schema.
No delegated lane; isolated parallel research would duplicate this continuous trace.
Reflection: C1/C2 confirm the unconditional production injection; C3 distinguishes
the containerapps tags contract. W1 says deployment history is not the template:
its properties contain parameter values, links/hash, state and output resource IDs.

#### Wave 2: Deeper

Prioritized Q1/Q2: W2 establishes that defaultValue belongs to the parameter
declaration and applies only on omission. W3 describes exportTemplate and W4
confirms Azure CLI exports the raw result.template, not its REST wrapper.
The CLI operation is metadata retrieval despite REST's POST verb; no deployment,
resource write or remote URL following is needed. Relevant default expressions
cannot safely be evaluated by this bounded classifier and must remain unknown.
Reflection: resolve recognized deploymentProfile/environmentName/tags values
against each exact bound deployment's exported declarations. Neither current
local main.bicep nor the deployment name establishes a historical contract.

#### Wave 3: Contrarian

Challenge targets: deleting the production branch would accept a full template
whose profile defaults to production; accepting only module tags can hide that
same default; empty/null parameter structures can be confused with absence;
unrelated successful development outputs cannot authorize the selected resources.
C4's existing tests cover explicit conflicts but encode arbitrary omission as
production and accept null tags on a bound deployment. Update that coupled
expectation to reject malformed relevant data rather than silently coerce it.
Also verify fetched environment identity before using its tags.
Reflection: exported neutral templates contribute no authorization, but cannot
fabricate production. Resource tags or exact bound explicit/default values
must still establish development and a safe environment. Failed bound history
and failed/unavailable export refuse before roster/Graph/SQL work.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Resolve actual contract, not omitted-name heuristic | C1-C3, W1-W4 | Accepted | Preserves neutral patches and true production defaults |
| Ignore every deployment without explicit profile | C1, W2 | Rejected | Loses real default-production conflicts |
| Trust direct ingress, purpose or resource name | C2, owner criteria | Rejected | No authoritative profile evidence |
| Evaluate arbitrary ARM expressions | W2 | Deferred | Unnecessary interpreter; fail closed instead |
| Fetch templateLink URI | W1/W3 | Rejected | Export retrieves historical template without arbitrary remote fetch |

#### Cycle Re-entry Evaluation

No further cycle needed: named contract sources, helpers, failure cause and
contrarian cases cover the bounded question. Live readback remains unperformed
and is not needed to verify parser behavior.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | infra/main.bicep:84, infra/main.bicep:132 | Main defaults production, propagates profile/environment tags |
| C2 | infra/scripts/setup-entra.py:568-612 | Bound history checked, but omission injects production independently of template |
| C3 | infra/modules/containerapps.bicep:1-3, infra/modules/containerapps.bicep:58 | Module accepts tags object, no deploymentProfile declaration |
| C4 | infra/tests/test_setup_entra.py:835-898 | Existing unknown/conflict/binding/default tests and null-tags coercion |
| C5 | infra/README.md:895-905, infra/README.md:1550-1602 | Editable source distributions, infra suite and unchanged admin/random-roster boundaries |
| C6 | infra/scripts/credential_arm.py:72-99 | Existing profile-neutral metadata/deployment shape; no reusable parameter-default resolver |
| W1 | https://learn.microsoft.com/en-us/rest/api/resources/deployments/get?view=rest-resources-2025-04-01 ; retrieved 2026-10-17 | DeploymentPropertiesExtended has values/state/outputResources, not inline template |
| W2 | https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/parameters ; retrieved 2026-10-17 | Types, secure omission and defaultValue/expression contract |
| W3 | https://learn.microsoft.com/en-us/rest/api/resources/deployments/export-template?view=rest-resources-2025-04-01 ; retrieved 2026-10-17 | Exports the template for the specified deployment, result.template |
| W4 | https://raw.githubusercontent.com/Azure/azure-cli/dev/src/azure-cli/azure/cli/command_modules/resource/custom.py ; export_deployment_as_template, retrieved 2026-10-17 | CLI prints json.dumps(result.template), raw template object |

## Findings, Alternatives and Decision State

Selected: a small setup-local resolver for three recognized contract parameters,
with strict value/declaration/container guards and literal defaults only. Read
each successful exact-resource-bound deployment's template using group export;
retain all independent app/environment/history conflict checks. No new package
or generic ARM evaluator. One sanitized actionable error on unknown contract.

Supplied coordinator shape is the regression fixture, not claimed fresh live
evidence: API lacks profile; environment has development/test; neutral staging
touches API; containerapps module has development/test tags; demo-env has
development/test parameters.

## Open Questions, Risks and Residual Uncertainty

* Export authority may be missing or historical template unavailable: refuse,
  do not invent a classification. Additional metadata call is intentional.
* Live credential access, initializer publication 403 and #360 d/e remain unmet.
* Historical conflicts deliberately continue to veto, not latest-wins.
* No actual Azure setup, Graph mutation, SQL, Docker or deployment is authorized.

## Self-check

All three waves executed inline in order; source and external contract evidence
recorded; alternatives challenged; no source edits or remote mutations performed.

## Planning Readiness

Ready. Research disposition: executed, complete. Parent next action: Plan with
one final-candidate independent critique, then Implement and one Review under
the owner's explicit full ordered execution direction.
