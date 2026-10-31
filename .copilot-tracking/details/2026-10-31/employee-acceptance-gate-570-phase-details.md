---
title: Employee acceptance browser gate phase details for 570
description: Bounded implementation and validation expectations
ms.date: 2026-10-31
---

## Metadata

Task ID: 570-employee-acceptance-gate. Slug: employee-acceptance-gate-570.
Plan: .copilot-tracking/plans/2026-10-31/employee-acceptance-gate-570-plan.md.
Evidence: research C1-C6 and W1. Implementation complete; critique Complete/Pass.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Focused validation complete; Review handoff ready | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Mandatory browser contract

Boundary: runner, owning tests and direct docs only; no workflow/app changes.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Wire runtime and trusted receipt matrix

C1-C4 show a current pin with incomplete matrix. Add CLI immediately after
install to both command sequences. Match literal pinned PYTHONPATH rather
than assuming editable imports cover tests. Add optional expected_count
to the existing parser, requiring the supplied count and no enumerated skips.
Apply expected_count=3 only when argv names the mandatory employee CLI.
Existing chat-panel expected_test and SQL/discovery parsing remain unchanged.
Evidence: matching dispatch/matrix unit test and runtime/receipt negative matrix.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add regression evidence and direct documentation

Depends on P01-T01. Add at most three owning test methods, remove none;
subtests cover missing command, altered argv/env/flags, failed exit, count
and skip failures including inherited SQL exception. Update both success
receipt fixtures identified by C5 for the new three-test suite.
Keep generated synthetic fixture output internal to tests where needed;
do not broaden global skip allowlists. Explain mandatory CLI and three/zero
evidence in src/README.md; index/log record the durable qualification.

<!-- rpi:phase id=P02 -->
## P02: Validate and prepare Review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused validation and prepare independent Review

Depends on P01. Requested tools unittest discovery; owning isolated Ruff,
format and strict mypy; diff/link review. Record actual counts and exits,
not assumed successes. Reconcile plan/details/changes before one independent
post-implementation Review. Preserve original outcomes; route findings later.
No live employee/hosted/human acceptance claim follows from focused tests.
Publication remains separately constrained by current repository policy.

## Completion Evidence

P01-T01: runtime/matrix CLI and expected_count=3 in both parsers.
P01-T02: three new owning tests, two fixture updates plus full suite count,
gate docs/index/log. No removals or generated outputs.
P02-T01: 42 tools tests pass, focused Ruff/format/mypy pass; new dispatch
regression fails against original HEAD runner with missing-command assertion.
One independent Review remains the immediate lifecycle action.
