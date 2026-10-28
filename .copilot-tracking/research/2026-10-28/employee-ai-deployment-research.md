<!-- markdownlint-disable-file -->
---
title: Employee AI deployment research
description: Scoped model deployment and reproducible employee Bicep configuration
ms.date: 2026-10-28
---

## Research Brief

Restore the missing model prerequisite for employee assistance, without changing
the running app. Audience: coordinator and infrastructure reviewer. Output mode:
convergence preparing Plan. Posture: focused, selected from the named account,
failure evidence and strict current-user boundaries. Research root:
`.copilot-tracking/research/2026-10-28/`.

Criteria: parameterized small chat deployment in Bicep; consistent AI settings;
one minimal live model deployment; employee managed-identity access; local
tests/build; original critique and independent Review; pushed topic PR with Refs,
settings and USD30 additional AI authorization through 2026-10-31.

Non-goals: app updates/redeployment, resident infrastructure, paid inference,
other resources/roles, reading secrets/.env/private datasets, RG deletion,
issue closure, production or release acceptance.

## Research Parameters and Direction Controls

* User quote (2026-10-27): "Yes, create a small deployment and configure the
  employee app, make sure there are deployments in the bicep file too".
* Current narrower instruction explicitly defers live app configuration to the
  coordinator after #514 merges.
* `/tmp/brief-common.md` supplies the existing branch and local-only gate:
  no full `--all`; at most one scoped `--changed`, heavy lock timeout zero.
* Existing branch is clean and has no PR; one commit behind fetched main.
* Explicit full-loop request is automatic authorization at intake, not an
  inferred switch from an existing manual session. Interaction unavailable.

## Extension Registry and Provenance

Repository instructions and named brief selected. `rpi-research` selected for
evidence protocol; later phase skills remain parent-owned. Web/design,
regulatory-currentness and model-inference skills skipped: no web changes,
legal claim or inference. Specialists skipped: this is one coupled bounded
infrastructure trace; critique and final independent Review are separate gates.

## Prior Knowledge and Questions

PR #514 supplies a hypothesis, not fresh state: no model deployments and absent
AI environment variables. Verify actual availability rather than assume old
model versions remain purchasable. Questions: which minimum SKU/model is
available; how deployment outputs reach apps; which identity holds invocation
access; which existing tests validate the change; which approvals remain.

## Research Cycle Log

### Cycle 1 Wider

Inspected PR #514, issues #73/#360/#104, required case-study/index/memory,
infrastructure module/main/app wiring, existing policy and identity tests, and
safe Azure metadata. Existing infrastructure already defines two model tiers,
but the app binding hardcodes standard/capable and account output is the
generic Cognitive Services endpoint. Live account has zero deployments; the
queried gpt-4o-mini catalogue entry is absent. Reflection: do not deploy an
unavailable legacy model or duplicate the resident implementation; investigate
the available small models and retain opt-in API access.

### Cycle 1 Deeper

Corrected the CLI catalogue query: list-models returns flat model objects,
not nested `model` objects. gpt-4o-mini 2024-07-18 is available with
GlobalStandard; provider advertises chatCompletion and inference retirement
2027-04-14. Capacity minimum is unspecified, so request one and require actual
provider acceptance. Regional usage CLI returned zero entries, not proof of
quota. API selected identity has no OpenAI User assignment at account or
inherited scopes; the existing agent principal has one. Account local auth is
disabled and public networking disabled. ARM endpoints explicitly advertise
the requested openai.azure.com address. Reflection: add exactly the permitted
API account-scoped role, and keep private networking unchanged.

### Cycle 1 Contrarian

Compared Standard/GlobalStandard alternatives and runtime parameter support.
gpt-4.1-mini Standard is available, but gpt-4o-mini is the user's explicit
small example and fits the existing max_tokens/temperature chat contract.
New reasoning/nano models would require compatibility proof and are unnecessary
for this bounded request. Do not claim cheapest-ever pricing. A single model
can serve both logical tiers; that does not establish a capable-tier quality
threshold. Runtime AI_MODEL_VERSION expects provider response model identity,
not just the dated ARM version: gpt-4o-mini-2024-07-18. Reflection: output
deployment names and response-version bindings from the configured array,
preserve manual paths/release gates, and document no inference acceptance.

