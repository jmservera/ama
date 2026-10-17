---
title: Issue 358 credential preservation plan
description: Bounded implementation and acceptance plan
ms.date: 2026-10-17
---

## Task Metadata

* Task ID: 358
* Task slug: entra-credential-preservation-358
* Planning status: Ready after direct disposition of the single critique
* Plan date: 2026-10-17
* Phase details: .copilot-tracking/details/2026-10-17/entra-credential-preservation-358-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/entra-credential-preservation-358-plan-critique.md

## Executive Summary

Protect existing app secrets while rotating a missing/expired browser credential.
Add regressions for both generated and legacy stored credential names, reconcile
read-visible KV references with returned app values before creating a password,
and refuse to switch auth when retained references fail verification.
An incomplete handoff retains a reference-only fingerprint tag until readback
matches, preventing an unverified newly stored pair from bypassing the check on
rerun. No values or private identifiers enter that fingerprint record.
Preserve the existing delegating CLI and all #370 job/CI behavior.

### What You May Not Know

The public API schema includes KV fields but does not require them individually.
The existing generated-name expiry test does not exercise legacy-name reuse.
No cloud round-trip is permitted here: actual non-production preservation stays
UNMET and delivery is partial against the issue, even if all offline gates pass.

## Sources

* .copilot-tracking/research/2026-10-17/entra-credential-preservation-358-research.md: C1-C7, W1-W6 and scope controls.
* Owner request 2026-10-17: full loop, failing-before/mutation evidence, no cloud/secret/private reads or writes, push PR then stop.

## User Decisions and Requirements

* Deliver #358 on test/entra-credential-preservation-358; retain abaca788 and #370.
* Prove stored expiry and preservation of keyVaultUrl/identity plus app references
  across response shapes and safe error paths, with real red/green evidence.
* Do not weaken crypto/identity/network guards or change broader #360 readiness.
* Never equate offline mocking/schema inspection with live acceptance.
* Commit dated phase evidence, use own pip venv, run focused/full infra and lint,
  push a Refs #358 PR, stop without merge or force push.

## Goals

* Prevent a secret rebuild from silently losing a KV reference or app value.
* Pin both expiry-reuse paths, reference verification and legacy compatibility.

## Scope and Non-Goals

In scope: setup-entra.py credential rebuild/readback only, existing setup tests,
infra README, existing cutover evidence, KB index/log and dated RPI artifacts.
Non-goals: job/roster readiness, crypto, identity policy, networking, frontend,
new dependencies, private data, Azure/Graph operations, builds/spend or merge.

## Functional Requirements

* Only strictly future credentials with matching stored names are reusable;
  exact expiry/past/missing expiry cannot be selected, including legacy names.
* Keep known KV URL/identity pairs even when listSecrets omits metadata or an
  entire KV entry; never materialize a returned KV value as an app-local secret.
* Preserve ordinary app values (including empty strings), names and unrelated
  env/auth token-store references. Reuse full KV references returned by the list
  when configuration contains only names.
* Reject malformed/duplicate/unrecoverable inventories with sanitized SetupError
  before addPassword or configuration/auth mutation. Do not guess missing values.
* Verify old names and KV URL/identity on readback before auth activation; do not
  expect write-only app values in readback.
* Atomically attach a reference-only inventory fingerprint to the rebuild PATCH;
  clear it only after matching readback. On rerun, unresolved mismatch blocks
  reuse/auth; a transient transport failure can recover after matching readback.
* Keep CLI main delegation and its existing regression unchanged.

## Non-Functional Requirements

No source guard relaxation, raw secret output, new remote operation, package or
framework. Offline tests use wholly fictional fixtures. Source changes remain
small and specific to preservation. Existing formats and exception conventions
remain intact.

## Acceptance Criteria

* New behavioral tests fail against original source for sparse KV inventory,
  unsafe inventory and missing-reference readback, then pass after the fix.
* Expiry guard bypass, independently dropped keyVaultUrl and identity, and an
  app-value-loss mutation each fail behavioral assertions, not imports/errors.
* Targeted setup/legacy tests and full infra suite pass with Bicep required;
  relevant Ruff/mypy/compile and Bicep build/lint pass.
* Existing docs record exact offline proof and unmet live criterion; no live
  acceptance checkboxes are ticked.
* Dated phase artifacts/log committed; topic pushed and PR opened with Refs #358.

## Test Ownership and Locked Candidate Boundary

Canonical regression owner: infra/tests/test_setup_entra.py. Removals: none.
Maximum new ordinary test methods: 10, using subtests for expiry/response/error
matrices. Maximum new mutation test methods: 1, in that same file. Reuse existing
legacy delegation regression; no new competing suite. No generated test targets.
Semantic checks assert actual PATCH payload, stored inventory, env/auth refs,
write ordering, failure return codes and sanitized logs. Regression mutations
execute altered functions in memory, keep real fake-Azure behavior and require
assertion failures with no runner errors. Evidence lives in changes artifact.
Include metadata-only GET success (ordinary values absent) and persisted
missing/altered reference plus rerun/transport recovery subcases.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement focused regression protection

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add behavioral regressions and capture failing-before evidence

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reconcile secret inventory and verify reference readback

Depends on P01-T01. Validate list/configuration shape and uniqueness, restore
known KV pairs, retain app values, fail safely on unavailable required data.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and document partial acceptance

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Kill safeguard mutations and run focused/full infra gates

Depends on P01-T02.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update runbook, evidence, index and append-only log

Depends on P02-T01. Preserve historical entries and owner memory.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review once and publish

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Execute one bounded postimplementation review and publish PR

Depends on P02-T02. Route review findings to later work, no repeat review loop.
Only nonblocking/out-of-scope residuals may support ready-for-offline-review
publication; any in-scope correctness/safety finding leaves the PR draft/unready
and is reported plainly, without claiming a passing review.
Commit Conventional Commit messages with privacy-safe author/committer and trailer.

## Dependencies

Merged #356/#352 establish existing setup/delegation; #370 staff job stays intact.
Shared file sequencing with #360: land/reconcile this narrow setup function and
tests before broader setup/job iteration; no branch rewrite or merge authorized.

## Critique Disposition

Single critique executed, verdict Revise. All findings applied directly:

| Finding | Owner/disposition | Resolving evidence in candidate |
| --- | --- | --- |
| PC-001 | Planner, resolved | Atomic reference fingerprint and pre-reuse gate; P01-T01/T02 persisted-mismatch and transport-recovery oracles |
| PC-002 | Planner, resolved | Explicit metadata-only GET success subcase, separate backing store/PATCH assertions |
| PC-003 | Planner, resolved | P03-T01 readiness conditional on review outcome; unresolved in-scope findings mean draft/unready |

No user decision required; no second critique.

## Follow-Up Items

* Authorized non-production preservation proof: owner/coordinator must establish
  permitted existing scope without altering/deleting real secrets or opening
  private services. Offline delivery cannot close that issue criterion.
* Broader job/setup/live readiness remains #360, not an active implementation task.

## Handoff

Ready for implementation after one critique and direct corrections. Changes record:
.copilot-tracking/changes/2026-10-17/entra-credential-preservation-358-changes.md.
Critique dispositions complete. Parent continues automatically.

## Explicit Phase Log

* 2026-10-17 Plan opened from completed Research; user controls and test boundary locked.
* 2026-10-17 Final candidate ready for its single independent critique.
* 2026-10-17 Critique executed once; PC-001-PC-003 directly resolved; Plan Ready.
* 2026-10-17 Implement P01/P02 complete: regression/mutation/full infra evidence and docs reconciled; P03 Review/publication remains.
