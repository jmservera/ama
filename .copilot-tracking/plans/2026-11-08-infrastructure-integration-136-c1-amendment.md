---
title: Infrastructure integration topic 136 corrective C1 amendment
description: Current-use amendment correcting the 144 session identity, the gate order and the module coverage table of the 136 integration topic record
ms.date: 2026-11-08
---

## Identity and supersession

Task `infrastructure-integration-136-c1`. Local only; base HEAD `f28e1fe003e1e1d7d2fe43546cbbe0d4a92851d2`, `origin/main` `0f05e9aae70768def8d1d9c300215f9ee2f11638` (fetched, no drift). Planning commit `0a39e68c85ead5ab53c4e2bf97f99bc26bf77151`. Basis: `.copilot-tracking/research/2026-11-08-infrastructure-integration-136-c1-research.md`, `.copilot-tracking/plans/2026-11-08-infrastructure-integration-136-c1-plan.md`, `.copilot-tracking/plans/2026-11-08-infrastructure-integration-136-c1-critique.md`.

For current use this amendment supersedes the statements listed in the last section. The original records, including critique IC-001 to IC-005, Review RV-001 to RV-003 and the original state, stay unchanged as dated historical records, with their erroneous assumptions preserved. Nothing here ticks a criterion, approves a document, accepts a child or claims CI success.

## F1: corrected 144 identity map

Git observations (separate from the session identifier):

| Ref | Observation |
| --- | --- |
| `6496f61f0361c27c297b97b12a5c46e374cd6a5f` | Body candidate; ancestor of local `ea7f36c0`; not an ancestor of the published head |
| `ea7f36c030e7a6fbac740d382fafa54f2de2dbf4` | Local `feat/slice-144` head; not an ancestor of the published head |
| `1a9616d4e9ab89d93a72204d82ee26c70baee06c` | Published PR 1141 head, base `main`; unchanged by this loop |

Session identifier, not source: `0bd489d3-4546-4229-94f9-d1812eadef27` is the Copilot session UUID of the original 144 loop, observed in the local session store (repository `jmservera/ama`, branch `feat/slice-144`). It is not a Git object, so the earlier "unresolvable in this repository, may exist in another clone" and "identity unverified" wording was a misclassification. A Git object database can neither verify nor disprove a session identifier. The session record shows that the conversation existed, not its outcome and not any commit.

## F2: corrected gate order

Observed: `.github/workflows/src-ci.yml` triggers on `pull_request` for `src/**`, `infra/**` and listed tooling paths, and on `workflow_dispatch`. An unpublished local commit cannot run it. Correct order, none authorized by this loop:

1. Focused local documentation validation (Markdown, link, Git diff, source blob review) and independent exact-head assessment of the final head.
2. Separately authorized push and draft parent PR to `main`.
3. Fresh hosted checks that GitHub selects on the actual head, before merge or any 144-dependent publication. Required and reported checks and the branch-protection mapping remain gates.

This topic changes only `.copilot-tracking/**`, so path-filtered Source projects CI may legitimately not be selected; that non-selection is not Bicep validation and not a failure. No manual all-project dispatch is proposed for a documentation-only anchor. Actual Source CI is absent for this head and is not claimed successful or as code validation. The original IC-003 ordering ("CI before publication") is historical and misordered; it is not edited.

## F3: complete coverage table

Static reading of `infra/` at `f28e1fe0`; wired-from by grep of `module` declarations. Status for every row is "authored Bicep, statically read": not compiled, not tested, not deployed, no Azure observation. Owner is the repository owner (@jmservera) per the README register unless a named human appears; the approver for any live apply, cost or policy action is a named human and is unknown unless stated.

Top-level units (9):

