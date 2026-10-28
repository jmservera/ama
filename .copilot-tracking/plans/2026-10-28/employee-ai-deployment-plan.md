---
title: Employee AI deployment plan
description: Minimal employee model and derived infrastructure settings
ms.date: 2026-10-28
---

## Task Metadata

* Task ID: employee-ai-deployment-2026-10-28
* Task slug: employee-ai-deployment
* Status: Complete through one Review and requested PR publication; scoped
  gate failed preflight and is explicitly not accepted as a passing gate.
* Details: .copilot-tracking/details/2026-10-28/employee-ai-deployment-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-28/employee-ai-deployment-plan-critique.md

## Executive Summary

Provision one minimum-capacity gpt-4.1-nano deployment on the existing employee
account and make future Bicep deployments reproduce that small configuration.
Derive logical-tier names and provider model-version bindings from the actual
deployment configuration, with the Azure OpenAI endpoint rather than the
account's generic Cognitive Services endpoint. Preserve multi-model overrides,
default-off API AI and all approval/manual routes.

### What You May Not Know

The app's selected identity lacks the invocation role; add only its missing
account-scoped OpenAI User role. Both logical tiers will share one model, not
an evaluated stronger tier. A capacity of one limits throughput, not dollars.
Original gpt-4o-mini deployment was rejected as deprecating; the approved
fallback is gpt-4.1-nano 2025-04-14, accepted at capacity one. It is listed
Legacy with inference retirement 2027-04-14: a bounded exercise choice,
not a long-term model recommendation. No live app
change or inference is authorized here. Quota list is empty; creation success
must prove allocation rather than invent quota headroom.

## Sources

* .copilot-tracking/research/2026-10-28/employee-ai-deployment-research.md:
  Complete / executed / Ready; C1-C8 and W1-W4.
* /tmp/brief-common.md and current user request: scope, write and gate authority.
* PR #514 and issues #73/#360/#104: dependencies and broader unmet criteria.

## User Decisions and Requirements

* Owner decision dated 2026-10-27: "Yes, create a small deployment and configure
  the employee app, make sure there are deployments in the bicep file too".
* Current scope narrows live action to one deployment on aif-cutover-test-rzsrg
  in ama plus the employee OpenAI User role only if absent.
* Do not modify/redeploy ca-cutover-test-demo-api; coordinator acts after #514.
* No keys, secrets/.env, private datasets, resident resources, other roles,
  group deletion or direct-main push.
* Include local Bicep/infra validation, commands/results, exact AI_* handover,
  USD30 additional AI authorization through 31 October, and a Refs-only PR.
* Full loop and dated committed artifacts required; explicit brief forbids
  full --all gate and permits at most one scoped --changed under timeout-zero lock.

## Goals

* Remove the absent employee model prerequisite with the smallest deployment.
* Prevent model definitions and app configuration from drifting in future Bicep.

## Scope and Non-Goals

Source scope: infra/main.bicep, modules/foundry.bicep,
modules/containerapps.bicep, existing infra/tests/test_bicep_policy.py,
infra/README.md and dated RPI artifacts. No source app edits, new dependency,
new entry point or generated compiled JSON committed.

Live scope: exact existing account child deployment standard plus exact
employee account role. No full ARM stack operation, resource creation outside
that child/role, networking change, app update, live inference or release change.

## Functional Requirements

* Scalar parameters for chat model name, dated version, Standard/GlobalStandard
  SKU and positive capacity; default gpt-4.1-nano/2025-04-14/GlobalStandard/1.
* Existing modelDeployments override remains; require nonempty array. Default
  contains one standard deployment. First entry serves standard; second (or
  first if single) serves capable. Document positional binding.
* Foundry outputs dedicated OpenAI endpoint plus derived names and provider
  response-model versions. Preserve its existing generic endpoint/project
  outputs for other workloads. Add dedicated app OpenAI endpoint and version
  parameters; API settings remain gated on enableApiAi.
* NoAutoUpgrade and Microsoft.DefaultV2 remain; no key authentication.

## Non-Functional Requirements

* Existing resource/network/profile/auth/scale behavior remains unchanged
  except explicitly cheaper default model configuration.
* No automated assurance claim for task evaluation, inference or human review.
* Failed tests and command attempts are preserved in Changes, not overwritten.

## Acceptance Criteria

* AC1: az bicep build succeeds; compiled default is one capacity-one model;
  scalar overrides and deployment-array overrides propagate.
* AC2: compiled single and two-model bindings match deployed names and dated
  provider-model identities; AI env omitted when disabled; identity unchanged.
* AC3: read-only list proves exactly one successful live standard deployment
  with selected name/version/SKU/capacity; selected identity has OpenAI User
  on exact account with name equal to ARM guid(account.id, principal,
  'openai-user'); no other new role.
* AC4: read-only app metadata confirms same revision/settings/identity; no
  claim that the app is configured or AI inference works.
* AC5: existing infra tests plus focused new regression checks pass; one
  independent critique and one post-implementation Review are recorded.
* AC6: commit/push topic branch; one PR to main with Refs #514/#360/#104/#73,
  dependency, cost boundary, settings, evidence and honest residuals.

## Test Ownership and Locked Boundary

