---
title: Orchestrator image resolution review
description: Single post-implementation acceptance review for issue 322
ms.date: 2026-10-16
---

## Scope and Evidence

Task #322; slug orchestrator-image-322. Full implementation boundary P01 and
P02-T01; P02-T02 publication follows this Review.

* Plan: .copilot-tracking/plans/2026-10-16/orchestrator-image-322-plan.md
* Details: .copilot-tracking/details/2026-10-16/orchestrator-image-322-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-16/orchestrator-image-322-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-16/orchestrator-image-322-changes.md
* Evidence: owner comment on issue #322; implementation and documentation diff;
  infra/scripts/deploy.py; infra/tests/test_deploy.py; local validation outputs.

## Opening Review State

Assess owner-directed Bicep bootstrap semantics and deployment image precedence,
printed choice, safe failures, offline tests and mutation sensitivity.
Evidence is ready: implementation, updated plan/details, passing critique and
recorded validation agree. Review authority is read-only except this record.
No blockers. Real Azure execution and pipeline #138 remain outside acceptance.

## Execution Status

Complete. One post-implementation Review on 2026-10-16; no repeat or correction
review is planned.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Empty default and conditional module forwarding; CLI selects exact three job names, unique real image, registry/repository lists, update-time tag ordering, placeholder warning | Conformant; unchanged job consumers and identity/RBAC |
| P01-T02 | Fifteen fake-az subprocess test methods; compiled default/empty/tag/digest and three-consumer checks | Conformant; exact argv, call order, failures and overrides covered |
| P02-T01 | 103 infra tests, seven mutations, actual old-source failure, Ruff/mypy and Bicep build/lint; README/index/log and existing CI selector | Conformant; evidence current |
| P02-T02 | Publication intentionally follows Review | Reconciled; no implementation dependency remains |

## Implementation-Time Update Assessment

Using successful registry/repository list responses to establish absence avoids
relying on Azure CLI error-message spellings. Authorization, network and invalid
JSON responses cannot become placeholder fallbacks. This is a compatible local
implementation judgment, recorded in details and changes, not a product or
architecture divergence. The final parameter ordering binds discovery identity
and deployment identity despite parameter-file defaults.

The critique executed once and passed with no findings. No unresolved PC item,
new user-owned decision, paused dependent work or unapproved scope expansion.
Application packages/build contexts remain in src/. The new helper is an
infrastructure entrypoint in the location explicitly requested by the user.

## Completed Work Assessment

The raw Bicep path intentionally still means placeholder for omitted/empty
input, matching the owner, rather than attempting unreliable existing-resource
lookup. The wrapper skips placeholder job images, preserves a unique real
image without querying ACR, refuses conflicts, and reports explicit overrides.
Registry discovery remains group scoped and newest tag ordering is explicit.
No failed CLI call is caught as successful absence; errors prevent deployment.
what-if is default; create is explicit and its exit code is propagated.

Tests run the actual wrapper with a fake executable on PATH; they cannot reach
real Azure. Mutants alter current-image selection, parameter forwarding,
placeholder warning and tag order. Compiled mutations cover the old default,
empty forwarding and unconditional placeholder. Pre-change HEAD Bicep fails
the new assertion when compiled in a temporary copy, independently confirming
the test is not merely passing the changed source.

## Validation Evidence

| Check | Result |
| --- | --- |
| Pip-venv infra unittest discovery, REQUIRE_AZ_BICEP=1 | Passed: 103 tests |
| Fake-az resolver tests | Passed: 15 methods including four killed mutants |
| Compiled Bicep contract | Passed, including three killed mutants |
| Actual pre-change HEAD Bicep | Rejected by new contract as required |
| Ruff check and format, changed Python | Passed |
| Mypy --check-untyped-defs, helper and resolver tests | Passed |
| main.bicep local build/lint and git diff --check | Passed |
| Real Azure/Docker/maintenance execution | Not run: outside offline scope |

Initial missing source-package imports were resolved with pip editable installs,
then the full suite passed. There are no remaining local failures.

## Findings and Defects

None. Severity counts: Critical 0, High 0, Medium 0, Low 0.
No RV entries or later implementation/plan/research correction are required.

## Follow-Up Assessment and Routing

Pipeline #138 integration is an existing, explicitly deferred owner follow-up.
Route it to the #138 implementation owner to reuse the resolver contract;
it is not a defect or part of this acceptance boundary.
Live permissions/private-registry connectivity, a reviewed rollout and
maintenance-job acceptance remain operational checks, not proven by fake az.

## Outcome

Conformant for the offline implementation boundary. No blockers.
Publication, hosted checks and the owner's merge decision are separate from
this local acceptance. Return to the rpi-quick parent for the explicitly
requested normal push and references-only PR.