Parent synthesis: accept C1-C8/W1-W4; select a capacity-one gpt-4o-mini
GlobalStandard default with parameters for model/version/SKU/capacity, keep
the existing deployment-array override for multi-tier setups, derive app names
and model-version settings rather than hardcoding capable. Keep enableApiAi
false by default. No extra standalone resource template or cloud deployment
of the full stack is needed. Stop after one complete focused cycle: remaining
quota uncertainty is answered only by the explicitly authorized minimum
deployment operation; live inference and redeploy are excluded.

## Evidence Log

* C1: `infra/main.bicep:113` existing modelDeployments defaults: two
  GlobalStandard models at capacity 30.
* C2: `infra/main.bicep:359` app deployment-name binding is hardcoded.
* C3: `infra/modules/foundry.bicep:47` model resource loop already supports
  model/version/SKU/capacity and pins NoAutoUpgrade.
* C4: `infra/modules/containerapps.bicep:164` API AI settings gated by enableApiAi.
* C5: `infra/tests/test_identity_rbac.py:48` matrix checks cover every Bicep role.
* W1: Azure CLI safe read on 2026-10-28: account AIServices/S0 in uksouth;
  zero deployments. Initial nested-model filter falsely returned empty and
  was corrected with the flat schema; it is not model-unavailability evidence. ARM source:
  https://management.azure.com/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aif-cutover-test-rzsrg
* W2: Azure CLI app metadata read on 2026-10-28: API identity
  id-cutover-test-api, selected client ID 1b1fe44e-f4cf-4aae-98d0-b30c7927a5e3,
  principal 6ac4c6b9-c516-4e24-81a6-f32663a93aab; revision 0000006;
  AI_ENDPOINT/AI_DEPLOYMENT/AI_DEPLOYMENT_STRONG absent.
  https://github.com/jmservera/ama/pull/514 supplies historical context.
* C6: `src/core/src/zava_forward/core/ai.py:22` endpoint/deployment settings,
  selected identity, chat API 2024-10-21, max_tokens/temperature and exact
  provider-model identity validation. No application changes planned.
* C7: `infra/README.md:1139` existing install/build/infra discovery commands.
* C8: `docs/adrs/0002-pilot-readiness-architecture.md:124` and PRD PR-008
  preserve advisory AI/human decisions. Issues #73/#360/#104 remain broad
  unmet parent scopes, so PR references only; no criterion ticked.
* W3: Corrected model catalogue read on 2026-10-28 at W1 `/models`:
  gpt-4o-mini 2024-07-18 GlobalStandard, chatCompletion=true,
  lifecycle Deprecating, inference date 2027-04-14; no numeric minimum.
  CLI usage list returned [], so quota remains unproven until creation.
* W4: Account-scoped role list including inherited assignments on 2026-10-28
  at W1 `/providers/Microsoft.Authorization/roleAssignments`:
  no role for employee principal; agent principal has OpenAI User and Foundry
  User. Only missing employee OpenAI User assignment is authorized.

## Findings, Alternatives and Decision State

Selected approach and rejected alternatives are recorded in the cycle synthesis.
No live write or source implementation during Research. Inference, authorized
release binding, evaluation and private network reachability remain coordinator
follow-ups, not a reason to provision a second model or modify the app.

## Risks and Residual Uncertainty

Model catalogue, quota and region must be checked now. Minimal throughput is
not a spend cap. Release/evaluation bindings and human approval remain
independent from resource existence and app configuration.

## Planning Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Self-check: three ordered inline waves, sources and corrections preserved;
all material questions answered or bounded as execution-dependent evidence;
no delegation needed; no secrets or private datasets read.
