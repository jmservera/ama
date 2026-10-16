---
title: Environment parameter sets implementation plan
description: Bounded infrastructure delivery for issue 137
ms.date: 2026-10-16
---

Task ID: issue-137. Task slug: environment-parameter-sets.
Mode: manual, with explicit user-requested implementation and review scope.

## Executive Summary

Retain the existing three parameter-file paths and naming lineage. Make dev/test
networking explicitly private, retain only declared development relaxations,
leave pilot region/ownership unresolved, and require references to recorded
region and quota checks. Enforce permanently private SQL and extend existing
issue 139 compiled/mutation gates. Deliver offline evidence and a PR, not Azure
or pilot acceptance.

## User Decisions and Requirements

* Implement issue 137; include issue 139 offline Bicep quality gates.
* Current request overrides the old pilot region/subscription-owner comment.
* Only src/ and infra/ executable changes; no legacy/private/config reads.
* Keep SQL public access disabled and all Azure resources inside ama.
* No deployment, consent, legal/safety/financial approval is implied.
* Update README and append the knowledge-base log; push and open a PR.
* Leave issue checkboxes for the coordinator at merge; use Refs references.

## Goals

Make environment differences reproducible, explicitly checked and honestly
documented without selecting unresolved owner decisions.

## Scope and Non-Goals

Scope: infra parameter files, main/guard/SQL wiring, deployment CLI safety,
existing infra tests, infra README and reference index/log.
Non-goals: deployments, resource deletion, owner decisions, policy exemptions,
new pipeline/check names and unrelated application behavior.

## Functional Requirements

* Three secret-free, marked parameter sets and one differences table.
* Production remains the default; development alone disables no protection.
  Independent keyVaultPurgeProtection and registryQuarantineEnabled inputs
  default true; only dev explicitly opts out.
* Location/model SKU/capacity remain inputs; missing check references fail
  through a named Bicep guard.
* SQL has no public switch/firewall; the CLI rejects groups other than ama.
* Document and test existing resource naming/tag propagation without renaming
  deployed resources.

## Non-Functional Requirements

Offline tests, error-level Bicep lint, compiled security controls and mutations;
ruff and mypy on changed Python; isolated synthetic local app smoke. No secrets
or actual subscription/tenant/Entra IDs in evidence.

## Acceptance Criteria

| Issue 137 criterion | Planned evidence | Boundary |
| --- | --- | --- |
| Parameter files for dev, test and pilot exist, with no secrets and with placeholders marked | P01-T01/T02: compile the three committed files and assert values/placeholders | Examples are not deployment-ready |
| Differences between environments are documented in one table (profile, SKUs, redundancy, retention, public access) | P01-T03: canonical README Environments table | Fixed service SKUs are documented, not invented configurable inputs |
| Production profile is the default and development relaxations are explicit | P01-T01/T02: independent opt-outs, defaults/profile matrix and mutations | No live production acceptance |
| Region and quota choices are parameters with recorded checks, not assumptions | P01-T01/T02/T03: location/model inputs, named reference guards, historical check register | Fresh actual checks remain not run |
| Resource naming and tagging convention is documented and applied | P01-T02/T03: compiled naming/tag forwarding assertions and README | No rename or new group |

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01 Environment implementation

* [x] P01-T01 Update parameters, named guards, SQL and deployment scope.
* [x] P01-T02 Extend compiled parameter/naming/tag and CLI/mutation tests.
* [x] P01-T03 Reconcile environment documentation and append reference log.

<!-- rpi:phase id=P02 -->
### P02 Validation and delivery

* [x] P02-T01 Run offline suite, all-file Bicep gates, ruff/mypy and local smoke.
* [x] P02-T02 Record one post-implementation review and acceptance audit.
* [x] P02-T03 Commit, push and open the PR without merging or ticking the issue.

Delivery: commit ab1fb52 on feat/environment-parameter-sets-137, pushed to origin;
PR 346 targets main. No merge or issue-checkbox changes.

## Critique Disposition

One final-candidate critique executed; Revise findings disposed directly:
PC-001 accepted: independent production-safe quarantine/purge inputs and matrix.
PC-002 accepted: synthetic valid-reference test baseline, separate missing checks
and bypass mutations; no fake committed evidence.
PC-003 accepted: reconcile Deployment profile, Environments and Governance controls.
PC-004 accepted: exact five-criterion mapping above.
PC-005 rejected: no supplied requirement forbids system/session temporary paths.
Existing TemporaryDirectory isolation is appropriate; smoke explicitly sets
synthetic paths and cleans them. Do not broaden test changes for an invented rule.
No user decision or second critique is needed.

Test ownership: primary agent; extend
test_bicep_policy.py and test_deploy.py, maximum 12 new methods. Reconcile the
existing source-text SQL and environment assertions in test_edge_module.py and
test_governance.py without adding test methods there. Remove only
obsolete conditional SQL firewall assertions; replace with stronger permanent
SQL isolation and mutation assertions. No test file removals. Canonical
targets are Bicep and parameter files; compiled JSON stays temporary. Semantic
coverage proves guard behavior, isolation, parameter values and tag forwarding;
regression coverage retains the existing resolver/security mutation gates.

## Follow-Up Items

Owner must decide pilot region and subscription ownership and record current
region, quota, zone capability and cost evidence before any deployment.
