---
title: Plan for issue-136-ci-template-c4-1110
description: Replace a brittle text assertion with a compiled scale contract
ms.date: 2026-11-10
---

## Objective

Fix `test_main_stack_remains_separate_from_resident_demo` in `infra/tests/test_resident_demo_deploy.py` without changing the template.

## Phases

* [ ] Phase 1: Edit the test per the details file (generalise `compiled()` with a file argument; assert compiled API scale; keep resident separation).
* [ ] Phase 2: Show green on the actual test, a mutation check that inversion, loss of cap 4 and a resident reference are each caught, then run the whole test module, the policy module, ruff and mypy comparison, and offline Bicep build and lint.
* [ ] Phase 3: Review once, commit with privacy-safe identity and Copilot trailer.

## Constraints

* Product path only `infra/tests/test_resident_demo_deploy.py`; no Bicep, replicas, budgets, permissions or src change.
* Existing runtime image `sha256:d6d6fe32...` is reused only on byte-identical source proof; startup tests rerun only if their inputs change (they do not).
* Baseline mypy stays exit 1 with three known errors.
* No push, PR, GitHub, cloud or model action.
