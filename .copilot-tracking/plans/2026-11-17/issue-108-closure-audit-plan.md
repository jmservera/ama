---
title: Issue 108 closure audit plan
ms.date: 2026-11-17
---

Phases:

* P1 Add `docs/reference/research/evaluation/issue-108-closure-audit.md` (criterion matrix vs main eb51af5c9; unproven rows named; no tick changes).
* P2 Add `ClosureAuditDocTests` to `src/agents/tests/test_ai_eval.py`: the audit page must name every assistant and registry task not exercised by the harness, and the five unmet gates; fails before P1.
* P3 Index row in `docs/reference/README.md`, log entry in `docs/reference/log.md`.
* P4 Focused validation: test_ai_eval, mypy src/agents, ruff format check, link review.

Details: .copilot-tracking/details/2026-11-17/issue-108-closure-audit-details.md
Tier FOCUSED: docs plus a unit test; no SQL, security, infra or deployment.

Critique (single pass, self-executed): compatible findings applied: keep test derived from registry, do not edit issue body, preserve the issue's `Refs #108` (not Closes).
