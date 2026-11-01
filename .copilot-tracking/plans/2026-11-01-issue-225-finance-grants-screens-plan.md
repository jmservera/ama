# Plan: issue 225 finance and grants screens (2026-11-01)

Research: .copilot-tracking/research/2026-11-01-issue-225-finance-grants-screens-research.md

## Phases

1. Append finance helpers and two `registerRoleScreen` calls to `role-screens.js`, reusing #226 helpers.
2. Add `src/api/tests/test_finance_grants_screens.py` (node vm harness, tests outside package).
3. Validate: unittest for new and existing role-screen tests, ruff check, ruff format --check, mypy on src/api.
4. Commit, push, open PR with Refs or Closes per proof.

## Critique (inline, one pass)

* Reuse risk: `assetCost` is the one AI cost renderer; reuse it, do not fork. Accepted.
* Risk of inferring payment: render only recorded `payment_status`, label as record. Accepted.
* Queue is cross-case but the host page queue is per-home; load `/api/finance` only for the invoice screen and label it as role-scoped, bounded. Accepted.
* Role check: no automated browser proof of keyboard behaviour in this slice, so the WCAG criterion is reported as unproven beyond native semantics.
