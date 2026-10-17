---
title: Setup API selection plan
description: Safe legacy-tag direct demo discovery and check guard
ms.date: 2026-10-17
---

## Task Metadata

360/setup-api-selection-360, same branch fix/initializer-acr-cli-360/PR385.
Startd11c273, fresh mainbbbc924 already ancestor. Research executed/Ready.

## Executive Summary

Repair direct migration discovery using existing explicit direct-ingress tag
with modern role or compatible legacy workload API tag, never name guesses.
Explicit names still override and ambiguous candidates refuse. Honor owner's
strict no-cloud-write --check contract by blocking Azure job/secret transport
in read-only mode, reporting unverified SQL rather than silently creating jobs.
No real setup, image/runtime or tenant acceptance claim.

## Sources

.copilot-tracking/research/2026-10-17/setup-api-selection-360-research.md C1-C4/W1-W2.

## User Decisions and Requirements

* Full ordered new RPI/one critique/one independent Review, new unique slug,
  same topic/worktree/open PR. Existing ACR evidence unchanged.
* Unique explicitly configured direct demo wins; explicit --container-app always
  overrides. Unknown/multiple valid candidates refuse, legacy single/edge retained.
* --check/read-only must not write cloud, SQL, Graph or secret payloads, even on
  failure. No actual setup mutations, retirement, IAM/network/build/image action.
* Narrow setup/tests/runbook; pip only worktree-local dependencies, red-first
  regressions, relevant lint/types. Normal source push; no closing/merge.

## Goals

Make normal laptop discovery recognize actual deployed compatibility tags and
keep target and read-only safety fail-closed.

## Scope and Non-Goals

infra/scripts/setup-entra.py, existing test_setup_entra.py/test_staff_azure.py
if needed, existing runbook and KB routing/additive log; new dated phase evidence.
No Bicep/IAM/deployment changes; no fuzzy ordering/new persistent selector.

## Functional Requirements

Accept zava-forward-ingress=direct with roleapi OR absent role/workloadapi.
A conflicting modern role must not qualify. Modern role is authoritative within
each resource, not a tie-break between multiple valid direct resources: direct
pool cardinality above one always refuses without an exact override.
Keep explicit old target and legacy edge path behavior. No writes from Azure
staff transport when args.check, dry_run or list_staff; keep mutation-mode
transport unchanged (including operation=check in a mutating invocation).

## Non-Functional Requirements

Use existing helpers/style/types, errors explicit, no new dependencies.
Tiny fictional fixtures, assert target exact identity not only successful exit.
No live setup/SQL/Graph/secrets, only already completed ARM metadata reads.

## Acceptance Criteria

1. Red-first deployed legacy-tag pair selects intended direct demo, either list
   order; explicit old selects old; duplicate direct and no explicit selector
   refuse; single legacy still resolves existing edge.
2. Modern-role precedence, unrelated ingress-only and conflicting-role exclusions
   are covered; direct path emits no afd/cdn/extension commands.
3. Check/dry-run/list-staff success, error, explicit Azure and local-fallback scenarios
   show no cloud/Graph/private SQL writes or secret payload tests. --check Azure
   cannot claim private verification; it must return clear blocked/incomplete.
4. Relevant existing setup/staff/legacy tests and scoped lint/types pass; historical
   ACR receipts/Review exact bytes preserved, no image/runtime proof invented.

## Test Ownership and Locked Candidate

Canonical owner existing SetupTests, SetupAzureTests. Remove none. Maximum six
new test methods, bounded subcases for selection, exact explicit override,
legacy/ambiguity, check transport/failure; extend existing methods as appropriate.
No golden/generated production output. Semantic tests exercise discover/main
and actual fake call capture; regressions existing setup/staff/legacy suite.
Validation: targeted red/green first, then test_setup_entra/test_staff_azure/
test_initialize_api_auth; setup existing F-only Ruff/compile, changed-test F-only,
staff module existing lint/types if touched; mypy scoped source baseline comparison
if setup pre-existing annotations prevent whole-file strictness. No broad reformat.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Regression and narrow implementation

* [x] P01-T01: Add failing selection/check transport tests.
* [x] P01-T02: Repair direct compatibility filter/read-only transport guard.
* [x] P01-T03: Existing regressions/lint/types and factual runbook/KB.

<!-- rpi:phase id=P02 -->
### P02: Review and publication

* [ ] P02-T01: Reconcile artifacts and one independent Review; at most two
  authorized bounded corrections only for concrete defects.
* [ ] P02-T02: Fresh privacy identity/trailer, commit/push ordinary and updatePR385
  title/body to include safe selection and preserved ACR limits; exact head.

## Critique Disposition

One final-candidate critique complete, verdict Revise; all three accepted and
resolved directly by this parent before implementation. PC-001: extend central
guard to list_staff, adapt existing listing tests to blocked local-host handoff.
PC-002: cardinality guard for mixed modern/legacy direct pool, keep per-resource
modern authority; no generic choose/legacy edge priority change. PC-003: modify
existing test_arm_generated_and_legacy_kv_reuse_retains_upstream_expiry_boundaries
overall check expectation to incomplete while preserving reuse/expiry bytes and
mutation assertions. New guard tests exercise real wrapper before execute/payload,
not a mock of wrapper. No removals, maximumsix methods unchanged. Ready.

## Follow-Up Items

Real operator setup/runtime acceptance, exact image smoke/pin and old-edge
retirement remain separate, no current cloud authority.

## Handoff

Details .copilot-tracking/details/2026-10-17/setup-api-selection-360-phase-details.md.
Changes .copilot-tracking/changes/2026-10-17/setup-api-selection-360-changes.md.
P01 complete: combined164 tests, lint/types/compile and prior eight ACR artifact
byte parity passed. Main advanced during execution to d400eb8; fresh authorized
owned-topic integration must finish before final independent Review/publication.
Original source historical record and prior Review remain unchanged.
