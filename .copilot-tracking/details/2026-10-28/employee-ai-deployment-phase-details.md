---
title: Employee AI deployment phase details
description: Evidence, write boundaries and validation per planned task
ms.date: 2026-10-28
---

## Metadata

Task ID: employee-ai-deployment-2026-10-28. Plan:
.copilot-tracking/plans/2026-10-28/employee-ai-deployment-plan.md.
Research: .copilot-tracking/research/2026-10-28/employee-ai-deployment-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete: builds, 466 tests, lint/types | P01-T01, P01-T02 |
| P02 | Complete: one Succeeded model and exact missing role | P02-T01 |
| P03 | Review Complete/Conformant with justified divergence; publication active | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Reproducible small-model infrastructure

Context: research C1-C7 proves deployment loop exists but defaults are two
large-capacity tiers; app names hardcoded and version pins absent.
Boundary: selected infra sources/docs/tests only; preserve existing
foundryEndpoint consumers and runtime/release code.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Parameters, outputs and API environment binding

Add positive-capacity scalar parameters and one small default to main; require
nonempty modelDeployments in main and foundry module. Derive names and response
versions from array entries. Output OpenAI endpoint using account-advertised
`OpenAI Language Model Instance API`; leave generic endpoint intact. Pass
separate OpenAI endpoint/name/version objects into containerapps; gate all five
AI_* values with enableApiAi and retain AZURE_CLIENT_ID. No key field.

Completion: source diff and compiled semantic assertions for single-model
fallback, two-model distinct names, model-version concatenation and API off/on.
Document existing deployments must retain explicit array overrides, not
unintentionally change an active evaluated model set.
Replace environment-only bootstrap's empty model array and explicitly note
that a model is now included even when app workloads are omitted.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Compiled regression tests and existing infra validation

Modify only existing BicepPolicyTests with <=6 methods, no removals. Reuse
compile/evaluate/module helpers and in-method cases/mutations. Scalar capacity
constraints plus array nonempty; compilation checks all source targets. Test
both single and two-entry overrides rather than hardcoded standard/capable.
Run `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q` using
installed namespace packages. Lint/format/type-check changed Python file.
No app suite needed because no app source changes; AI runtime contract is
read evidence, not changed behavior. External validation logs retained.
Operational UUID validation uses RFC UUID-v5 known answer plus Microsoft ARM
guid namespace 11fb06fb-712d-4ddd-98c7-e71bbd588830 and hyphen-joined inputs,
not the policy evaluator's joined-string guid stub.

<!-- rpi:phase id=P02 -->
## P02: Scoped Azure prerequisite

Context: W1-W4; no quota entries; creation must prove provider acceptance.
Prerequisite P01 validation. No app, network, tenant, resident or other writes.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Create minimal model and missing invocation role

Re-read exact account/location, selected client ID, role absence and empty
deployment list immediately before writes. Use `az rest` exact child-resource
PUT to pin upgrade policy/content filtering (CLI create omits those flags).
Original standard/gpt-4o-mini/2024-07-18/GlobalStandard/1 was rejected by the
provider as deprecating, with no child left behind. The planned in-scope
fallback standard/gpt-4.1-nano/2025-04-14/GlobalStandard/1 succeeded.
Defaults, targeted tests and handover now match that one accepted child.
No throughput increase, second child or broadened resource scope occurred.

Role is account-scoped OpenAI User for id-cutover-test-api only if missing.
Derive deterministic UUID with documented ARM guid namespace and join inputs,
matching future Bicep resource naming; read back principal/role/scope. Do not
create Foundry User for API. Poll via bounded read-only deployment list if
provisioning is asynchronous; report actual state.
Record exact account-ID spelling, principal and seed, known-answer check and
expected UUID before write; read back and compare the actual assignment name.

Completion: sanitized exact command/results in Changes, read-only list with
one Succeeded child, correct role, unchanged live app revision and five AI_*
names absent. No inference or broader resource-list/private-data read.
Actual evidence: exactly one model Succeeded; assignment UUID matches expected
207df5ea-ca56-5fb7-9ebb-f533d02dadb8; live app remains revision 0000006,
same identity and AI_* absent. Final 466-test suite passes after reconciliation.

<!-- rpi:phase id=P03 -->
## P03: Independent Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Reconcile evidence, execute one Review, commit and PR

Reconcile plan/details/Changes with all executed checks and explicit residuals.
Invoke rpi-review once with a fresh independent worker, canonical pointers,
source diff and validation evidence. Preserve original outcome and route
findings separately; never cycle back to repair/review inside this task.
Human approval stays unchecked.

Commit using `gh api user` identity and noreply email for author/committer.
Attempt one `--changed` gate only if timeout-zero heavy lock is available;
do not deadlock runner's own lock. Inspect gate command lock behavior first.
No `--all` even if broad selection occurs. Missing prerequisites/failure
must be disclosed, never repaired via Azure/cloud fallback.
Use runner's native `--lock-timeout 0`; parent has no /tmp prohibition (PC-001
rejected on unsupported premise). Preserve one-attempt limit. Fetch main before
push; a successful receipt needs `--required-scope partial` verification against
fresh base. Missing/failed/skipped/invalidated receipt is disclosed as such.
Identify the one Review's source tree and later publication-only changes;
no repeated Review or acceptance claim for later changes.

PR to main on feat/employee-ai-deployment-bicep, Refs #514/#360/#104/#73;
no closure or merge. Include exact endpoint, both standard names, both
gpt-4.1-nano-2025-04-14 model identities, retained AZURE_CLIENT_ID, one
missing role added, USD30 additional AI authorization through 2026-10-31
(not a configured hard cap), no calls/no app change, actual gate status.