Owner: infra/tests/test_bicep_policy.py. Remove none. Add at most six test
methods to its existing compiled-template test class. Cover defaults, scalar
and array override propagation, empty-array/positive-capacity constraints,
single/two-tier mapping, endpoint selection, version pins, and enabled/disabled
API env. Use existing compile_bicep/evaluate/module helpers. Semantic tests
must evaluate compiled values, not merely assert source tokens. Add a mutation
check within the six-method budget where useful. No new test file/framework.
Generated output: new external directory only; canonical sources are Bicep.
Before the live role write, locally check UUID v5 against the RFC DNS known
answer and the documented ARM namespace/argument joining algorithm; record
exact inputs and require matching assignment name on readback. This is
bounded operational validation, not a new production UUID helper.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reproducible small-model infrastructure

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Parameters, outputs and API environment binding

Implement AC1/AC2 and document exact opt-in/override/version behavior.
Replace the existing environment-only bootstrap `modelDeployments=[]` example:
the nonempty contract now provisions a model even when apps are not deployed;
preserving an existing evaluated array requires an explicit reviewed override.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Compiled regression tests and existing infra validation

Run build, focused compiled tests, then full existing infra discovery; targeted
Ruff/format/mypy. Install existing declared packages only after missing-package
failure (already observed by pip show). Use an external task venv.

<!-- rpi:phase id=P02 -->
### [x] P02: Scoped Azure prerequisite

Depends on P01 source contract/build/tests, not app deployment.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Create minimal model and missing invocation role

Fresh-check empty list and identity before writes. PUT only
accounts/aif-cutover-test-rzsrg/deployments/standard with model
gpt-4.1-nano/2025-04-14, GlobalStandard/1, NoAutoUpgrade/Microsoft.DefaultV2.
Grant only role 5e0bd9bd-7b93-4f28-af87-19fc36ad61bd to principal
6ac4c6b9-c516-4e24-81a6-f32663a93aab if still missing. Use deterministic
assignment identity matching existing Bicep guid(account.id, principal, openai-user).
Record exact commands, outputs and subsequent read-only list/app invariants.
If creation rejects the selected configuration, stop unless another compatible
capacity-one model is supported. Any replacement must reconcile source defaults
or retained explicit overrides, compiled tests, response-version bindings and
handover before Review. Never create a second child or increase capacity.

<!-- rpi:phase id=P03 -->
### [x] P03: Independent Review and publication

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Reconcile evidence, execute one Review, commit and PR

Reconcile P01/P02 markers first. Run one rpi-review independent assessment;
route findings, never repeat Review in this task. Commit original evidence
using authenticated privacy-safe email and required trailer. For this
infrastructure change attempt at most one --changed gate under nonblocking
heavy lock, no --all; if lock busy record skip. Do not equate partial gate
with complete repository-default tier. Open the explicitly requested PR
with all gate exceptions/failures disclosed; do not merge.

Publication decision table:

| Gate state | Publication evidence |
| --- | --- |
| Successful scoped receipt | Fetch main; verify with `--required-scope partial` against current base immediately before push; identify reviewed tree and pushed head |
| Busy lock, missing prerequisite or failed run | Preserve exact failure; no retry/resume or success claim; requested PR discloses exception |
| Head/base changed after run | Receipt invalid; no repeat run under one-attempt limit; disclose invalidation |

Preserve the single independent Review's source boundary/tree; later evidence
or publication-only commits do not imply repeat independent acceptance.

## Dependencies

Existing API identity/account and signed-in az context; Bicep compiler; pip
namespace packages and existing test dependencies. PR #514 is a live redeploy
dependency only, not a source ancestry dependency. Pre-created branch was
fast-forwarded to origin/main d783b63a without rewriting any commit.

## Critique Disposition

Original critique execution Complete, verdict Revise, preserved unchanged at
the recorded critique path. No second critique.

| Finding | Disposition | Resolving change |
| --- | --- | --- |
| PC-001 | Rejected: unsupported premise | Parent has no restriction on /tmp; user explicitly requires /tmp brief and lock. Worker-specific restriction cannot constrain parent. Native `--lock-timeout 0` is permitted; no outer lock or runner change |
| PC-002 | Applied | Publication decision table, fresh-base/conditional partial receipt verification, assessed-tree and invalidation disclosure added |
| PC-003 | Applied | Exact ARM-compatible UUID algorithm/known-answer/readback proof added to AC3/P02; bounded local validation |
| PC-004 | Applied | Capacity-one fallback requires source/test/handover reconciliation before Review or remains blocked |
| PC-005 | Applied | Explicitly replace incompatible bootstrap command and disclose nonempty model provisioning/cost implications |

Implementation-time reconciliation: P02's planned fallback was required after
ServiceModelDeprecating. Selected capacity-one compatible GPT-4.1 nano; source
defaults, tests and handover updated with no extra resource or role authority.
Original research and critique preserve the earlier candidate, not rewritten.

## Follow-Up Items

* Coordinator: after #514 merges, configure/redeploy reviewed employee app,
  preserve auth/data/identity and verify private access plus registered
  source=ai result under current task release/evaluation and budget controls.
* Owner: future model-retirement/quality/cost review outside this short exercise.
* Separate engineering task: reconcile observed src-deploy.yml workflow-matrix
  drift before a later gate attempt; no runner/workflow change here.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-28/employee-ai-deployment-changes.md.
Execution complete; PR https://github.com/jmservera/ama/pull/515.
Review Complete / Conformant with justified divergence; zero implementation
defects. Sole partial gate failed preflight, disclosed in PR under explicit
owner scope exception. Hosted/human approval and operator activation remain
unmet; no merge or full-tier gate acceptance. No automatic child task.
