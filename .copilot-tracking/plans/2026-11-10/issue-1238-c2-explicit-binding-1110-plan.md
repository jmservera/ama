<!-- markdownlint-disable-file -->
# Plan: issue 1238 C2 explicit approval-role binding (1110)

Prospective, written 2026-11-10T00:34Z before any test or source edit.
Research: [research](../../research/2026-11-10/issue-1238-c2-explicit-binding-1110-research.md).
Details: [details](../../details/2026-11-10/issue-1238-c2-explicit-binding-1110-details.md).

## Objective

Remove the inferred service-owner = control-owner and redress-owner = reviewer
authority. Replace it with an immutable, trusted, unconfigured-by-default
approval-role binding. Q6 `manual_verified` is already approved and is not
re-asked.

## Phases

* [x] Phase 1: one critique of this plan and details (before tests or source).
* [x] Phase 2: ordinary merge of main ddeebd0 if no source conflict.
* [x] Phase 3: red tests in `test_resident_decisions.py` (default denial,
  forged stored approvals, binding change, binding validation, synthetic
  bound success) and existing supersede tests rebound to a synthetic fixture.
* [x] Phase 4: implement `SupersessionBinding` and the handler change; README.
* [x] Phase 5: validate: module (JSON, SQLite), selected MSSQL under one
  nonqueued admission, exact Core project mypy, Ruff check and format, exact
  API project mypy if Core signatures reach the API, pinned declared tools.
* [x] Phase 6: one Review, then commit and handoff.

## Boundaries

No edit to Store, CoreSqlStore, sqlstore, procurement, server, app.js,
navigation, roles, resident_demo, Quality files; no schema; no UI; no live
provider or resend; no actual binding or approval populated anywhere.

Completion recorded 2026-11-10T00:47Z after evidence: see changes and review files.
