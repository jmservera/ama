---
title: Issue 2164 roster-bound Entra scope in assistants.authorize, re-verification
description: Evidence that roster-bound Entra staff inherit roster scope and revocation in assistants.authorize, plus one added view_only test
ms.date: 2026-11-27
---

Demo context: synthetic data, desktop only. The rule is a pure authorization check with no deployed surface, so no live Azure probe applies.

## Decision

Roster-bound Entra staff inherit the scope of their bound roster row. `assistants.authorize` in `src/core/src/zava_forward/core/assistants.py` rejects view_only principals, then re-reads the row by the verified `bound` pointer (matching `oid` and tenant) and applies role, disabled/active, `case_ids` and `areas`. Unbound principals keep the verified tenant and object keys as authority. Delivered by commit 6a03928ccb (#2274).

## Evidence (2026-11-27)

* `python3 -m unittest tests.test_assistants -k entra -k bound -k view_only` from `src/api`: 20 tests, OK (10 skipped, unrelated browser or model cases).
* New test `test_bound_view_only_entra_principal_is_denied`: a bound principal with an eligible role authorizes, and the same principal with `view_only` is denied for scoped and unscoped calls. Mutation check: disabling the view_only guard makes the test fail; the source was restored.
* `python3 -m mypy` in `src/api` and `ruff check` on the test file pass.

## Criteria

| Criterion from issue | Result |
| --- | --- |
| Decide whether bound Entra staff inherit roster scope | Proven: yes, implemented and tested (#2274) |
| Test for view_only with an eligible role | Proven: existing unbound test plus new bound test |
| Test for scope bypass | Proven: `test_bound_entra_forged_pointer_tenant_and_area_scope` and `test_bound_entra_staff_inherit_roster_scope_and_revocation` |
