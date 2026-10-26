---
title: Issue 349 preflight correction3 plan
description: Require platform and Azure AD provider enablement
ms.date: 2026-10-22
---

## Task Metadata

Task ID: 349-correction3. Slug: issue349-tenant-readiness-preflight-correction3.
Status: Ready after one independent critique and parent dispositions.
Date: 2026-10-22.

## Executive Summary

Add the provider-enabled boolean to the existing read-only auth projection and
require strict true for both flags. Preserve the existing check IDs, reasons
and sanitized output. Add focused synthetic tests before changing logic.

### What You May Not Know

Azure CLI returns auth resource properties without the ARM envelope. A valid
registration is not evidence that its provider is enabled. Passing this local
checker never establishes sign-in or issue acceptance.

No unresolved design decision. Publication remains prohibited.

## User Decisions and Requirements

* Run one ordered Research, Plan/critique, Implement, Review correction loop.
* Work on current PR #437 branch at 3b881a65c808b02f6ca1bd29d227172f5ad453f6.
* Require platform and Azure AD provider enabled; false/missing/malformed blocks.
* Change only checker, tests and this correction's dated RPI artifacts.
* No tenant/Graph/Azure writes, credentials, deployment, acceptance ticks,
  issue comment, PR change or push. Keep draft.
* Run focused unittest with bytecode disabled and no-cache lint/format.
* Create one local Conventional Commit using authenticated privacy-safe local
  email and required co-author trailer; then exactly one full gate against
  b4d467cad84535ed106cffa1ae9aa303db7bfed2, with unique external output.
  Verify exact-head receipt; stop on gate failure and preserve outputs.

## Goals

Eliminate platform-only false readiness without expanding runtime permissions
or changing existing reporting semantics.

## Scope and Non-Goals

Two canonical targets: infra/scripts/tenant-readiness-preflight.py and
infra/tests/test_tenant_readiness_preflight.py. Generated targets: none.
No Bicep edits, shared documentation edits, live readiness checks or tenant work.

## Functional Requirements

AUTH_QUERY projects `providerEnabled:identityProviders.azureActiveDirectory.enabled`.
`api-auth-enabled` is ready only when both `enabled` and `providerEnabled`
are literally True. Otherwise retain mismatch/auth-disabled, empty facts.
Retain other checks, read-only guard, exit code and acceptance disclaimer.

## Non-Functional Requirements

No additional calls, secrets or raw-response output; strict boolean identity,
not truthiness. Reuse existing test transport and CLI helpers. Preserve all
32 original tests.

## Acceptance Criteria

Synthetic tests prove both-true succeeds, either flag missing or non-true
blocks, and text/JSON CLI output stays sanitized with exit 1 and acceptance
false. Assert the exact provider query path independently of Fake routing.
Focused suite and targeted Ruff pass. One Review preserved before committing.
Gate and receipt outcomes are external, honest and not inferred.

## Sources

.copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction3-research.md:
C1-C5/W1-W2, complete and Ready.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement and validate

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add regressions and strict provider requirement

Test owner: implementation parent. Removals: none. Maximum additions: three
test methods, plus the positive Fake provider boolean. One method locks query
path, one covers both flag states at Finding/overall level, one covers
CLI text/JSON sanitization and exit contract. Existing positive tests must
continue to pass. Red-first run is expected to fail new behavior assertions.
Only query and boolean conjunction change in production.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Run targeted validation

`python3 -B -m unittest discover -s infra/tests -p test_tenant_readiness_preflight.py -q`.
Use available pinned Ruff 0.17.1 with `check --isolated --no-cache --select
E,F,I,B,UP --target-version py312 --line-length 100` and `format --isolated
--no-cache --line-length 100 --check` on the two targets; `git diff --check`.

<!-- rpi:phase id=P02 -->
### [ ] P02: Review and local candidate gate

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute one independent Review

Fresh reviewer activates rpi-review. Assessed boundary: bounded correction diff,
research, plan/critique, details and changes evidence, not whole-issue acceptance.
Preserve outcome and route any findings; do not repeat Review in this loop.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Commit once and run one full gate

After Review, reconcile evidence and commit only authorized targets. Fetch main,
confirm base, then invoke exactly once `python3 tools/rpi-checks.py --all --base
b4d467cad84535ed106cffa1ae9aa303db7bfed2 --out <unique-/tmp-directory>`.
Do not interrupt or duplicate a lock owner. Verify resulting receipt for exact
HEAD/base. On failure, preserve outputs and stop. No later repository writes
invalidate the gated HEAD; record post-commit gate results externally.

## Dependencies

P01-T02 depends on P01-T01; P02-T01 on P01-T02; P02-T02 on P02-T01.
Gate tools/lock are shared prerequisites, not authority for any cloud fallback.

## Critique Disposition

Execution: complete, one critique. Original verdict: Revise, retained unchanged
in .copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan-critique.md.

| Finding | Parent disposition | Evidence and rationale |
| --- | --- | --- |
| PC-001 | Rejected: conflicts with explicit owner direction | User explicitly requires unique /tmp gate output. No /tmp or mktemp prohibition exists in this parent's applicable instructions. Worker-specific restriction does not constrain parent execution or override user direction. Preserve required single gate and exact base. |
| PC-002 | Rejected: unsupported parent restriction and unnecessary scope expansion | No parent prohibition on temporary directories; existing unittest fixture is authorized by requested focused suite. Preserve all existing tests unchanged except positive Fake flag. |

No product, schema, test coverage or implementation concern was identified.
No second critique and no user decision are needed.

## Follow-Up Items

* Independent coordinator exact-head assessment after local gate, retained
  hosted checks and human sign-in/tenant acceptance remain separate.

## Handoff

P01 and P02-T01 complete. Review execution Complete; outcome Conformant for
the bounded pre-commit correction; no technical defects. Reviewer separately
passed 34 tests, excluding the unchanged temporary-directory fixture under
worker-local restrictions; parent's complete 35-test run passed.
RV-001 routes P02-T02 to the parent; RV-002/RV-003 retain independent
coordinator and hosted/human acceptance. P02-T02 remains pending at the
pre-commit snapshot; final gate outcomes must remain external.
Review: .copilot-tracking/reviews/logs/2026-10-22/issue349-tenant-readiness-preflight-correction3-review.md.
Details: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction3-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan-critique.md.
Changes: .copilot-tracking/changes/2026-10-22/issue349-tenant-readiness-preflight-correction3-changes.md.
