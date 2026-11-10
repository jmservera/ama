---
title: Issue 136 binding C2 plan
description: Plan for one bounded C2 on the initial-candidate policy test lint, format and typing regressions
ms.date: 2026-11-10
---

## Provenance

After the [research](../research/2026-11-10-issue-136-binding-c2-1110-research.md); [details](../details/2026-11-10-issue-136-binding-c2-1110-details.md); one author-inline [critique](../challenges/2026-11-10-issue-136-binding-c2-1110-critique.md).

## Scope

Refs #136 and #1288. Only `infra/tests/test_bicep_policy.py` (and the new startup test only if typing needs it). No Bicep, README, flag, guard, scale, auth, accounting, AI, budget, Core, API or image change. C1 import fix and clock fix untouched. No push, PR, rebase, merge or hooks override.

## Plan

* P1 Reproduce red on the C1 head: pinned isolated Ruff check (four E501), format diff and `mypy --check-untyped-defs` (five diagnostics) with raw output and exits.
* P2 Run `ruff format` (isolated, line length 100) on the policy file; verify the diff touches only the four introduced hunks.
* P3 Annotate `refusals` as `dict[str, tuple[dict[str, object], str]]`.
* P4 Green: Ruff check and format on both infra test files, mypy on both with the three baseline diagnostics only, base comparison.
* P5 Impacted tests: policy 60, container contract 7, IoT Hub 23, API simulation 30, Bicep build and lint, startup 4 (nonqueued lock, unchanged image identity proven first).