| File | Scope | Wired from or calls | Owner or approver, unknowns |
| --- | --- | --- | --- |
| `infra/main.bicep` | Resource group | Calls guard, identity, network, monitoring, keyvault, storage, registry, sql, foundry, iothub, apps (conditional), edge (conditional), authTokenStore (conditional), operationalMonitoring; also declares alerts, scheduled-query rules and a budget | Repository owner; live deployment authority and cost values unknown |
| `infra/governance.bicep` | Subscription | Not called by main; no modules | Juan Manuel Servera per `infra/defender-decision.json`; Policy audit only, Defender deferred, cost approval pending |
| `infra/iot-hub-live.bicep` | Resource group | Calls `modules/iothub-scope-guard.bicep`; reconciles children of an existing hub only | Repository owner; live apply is an owner-gated step; approver and cost authority unknown |
| `infra/live-simulator-job.bicep` | Resource group | Calls `modules/staff-initializer-guard.bicep`; header says authored and compiled only, not deployed | Repository owner; IoT live approval and device steps unknown |
| `infra/private-proof-publisher.bicep` | Resource group | Calls `modules/staff-initializer-guard.bicep` | Repository owner; operator-run, authority unknown |
| `infra/public-edge-existing.bicep` | Resource group | Calls `edge-existing-guard`, `edge`, `edge-existing-auth` | Repository owner; 143 open, deferred for the synthetic demo; not deployed |
| `infra/resident-assistant.bicep` | Resource group | No module calls; explicit opt-in, default off | Repository owner; resident-facing authority not evidenced |
| `infra/resident-demo.bicep` | Resource group | Calls `staff-initializer-guard`; referenced by `infra/scripts/resident_demo_deploy.py` | Repository owner; demo secrets owner-written; live state unknown |
| `infra/staff-initializer-rbac.bicep` | Resource group | Calls `staff-initializer-guard` | Repository owner; tenant staff reconciliation unknown |

Modules (20), under `infra/modules/`:

| File | Called by | Calls | Owner or unknown |
| --- | --- | --- | --- |
| `authTokenStore.bicep` | main (conditional, default off) | privateEndpoint | Repository owner; not observed |
| `containerapps.bicep` | main (conditional) | envDns | Repository owner; 144 open, worker images and hosted evidence missing |
| `edge-existing-auth.bicep` | public-edge-existing | none | Repository owner; 143 open |
| `edge-existing-guard.bicep` | public-edge-existing | none | Repository owner |
| `edge.bicep` | main (conditional), public-edge-existing | none | Repository owner; 143 open |
| `envDns.bicep` | containerapps | none | Repository owner |
| `foundry.bicep` | main | privateEndpoint | Repository owner; model availability and quota target-specific |
| `guard.bicep` | main only | none | Repository owner |
| `identity.bicep` | main | none | Repository owner; 141 closed, live role state unknown |
| `iothub-scope-guard.bicep` | iothub, iot-hub-live | none | Repository owner |
| `iothub.bicep` | main | iothub-scope-guard, privateEndpoint | Repository owner; 140 open |
| `keyvault.bicep` | main | privateEndpoint | Repository owner; 142 open |
| `monitoring.bicep` | main | privateEndpoint | Repository owner; 146 open |
| `network.bicep` | main | none | Repository owner; 143 open |
| `operationalMonitoring.bicep` | main | none | Repository owner; 146 open |
| `privateEndpoint.bicep` | authTokenStore, foundry, iothub, keyvault, monitoring, registry, sql, storage | none | Repository owner |
| `registry.bicep` | main | privateEndpoint | Repository owner; image release acceptance in 138 |
| `sql.bicep` | main | privateEndpoint | Repository owner; 145 open |
| `staff-initializer-guard.bicep` | live-simulator-job, private-proof-publisher, resident-demo, staff-initializer-rbac | none | Repository owner |
| `storage.bicep` | main | privateEndpoint (blob and queue) | Repository owner |

Intentionally manual, scripted or missing rows are unchanged from the original topic record table and are not repeated; this table replaces its consolidated Bicep rows for current use.

## Unchanged gates

All five 136 acceptance criteria stay unmet; 440 checkpoint, 107 and 118 source verification before 144 engineering, the named human decisions (Policy and Defender, manual resources, real deployment) and the 144 live acceptance gates stay open. This amendment does not unblock 144, change PR 1141, or publish anything.

## Superseded statements (original records, by line at `f28e1fe0`, left unchanged)

* F1: research lines 31, 48 and 65; critique IC-004 (line 18); topic record line 47 (144 stacking rule) and C5 (line 129); Review RV-002 (line 30).
* F2: research line 69; plan lines 30, 32 and 59; critique IC-003 (line 17); topic record lines 47 and 141; Changes line 47; Review line 41; original state `next_action` and follow-up rank 1.
* F3: topic record module coverage table and its consolidated rows.
