---
title: Plan for #138 run summary slice
ms.date: 2026-11-04
---

Task: issue-138-run-summary. Refs #138.

* Stacked slices: (1) this run summary; (2) live OIDC/environment proof by an operator; (3) live deployment evidence. Only slice 1 is local.
* Phase 1: add `publish_step_summary` and `what_if_lines` to `pipeline.py`; call after what-if and after successful deployment.
* Phase 2: test sanitization (no canary delta, subscription or host), absence on failed what-if, no-op without the env variable.
* Phase 3: README sentence, log entry, RPI evidence.
* Constraints: no new secrets, permissions or PR comment token; summary uses only counts, SHA, status and check names.
* Details: [details](../details/2026-11-04-issue-138-run-summary-details.md). Critique: executed once, see [critique](../reviews/plans/2026-11-04-issue-138-run-summary-plan-critique.md).
