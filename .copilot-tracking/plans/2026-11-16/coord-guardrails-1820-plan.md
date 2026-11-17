---
title: Plan for issue 1820 coordinator guardrails
ms.date: 2026-11-16
---

## Phases

* P01-T01: In Step 5 of `.github/agents/ama-backlog-delivery-coordinator.agent.md`, extend the witness call-list paragraph with artifact-before-record ordering and the never-stage-cache rule.
* P01-T02: Add an execution-hygiene paragraph (sequential src/core then src/api suites, `read_bash` delay <= 600, heavy-lock check or `--lock-timeout 0`).
* P01-T03: Replace the blanket "Sonnet 5.5 for all" sentence with model-fit guidance, keeping the no-silent-fallback rule.
* P01-T04: Static consistency review, commit locally.

Research: [research](../../research/2026-11-16/coord-guardrails-1820-research.md). Details: [details](../../details/2026-11-16/coord-guardrails-1820-phase-details.md). Critique: [critique](../../reviews/logs/2026-11-16/coord-guardrails-1820-plan-critique.md).
