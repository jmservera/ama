---
title: Issue 93 R1 RULE-010 boundary plan
ms.date: 2026-11-03
---

Details: [details](../../details/2026-11-03/issue-93-r1-rule010-boundary-details.md).

## Plan

* [x] Phase 1: add `src/core/tests/test_funding_automation_boundary.py` (static and behavioural probes).
* [x] Phase 2: run focused tests, ruff, mypy; mutation-check the guards.
* [x] Phase 3: evidence, review, PR with `Refs #93`.

## Critique (executed once, inline)

Verdict: proceed. Findings applied directly: probes must read source, not installed copies; the AI probe must stay offline (patch `run_text_task`); static scan scope must be explicit and non-empty. No conflict with confirmed decisions; no user decision needed.

## Boundaries

Validation tier: focused. No security, infrastructure, SQL or deployment code changed (the test only reads source and uses the file-backed store). Complete gate is for the coordinator.
