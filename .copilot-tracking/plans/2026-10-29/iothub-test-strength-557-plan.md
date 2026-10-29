---
title: IoT Hub test strength implementation plan
description: Test-only correction of the two PR 557 findings
ms.date: 2026-10-29
---

Task ID: pr-557-test-strength
Task slug: iothub-test-strength-557
Status: implementation, validation and one independent Review complete;
local commit remains.

## Executive Summary

Strengthen the existing live IoT Hub assertions without changing production
templates. Bind SKU/unit and location reference fixtures to the exact synthetic
hub ID and reject isolated wrong-hub mutations. Pin the diagnostic name to
`to-log-analytics` and reject a name-only mutation. Keep the existing mismatch
matrices, consumer-group assertions and scope/dependency coverage.

## Sources

Research: .copilot-tracking/research/2026-10-29/iothub-test-strength-557-research.md
(C1-C6). Details:
.copilot-tracking/details/2026-10-29/iothub-test-strength-557-phase-details.md.

## User Decisions and Requirements

* Run initial `git pull --rebase` (done, already up to date).
* Execute all four RPI phases with dated tracking evidence; commit locally.
* Make test-only changes in infra/tests/test_iothub_module.py for PR #557.
* Assert both reference fixtures target `/fixture/Microsoft.Devices/IotHubs/fixture`.
* Add wrong-hub mutation coverage and diagnostic name pin/mutation.
* From infra run `python3 -m unittest discover -s tests -p 'test_iothub*'`.
* Run Ruff check and format check on touched Python.
* No push, Azure operations or manual rubric score edits.

## Goals

Prove live guard validation reads the intended existing hub and diagnostics
update the intended setting rather than silently accepting another resource.

## Scope and Non-Goals

Only the named test file and dated RPI artifacts may change. No runtime, Bicep,
shared evaluator, dependencies, cloud resources, generated score or KB changes.
Local `az bicep build`/`build-params` are compiler-only operations, not Azure
service access. This local-only candidate does not claim publication approval,
complete local gate, human acceptance or closure of the parent PR/issues.

## Functional Requirements

* Both reference fixtures assert the first reference argument before returning
  their synthetic properties, using existing named-fixture precedent C6.
* SKU/unit validation becomes a reusable template-taking assertion helper.
* Mutations independently replace only the hub-name resourceId argument in
  the SKU, unit and location guard expressions; unchanged expressions must fail
  the mutation setup rather than pass vacuously.
* The live diagnostic helper asserts the exact setting name; its existing
  mutation test gains a name-only case.

## Non-Functional Requirements

Preserve matrix coverage and keep the test helpers local and simple.
Use existing unittest/deepcopy/evaluate conventions. Ruff must pass.
Use an external environment to restore missing pinned Ruff only.

## Acceptance Criteria

* AC1: Valid B1/one-unit and location cases retain their current outcomes.
* AC2: Each SKU, unit and location wrong-hub mutation raises AssertionError
  identifying expected/actual hub IDs, not an unrelated failure.
* AC3: Correct diagnostic identity passes and name-only mutation fails.
* AC4: Requested selector completes with no failures or unexpected skips;
  Ruff check and format check pass.
* AC5: Independent critique and exactly one post-implementation Review are
  recorded, followed by a local commit and no push.

## Test Ownership and Candidate Lock

Canonical test owner/target: infra/tests/test_iothub_module.py.
Generated targets: none. Exact test removals: none. Maximum new test methods:
one for wrong-reference mutations; retain all existing methods.
Helpers: at most one extracted SKU/unit helper plus two local named reference
fixtures. Semantic coverage: full existing SKU/unit and location matrices.
Regression coverage: three independent reference mutations and one diagnostic
name mutation. Validation evidence: requested unittest selector, Ruff commands,
diff review, one independent post-implementation Review.

## Phase Checklist

<!-- phase: P01 -->
### P01: Strengthen live contract assertions

* [x] P01-T01: Extract SKU/unit helper and bind both reference fixtures.
* [x] P01-T02: Pin diagnostic name and add isolated identity mutations.

<!-- phase: P02 -->
### P02: Validate and review

* [x] P02-T01: Run requested tests, lint, format and scoped diff checks.
* [x] P02-T02: Record one independent Review and reconcile all evidence.
* [ ] P02-T03: Commit implementation and dated evidence locally, no push.

P01-T02 depends on P01-T01; P02-T01 depends on both P01 tasks; P02-T02
depends on P02-T01; P02-T03 depends on P02-T02.

## Critique Disposition

Original independent critique:
.copilot-tracking/plans/2026-10-29/iothub-test-strength-557-critique.md.
Execution: complete, once. Original verdict: Revise (two Medium findings).

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Accept explicit successful-closeout gate; reject suggested post-Review implementation as conflicting with the one-pass RPI routing contract. In-scope material Review findings block a successful delivery claim and route to later work, without another Review. | Updated P02-T02/T03 details; preserve original outcome and report any unmet criteria rather than claiming acceptance. |
| PC-002 | Accept directly; pin Ruff 0.17.1 and isolated CI-matching flags. | Updated P02-T01 exact commands, restored tool outside repository. |

No unresolved planning blocker and no second critique. Changes to lifecycle
reporting do not authorize a conformant Review outcome with material open work.

## Follow-Up Items

None currently supported within the user's bounded request. Hosted/human and
full exact-head publication gates remain outside this no-push task.

## Handoff

P01 complete. P02-T01 complete with 23 tests, no failures or skips, Ruff
lint/format pass and all four mutation-sensitivity failures demonstrated in
memory. P02-T02 complete: independent Review execution Complete, outcome
Conformant, no findings or blockers. Original Review:
.copilot-tracking/reviews/logs/2026-10-29/iothub-test-strength-557-review.md.
P02-T03 local commit remains. No corrective phase or follow-up needed.
Changes record:
.copilot-tracking/changes/2026-10-29/iothub-test-strength-557-changes.md.
