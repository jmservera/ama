---
title: Issue 116 live round 4 changes
ms.date: 2026-11-19
---

## Files

* `src/core/src/zava_forward/core/projection.py`: `reason_roles()` drops `Contractor` from `ZF_REASON_ROLES`; docstring records the demo confirmation.
* `src/api/tests/test_role_matrix.py`: `test_reason_role_override_never_grants_the_contractor`.
* `docs/reference/research/issue-116-live-r4-evidence-2026-11-19.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

* `python3 -m unittest test_role_matrix test_role_endpoint_inventory -q` (src/api): 41 tests OK.
* `python3 -m mypy` in src/core: 22 errors, identical to the unmodified tree (missing opentelemetry stubs); none in projection.py.
* ruff format check: projection.py is already flagged on the unmodified tree; not caused here.
* Tier: FULL applies (src change); full gate not run, heavy lock held and owner forbade it. Gap recorded.

## Divergence

The first source edit (reverted, wrong barred set) and the final edit ran in parallel with the implement-start witness, so the witness records "source already dirty". The edits are in this diff only.

## Per-criterion status

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Roles allowed to see a vulnerability reason confirmed | Proven for the demo (owner decision 2026-11-18, matrix tests, new override test) |
| 2 | Allowlists at every provider boundary | Unproven (offline evidence only, no live payload exposure) |
| 3 | Permissions rechecked on outputs and exports | Unproven (one role live only) |
| 4 | Document AI derivative or necessity exception | Unproven live |
