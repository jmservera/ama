---
title: Issue 349 preflight correction2 changes
description: Implementation and validation evidence for response shape guards
ms.date: 2026-10-22
---

## Scope and Status

Task: issue349-tenant-readiness-preflight-correction2; issue #349.
Implementation scope: P01 of the correction2 plan, followed by P02 Review and
publication gates. P01 complete; P02-T01 Review complete, outcome Residual work.
Plan and phase details are ready after one critique with recorded dispositions.

## Completed P01 Changes

Three explicit list-shape guards and exactly three focused regression methods.
No removals or generated artifacts. All tests use canned transport only.
No live tenant, Graph, Entra, credentials, Azure or resource operations.

Actual changes: three guards validate non-null collection values before iteration,
emitting unknown/malformed-response with empty facts. Missing/null and valid
lists retain prior results; callback target blocker retains precedence.
Three test methods cover 60 malformed field/shape/output combinations, nine
missing/null/empty combinations, mixed-member lists and missing callback target.
All original 29 tests remain.

## Validation

Pre-change baseline: 29 focused tests pass. Offline matrix reproduces TypeError
for all three integer-valued fields and false-ready dictionary URI keys.
Red-first regression run: 32 tests, 42 failures and 19 errors before source fix;
log /tmp/ama-349-correction2-red.log. Final correction checks:

* python3 -B -m unittest discover -s infra/tests -p test_tenant_readiness_preflight.py -q:
  32 tests pass.
* /tmp/ama-349-correction2-checks/bin/ruff check --isolated --no-cache
  --select E,F,I,B,UP --target-version py312 --line-length 100 on both files: pass.
* Ruff format --isolated --line-length 100 --check on both files: pass.
* /tmp/ama-349-correction2-checks/bin/python -m mypy --strict
  --cache-dir /tmp/ama-349-correction2-mypy infra/scripts/tenant-readiness-preflight.py:
  pass, one source file.
* git diff --check: pass.

One RPI Review executed: Complete / Residual work. No source defects found.
Its simultaneous-malformed-fields CLI cross-check passes. Commit, full gate
and publication remain pending at this pre-gate evidence snapshot.
The old-head receipt is invalid for this correction and is not reused.

## Amendments and Divergences

P01-T02 strict mypy initially found two existing union-attr errors in repeated
api/web `.get()` expressions. Reproduced both on the original HEAD script in
/tmp/ama-349-correction2-original.py. Bind the raw values once before their
existing dict guards so strict narrowing works without casts, ignores or
behavior changes. This small adjacent type clarification preserves scope and
requires no new user decision or repeat critique. Plan/details reconciled.
Planning critique dispositions remain in the plan; final post-gate fetch mandatory.

## Remaining Work

P01 and P02-T01 complete. P02-T02 commit/full gate/publication remains unfinished
at commit time; final receipt and publication state are retained externally to
avoid changing the gated head. RV-001 is the authorized publication continuation.
All issue #349 acceptance criteria and independent final PR review remain unmet.
